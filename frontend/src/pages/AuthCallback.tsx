import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authAPI } from '../services/api';

const AuthCallback: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const code = searchParams.get('code');
        const error = searchParams.get('error');

        if (error) {
          setStatus('error');
          setError(`OAuth error: ${error}`);
          return;
        }

        if (!code) {
          setStatus('error');
          setError('No authorization code received');
          return;
        }

        // Exchange code for tokens
        const tokenResponse = await authAPI.googleCallback(code);
        
        // Store tokens
        localStorage.setItem('token', tokenResponse.access_token);
        localStorage.setItem('refresh_token', tokenResponse.refresh_token);

        // Get user profile
        try {
          await authAPI.getMe();
          // User data will be loaded by AuthContext on next page load
          setStatus('success');
          
          // Redirect to home after a brief delay
          setTimeout(() => {
            navigate('/', { replace: true });
          }, 2000);
        } catch (profileError) {
          console.error('Failed to get user profile after OAuth:', profileError);
          // Still consider OAuth successful, user can create profile later
          setStatus('success');
          setTimeout(() => {
            navigate('/', { replace: true });
          }, 2000);
        }

      } catch (err: any) {
        console.error('OAuth callback error:', err);
        setStatus('error');
        setError(err.response?.data?.detail || 'Authentication failed');
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  const handleRetry = () => {
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl flex items-center justify-center shadow-lg">
            <span className="text-white font-bold text-2xl">CB</span>
          </div>
        </div>
        
        {status === 'loading' && (
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Completing Authentication...
            </h2>
            <div className="flex justify-center mb-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
            <p className="text-gray-600">
              Please wait while we complete your Google sign-in.
            </p>
          </div>
        )}

        {status === 'success' && (
          <div className="text-center">
            <div className="mb-4">
              <svg className="w-16 h-16 text-green-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Authentication Successful!
            </h2>
            <p className="text-gray-600 mb-4">
              You have been successfully signed in with Google.
            </p>
            <p className="text-sm text-gray-500">
              Redirecting to your dashboard...
            </p>
          </div>
        )}

        {status === 'error' && (
          <div className="text-center">
            <div className="mb-4">
              <svg className="w-16 h-16 text-red-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.996-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Authentication Failed
            </h2>
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
            <button
              onClick={handleRetry}
              className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Try Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthCallback;
