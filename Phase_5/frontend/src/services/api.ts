import { LOCAL_STORAGE_KEYS } from "../utils/constants";

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
    // Use environment variable for API URL - supports both local (localhost:8000) and production (backend-service:8000)
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    console.log("🔗 API baseUrl configured:", this.baseUrl);
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
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Handle 401 errors - but NOT for login endpoint
      if (response.status === 401 && !endpoint.includes("/api/auth/login")) {
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

        if (isTokenExpired) {
          console.log("🔐 Token confirmed expired/invalid, clearing tokens");
          localStorage.removeItem(LOCAL_STORAGE_KEYS.AUTH_TOKEN);
          localStorage.removeItem(LOCAL_STORAGE_KEYS.USER_ID);
          throw new Error("Session expired. Please login again.");
        }
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      return await response.json();
    } catch (error: any) {
      if (error.name === "AbortError") {
        throw new Error("Request timeout. Please try again.");
      }
      throw error;
    }
  }

  /**
   * Generic GET request
   */
  async get<T = any>(endpoint: string): Promise<T> {
    const options = this.getOptions("GET", null, true);
    return this.request(endpoint, options);
  }

  /**
   * Generic POST request
   */
  async post<T = any>(endpoint: string, data: any): Promise<T> {
    const options = this.getOptions("POST", data, true);
    return this.request(endpoint, options);
  }

  /**
   * Generic PUT request
   */
  async put<T = any>(endpoint: string, data: any): Promise<T> {
    const options = this.getOptions("PUT", data, true);
    return this.request(endpoint, options);
  }

  /**
   * Generic PATCH request
   */
  async patch<T = any>(endpoint: string, data?: any): Promise<T> {
    const options = this.getOptions("PATCH", data, true);
    return this.request(endpoint, options);
  }

  /**
   * Generic DELETE request
   */
  async delete<T = any>(endpoint: string): Promise<T> {
    const options = this.getOptions("DELETE", null, true);
    return this.request(endpoint, options);
  }

  /**
   * Registration API call
   */
  async register(userData: any) {
    const options = this.getOptions("POST", userData, false);
    return this.request("/api/auth/register", options);
  }


  /**
   * Login API call
   */
  async login(credentials: any) {
    console.log("DEBUG: Login function called with credentials:", credentials);
    console.log("DEBUG: Request payload being sent:", JSON.stringify(credentials));

    const options = this.getOptions("POST", credentials, false);
    console.log("DEBUG: Request options:", options);
    console.log("DEBUG: Full request URL:", `${this.baseUrl}/api/auth/login`);

    try {
      const result = await this.request("/api/auth/login", options);
      console.log("DEBUG: Login response received:", result);
      return result;
    } catch (error) {
      console.log("DEBUG: Login error response:", error);
      console.error("DEBUG: Full error details:", error);
      throw error;
    }
  }

  /**
   * Logout API call
   */
  async logout() {
    const options = this.getOptions("POST", null, true);
    return this.request("/api/auth/logout", options);
  }

  /**
   * Get current user API call
   */
  async getCurrentUser() {
    const options = this.getOptions("GET", null, true);
    return this.request("/api/auth/me", options);
  }

  /**
   * Send chat message API call
   */
  async sendChatMessage(messageData: ChatMessageData) {
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

    return this.request("/api/chat", options);
  }
}

export default new ApiService();
