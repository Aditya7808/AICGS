import React, { useState, useEffect } from 'react';
import { SkillGapResponse, recommendationAPI } from '../services/api';
import Loading from './Loading';

interface SkillGapAnalyzerProps {
  userId: number;
  targetCareers?: string[];
}

const SkillGapAnalyzer: React.FC<SkillGapAnalyzerProps> = ({ userId }) => {
  const [data, setData] = useState<SkillGapResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCareer, setSelectedCareer] = useState<string>('');

  useEffect(() => {
    const fetchSkillGapData = async () => {
      try {
        setLoading(true);
        // For demo purposes, we'll use a mock request
        // In a real app, you'd pass the actual career IDs and user skills
        const mockRequest = {
          user_id: userId,
          target_career_id: 1, // Mock career ID
          current_skills: ['Python', 'Web Development', 'Problem Solving'],
          current_education_level: 'Undergraduate',
          time_horizon_months: 12
        };
        
        const response = await recommendationAPI.analyzeSkillGap(mockRequest);
        setData(response);
        
        // Set the first career as selected if available
        if (response.career_analyses && Object.keys(response.career_analyses).length > 0) {
          setSelectedCareer(Object.keys(response.career_analyses)[0]);
        }
      } catch (err) {
        setError('Failed to load skill gap analysis');
        console.error('Error fetching skill gap analysis:', err);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchSkillGapData();
    }
  }, [userId]);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <div className="text-red-600 mb-2">⚠️ Unable to load skill gap analysis</div>
        <div className="text-red-500 text-sm">{error}</div>
      </div>
    );
  }

  if (!data || !data.career_analyses) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500">No skill gap analysis data available</div>
      </div>
    );
  }

  const careerNames = Object.keys(data.career_analyses);
  const currentAnalysis = selectedCareer ? data.career_analyses[selectedCareer] : null;

  return (
    <div className="space-y-8">
      {/* Career Selection */}
      {careerNames.length > 1 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            🎯 Select Career for Analysis
          </h3>
          <div className="flex flex-wrap gap-2">
            {careerNames.map((career) => (
              <button
                key={career}
                onClick={() => setSelectedCareer(career)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                  selectedCareer === career
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {career}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Overall Recommendations */}
      {data.overall_recommendations && data.overall_recommendations.length > 0 && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            🚀 Overall Recommendations
          </h3>
          <ul className="space-y-2">
            {data.overall_recommendations.map((rec, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-600 mr-2 text-lg">✓</span>
                <span className="text-gray-700">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Skill Priorities */}
      {data.skill_priorities && data.skill_priorities.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            ⭐ Skill Priorities
          </h3>
          <div className="space-y-3">
            {data.skill_priorities.slice(0, 5).map((skill, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">{skill.skill}</div>
                  <div className="text-sm text-gray-600">
                    Required by: {skill.careers_requiring.join(', ')}
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                  skill.priority === 'High' 
                    ? 'bg-red-100 text-red-800'
                    : skill.priority === 'Medium'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-green-100 text-green-800'
                }`}>
                  {skill.priority}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Career-Specific Analysis */}
      {currentAnalysis && (
        <div className="space-y-6">
          {/* Readiness Score */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              📊 Career Readiness for {selectedCareer}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {Math.round(currentAnalysis.readiness_score * 100)}%
                </div>
                <div className="text-sm text-gray-600">Overall Readiness</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {currentAnalysis.overall_gaps?.completion_percentage || 0}%
                </div>
                <div className="text-sm text-gray-600">Skills Complete</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {currentAnalysis.time_estimate?.total_weeks || 0}
                </div>
                <div className="text-sm text-gray-600">Weeks to Ready</div>
              </div>
            </div>
            <div className="mt-4 text-center">
              <span className={`px-4 py-2 rounded-full font-medium ${
                currentAnalysis.overall_gaps?.readiness_level === 'Advanced'
                  ? 'bg-green-100 text-green-800'
                  : currentAnalysis.overall_gaps?.readiness_level === 'Intermediate'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {currentAnalysis.overall_gaps?.readiness_level || 'Beginner'} Level
              </span>
            </div>
          </div>

          {/* Skill Gaps */}
          {currentAnalysis.skill_gaps && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">
                🎯 Skill Gap Analysis
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Missing Skills */}
                {currentAnalysis.skill_gaps.missing_skills && currentAnalysis.skill_gaps.missing_skills.length > 0 && (
                  <div>
                    <h5 className="font-medium text-red-700 mb-3">Skills to Develop:</h5>
                    <div className="space-y-2">
                      {currentAnalysis.skill_gaps.missing_skills.map((skill, index) => (
                        <div key={index} className="bg-red-50 text-red-800 px-3 py-2 rounded-lg text-sm">
                          {skill}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Available Skills */}
                {currentAnalysis.skill_gaps.available_skills && currentAnalysis.skill_gaps.available_skills.length > 0 && (
                  <div>
                    <h5 className="font-medium text-green-700 mb-3">Skills You Have:</h5>
                    <div className="space-y-2">
                      {currentAnalysis.skill_gaps.available_skills.map((skill, index) => (
                        <div key={index} className="bg-green-50 text-green-800 px-3 py-2 rounded-lg text-sm">
                          ✓ {skill}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Learning Roadmap */}
          {currentAnalysis.learning_roadmap && currentAnalysis.learning_roadmap.phases && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">
                🗺️ Learning Roadmap
              </h4>
              <div className="space-y-4">
                {currentAnalysis.learning_roadmap.phases.map((phase, index) => (
                  <div key={index} className="border-l-4 border-blue-400 pl-4 py-3">
                    <div className="flex justify-between items-start mb-2">
                      <h5 className="font-medium text-gray-900">{phase.phase}</h5>
                      <span className="text-sm text-gray-500">
                        {phase.duration_weeks} weeks
                      </span>
                    </div>
                    {phase.skills && phase.skills.length > 0 && (
                      <div className="mb-3">
                        <div className="text-sm text-gray-600 mb-1">Skills to learn:</div>
                        <div className="flex flex-wrap gap-1">
                          {phase.skills.map((skill, skillIndex) => (
                            <span key={skillIndex} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    {phase.resources && phase.resources.length > 0 && (
                      <div>
                        <div className="text-sm text-gray-600 mb-2">Recommended resources:</div>
                        <div className="space-y-1">
                          {phase.resources.slice(0, 3).map((resource, resIndex) => (
                            <div key={resIndex} className="text-sm bg-gray-50 p-2 rounded">
                              <div className="font-medium text-gray-800">{resource.title}</div>
                              <div className="text-gray-600">
                                {resource.type} • {resource.duration} • {resource.difficulty}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {currentAnalysis.recommendations && currentAnalysis.recommendations.length > 0 && (
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-200">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">
                💡 Personalized Recommendations
              </h4>
              <ul className="space-y-2">
                {currentAnalysis.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-purple-600 mr-2">→</span>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SkillGapAnalyzer;
