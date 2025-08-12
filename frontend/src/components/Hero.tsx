import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Hero: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <section className="relative min-h-screen bg-gradient-to-br from-gray-50 via-white to-purple-50 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float" style={{animationDelay: '2s'}}></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float" style={{animationDelay: '4s'}}></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center min-h-screen">
          {/* Left Content */}
          <div className="space-y-8">
            {/* Main headline */}
            <div className="space-y-6 animate-fade-in">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight">
                <span className="block text-gray-900">AI-Powered Career</span>
                <span className="block text-gray-900">Guidance for</span>
                <span className="block text-primary-600">Everyone</span>
              </h1>
              <p className="text-xl text-gray-600 max-w-lg leading-relaxed">
                Discover personalized career paths with our culturally-aware AI system supporting 15+ Indian languages, designed for urban, semi-urban and rural students across India
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 animate-slide-up" style={{animationDelay: '0.2s'}}>
              {isAuthenticated ? (
                <>
                  <Link
                    to="/mare-assessment"
                    className="inline-flex items-center justify-center bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                  >
                    🧠 MARE AI Assessment
                  </Link>
                  <Link
                    to="/cast-demo"
                    className="inline-flex items-center justify-center border-2 border-purple-500 text-purple-600 hover:bg-purple-500 hover:text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300"
                  >
                    🌐 CAST AI Demo
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    to="/mare-assessment"
                    className="inline-flex items-center justify-center bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                  >
                    🧠 Start MARE AI Assessment
                  </Link>
                  <Link
                    to="/cast-demo"
                    className="inline-flex items-center justify-center border-2 border-purple-500 text-purple-600 hover:bg-purple-500 hover:text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300"
                  >
                    🌐 CAST AI Demo
                  </Link>
                </>
              )}
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 pt-8 animate-slide-up" style={{animationDelay: '0.4s'}}>
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <svg className="w-6 h-6 text-primary-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                  <span className="text-2xl font-bold text-primary-600">600M+</span>
                </div>
                <div className="text-gray-600 text-sm">Indian Youth</div>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <svg className="w-6 h-6 text-primary-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                  </svg>
                  <span className="text-2xl font-bold text-primary-600">15+</span>
                </div>
                <div className="text-gray-600 text-sm">Languages</div>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <svg className="w-6 h-6 text-primary-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  <span className="text-2xl font-bold text-primary-600">AI</span>
                </div>
                <div className="text-gray-600 text-sm">Powered</div>
              </div>
            </div>
          </div>

          {/* Right Content - Animated Cards */}
          <div className="relative animate-slide-up" style={{animationDelay: '0.6s'}}>
            <div className="relative mx-auto max-w-md">
              {/* Instructor Card */}
              <div className="absolute top-0 right-0 bg-white rounded-xl shadow-lg p-4 z-20 transform rotate-3 hover:rotate-0 transition-transform duration-300">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-lg">AT</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 text-sm">Ali Tufan</h4>
                    <p className="text-gray-500 text-xs">Instructor</p>
                  </div>
                </div>
                <div className="mt-2 flex items-center">
                  <div className="flex text-yellow-400">
                    {'★'.repeat(5)}
                  </div>
                  <span className="text-gray-500 text-xs ml-1">4.9</span>
                </div>
              </div>

              {/* Success Popup */}
              <div className="absolute top-16 left-0 bg-green-500 text-white rounded-lg p-3 z-10 transform -rotate-2 hover:rotate-0 transition-transform duration-300">
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="font-semibold text-sm">Admission Success!</span>
                </div>
              </div>

              {/* Free Courses Tag */}
              <div className="absolute bottom-4 right-4 bg-blue-500 text-white rounded-lg p-3 z-10 transform rotate-1 hover:rotate-0 transition-transform duration-300">
                <div className="text-center">
                  <div className="text-lg font-bold">40+</div>
                  <div className="text-xs">Free Courses</div>
                </div>
              </div>

              {/* Main Image Container */}
              <div className="bg-gradient-to-br from-primary-100 to-purple-100 rounded-2xl p-8 h-96 flex items-end justify-center relative overflow-hidden">
                {/* Student Figure */}
                <div className="w-48 h-56 bg-gradient-to-b from-gray-300 to-gray-400 rounded-t-full relative">
                  {/* Head */}
                  <div className="w-16 h-16 bg-gradient-to-b from-yellow-200 to-yellow-300 rounded-full mx-auto mb-2"></div>
                  {/* Body */}
                  <div className="w-full h-32 bg-gradient-to-b from-blue-400 to-blue-500 rounded-t-3xl"></div>
                </div>
                
                {/* Floating Elements */}
                <div className="absolute top-4 left-4 w-4 h-4 bg-yellow-400 rounded-full animate-bounce-subtle"></div>
                <div className="absolute top-8 right-8 w-3 h-3 bg-green-400 rounded-full animate-bounce-subtle" style={{animationDelay: '1s'}}></div>
                <div className="absolute bottom-16 left-8 w-2 h-2 bg-blue-400 rounded-full animate-bounce-subtle" style={{animationDelay: '2s'}}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
