import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import LanguageToggle from './LanguageToggle';

const Navbar: React.FC = () => {
  const { t } = useTranslation();
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="bg-white/95 backdrop-blur-sm shadow-soft border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">CB</span>
              </div>
              <h1 className="text-2xl font-bold gradient-text">CareerBuddy</h1>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <LanguageToggle />
            
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <Link
                  to="/assessment"
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-primary-50"
                >
                  {t('navigation.assessment')}
                </Link>
                <Link
                  to="/results"
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-primary-50"
                >
                  {t('navigation.results')}
                </Link>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-sm">
                      {user?.username?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="text-gray-700 text-sm font-medium">
                    {user?.username}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="btn-secondary text-sm"
                >
                  {t('common.logout')}
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-primary-600 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-primary-50"
                >
                  {t('common.login')}
                </Link>
                <Link
                  to="/signup"
                  className="btn-primary text-sm"
                >
                  {t('common.signup')}
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMobileMenu}
              className="text-gray-700 hover:text-gray-900 focus:outline-none focus:text-gray-900 p-2"
            >
              <svg className="h-6 w-6 fill-current" viewBox="0 0 24 24">
                {isMobileMenuOpen ? (
                  <path fillRule="evenodd" clipRule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z" />
                ) : (
                  <path fillRule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-white border-t border-gray-200">
              <LanguageToggle />
              
              {isAuthenticated ? (
                <>
                  <div className="flex items-center space-x-3 px-3 py-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
                      <span className="text-white font-semibold text-sm">
                        {user?.username?.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <span className="text-gray-700 font-medium">
                      {user?.username}
                    </span>
                  </div>
                  <Link
                    to="/assessment"
                    className="block px-3 py-2 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {t('navigation.assessment')}
                  </Link>
                  <Link
                    to="/results"
                    className="block px-3 py-2 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {t('navigation.results')}
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-3 py-2 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200"
                  >
                    {t('common.logout')}
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="block px-3 py-2 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {t('common.login')}
                  </Link>
                  <Link
                    to="/signup"
                    className="block px-3 py-2 bg-primary-600 text-white hover:bg-primary-700 rounded-lg transition-all duration-200"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {t('common.signup')}
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
