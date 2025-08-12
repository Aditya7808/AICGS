import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import ProfileSetup from './ProfileSetup';

interface AuthenticatedWrapperProps {
  children: React.ReactNode;
}

const AuthenticatedWrapper: React.FC<AuthenticatedWrapperProps> = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();
  const [needsProfile, setNeedsProfile] = useState(false);
  const [checkingProfile, setCheckingProfile] = useState(true);

  useEffect(() => {
    if (!loading && isAuthenticated) {
      // Check if user profile exists
      const token = localStorage.getItem('token');
      if (token && !user) {
        // User is authenticated but no profile data
        setNeedsProfile(true);
      }
      setCheckingProfile(false);
    } else if (!loading) {
      setCheckingProfile(false);
    }
  }, [loading, isAuthenticated, user]);

  if (loading || checkingProfile) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated && needsProfile) {
    return (
      <ProfileSetup 
        onProfileCreated={() => {
          setNeedsProfile(false);
          window.location.reload(); // Refresh to get updated user data
        }} 
      />
    );
  }

  return <>{children}</>;
};

export default AuthenticatedWrapper;
