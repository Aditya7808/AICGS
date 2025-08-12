import React, { useState } from 'react';

interface MAREResult {
  career_id: number;
  title: string;
  industry: string;
  overall_score: number;
  dimension_scores: {
    skills_match: number;
    cultural_fit: number;
    economic_viability: number;
    geographic_accessibility: number;
    social_alignment: number;
    growth_potential: number;
  };
  explanation: {
    [key: string]: string;
  };
  confidence_level: string;
}

interface MAREResponse {
  recommendations: MAREResult[];
  user_profile_summary: {
    primary_strengths: string[];
    key_preferences: {[key: string]: string};
    cultural_context: string;
    geographic_scope: string;
    career_stage: string;
  };
  algorithm_info: {
    engine_version: string;
    dimension_weights: {[key: string]: number};
    total_opportunities_analyzed: number;
    recommendations_generated: number;
    similarity_threshold: number;
  };
  processing_time: number;
  timestamp: string;
}

const MAREResults: React.FC = () => {
  const [results] = useState<MAREResponse | null>(null);
  const [selectedRecommendation, setSelectedRecommendation] = useState<MAREResult | null>(null);
  const [feedbackModal, setFeedbackModal] = useState(false);

  const getDimensionColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500';
    if (score >= 0.6) return 'bg-blue-500';
    if (score >= 0.4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case 'high': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const formatPercentage = (score: number) => Math.round(score * 100);

  const submitFeedback = async (recommendation: MAREResult, rating: number, feedback: string) => {
    try {
      const response = await fetch('/api/mare/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          career_opportunity_id: recommendation.career_id,
          rating: rating,
          feedback_text: feedback,
          selected: true
        })
      });

      if (response.ok) {
        alert('Thank you for your feedback! This helps improve our recommendations.');
        setFeedbackModal(false);
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  if (!results) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            MARE Results Loading...
          </h2>
          <p className="text-gray-600">
            Please complete the assessment to see your AI-powered recommendations.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Your AI-Powered Career Recommendations
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Powered by Multi-Dimensional Adaptive Recommendation Engine (MARE)
          </p>
          
          {/* Algorithm Info */}
          <div className="bg-white rounded-lg shadow-sm p-6 max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-blue-600">
                  {results.algorithm_info.recommendations_generated}
                </div>
                <div className="text-sm text-gray-600">Recommendations</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">
                  {results.algorithm_info.total_opportunities_analyzed}
                </div>
                <div className="text-sm text-gray-600">Careers Analyzed</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">
                  {results.processing_time}s
                </div>
                <div className="text-sm text-gray-600">Processing Time</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-indigo-600">
                  {results.algorithm_info.engine_version}
                </div>
                <div className="text-sm text-gray-600">AI Engine</div>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Summary */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Profile Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Career Stage</h3>
              <p className="text-gray-600">{results.user_profile_summary.career_stage}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Cultural Context</h3>
              <p className="text-gray-600 capitalize">{results.user_profile_summary.cultural_context}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Geographic Scope</h3>
              <p className="text-gray-600">{results.user_profile_summary.geographic_scope.replace('_', ' ')}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Primary Strengths</h3>
              <p className="text-gray-600">{results.user_profile_summary.primary_strengths.slice(0, 2).join(', ')}</p>
            </div>
          </div>
        </div>

        {/* Dimension Weights Visualization */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">AI Algorithm Weights</h2>
          <div className="space-y-4">
            {Object.entries(results.algorithm_info.dimension_weights).map(([dimension, weight]) => (
              <div key={dimension} className="flex items-center">
                <div className="w-40 text-sm font-medium text-gray-700 capitalize">
                  {dimension.replace('_', ' ')}
                </div>
                <div className="flex-1 bg-gray-200 rounded-full h-3 mx-4">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${weight * 100}%` }}
                  />
                </div>
                <div className="w-12 text-sm font-medium text-gray-900">
                  {Math.round(weight * 100)}%
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="space-y-6">
          {results.recommendations.map((recommendation, index) => (
            <div key={recommendation.career_id} className="bg-white rounded-2xl shadow-lg overflow-hidden">
              {/* Recommendation Header */}
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="bg-white bg-opacity-20 text-white px-3 py-1 rounded-full text-sm font-medium">
                        #{index + 1}
                      </span>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(recommendation.confidence_level)}`}>
                        {recommendation.confidence_level} Confidence
                      </span>
                    </div>
                    <h3 className="text-2xl font-bold text-white mb-1">
                      {recommendation.title}
                    </h3>
                    <p className="text-blue-100">{recommendation.industry}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold text-white">
                      {formatPercentage(recommendation.overall_score)}%
                    </div>
                    <div className="text-blue-100 text-sm">Overall Match</div>
                  </div>
                </div>
              </div>

              {/* Dimension Scores */}
              <div className="p-8">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  Multi-Dimensional Analysis
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                  {Object.entries(recommendation.dimension_scores).map(([dimension, score]) => (
                    <div key={dimension} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700 capitalize">
                          {dimension.replace('_', ' ')}
                        </span>
                        <span className="text-sm font-bold text-gray-900">
                          {formatPercentage(score)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full transition-all duration-500 ${getDimensionColor(score)}`}
                          style={{ width: `${score * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                {/* Explanations */}
                <div className="bg-blue-50 rounded-lg p-6 mb-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">
                    Why This Career Matches You
                  </h4>
                  <div className="space-y-3">
                    {Object.entries(recommendation.explanation).map(([dimension, explanation]) => (
                      <div key={dimension} className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                        <p className="text-gray-700">{explanation}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-4">
                  <button
                    onClick={() => {
                      setSelectedRecommendation(recommendation);
                      setFeedbackModal(true);
                    }}
                    className="flex-1 bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-3 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all duration-200"
                  >
                    I'm Interested
                  </button>
                  <button className="flex-1 border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-200">
                    Learn More
                  </button>
                  <button className="px-6 py-3 border-2 border-red-300 text-red-600 rounded-lg font-semibold hover:bg-red-50 transition-all duration-200">
                    Not Interested
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Feedback Modal */}
        {feedbackModal && selectedRecommendation && (
          <FeedbackModal 
            recommendation={selectedRecommendation}
            onSubmit={submitFeedback}
            onClose={() => setFeedbackModal(false)}
          />
        )}
      </div>
    </div>
  );
};

const FeedbackModal: React.FC<{
  recommendation: MAREResult;
  onSubmit: (recommendation: MAREResult, rating: number, feedback: string) => void;
  onClose: () => void;
}> = ({ recommendation, onSubmit, onClose }) => {
  const [rating, setRating] = useState(5);
  const [feedback, setFeedback] = useState('');

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl p-8 max-w-lg w-full mx-4">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">
          Provide Feedback
        </h3>
        <p className="text-gray-600 mb-6">
          Help us improve our recommendations for "{recommendation.title}"
        </p>
        
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            How relevant is this recommendation? (1-5 stars)
          </label>
          <div className="flex space-x-2">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                onClick={() => setRating(star)}
                className={`text-2xl ${star <= rating ? 'text-yellow-400' : 'text-gray-300'} hover:text-yellow-400 transition-colors`}
              >
                ★
              </button>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Additional feedback (optional)
          </label>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            rows={3}
            placeholder="Tell us more about why this recommendation fits or doesn't fit..."
          />
        </div>

        <div className="flex space-x-4">
          <button
            onClick={() => onSubmit(recommendation, rating, feedback)}
            className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Submit Feedback
          </button>
          <button
            onClick={onClose}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default MAREResults;
