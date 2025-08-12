import React from 'react';
import { Link } from 'react-router-dom';

const Features: React.FC = () => {
  const features = [
    "Multi-Dimensional Adaptive Recommendations (MARE)",
    "Context-Aware Skills Translation (CAST-F)", 
    "15+ Indian Language Support",
    "Cultural Context Preservation",
    "Infrastructure-Adaptive Technology (IAOP)",
    "Privacy-Preserving Learning (HFLS)",
    "Family Engagement Tools",
    "Rural & Urban Specific Guidance"
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-6">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 leading-tight">
                AI-Powered Career Guidance System (AICGS)
              </h2>
              <p className="text-lg text-gray-600 leading-relaxed">
                Experience India's most advanced career guidance platform with culturally-sensitive AI that adapts to your social, economic, geographic, and linguistic context.
              </p>
            </div>

            {/* Features List */}
            <div className="space-y-4">
              {features.map((feature, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <span className="text-gray-700 font-medium">{feature}</span>
                </div>
              ))}
            </div>

            {/* CTA Button */}
            <div className="pt-4">
              <Link
                to="/mare-assessment"
                className="inline-flex items-center bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                Start MARE AI Assessment
              </Link>
            </div>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="relative mx-auto max-w-md">
              {/* Main Image Container */}
              <div className="bg-gradient-to-br from-primary-100 to-purple-100 rounded-2xl p-8 h-96 flex items-end justify-center relative overflow-hidden">
                {/* Woman Figure */}
                <div className="w-48 h-64 relative">
                  {/* Head */}
                  <div className="w-16 h-16 bg-gradient-to-b from-yellow-200 to-yellow-300 rounded-full mx-auto mb-2"></div>
                  {/* Hair */}
                  <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-20 h-12 bg-gradient-to-b from-amber-600 to-amber-700 rounded-t-full"></div>
                  {/* Body */}
                  <div className="w-full h-40 bg-gradient-to-b from-blue-400 to-blue-500 rounded-t-3xl relative">
                    {/* Arms */}
                    <div className="absolute -left-4 top-4 w-8 h-16 bg-gradient-to-b from-blue-400 to-blue-500 rounded-full transform -rotate-12"></div>
                    <div className="absolute -right-4 top-4 w-8 h-16 bg-gradient-to-b from-blue-400 to-blue-500 rounded-full transform rotate-12"></div>
                  </div>
                </div>
                
                {/* City Background */}
                <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-gray-400 to-gray-300">
                  {/* Buildings */}
                  <div className="absolute bottom-0 left-4 w-12 h-20 bg-gray-600 rounded-t-lg"></div>
                  <div className="absolute bottom-0 left-20 w-8 h-16 bg-gray-700 rounded-t-lg"></div>
                  <div className="absolute bottom-0 right-8 w-10 h-24 bg-gray-600 rounded-t-lg"></div>
                  <div className="absolute bottom-0 right-24 w-6 h-12 bg-gray-700 rounded-t-lg"></div>
                </div>

                {/* Floating Elements */}
                <div className="absolute top-4 left-4 w-4 h-4 bg-yellow-400 rounded-full animate-bounce-subtle"></div>
                <div className="absolute top-8 right-8 w-3 h-3 bg-green-400 rounded-full animate-bounce-subtle" style={{animationDelay: '1s'}}></div>
                <div className="absolute bottom-32 left-8 w-2 h-2 bg-blue-400 rounded-full animate-bounce-subtle" style={{animationDelay: '2s'}}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;
