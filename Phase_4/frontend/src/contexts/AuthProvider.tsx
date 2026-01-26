"use client";

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";

interface User {
  id: string;
  email?: string;
}

interface AuthContextType {
  user: User | null;
  login: (userData: any) => void;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem("auth_token");
    const userId = localStorage.getItem("user_id");

    console.log('🔍 AuthProvider checking existing session:', { token: token?.substring(0, 20), userId });

    if (token && userId) {
      setUser({ id: userId });
      console.log('✅ User restored from localStorage:', userId);
    } else {
      console.log('❌ No existing session found');
    }

    setLoading(false);
  }, []);

  const login = (userData: any) => {
    console.log('🔑 AuthProvider.login() called with:', userData);
    
    // Note: authService already saved to localStorage, so we just update state
    // But we'll save again here to be safe (idempotent operation)
    if (userData.token) {
      localStorage.setItem("auth_token", userData.token);
    }
    if (userData.user_id) {
      localStorage.setItem("user_id", userData.user_id);
    }
    
    setUser({ id: userData.user_id, email: userData.email });
    
    console.log('✅ User state updated:', { id: userData.user_id, email: userData.email });
  };

  const logout = async () => {
    console.log('🚪 Logging out...');
    try {
      const token = localStorage.getItem("auth_token");
      if (token) {
        const apiUrl =
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

        await fetch(`${apiUrl}/api/auth/logout`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        console.log('✅ Logout API call successful');
      }
    } catch (error) {
      console.error("❌ Logout API error:", error);
    } finally {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user_id");
      setUser(null);
      console.log('✅ Logout complete');
    }
  };

  const value: AuthContextType = {
    user,
    login,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;