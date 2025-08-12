import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

interface GroqEnhancedSuggestion {
  career_title: string;
  personalized_insight: string;
  actionable_steps: string[];
  skill_development_plan: string[];
  cultural_considerations: string;
  timeline_suggestion: string;
  confidence_score: number;
}

interface MARERecommendation {
  career_id: string;
  title: string;
  industry: string;
  overall_score: number;
  dimension_scores: Record<string, number>;
  explanation: Record<string, string>;
  confidence_level: string;
}

interface EnhancedMAREResponse {
  standard_recommendations: MARERecommendation[];
  groq_enhanced_suggestions: GroqEnhancedSuggestion[];
  career_pathway_summary: string | null;
  enhancement_available: boolean;
}

interface Props {
  assessmentData?: any;
  onBack?: () => void;
}

const GroqEnhancedMAREResults: React.FC<Props> = ({ assessmentData, onBack }) => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [results, setResults] = useState<EnhancedMAREResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'suggestions' | 'pathway'>('overview');

  const fetchEnhancedRecommendations = async () => {
    if (!assessmentData || !user) return;

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/mare/recommendations/enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(assessmentData)
      });

      if (response.ok) {
        const data = await response.json();
        setResults(data);
      } else {
        console.error('Failed to fetch enhanced recommendations');
      }
    } catch (error) {
      console.error('Error fetching enhanced recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (assessmentData) {
      fetchEnhancedRecommendations();
    }
  }, [assessmentData]);

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100';
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500';
    if (score >= 0.6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">{t('mare.no_results', 'No results available')}</p>
        {onBack && (
          <button
            onClick={onBack}
            className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            {t('common.back', 'Back')}
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              🤖 {t('mare.enhanced_results_title', 'AI-Enhanced Career Recommendations')}
            </h1>
            <p className="text-gray-600">
              {t('mare.enhanced_subtitle', 'Powered by MARE Engine & Groq LLM for personalized insights')}
            </p>
          </div>
          {onBack && (
            <button
              onClick={onBack}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 flex items-center"
            >
              ← {t('common.back', 'Back')}
            </button>
          )}
        </div>

        {/* Enhancement Status */}
        <div className="mt-4 flex items-center space-x-2">
          <div className={`px-3 py-1 rounded-full text-sm ${
            results.enhancement_available 
              ? 'bg-green-100 text-green-800' 
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            {results.enhancement_available 
              ? '✨ AI Enhancement Active' 
              : '⚠️ AI Enhancement Unavailable'}
          </div>
          <span className="text-sm text-gray-500">
            {results.standard_recommendations.length} recommendations • 
            {results.groq_enhanced_suggestions.length} AI insights
          </span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'overview'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📊 Overview
          </button>
          <button
            onClick={() => setActiveTab('suggestions')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'suggestions'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            🤖 AI Insights ({results.groq_enhanced_suggestions.length})
          </button>
          <button
            onClick={() => setActiveTab('pathway')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'pathway'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            🗺️ Career Pathway
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.standard_recommendations.map((rec, index) => (
            <div key={rec.career_id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{rec.title}</h3>
                <span className="text-sm text-gray-500">#{index + 1}</span>
              </div>
              
              <p className="text-gray-600 mb-4">{rec.industry}</p>
              
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">Overall Score</span>
                  <span className="text-sm font-bold">{(rec.overall_score * 100).toFixed(0)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${getScoreColor(rec.overall_score)}`}
                    style={{ width: `${rec.overall_score * 100}%` }}
                  ></div>
                </div>
              </div>

              <div className="space-y-2">
                {Object.entries(rec.dimension_scores).slice(0, 3).map(([dimension, score]) => (
                  <div key={dimension} className="flex justify-between text-sm">
                    <span className="text-gray-600 capitalize">{dimension.replace('_', ' ')}</span>
                    <span className="font-medium">{(score * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>

              <div className={`mt-4 px-3 py-1 rounded-full text-xs ${
                rec.confidence_level === 'high' ? 'bg-green-100 text-green-800' :
                rec.confidence_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {rec.confidence_level} confidence
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'suggestions' && (
        <div className="space-y-6">
          {results.groq_enhanced_suggestions.length === 0 ? (
            <div className="text-center py-8 bg-gray-50 rounded-lg">
              <p className="text-gray-600 mb-2">
                {results.enhancement_available 
                  ? 'AI enhancements are being processed...' 
                  : 'AI enhancements are currently unavailable'}
              </p>
              <p className="text-sm text-gray-500">
                Standard recommendations are available in the Overview tab
              </p>
            </div>
          ) : (
            results.groq_enhanced_suggestions.map((suggestion, index) => (
              <div key={index} className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6 border border-purple-200">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-xl font-bold text-gray-900">{suggestion.career_title}</h3>
                  <div className={`px-3 py-1 rounded-full text-xs ${getConfidenceColor(suggestion.confidence_score)}`}>
                    {(suggestion.confidence_score * 100).toFixed(0)}% confidence
                  </div>
                </div>

                {/* Personalized Insight */}
                <div className="mb-6">
                  <h4 className="text-lg font-semibold text-purple-800 mb-3">💡 Personalized Insight</h4>
                  <p className="text-gray-700 leading-relaxed">{suggestion.personalized_insight}</p>
                </div>

                {/* Grid Layout for Steps and Skills */}
                <div className="grid md:grid-cols-2 gap-6 mb-6">
                  {/* Actionable Steps */}
                  <div>
                    <h4 className="text-lg font-semibold text-purple-800 mb-3">🎯 Next Steps</h4>
                    <ul className="space-y-2">
                      {suggestion.actionable_steps.map((step, stepIndex) => (
                        <li key={stepIndex} className="flex items-start">
                          <span className="flex-shrink-0 w-6 h-6 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-medium mr-3 mt-0.5">
                            {stepIndex + 1}
                          </span>
                          <span className="text-gray-700">{step}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Skill Development */}
                  <div>
                    <h4 className="text-lg font-semibold text-purple-800 mb-3">📚 Skill Development</h4>
                    <ul className="space-y-2">
                      {suggestion.skill_development_plan.map((skill, skillIndex) => (
                        <li key={skillIndex} className="flex items-start">
                          <span className="flex-shrink-0 w-2 h-2 bg-purple-400 rounded-full mr-3 mt-2"></span>
                          <span className="text-gray-700">{skill}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Cultural Considerations */}
                <div className="mb-4">
                  <h4 className="text-lg font-semibold text-purple-800 mb-3">🏛️ Cultural Considerations</h4>
                  <p className="text-gray-700 leading-relaxed">{suggestion.cultural_considerations}</p>
                </div>

                {/* Timeline */}
                <div>
                  <h4 className="text-lg font-semibold text-purple-800 mb-3">⏰ Timeline</h4>
                  <p className="text-gray-700">{suggestion.timeline_suggestion}</p>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'pathway' && (
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">🗺️ Your Career Pathway Summary</h2>
          
          {results.career_pathway_summary ? (
            <div className="prose max-w-none">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
                <div className="whitespace-pre-line text-gray-800 leading-relaxed">
                  {results.career_pathway_summary}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 bg-gray-50 rounded-lg">
              <p className="text-gray-600 mb-2">Career pathway summary is being generated...</p>
              <p className="text-sm text-gray-500">This provides strategic guidance across your top career options</p>
            </div>
          )}

          {/* Quick Action Cards */}
          <div className="grid md:grid-cols-3 gap-4 mt-8">
            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <h4 className="font-semibold text-green-800 mb-2">🎯 Immediate Focus</h4>
              <p className="text-sm text-green-700">Start skill development and networking in your top career areas</p>
            </div>
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <h4 className="font-semibold text-blue-800 mb-2">📈 Long-term Growth</h4>
              <p className="text-sm text-blue-700">Plan for advancement and specialization opportunities</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
              <h4 className="font-semibold text-purple-800 mb-2">🤝 Cultural Balance</h4>
              <p className="text-sm text-purple-700">Navigate family expectations while pursuing your goals</p>
            </div>
          </div>
        </div>
      )}

      {/* Footer Actions */}
      <div className="mt-8 flex justify-center space-x-4">
        <button
          onClick={() => window.print()}
          className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        >
          📄 Save Results
        </button>
        <button
          onClick={() => setActiveTab('suggestions')}
          className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          🤖 View AI Insights
        </button>
        <button
          onClick={fetchEnhancedRecommendations}
          className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          🔄 Refresh Analysis
        </button>
      </div>
    </div>
  );
};

export default GroqEnhancedMAREResults;
