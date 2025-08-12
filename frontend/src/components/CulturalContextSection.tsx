import React from 'react';

const CulturalContextSection: React.FC = () => {
  const culturalFeatures = [
    {
      title: 'Regional Language Support',
      description: 'Native support for 15+ Indian languages including Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, and more.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
        </svg>
      )
    },
    {
      title: 'Cultural Context Preservation',
      description: 'Career recommendations that respect family values, community expectations, and regional traditions.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      )
    },
    {
      title: 'Family Engagement Tools',
      description: 'Features designed to help parents understand modern career options and support their children effectively.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
        </svg>
      )
    },
    {
      title: 'Rural-Urban Adaptive Guidance',
      description: 'Tailored recommendations based on geographic location, infrastructure, and local economic opportunities.',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      )
    }
  ];

  const supportedLanguages = [
    'हिन्दी (Hindi)', 'தமிழ் (Tamil)', 'తెలుగు (Telugu)', 'বাংলা (Bengali)',
    'मराठी (Marathi)', 'ગુજરાતી (Gujarati)', 'ಕನ್ನಡ (Kannada)', 'മലയാളം (Malayalam)',
    'ਪੰਜਾਬੀ (Punjabi)', 'অসমীয়া (Assamese)', 'ଓଡ଼ିଆ (Odia)', 'उर्दू (Urdu)',
    'संस्कृत (Sanskrit)', 'नेपाली (Nepali)', 'मैथिली (Maithili)'
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Culturally-Sensitive AI for India
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our AICGS system is specifically designed to understand and respect India's rich cultural diversity, 
            linguistic variety, and regional differences while providing personalized career guidance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {culturalFeatures.map((feature, index) => (
            <div 
              key={index}
              className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
            >
              <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg text-white mb-4">
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-6">
            <h3 className="text-2xl font-bold text-white mb-2">
              15+ Indian Languages Supported
            </h3>
            <p className="text-indigo-100">
              Making career guidance accessible in your native language
            </p>
          </div>
          
          <div className="p-8">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {supportedLanguages.map((language, index) => (
                <div 
                  key={index}
                  className="bg-gray-50 rounded-lg p-3 text-center hover:bg-indigo-50 transition-colors duration-200"
                >
                  <span className="text-sm font-medium text-gray-700">
                    {language}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-16 bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl p-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-green-600 mb-2">65%</div>
              <div className="text-gray-700 font-medium">Rural Population Served</div>
              <div className="text-gray-600 text-sm mt-1">Bridging the rural-urban guidance gap</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">75%</div>
              <div className="text-gray-700 font-medium">Cultural Context Preserved</div>
              <div className="text-gray-600 text-sm mt-1">Maintaining cultural appropriateness</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-600 mb-2">40%</div>
              <div className="text-gray-700 font-medium">Improved Family Engagement</div>
              <div className="text-gray-600 text-sm mt-1">Better family involvement in career planning</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CulturalContextSection;
