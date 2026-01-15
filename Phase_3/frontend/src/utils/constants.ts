/**
 * Application constants
 */

// API endpoints
export const API_ENDPOINTS = {
  REGISTER: '/api/auth/register',
  LOGIN: '/api/auth/login',
  LOGOUT: '/api/auth/logout',
  ME: '/api/auth/me',
  CHAT: '/api/chat'
};

// Local storage keys
export const LOCAL_STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_ID: 'user_id',
  CONVERSATION_ID: 'conversation_id'
};

// Error messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Connection failed. Please try again.',
  INVALID_CREDENTIALS: 'Invalid credentials',
  EMAIL_EXISTS: 'Email already registered',
  TOKEN_EXPIRED: 'Session expired. Please login again.',
  SERVER_ERROR: 'Something went wrong. Please try again.',
  TIMEOUT: 'Request timed out. Please try again.',
  EMPTY_RESPONSE: 'No response from server'
};

// Success messages
export const SUCCESS_MESSAGES = {
  REGISTRATION_SUCCESS: 'Account created successfully!',
  LOGIN_SUCCESS: 'Login successful!',
  LOGOUT_SUCCESS: 'Logged out successfully!'
};

// Timeout values
export const TIMEOUT_VALUES = {
  REQUEST_TIMEOUT: 10000, // 10 seconds
  SESSION_TIMEOUT: 7 * 24 * 60 * 60 * 1000 // 7 days in milliseconds
};