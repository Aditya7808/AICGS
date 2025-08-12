import React, { useState } from 'react';

// Example component showing how to access Groq results
const GroqResultsExample: React.FC = () => {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Sample assessment data for testing
  const sampleAssessmentData = {
    age: 25,
    education_level: "Bachelor's Degree",
    location: "Mumbai, India",
    cultural_context: "Urban Indian family",
    family_background: "Middle class, supportive of tech careers",
    language_preference: "en",
    economic_context: "Stable income family",
    geographic_constraints: "Prefer to stay in major cities",
    urban_rural_type: "urban",
    infrastructure_level: "good",
    family_expectations: "Stable, well-paying career",
    peer_influence_score: 0.7,
    skills: ["Python", "JavaScript", "Problem Solving", "Communication"],
    interests: ["Technology", "Innovation", "Software Development"],
    career_goals: "Become a successful software engineer",
    preferred_industries: ["Technology", "Startups"],
    work_environment_preference: "office",
    salary_expectations: "5-10 LPA",
    work_life_balance_priority: 7
  };

  const fetchGroqResults = async () => {
    setLoading(true);
    try {
      console.log('🚀 Fetching Groq enhanced results...');
      
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Please login first!');
        return;
      }

      const response = await fetch('/api/v1/mare/recommendations/enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(sampleAssessmentData)
      });

      console.log('📡 API Response status:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Enhanced results received:', data);
        
        // Check if Groq results are available
        if (data.groq_enhanced_suggestions && data.groq_enhanced_suggestions.length > 0) {
          console.log('🤖 Groq suggestions found:', data.groq_enhanced_suggestions.length);
          console.log('📊 First Groq suggestion:', data.groq_enhanced_suggestions[0]);
        } else {
          console.log('⚠️ No Groq suggestions - check if GROQ_API_KEY is configured');
        }
        
        setResults(data);
      } else {
        const errorText = await response.text();
        console.error('❌ API Error:', response.status, errorText);
        alert(`API Error: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('💥 Fetch error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      alert(`Network error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">🧪 Groq Results Test</h2>
      
      {/* Test Button */}
      <div className="mb-6">
        <button
          onClick={fetchGroqResults}
          disabled={loading}
          className={`px-6 py-3 rounded-lg text-white font-semibold ${
            loading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? '⏳ Fetching Groq Results...' : '🚀 Test Groq Integration'}
        </button>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Getting AI insights from Groq...</p>
        </div>
      )}

      {/* Results Display */}
      {results && !loading && (
        <div className="space-y-6">
          {/* Enhancement Status */}
          <div className={`p-4 rounded-lg ${
            results.enhancement_available 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-yellow-50 border border-yellow-200'
          }`}>
            <h3 className="font-semibold">
              {results.enhancement_available ? '✅ Groq Enhancement Available' : '⚠️ Groq Enhancement Not Available'}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              {results.enhancement_available 
                ? 'AI-powered insights are included in the results below'
                : 'Standard MARE recommendations only (check GROQ_API_KEY configuration)'
              }
            </p>
          </div>

          {/* Standard Recommendations */}
          <div>
            <h3 className="text-xl font-semibold mb-3">📊 Standard MARE Recommendations</h3>
            <div className="grid gap-4">
              {results.standard_recommendations?.map((rec: any, index: number) => (
                <div key={index} className="border rounded-lg p-4">
                  <h4 className="font-semibold text-lg">{rec.title}</h4>
                  <p className="text-gray-600">{rec.industry}</p>
                  <div className="mt-2">
                    <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                      Score: {(rec.overall_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              )) || <p className="text-gray-500">No standard recommendations found</p>}
            </div>
          </div>

          {/* Groq Enhanced Suggestions */}
          <div>
            <h3 className="text-xl font-semibold mb-3">
              🤖 Groq Enhanced Insights ({results.groq_enhanced_suggestions?.length || 0})
            </h3>
            
            {results.groq_enhanced_suggestions && results.groq_enhanced_suggestions.length > 0 ? (
              <div className="space-y-6">
                {results.groq_enhanced_suggestions.map((suggestion: any, index: number) => (
                  <div key={index} className="border-2 border-purple-200 rounded-lg p-6 bg-purple-50">
                    <h4 className="text-xl font-bold text-purple-900 mb-3">
                      {suggestion.career_title}
                    </h4>
                    
                    {/* Personalized Insight */}
                    <div className="mb-4">
                      <h5 className="font-semibold text-gray-800 mb-2">💡 Personalized Insight:</h5>
                      <p className="text-gray-700 bg-white p-3 rounded">
                        {suggestion.personalized_insight}
                      </p>
                    </div>

                    {/* Cultural Considerations */}
                    <div className="mb-4">
                      <h5 className="font-semibold text-gray-800 mb-2">🌍 Cultural Considerations:</h5>
                      <p className="text-gray-700 bg-white p-3 rounded">
                        {suggestion.cultural_considerations}
                      </p>
                    </div>

                    {/* Actionable Steps */}
                    <div className="mb-4">
                      <h5 className="font-semibold text-gray-800 mb-2">🎯 Actionable Steps:</h5>
                      <ul className="bg-white p-3 rounded">
                        {suggestion.actionable_steps?.map((step: string, i: number) => (
                          <li key={i} className="flex items-start mb-2">
                            <span className="text-green-600 mr-2">✓</span>
                            <span className="text-gray-700">{step}</span>
                          </li>
                        )) || <li className="text-gray-500">No action steps provided</li>}
                      </ul>
                    </div>

                    {/* Skill Development Plan */}
                    <div className="mb-4">
                      <h5 className="font-semibold text-gray-800 mb-2">📚 Skill Development Plan:</h5>
                      <ul className="bg-white p-3 rounded">
                        {suggestion.skill_development_plan?.map((skill: string, i: number) => (
                          <li key={i} className="flex items-start mb-2">
                            <span className="text-blue-600 mr-2">📖</span>
                            <span className="text-gray-700">{skill}</span>
                          </li>
                        )) || <li className="text-gray-500">No skill plan provided</li>}
                      </ul>
                    </div>

                    {/* Timeline */}
                    <div className="mb-4">
                      <h5 className="font-semibold text-gray-800 mb-2">⏰ Timeline Suggestion:</h5>
                      <p className="text-gray-700 bg-white p-3 rounded">
                        {suggestion.timeline_suggestion || 'No timeline provided'}
                      </p>
                    </div>

                    {/* Confidence Score */}
                    <div>
                      <h5 className="font-semibold text-gray-800 mb-2">📈 Confidence Score:</h5>
                      <div className="bg-white p-3 rounded">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 rounded-full h-2.5 mr-3">
                            <div 
                              className="bg-green-600 h-2.5 rounded-full" 
                              style={{ width: `${(suggestion.confidence_score || 0) * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium text-gray-700">
                            {((suggestion.confidence_score || 0) * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 bg-gray-50 rounded-lg">
                <p className="text-gray-600 mb-2">❌ No Groq enhanced suggestions available</p>
                <p className="text-sm text-gray-500">
                  This usually means the GROQ_API_KEY is not configured in the backend.
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Check backend logs for: "GROQ_API_KEY not found" message
                </p>
              </div>
            )}
          </div>

          {/* Career Pathway Summary */}
          {results.career_pathway_summary && (
            <div>
              <h3 className="text-xl font-semibold mb-3">🗺️ Career Pathway Summary</h3>
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border">
                <p className="text-gray-700">{results.career_pathway_summary}</p>
              </div>
            </div>
          )}

          {/* Raw JSON (for debugging) */}
          <details className="bg-gray-50 p-4 rounded-lg">
            <summary className="cursor-pointer font-semibold text-gray-700 mb-2">
              🔍 View Raw JSON Response (Debug)
            </summary>
            <pre className="text-xs bg-white p-3 rounded border overflow-auto max-h-64">
              {JSON.stringify(results, null, 2)}
            </pre>
          </details>
        </div>
      )}

      {/* Instructions */}
      <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-2">📝 Instructions:</h3>
        <ol className="text-sm text-blue-800 space-y-1">
          <li>1. Make sure you're logged in</li>
          <li>2. Click "Test Groq Integration" button</li>
          <li>3. Check browser console for detailed logs</li>
          <li>4. If no Groq results, check backend GROQ_API_KEY configuration</li>
          <li>5. Backend logs should show "Groq client initialized successfully"</li>
        </ol>
      </div>
    </div>
  );
};

export default GroqResultsExample;
