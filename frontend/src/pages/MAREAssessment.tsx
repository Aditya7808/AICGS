import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import MAREAssessmentForm from '../components/MAREAssessmentForm';
import { useTranslation } from 'react-i18next';

const MAREAssessment: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { t } = useTranslation();

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            {t('mare.title', 'MARE AI Career Assessment')}
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {t('mare.description', 'Get personalized career recommendations using our Multi-Dimensional Adaptive Recommendation Engine. Complete the comprehensive assessment to receive AI-powered insights tailored to your unique profile.')}
          </p>
        </div>

        {/* Key Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 text-3xl mb-4">🎯</div>
            <h3 className="text-lg font-semibold mb-2">{t('mare.feature1.title', 'Multi-Dimensional Analysis')}</h3>
            <p className="text-gray-600">{t('mare.feature1.desc', 'Analyzes 6 key dimensions: skills, culture, economics, geography, social factors, and growth potential.')}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-green-600 text-3xl mb-4">🧠</div>
            <h3 className="text-lg font-semibold mb-2">{t('mare.feature2.title', 'AI-Powered Insights')}</h3>
            <p className="text-gray-600">{t('mare.feature2.desc', 'Advanced machine learning algorithms provide highly accurate career matches based on your unique profile.')}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-purple-600 text-3xl mb-4">🌍</div>
            <h3 className="text-lg font-semibold mb-2">{t('mare.feature3.title', 'Cultural Awareness')}</h3>
            <p className="text-gray-600">{t('mare.feature3.desc', 'Considers your cultural context, family values, and social environment for relevant recommendations.')}</p>
          </div>
        </div>

        {/* Assessment Form */}
        <div className="bg-white rounded-lg shadow-lg">
          <MAREAssessmentForm />
        </div>
      </div>
    </div>
  );
};

export default MAREAssessment;
