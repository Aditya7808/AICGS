import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, UserProfile } from '../services/api';

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  signup: (email: string, password: string, full_name?: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
  createProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.getMe()
        .then(setUser)
        .catch((error) => {
          console.error('Auth check failed:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('refresh_token');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const response = await authAPI.login({ email, password });
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    
    // Get user profile after login
    try {
      const userData = await authAPI.getMe();
      setUser(userData);
    } catch (error: any) {
      console.error('Failed to get user profile:', error);
      
      // If profile doesn't exist (404), it's expected - user needs to create profile
      if (error.response?.status === 404) {
        console.log('No profile found, user will need to create one');
        // Don't throw error, let the app handle the missing profile
      } else {
        // For other errors, re-throw
        throw error;
      }
    }
  };

  const signup = async (email: string, password: string, full_name?: string) => {
    const signupResponse = await authAPI.signup({ email, password, full_name });
    
    // Note: With Supabase, we don't auto-login after signup
    // User needs to verify email first (depending on Supabase settings)
    console.log('Signup successful:', signupResponse.message);
    
    // Optionally auto-login if email confirmation is disabled
    if (signupResponse.email_confirmed) {
      await login(email, password);
    }
  };

  const createProfile = async () => {
    await authAPI.createProfile();
    // Refresh user data after creating profile
    const userData = await authAPI.getMe();
    setUser(userData);
  };

  const loginWithGoogle = async () => {
    try {
      const response = await authAPI.googleSignin();
      // Redirect to Google OAuth URL
      window.location.href = response.url;
    } catch (error) {
      console.error('Google OAuth initiation failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    loginWithGoogle,
    signup,
    logout,
    loading,
    createProfile
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
