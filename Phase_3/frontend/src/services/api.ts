import {
  API_ENDPOINTS,
  LOCAL_STORAGE_KEYS,
  ERROR_MESSAGES,
} from "../utils/constants";

interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: string;
}

interface ChatMessageData {
  message: string;
  conversation_id?: number | null;
}


interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

/**
 * API service module for handling all API requests
 */
class ApiService {
  private baseUrl: string;

  constructor() {
    // Validate environment variables
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    const domainKey = process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY;

    if (!apiUrl) {
      console.warn(
        "NEXT_PUBLIC_API_URL is not set, using default http://localhost:8000"
      );
    }
    
    if (!domainKey) {
      console.warn("NEXT_PUBLIC_OPENAI_DOMAIN_KEY is not set");
    }

    this.baseUrl = apiUrl || "http://localhost:8000";
  }
  

  /**
   * Helper method to create request options with auth headers
   */
  private getOptions(method = "GET", body: any = null, includeAuth = true) {
    const options: RequestOptions = {
      method,
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (includeAuth) {
      const token = localStorage.getItem(LOCAL_STORAGE_KEYS.AUTH_TOKEN);
      console.log(
        "🔐 getOptions - includeAuth:",
        includeAuth,
        "token exists:",
        !!token,
        "token preview:",
        token ? token.substring(0, 20) + "..." : null
      );

      if (token) {
        options.headers!["Authorization"] = `Bearer ${token}`;
        console.log(
          "🔐 Authorization header set:",
          `Bearer ${token.substring(0, 20)}...`
        );
      } else {
        console.log("❌ No token found, skipping Authorization header");
      }
    }

    if (body) {
      options.body = JSON.stringify(body);
    }

    return options;
  }

  /**
   * Generic request method
   */
  private async request(endpoint: string, options: RequestOptions = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout (increased from 10s)

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Handle 401 errors specially (token expired)
      if (response.status === 401) {
        // Check if this is specifically a token expiration error by examining the response
        const errorData = await response
          .clone()
          .json()
          .catch(() => ({}));
        const isTokenExpired =
          errorData.detail &&
          (errorData.detail.includes("expired") ||
            errorData.detail.includes("invalid") ||
            errorData.detail.includes("authentication"));

        console.log("🔍 401 Error details:", errorData);

        // Only clear tokens if it's a confirmed token expiration, not for other auth issues
        if (isTokenExpired) {
          console.log("🔐 Token confirmed expired/invalid, clearing tokens");
          localStorage.removeItem(LOCAL_STORAGE_KEYS.AUTH_TOKEN);
          localStorage.removeItem(LOCAL_STORAGE_KEYS.USER_ID);
          throw new Error(ERROR_MESSAGES.TOKEN_EXPIRED);
        } else {
          // For other 401 errors, don't clear tokens as they might be valid
          console.log(
            "⚠️ 401 received but not token expiration - keeping tokens"
          );
          // Still throw the error to be handled upstream, but don't clear tokens
          const errorDataOther = await response
            .clone()
            .json()
            .catch(() => ({}));
          throw new Error(
            errorDataOther.error || `HTTP error! status: ${response.status}`
          );
        }
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      return await response.json();
    } catch (error: any) {
      if (error.name === "AbortError") {
        throw new Error(ERROR_MESSAGES.TIMEOUT);
      }
      throw error;
    }
  }

  /**
   * Registration API call
   */
  async register(userData: any) {
    const options = this.getOptions("POST", userData, false);
    return this.request(API_ENDPOINTS.REGISTER, options);
  }
  

  /**
   * Login API call
   */
  async login(credentials: any) {
    const options = this.getOptions("POST", credentials, false);
    return this.request(API_ENDPOINTS.LOGIN, options);
  }

  /**
   * Logout API call
   */
  async logout() {
    const options = this.getOptions("POST", null, true);
    return this.request(API_ENDPOINTS.LOGOUT, options);
  }

  /**
   * Get current user API call
   */
  async getCurrentUser() {
    const options = this.getOptions("GET", null, true);
    return this.request(API_ENDPOINTS.ME, options);
  }

  /**
   * Send chat message API call
   */
  async sendChatMessage(messageData: ChatMessageData) {
    // Add logging to debug token issues
    const token = localStorage.getItem(LOCAL_STORAGE_KEYS.AUTH_TOKEN);
    console.log(
      "💬 Preparing chat request - token exists:",
      !!token,
      "token preview:",
      token ? token.substring(0, 20) + "..." : null
    );
    

    const options = this.getOptions("POST", messageData, true);
    console.log("💬 Chat request options:", {
      method: options.method,
      headers: options.headers,
      hasAuth: !!options.headers?.["Authorization"],
    });

    return this.request(API_ENDPOINTS.CHAT, options);
  }
}

export default new ApiService();
