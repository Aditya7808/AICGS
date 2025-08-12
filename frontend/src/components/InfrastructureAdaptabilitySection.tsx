import React from 'react';

const InfrastructureAdaptabilitySection: React.FC = () => {
  const adaptabilityFeatures = [
    {
      title: 'Network Condition Monitoring',
      description: 'Automatically detects and adapts to varying internet connectivity speeds and stability.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
        </svg>
      ),
      stats: '50% data reduction'
    },
    {
      title: 'Device Capability Assessment',
      description: 'Optimizes interface and functionality based on device specifications and capabilities.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      ),
      stats: '40% faster response'
    },
    {
      title: 'Progressive Enhancement',
      description: 'Delivers optimal experience across different technology environments and digital literacy levels.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      stats: '60% improvement'
    },
    {
      title: 'Offline Functionality',
      description: 'Core features work offline with intelligent synchronization when connectivity is restored.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
      ),
      stats: '70% core features'
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Intelligent Accessibility Optimization Protocol (IAOP)
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our advanced system automatically adapts to your device capabilities, network conditions, 
            and digital literacy level to ensure optimal performance across India's diverse technology landscape.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {adaptabilityFeatures.map((feature, index) => (
            <div 
              key={index}
              className="group bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 opacity-0 group-hover:opacity-5 transition-opacity duration-300"></div>
              
              <div className="relative">
                <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white mb-4">
                  {feature.icon}
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 text-sm leading-relaxed mb-4">
                  {feature.description}
                </p>

                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-3">
                  <div className="text-sm font-bold text-blue-600 mb-1">Performance Improvement</div>
                  <div className="text-lg font-bold text-gray-900">{feature.stats}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-6">
            <h3 className="text-2xl font-bold text-white mb-2">
              Infrastructure Challenge Solution
            </h3>
            <p className="text-blue-100">
              Addressing India's diverse technology infrastructure
            </p>
          </div>
          
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-green-400 to-green-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  ✓
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-3">Urban Areas</h4>
                <p className="text-gray-600">
                  Full-featured experience with advanced AI capabilities, real-time recommendations, and rich multimedia content.
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  ⚡
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-3">Semi-Urban Areas</h4>
                <p className="text-gray-600">
                  Optimized experience with adaptive content loading, reduced data usage, and core AI functionality.
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  📱
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-3">Rural Areas</h4>
                <p className="text-gray-600">
                  Essential features work offline, text-based interface, and simplified navigation optimized for basic devices.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-16 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Bridging the Digital Divide
            </h3>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Our IAOP ensures that every student, regardless of their technology environment, 
              receives quality career guidance adapted to their specific constraints and capabilities.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="text-3xl font-bold text-indigo-600 mb-2">2G+</div>
              <div className="text-gray-600 text-sm">Network Support</div>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="text-3xl font-bold text-purple-600 mb-2">Basic</div>
              <div className="text-gray-600 text-sm">Device Support</div>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="text-3xl font-bold text-blue-600 mb-2">65%</div>
              <div className="text-gray-600 text-sm">Rural Coverage</div>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="text-3xl font-bold text-green-600 mb-2">24/7</div>
              <div className="text-gray-600 text-sm">Availability</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default InfrastructureAdaptabilitySection;
