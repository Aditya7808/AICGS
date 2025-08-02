import React from 'react';
import { useTranslation } from 'react-i18next';

const Features: React.FC = () => {
  const { t } = useTranslation();

  const features = [
    {
      icon: "🧠",
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze your skills, interests, and personality to provide accurate career recommendations.",
      color: "from-primary-500 to-primary-700"
    },
    {
      icon: "🎯",
      title: "Personalized Matching",
      description: "Get career suggestions tailored specifically to your unique profile, location, and career aspirations.",
      color: "from-secondary-500 to-secondary-700"
    },
    {
      icon: "📊",
      title: "Comprehensive Assessment",
      description: "Detailed evaluation covering skills, interests, values, and work preferences for holistic career guidance.",
      color: "from-accent-500 to-accent-700"
    },
    {
      icon: "🌍",
      title: "Location-Based Results",
      description: "Discover career opportunities and educational paths available in your specific geographical area.",
      color: "from-green-500 to-green-700"
    },
    {
      icon: "📈",
      title: "Growth Tracking",
      description: "Monitor your career development journey with progress tracking and milestone achievements.",
      color: "from-purple-500 to-purple-700"
    },
    {
      icon: "🔄",
      title: "Multi-Language Support",
      description: "Access career guidance in multiple languages including English and Hindi for better understanding.",
      color: "from-indigo-500 to-indigo-700"
    }
  ];

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Why Choose <span className="gradient-text">CareerBuddy</span>?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our platform combines cutting-edge AI technology with comprehensive career expertise to guide you towards your ideal profession.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group relative bg-white rounded-2xl p-8 border border-gray-100 shadow-soft hover:shadow-large transition-all duration-500 transform hover:-translate-y-2"
            >
              {/* Background gradient on hover */}
              <div className={`absolute inset-0 bg-gradient-to-r ${feature.color} opacity-0 group-hover:opacity-5 rounded-2xl transition-opacity duration-500`}></div>
              
              {/* Content */}
              <div className="relative z-10">
                <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors duration-300">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>

              {/* Decorative corner */}
              <div className={`absolute top-0 right-0 w-16 h-16 bg-gradient-to-br ${feature.color} opacity-10 rounded-bl-2xl rounded-tr-2xl`}></div>
            </div>
          ))}
        </div>

        {/* Call to action */}
        <div className="text-center mt-16">
          <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-2xl p-8 max-w-4xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Ready to Discover Your Career Path?
            </h3>
            <p className="text-gray-600 mb-6">
              Join thousands of students who have found their perfect career match with CareerBuddy.
            </p>
            <button className="btn-primary text-lg px-8 py-3">
              Start Your Journey Today
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;
