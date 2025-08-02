import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';

const Hero: React.FC = () => {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();

  return (
    <section className="relative min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-secondary-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float" style={{animationDelay: '2s'}}></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-accent-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float" style={{animationDelay: '4s'}}></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center space-y-8">
          {/* Main headline */}
          <div className="space-y-4 animate-fade-in">
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold leading-tight">
              <span className="block text-gray-900">Discover Your</span>
              <span className="block gradient-text">Perfect Career</span>
              <span className="block text-gray-900">Path</span>
            </h1>
            <p className="text-xl sm:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
              {t('hero.subtitle')}
            </p>
          </div>

          {/* Feature highlights */}
          <div className="flex flex-wrap justify-center gap-4 text-sm font-medium animate-slide-up" style={{animationDelay: '0.2s'}}>
            <span className="bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border border-gray-200 shadow-soft">
              🤖 AI-Powered Matching
            </span>
            <span className="bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border border-gray-200 shadow-soft">
              🌍 Location-Based
            </span>
            <span className="bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border border-gray-200 shadow-soft">
              📊 Personalized Results
            </span>
            <span className="bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border border-gray-200 shadow-soft">
              🔄 Multi-language
            </span>
          </div>

          {/* CTA Section */}
          <div className="space-y-6 animate-slide-up" style={{animationDelay: '0.4s'}}>
            {isAuthenticated ? (
              <Link
                to="/assessment"
                className="inline-flex items-center bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300 shadow-large hover:shadow-xl transform hover:-translate-y-1 group"
              >
                {t('hero.cta')}
                <svg className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
            ) : (
              <div className="space-y-4">
                <Link
                  to="/signup"
                  className="inline-flex items-center bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300 shadow-large hover:shadow-xl transform hover:-translate-y-1 group"
                >
                  {t('hero.cta')}
                  <svg className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
                <p className="text-gray-600">
                  {t('hero.loginPrompt')}{' '}
                  <Link to="/login" className="text-primary-600 hover:text-primary-700 font-semibold underline underline-offset-2">
                    {t('common.login')}
                  </Link>
                </p>
              </div>
            )}
          </div>

          {/* Stats section */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 pt-16 animate-slide-up" style={{animationDelay: '0.6s'}}>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">1000+</div>
              <div className="text-gray-600">Career Paths</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">95%</div>
              <div className="text-gray-600">Accuracy Rate</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">50K+</div>
              <div className="text-gray-600">Happy Users</div>
            </div>
          </div>
        </div>

        {/* Visual elements */}
        <div className="relative mt-20 animate-slide-up" style={{animationDelay: '0.8s'}}>
          <div className="relative mx-auto max-w-4xl">
            {/* Mockup dashboard */}
            <div className="bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden">
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                  <div className="ml-4 text-sm text-gray-600">CareerBuddy Dashboard</div>
                </div>
              </div>
              <div className="p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                    <div className="space-y-2">
                      <div className="h-3 bg-primary-200 rounded w-full"></div>
                      <div className="h-3 bg-secondary-200 rounded w-4/5"></div>
                      <div className="h-3 bg-accent-200 rounded w-3/5"></div>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-primary-500 rounded-full"></div>
                      <div className="h-3 bg-gray-200 rounded flex-1"></div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-secondary-500 rounded-full"></div>
                      <div className="h-3 bg-gray-200 rounded flex-1"></div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-accent-500 rounded-full"></div>
                      <div className="h-3 bg-gray-200 rounded flex-1"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
