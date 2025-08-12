// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const config = {
  apiBaseUrl: API_BASE_URL,
  // Remove trailing slash if present
  apiUrl: API_BASE_URL.replace(/\/$/, ''),
  
  // Environment
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  
  // Feature flags
  enableAnalytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
  
  // App info
  appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',
  appName: 'CareerBuddy',
};

// API endpoints
export const endpoints = {
  auth: {
    signup: '/api/auth/signup',
    login: '/api/auth/login',
    profile: '/api/auth/profile',
    updateProfile: '/api/auth/profile',
  },
  recommendations: '/api/recommendations',
  progress: '/api/progress',
  education: '/api/education',
  mare: '/api/v1/mare',
  cast: '/api/cast',
  ml: '/api/v1',
};

export default config;
