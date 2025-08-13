import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, UserProfile } from '../services/api';

// Types for Supabase integration
interface SupabaseUser {
  id: string;
  email?: string;
  user_metadata?: any;
}

interface AuthContextType {
  user: UserProfile | null;
  supabaseUser: SupabaseUser | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  loginWithSupabaseGoogle: () => Promise<void>;
  signup: (email: string, password: string, full_name?: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
  createProfile: () => Promise<void>;
  useSupabaseDirect: boolean;
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
  const [supabaseUser, setSupabaseUser] = useState<SupabaseUser | null>(null);
  const [loading, setLoading] = useState(true);

  // Check if Supabase is available (environment variables set)
  const useSupabaseDirect = Boolean(
    import.meta.env.VITE_SUPABASE_URL && 
    import.meta.env.VITE_SUPABASE_ANON_KEY
  );

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        if (useSupabaseDirect) {
          // Try Supabase direct authentication first
          await initializeSupabaseAuth();
        } else {
          // Fallback to backend API authentication
          await initializeBackendAuth();
        }
      } catch (error) {
        console.error('Auth initialization failed:', error);
        setLoading(false);
      }
    };

    initializeAuth();
  }, [useSupabaseDirect]);

  const initializeSupabaseAuth = async () => {
    try {
      // Dynamic import to avoid errors if package not installed
      const { createClient } = await import('@supabase/supabase-js');
      const supabase = createClient(
        import.meta.env.VITE_SUPABASE_URL!,
        import.meta.env.VITE_SUPABASE_ANON_KEY!
      );

      // Check current session
      const { data: { session }, error } = await supabase.auth.getSession();
      
      if (error) {
        console.error('Supabase session error:', error);
        await initializeBackendAuth();
        return;
      }

      if (session?.user) {
        setSupabaseUser({
          id: session.user.id,
          email: session.user.email,
          user_metadata: session.user.user_metadata
        });

        // Try to get full user profile from backend
        try {
          if (session.access_token) {
            localStorage.setItem('token', session.access_token);
            const userData = await authAPI.getMe();
            setUser(userData);
          }
        } catch (profileError) {
          console.log('No backend profile found, using Supabase user data');
        }
      }

      // Listen for auth state changes
      supabase.auth.onAuthStateChange(async (event: any, session: any) => {
        console.log('Supabase auth state changed:', event);
        
        if (event === 'SIGNED_IN' && session?.user) {
          setSupabaseUser({
            id: session.user.id,
            email: session.user.email,
            user_metadata: session.user.user_metadata
          });

          if (session.access_token) {
            localStorage.setItem('token', session.access_token);
            if (session.refresh_token) {
              localStorage.setItem('refresh_token', session.refresh_token);
            }
          }
        } else if (event === 'SIGNED_OUT') {
          setSupabaseUser(null);
          setUser(null);
          localStorage.removeItem('token');
          localStorage.removeItem('refresh_token');
        }
      });

      setLoading(false);
    } catch (supabaseError) {
      console.warn('Supabase not available, falling back to backend auth:', supabaseError);
      await initializeBackendAuth();
    }
  };

  const initializeBackendAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const userData = await authAPI.getMe();
        setUser(userData);
      } catch (error) {
        console.error('Backend auth check failed:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
      }
    }
    setLoading(false);
  };

  const login = async (email: string, password: string) => {
    if (useSupabaseDirect) {
      await loginWithSupabase(email, password);
    } else {
      await loginWithBackend(email, password);
    }
  };

  const loginWithSupabase = async (email: string, password: string) => {
    try {
      const { createClient } = await import('@supabase/supabase-js');
      const supabase = createClient(
        import.meta.env.VITE_SUPABASE_URL!,
        import.meta.env.VITE_SUPABASE_ANON_KEY!
      );

      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) throw error;

      if (data.session?.access_token) {
        localStorage.setItem('token', data.session.access_token);
        if (data.session.refresh_token) {
          localStorage.setItem('refresh_token', data.session.refresh_token);
        }
      }
    } catch (error) {
      console.error('Supabase login failed, trying backend:', error);
      await loginWithBackend(email, password);
    }
  };

  const loginWithBackend = async (email: string, password: string) => {
    const response = await authAPI.login({ email, password });
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    
    try {
      const userData = await authAPI.getMe();
      setUser(userData);
    } catch (error: any) {
      console.error('Failed to get user profile:', error);
      if (error.response?.status === 404) {
        console.log('No profile found, user will need to create one');
      } else {
        throw error;
      }
    }
  };

  const signup = async (email: string, password: string, full_name?: string) => {
    if (useSupabaseDirect) {
      await signupWithSupabase(email, password, full_name);
    } else {
      await signupWithBackend(email, password, full_name);
    }
  };

  const signupWithSupabase = async (email: string, password: string, full_name?: string) => {
    try {
      const { createClient } = await import('@supabase/supabase-js');
      const supabase = createClient(
        import.meta.env.VITE_SUPABASE_URL!,
        import.meta.env.VITE_SUPABASE_ANON_KEY!
      );

      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: full_name || '',
          }
        }
      });

      if (error) throw error;

      console.log('Supabase signup successful:', data.user?.email_confirmed_at ? 'confirmed' : 'needs confirmation');
    } catch (error) {
      console.error('Supabase signup failed, trying backend:', error);
      await signupWithBackend(email, password, full_name);
    }
  };

  const signupWithBackend = async (email: string, password: string, full_name?: string) => {
    const signupResponse = await authAPI.signup({ email, password, full_name });
    console.log('Backend signup successful:', signupResponse.message);
    
    if (signupResponse.email_confirmed) {
      await loginWithBackend(email, password);
    }
  };

  const createProfile = async () => {
    await authAPI.createProfile();
    const userData = await authAPI.getMe();
    setUser(userData);
  };

  const loginWithGoogle = async () => {
    try {
      console.log('Initiating Google OAuth via backend...');
      const response = await authAPI.googleSignin();
      console.log('Google OAuth URL received:', response.url);
      
      window.location.href = response.url;
    } catch (error: any) {
      console.error('Google OAuth initiation failed:', error);
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      });
      throw new Error(error.response?.data?.detail || error.message || 'Failed to initiate Google sign-up');
    }
  };

  const loginWithSupabaseGoogle = async () => {
    try {
      if (!useSupabaseDirect) {
        throw new Error('Supabase direct auth not available, falling back to backend');
      }

      const { createClient } = await import('@supabase/supabase-js');
      const supabase = createClient(
        import.meta.env.VITE_SUPABASE_URL!,
        import.meta.env.VITE_SUPABASE_ANON_KEY!
      );

      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`
        }
      });

      if (error) throw error;

      console.log('Supabase Google OAuth initiated successfully');
    } catch (error) {
      console.error('Supabase Google OAuth failed, falling back to backend:', error);
      await loginWithGoogle();
    }
  };

  const logout = async () => {
    try {
      if (useSupabaseDirect && supabaseUser) {
        try {
          const { createClient } = await import('@supabase/supabase-js');
          const supabase = createClient(
            import.meta.env.VITE_SUPABASE_URL!,
            import.meta.env.VITE_SUPABASE_ANON_KEY!
          );
          await supabase.auth.signOut();
        } catch (supabaseError) {
          console.error('Supabase logout failed:', supabaseError);
        }
      }

      // Always try backend logout as well
      try {
        await authAPI.logout();
      } catch (error) {
        console.error('Backend logout failed:', error);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      setSupabaseUser(null);
    }
  };

  const value = {
    user,
    supabaseUser,
    isAuthenticated: !!(user || supabaseUser),
    login,
    loginWithGoogle,
    loginWithSupabaseGoogle,
    signup,
    logout,
    loading,
    createProfile,
    useSupabaseDirect
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
