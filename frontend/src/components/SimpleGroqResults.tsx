import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

/**
 * Simple example showing how to access Groq-enhanced MARE recommendations
 * This is a minimal implementation for demonstration purposes
 */

interface SimpleGroqResultsProps {
  onResults?: (results: any) => void;
}

const SimpleGroqResults: React.FC<SimpleGroqResultsProps> = ({ onResults }) => {
  const { user } = useAuth();
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Sample assessment data for demonstration
  const sampleAssessmentData = {
    // Personal dimensions
    age: 22,
    education_level: "bachelor",
    location: "Urban City",
    
    // Cultural dimensions
    cultural_context: "Modern urban professional",
    family_background: "Middle class",
    language_preference: "en",
    
    // Economic dimensions
    economic_context: "Stable middle class",
    financial_constraints: "Moderate student loans",
    
    // Geographic dimensions
    geographic_constraints: "Willing to relocate",
    urban_rural_type: "urban",
    infrastructure_level: "excellent",
    
    // Social dimensions
    family_expectations: "Professional career preferred",
    peer_influence_score: 0.6,
    community_values: "Education and success valued",
    
    // Skills and interests
    skills: ["Programming", "Data Analysis", "Problem Solving", "Communication"],
    interests: ["Technology", "Innovation", "Learning", "Problem Solving"],
    
    // Career preferences
    career_goals: "Become a software engineer at a tech company",
    preferred_industries: ["Technology", "Software"],
    work_environment_preference: "hybrid",
    salary_expectations: "Competitive market rate",
    work_life_balance_priority: 7
  };

  const fetchGroqResults = async () => {
    if (!user) {
      setError('Please log in to access AI recommendations');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      
      const response = await fetch('/api/v1/mare/recommendations/enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(sampleAssessmentData)
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data);
      
      // Call the callback if provided
      if (onResults) {
        onResults(data);
      }

      console.log('Groq Enhanced Results:', data);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('Error fetching Groq results:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          🤖 Groq AI Career Recommendations Demo
        </h2>
        
        <p className="text-gray-600 mb-6">
          This demo shows how to access Groq-enhanced MARE recommendations. 
          Click the button below to get AI-powered career insights.
        </p>

        <button
          onClick={fetchGroqResults}
          disabled={loading || !user}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            loading || !user
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {loading ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Getting AI Recommendations...
            </span>
          ) : (
            'Get Groq Enhanced Recommendations'
          )}
        </button>

        {!user && (
          <p className="text-red-600 mt-2 text-sm">
            Please log in to access AI recommendations
          </p>
        )}

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 className="text-red-800 font-medium">Error</h3>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        )}

        {results && (
          <div className="mt-6 space-y-6">
            {/* Enhancement Status */}
            <div className={`p-4 rounded-lg ${
              results.enhancement_available 
                ? 'bg-green-50 border border-green-200' 
                : 'bg-yellow-50 border border-yellow-200'
            }`}>
              <h3 className="font-medium">
                {results.enhancement_available ? '✅ AI Enhancement Active' : '⚠️ Standard Mode'}
              </h3>
              <p className="text-sm mt-1">
                {results.enhancement_available 
                  ? 'Groq AI has enhanced your career recommendations with personalized insights.'
                  : 'AI enhancement is not available. Showing standard MARE recommendations.'}
              </p>
            </div>

            {/* Groq Enhanced Suggestions */}
            {results.enhancement_available && results.groq_enhanced_suggestions?.length > 0 && (
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  🎯 AI-Enhanced Career Insights
                </h3>
                
                {results.groq_enhanced_suggestions.map((suggestion: any, index: number) => (
                  <div key={index} className="bg-white rounded-lg p-4 mb-4 shadow-sm">
                    <div className="flex justify-between items-start mb-3">
                      <h4 className="text-lg font-semibold text-gray-900">
                        {suggestion.career_title}
                      </h4>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        suggestion.confidence_score >= 0.8 
                          ? 'bg-green-100 text-green-800'
                          : suggestion.confidence_score >= 0.6
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {Math.round(suggestion.confidence_score * 100)}% confidence
                      </span>
                    </div>

                    <div className="space-y-3 text-sm">
                      <div>
                        <h5 className="font-medium text-gray-700 mb-1">💡 Personalized Insight</h5>
                        <p className="text-gray-600">{suggestion.personalized_insight}</p>
                      </div>

                      <div>
                        <h5 className="font-medium text-gray-700 mb-1">🎯 Next Steps</h5>
                        <ul className="list-disc list-inside text-gray-600 space-y-1">
                          {suggestion.actionable_steps?.slice(0, 3).map((step: string, stepIndex: number) => (
                            <li key={stepIndex}>{step}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="grid md:grid-cols-2 gap-3">
                        <div>
                          <h5 className="font-medium text-gray-700 mb-1">🌍 Cultural Fit</h5>
                          <p className="text-gray-600 text-xs">{suggestion.cultural_considerations}</p>
                        </div>
                        <div>
                          <h5 className="font-medium text-gray-700 mb-1">⏰ Timeline</h5>
                          <p className="text-gray-600 text-xs">{suggestion.timeline_suggestion}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Career Pathway Summary */}
            {results.career_pathway_summary && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-2">🛤️ Your Career Pathway</h3>
                <p className="text-gray-700 text-sm">{results.career_pathway_summary}</p>
              </div>
            )}

            {/* Standard Recommendations Summary */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-medium text-gray-900 mb-3">📊 Analysis Summary</h3>
              <div className="text-sm text-gray-600">
                <p>Found {results.standard_recommendations?.length || 0} career matches</p>
                {results.standard_recommendations?.slice(0, 3).map((rec: any) => (
                  <div key={rec.career_id} className="flex justify-between items-center py-2 border-b border-gray-200 last:border-b-0">
                    <span className="font-medium">{rec.title}</span>
                    <span className="text-blue-600 font-medium">
                      {Math.round(rec.overall_score * 100)}% match
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Raw Data (for debugging) */}
            <details className="bg-gray-100 rounded-lg p-4">
              <summary className="cursor-pointer font-medium text-gray-900 mb-2">
                🔍 View Raw API Response (Debug)
              </summary>
              <pre className="text-xs text-gray-600 overflow-auto max-h-64">
                {JSON.stringify(results, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
};

export default SimpleGroqResults;
