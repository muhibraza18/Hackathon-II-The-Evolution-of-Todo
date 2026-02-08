/**
 * Dapr State Service for client-side state management
 * Falls back to localStorage if Dapr is unavailable
 */

const DAPR_HTTP_PORT = process.env.NEXT_PUBLIC_DAPR_HTTP_PORT || '3500';
const DAPR_BASE_URL = `http://localhost:${DAPR_HTTP_PORT}/v1.0`;
const STATE_STORE_NAME = 'postgresql-state-store';
const STATE_KEY_PREFIX = 'chat-';

interface StateValue<T> {
  value: T;
  etag?: string;
}

class DaprStateService {
  private useDapr: boolean = false;

  constructor() {
    // Try to detect if Dapr sidecar is available
    // In Kubernetes, Dapr sidecar runs at localhost:3500
    this.detectDapr();
  }

  private async detectDapr() {
    try {
      const response = await fetch(`${DAPR_BASE_URL}/healthz`, {
        method: 'GET',
        signal: AbortSignal.timeout(1000), // Quick timeout
      });
      this.useDapr = response.ok;
      console.log(`📡 Dapr sidecar detected: ${this.useDapr}`);
    } catch {
      this.useDapr = false;
      console.log('📡 Dapr sidecar not available, using localStorage fallback');
    }
  }

  /**
   * Get state for a specific key
   */
  async get<T>(key: string): Promise<T | null> {
    const fullKey = `${STATE_KEY_PREFIX}${key}`;

    if (this.useDapr) {
      try {
        const response = await fetch(
          `${DAPR_BASE_URL}/state/${STATE_STORE_NAME}/${fullKey}`
        );
        if (response.ok) {
          const data: StateValue<T> = await response.json();
          return data.value;
        }
        return null;
      } catch (error) {
        console.error('Dapr get error:', error);
        // Fall through to localStorage
      }
    }

    // localStorage fallback
    try {
      const item = localStorage.getItem(fullKey);
      return item ? JSON.parse(item) : null;
    } catch {
      return null;
    }
  }

  /**
   * Set state for a specific key
   */
  async set<T>(key: string, value: T): Promise<void> {
    const fullKey = `${STATE_KEY_PREFIX}${key}`;

    if (this.useDapr) {
      try {
        await fetch(`${DAPR_BASE_URL}/state/${STATE_STORE_NAME}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([
            {
              key: fullKey,
              value,
            },
          ]),
        });
        return;
      } catch (error) {
        console.error('Dapr set error:', error);
        // Fall through to localStorage
      }
    }

    // localStorage fallback
    try {
      localStorage.setItem(fullKey, JSON.stringify(value));
    } catch (error) {
      console.error('localStorage error:', error);
    }
  }

  /**
   * Delete state for a specific key
   */
  async delete(key: string): Promise<void> {
    const fullKey = `${STATE_KEY_PREFIX}${key}`;

    if (this.useDapr) {
      try {
        await fetch(`${DAPR_BASE_URL}/state/${STATE_STORE_NAME}/${fullKey}`, {
          method: 'DELETE',
        });
        return;
      } catch (error) {
        console.error('Dapr delete error:', error);
        // Fall through to localStorage
      }
    }

    // localStorage fallback
    try {
      localStorage.removeItem(fullKey);
    } catch (error) {
      console.error('localStorage error:', error);
    }
  }

  /**
   * Check if Dapr is being used
   */
  isUsingDapr(): boolean {
    return this.useDapr;
  }
}

// Export singleton instance
export const daprState = new DaprStateService();
