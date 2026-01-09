'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authClient, signIn, signUp, signOut, getSession } from '@/lib/auth';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<boolean>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isInitialized, setIsInitialized] = useState(false); // Track if auth state is initialized

  useEffect(() => {
    checkSession();
  }, []); // Only run once on mount

  const checkSession = async () => {
    try {
      // First check if we have a token in localStorage
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

      if (token) {
        // If we have a token, try to get session
        try {
          const session: any = await getSession();
          if (session?.user) {
            setUser({
              id: session.user?.id || '',
              email: session.user?.email || '',
              name: session.user?.name || session.user?.email || ''
            });
          } else {
            // If session call fails, clear the invalid token
            localStorage.removeItem('auth_token');
            setUser(null);
          }
        } catch (sessionError) {
          // If session call fails, clear the invalid token
          localStorage.removeItem('auth_token');
          setUser(null);
          console.error('Session check error:', sessionError);
        }
      } else {
        // No token in localStorage, user is not authenticated
        setUser(null);
      }
    } catch (error) {
      setUser(null);
      console.error('Session check error:', error);
    } finally {
      setLoading(false);
      setIsInitialized(true); // Mark as initialized after first check
    }
  };

  // Add effect to handle token changes
  useEffect(() => {
    if (user) {
      // Store user info in localStorage to persist across page refreshes
      localStorage.setItem('user_info', JSON.stringify(user));
    } else {
      // Clear user info when logging out
      localStorage.removeItem('user_info');
    }
  }, [user]);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      let result: any;

      // Try Better Auth client first
      try {
        result = await signIn.email({
          email,
          password,
        });

        // Better Auth client returns response with user data or error
        // Check if the response has the expected structure
        if (!result || typeof result !== 'object') {
          console.warn('Better Auth client returned unexpected response, attempting direct API call', result);
          throw new Error('Better Auth client returned unexpected response');
        }
      } catch (clientError) {
        console.warn('Better Auth client failed, attempting direct API call:', clientError);

        // Fallback to direct API call
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/sign-in/email`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
          console.error('Direct API call failed:', response.status, response.statusText);
          return false;
        }

        result = await response.json();
      }

      console.log('Sign in result:', result); // Debug logging

      // Handle response - check if it has user data
      // Better Auth response format may be different from our direct API response
      let userData: any;
      let sessionData: any;

      // Try different possible response structures
      if (result.user) {
        // Direct API response format: { user: {...}, session: {...} }
        userData = result.user;
        sessionData = result.session;
      } else if (result.data && result.data.user) {
        // Possible wrapped format: { data: { user: {...}, session: {...} } }
        userData = result.data.user;
        sessionData = result.data.session;
      } else if (result.token && result.user) {
        // Another possible format from Better Auth
        userData = result.user;
        sessionData = { accessToken: result.token };
      } else {
        // If we have a result but no user, it might be a success without user data
        console.error('Unexpected response format:', result);
        return false;
      }

      if (userData && userData.id) {
        setUser({
          id: userData.id,
          email: userData.email || email,
          name: userData.name || email
        });

        // Store token if available
        if (sessionData && sessionData.accessToken) {
          localStorage.setItem('auth_token', sessionData.accessToken);
        } else {
          // If we have user data but no access token, we may need to get the token differently
          // Try to get a session token using the authClient
          try {
            const session: any = await getSession(); // Using any to avoid complex type issues
            if (session && session.session) {
              // Better Auth stores session data in the session property
              const sessionToken = session.session.id; // Use session ID as token
              localStorage.setItem('auth_token', sessionToken);
            }
          } catch (getTokenError) {
            console.warn('Could not retrieve session token:', getTokenError);
          }
        }

        return true;
      } else {
        console.error('User data not found in response:', result);
        return false;
      }
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const signup = async (email: string, password: string, name?: string): Promise<boolean> => {
    try {
      const result: any = await signUp.email({
        email,
        password,
        name: name || email, // Better Auth requires name field
      });

      // Handle response - check different possible structures
      let sessionData: any;

      if (result.session) {
        // Direct API response format: { user: {...}, session: {...} }
        sessionData = result.session;
      } else if (result.data && result.data.session) {
        // Possible wrapped format: { data: { user: {...}, session: {...} } }
        sessionData = result.data.session;
      } else if (result.token) {
        // Another possible format from Better Auth
        sessionData = { accessToken: result.token };
      } else {
        // If no session data, check if it's just a success response
        console.log('Signup response:', result);
      }

      // Store token if available
      if (sessionData && sessionData.accessToken) {
        localStorage.setItem('auth_token', sessionData.accessToken);
      } else {
        // If no access token, try to get session token
        try {
          const session: any = await getSession(); // Using any to avoid complex type issues
          if (session && session.session) {
            // Better Auth stores session data in the session property
            const sessionToken = session.session.id; // Use session ID as token
            localStorage.setItem('auth_token', sessionToken);
          }
        } catch (getTokenError) {
          console.warn('Could not retrieve session token:', getTokenError);
        }
      }
      return true;
    } catch (error) {
      console.error('Signup error:', error);
      return false;
    }
  };

  const logout = async () => {
    try {
      await signOut();
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_info');
      setUser(null);
      window.location.href = '/login';
    } catch (error) {
      // Even if signOut fails, clear local state and token
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_info');
      setUser(null);
      window.location.href = '/login';
      console.error('Logout error:', error);
    }
  };

  const isAuthenticated = isInitialized && !!user && !loading;

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, signup, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};