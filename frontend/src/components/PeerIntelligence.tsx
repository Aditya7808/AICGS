import React, { useState, useEffect } from 'react';
import { PeerIntelligenceResponse, recommendationAPI } from '../services/api';
import Loading from './Loading';

interface PeerIntelligenceProps {
  userId: number;
}

const PeerIntelligence: React.FC<PeerIntelligenceProps> = ({ userId }) => {
  const [data, setData] = useState<PeerIntelligenceResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPeerIntelligence = async () => {
      try {
        setLoading(true);
        const response = await recommendationAPI.getPeerIntelligence(userId);
        setData(response);
      } catch (err) {
        setError('Failed to load peer intelligence data');
        console.error('Error fetching peer intelligence:', err);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchPeerIntelligence();
    }
  }, [userId]);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <div className="text-red-600 mb-2">⚠️ Unable to load peer insights</div>
        <div className="text-red-500 text-sm">{error}</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500">No peer intelligence data available</div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Peer Insights Overview */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          🧠 Peer Intelligence Insights
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {data.similar_students?.length || 0}
            </div>
            <div className="text-sm text-gray-600">Similar Students Found</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-indigo-600">
              {data.success_stories?.length || 0}
            </div>
            <div className="text-sm text-gray-600">Success Stories</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">
              {data.popular_choices?.length || 0}
            </div>
            <div className="text-sm text-gray-600">Popular Choices</div>
          </div>
        </div>
      </div>

      {/* Similar Students */}
      {data.similar_students && data.similar_students.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            👥 Students Similar to You
          </h4>
          <div className="space-y-4">
            {data.similar_students.slice(0, 5).map((student, index) => (
              <div key={student.student_id} className="border-l-4 border-blue-400 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="font-medium text-gray-900">
                      Student #{index + 1} ({Math.round(student.similarity_score * 100)}% match)
                    </div>
                    <div className="text-sm text-gray-600">
                      {student.education_level} • {student.current_marks}% marks
                    </div>
                    {student.career_outcomes && student.career_outcomes.length > 0 && (
                      <div className="text-sm text-blue-600 mt-1">
                        Career outcomes: {student.career_outcomes.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
                {student.similarity_reasons && student.similarity_reasons.length > 0 && (
                  <div className="mt-2 text-xs text-gray-500">
                    Similar because: {student.similarity_reasons.join(' • ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Success Stories */}
      {data.success_stories && data.success_stories.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            🌟 Success Stories
          </h4>
          <div className="space-y-4">
            {data.success_stories.slice(0, 3).map((story, index) => (
              <div key={index} className="bg-green-50 rounded-lg p-4 border border-green-200">
                <div className="font-medium text-green-800 mb-2">
                  {story.career_choice}
                </div>
                <div className="text-sm text-green-700 mb-2">
                  {story.inspiration_message}
                </div>
                {story.success_factors && story.success_factors.length > 0 && (
                  <div className="text-xs text-green-600">
                    Success factors: {story.success_factors.join(' • ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Popular Choices */}
      {data.popular_choices && data.popular_choices.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            📈 Popular Career Choices Among Peers
          </h4>
          <div className="space-y-3">
            {data.popular_choices.slice(0, 5).map((choice, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">{choice.career_name}</div>
                  <div className="text-sm text-gray-600">
                    {choice.popularity_count} peers chose this • {choice.recommendation_strength} recommendation
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-semibold text-indigo-600">
                    {Math.round(choice.avg_success_rate * 100)}%
                  </div>
                  <div className="text-xs text-gray-500">success rate</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Peer Comparison */}
      {data.peer_comparison && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            📊 How You Compare to Peers
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-sm text-blue-600 font-medium">Academic Standing</div>
              <div className="text-lg font-semibold text-blue-800">
                {data.peer_comparison.academic_standing}
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <div className="text-sm text-purple-600 font-medium">Career Diversity</div>
              <div className="text-lg font-semibold text-purple-800">
                {data.peer_comparison.career_diversity} options explored
              </div>
            </div>
          </div>
          {data.peer_comparison.insights && data.peer_comparison.insights.length > 0 && (
            <div className="mt-4">
              <div className="text-sm font-medium text-gray-700 mb-2">Key Insights:</div>
              <ul className="text-sm text-gray-600 space-y-1">
                {data.peer_comparison.insights.map((insight, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    {insight}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* General Peer Insights */}
      {data.peer_insights && (
        <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-6 border border-amber-200">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            💡 Peer-Driven Recommendations
          </h4>
          <div className="space-y-4">
            {data.peer_insights.trending_careers && data.peer_insights.trending_careers.length > 0 && (
              <div>
                <div className="text-sm font-medium text-amber-700 mb-2">Trending Careers:</div>
                <div className="flex flex-wrap gap-2">
                  {data.peer_insights.trending_careers.map((career, index) => (
                    <span key={index} className="bg-amber-100 text-amber-800 px-3 py-1 rounded-full text-sm">
                      {career}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {data.peer_insights.recommendations && data.peer_insights.recommendations.length > 0 && (
              <div>
                <div className="text-sm font-medium text-orange-700 mb-2">Recommendations:</div>
                <ul className="text-sm text-gray-700 space-y-1">
                  {data.peer_insights.recommendations.map((rec, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-orange-500 mr-2">→</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default PeerIntelligence;
