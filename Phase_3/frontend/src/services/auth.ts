import api from './api';
import { ERROR_MESSAGES } from '../utils/constants';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  name?: string;
}

interface AuthResult {
  success: boolean;
  data?: any;
  error?: string;
}

interface AuthService {
  login: (credentials: LoginCredentials) => Promise<AuthResult>;
  register: (userData: RegisterData) => Promise<AuthResult>;
}

// Utility function to check if localStorage is available
function isLocalStorageAvailable(): boolean {
  try {
    const testKey = '__storage_test__';
    localStorage.setItem(testKey, testKey);
    localStorage.removeItem(testKey);
    return true;
  } catch (e) {
    console.error('localStorage is not available:', e);
    return false;
  }
}

export const authService: AuthService = {
  async login(credentials) {
    try {
      console.log('🔐 authService.login() called with credentials:', credentials);

      const response = await api.login(credentials);
      console.log('✅ API login response received:', response);

      // Verify response structure
      if (!response || typeof response !== 'object') {
        throw new Error('Invalid response from login API');
      }

      if (!response.token) {
        throw new Error('No token returned from login API');
      }

      if (!response.user_id) {
        throw new Error('No user_id returned from login API');
      }

      if (!response.email) {
        throw new Error('No email returned from login API');
      }

      console.log('✅ Token value:', response.token.substring(0, 20) + '...');
      console.log('✅ User ID:', response.user_id);
      console.log('✅ Email:', response.email);

      // Check if localStorage is available
      if (!isLocalStorageAvailable()) {
        throw new Error('localStorage is not available in this environment');
      }

      // Store tokens with error handling
      try {
        localStorage.setItem('auth_token', response.token);
        console.log('✅ localStorage.auth_token set');
      } catch (setItemError: any) {
        console.error('❌ Failed to set auth_token in localStorage:', setItemError);
        if (setItemError.name === 'QuotaExceededError') {
          throw new Error('Storage quota exceeded. Please clear some data and try again.');
        } else if (setItemError.name === 'SecurityError') {
          throw new Error('Security error: Cannot access localStorage. Are you in an iframe or private mode?');
        } else {
          throw new Error(`Failed to save authentication token: ${setItemError.message}`);
        }
      }

      try {
        localStorage.setItem('user_id', response.user_id);
        console.log('✅ localStorage.user_id set');
      } catch (setItemError: any) {
        console.error('❌ Failed to set user_id in localStorage:', setItemError);
        // Remove auth_token if user_id fails to save for consistency
        try {
          localStorage.removeItem('auth_token');
        } catch (cleanupError) {
          console.error('❌ Failed to cleanup auth_token after user_id error:', cleanupError);
        }
        throw setItemError;
      }

      // Verify tokens were saved
      const savedToken = localStorage.getItem('auth_token');
      const savedUserId = localStorage.getItem('user_id');
      console.log('✅ Token verification - saved token:', savedToken ? savedToken.substring(0, 20) + '...' : null);
      console.log('✅ Token verification - saved user_id:', savedUserId);

      if (savedToken !== response.token) {
        throw new Error('Token verification failed: saved token does not match original');
      }

      if (savedUserId !== response.user_id.toString()) {
        throw new Error('User ID verification failed: saved user_id does not match original');
      }

      console.log('✅ Login successful - tokens saved and verified');

      return {
        success: true,
        data: {
          token: response.token,
          user_id: response.user_id,
          email: response.email
        }
      };
    } catch (error: any) {
      console.error('❌ Login error in authService:', error);
      return {
        success: false,
        error: error.message || ERROR_MESSAGES.INVALID_CREDENTIALS
      };
    }
  },

  async register(userData) {
    try {
      console.log('🔐 authService.register() called with userData:', userData);

      const response = await api.register(userData);
      console.log('✅ API register response received:', response);

      // Verify response structure
      if (!response || typeof response !== 'object') {
        throw new Error('Invalid response from register API');
      }

      if (!response.token) {
        throw new Error('No token returned from register API');
      }

      if (!response.user_id) {
        throw new Error('No user_id returned from register API');
      }

      if (!response.email) {
        throw new Error('No email returned from register API');
      }

      console.log('✅ Token value:', response.token.substring(0, 20) + '...');
      console.log('✅ User ID:', response.user_id);
      console.log('✅ Email:', response.email);

      // Check if localStorage is available
      if (!isLocalStorageAvailable()) {
        throw new Error('localStorage is not available in this environment');
      }

      // Store tokens with error handling
      try {
        localStorage.setItem('auth_token', response.token);
        console.log('✅ localStorage.auth_token set');
      } catch (setItemError: any) {
        console.error('❌ Failed to set auth_token in localStorage:', setItemError);
        if (setItemError.name === 'QuotaExceededError') {
          throw new Error('Storage quota exceeded. Please clear some data and try again.');
        } else if (setItemError.name === 'SecurityError') {
          throw new Error('Security error: Cannot access localStorage. Are you in an iframe or private mode?');
        } else {
          throw new Error(`Failed to save authentication token: ${setItemError.message}`);
        }
      }

      try {
        localStorage.setItem('user_id', response.user_id);
        console.log('✅ localStorage.user_id set');
      } catch (setItemError: any) {
        console.error('❌ Failed to set user_id in localStorage:', setItemError);
        // Remove auth_token if user_id fails to save for consistency
        try {
          localStorage.removeItem('auth_token');
        } catch (cleanupError) {
          console.error('❌ Failed to cleanup auth_token after user_id error:', cleanupError);
        }
        throw setItemError;
      }

      // Verify tokens were saved
      const savedToken = localStorage.getItem('auth_token');
      const savedUserId = localStorage.getItem('user_id');
      console.log('✅ Token verification - saved token:', savedToken ? savedToken.substring(0, 20) + '...' : null);
      console.log('✅ Token verification - saved user_id:', savedUserId);

      if (savedToken !== response.token) {
        throw new Error('Token verification failed: saved token does not match original');
      }

      if (savedUserId !== response.user_id.toString()) {
        throw new Error('User ID verification failed: saved user_id does not match original');
      }

      console.log('✅ Registration successful - tokens saved and verified');

      return {
        success: true,
        data: {
          token: response.token,
          user_id: response.user_id,
          email: response.email
        }
      };
    } catch (error: any) {
      console.error('❌ Registration error in authService:', error);
      return {
        success: false,
        error: error.message || ERROR_MESSAGES.EMAIL_EXISTS
      };
    }
  }
};