import React from 'react';
import { useTranslation } from 'react-i18next';
import CASTFrameworkDemo from '../components/CASTFrameworkDemo';

const CASTDemo: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {t('cast.title', 'CAST Framework')}
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {t('cast.subtitle', 'Context-Aware Skills Translation Framework for multilingual career guidance with cultural sensitivity')}
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            {t('cast.about_title', 'About CAST Framework')}
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-medium text-gray-800 mb-2">
                {t('cast.features_title', 'Key Features')}
              </h3>
              <ul className="space-y-2 text-gray-600">
                <li>• {t('cast.feature_1', 'Multilingual NLP for 15+ Indian languages')}</li>
                <li>• {t('cast.feature_2', 'Cultural context preservation')}</li>
                <li>• {t('cast.feature_3', 'Cross-cultural skills mapping')}</li>
                <li>• {t('cast.feature_4', 'Bias detection and reduction')}</li>
                <li>• {t('cast.feature_5', 'Alternative translation suggestions')}</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-800 mb-2">
                {t('cast.supported_languages', 'Supported Languages')}
              </h3>
              <div className="grid grid-cols-3 gap-2 text-sm text-gray-600">
                <span>English</span>
                <span>Hindi (हिंदी)</span>
                <span>Tamil (தமிழ்)</span>
                <span>Telugu (తెలుగు)</span>
                <span>Bengali (বাংলা)</span>
                <span>Marathi (मराठी)</span>
                <span>Gujarati (ગુજરાતી)</span>
                <span>Kannada (ಕನ್ನಡ)</span>
                <span>Malayalam (മലയാളം)</span>
                <span>Punjabi (ਪੰਜਾਬੀ)</span>
                <span>Odia (ଓଡ଼ିଆ)</span>
                <span>Assamese (অসমীয়া)</span>
                <span>Urdu (اردو)</span>
                <span>Sindhi (سندھی)</span>
                <span>Nepali (नेपाली)</span>
                <span>Konkani (कोंकणी)</span>
              </div>
            </div>
          </div>
        </div>

        <CASTFrameworkDemo />
      </div>
    </div>
  );
};

export default CASTDemo;
