import React, { useState, useEffect } from 'react';
import { mlService, SkillRecommendation, UserProfile } from '../services/mlService';
import Loading from './Loading';

interface EnhancedSkillGapAnalyzerProps {
  currentSkills: string[];
  targetCareer: string;
  userProfile?: {
    experienceYears?: number;
    academicScore?: number;
    learningCapacity?: number;
  };
}

const EnhancedSkillGapAnalyzer: React.FC<EnhancedSkillGapAnalyzerProps> = ({
  currentSkills,
  targetCareer,
  userProfile = {}
}) => {
  const [recommendations, setRecommendations] = useState<SkillRecommendation[]>([]);
  const [roadmap, setRoadmap] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'recommendations' | 'roadmap'>('recommendations');

  useEffect(() => {
    const fetchMLRecommendations = async () => {
      try {
        setLoading(true);
        setError(null);

        // Create user profile for ML model
        const mlUserProfile: UserProfile = {
          current_skills: currentSkills,
          experience_years: userProfile.experienceYears || 0,
          academic_score: userProfile.academicScore || 75,
          learning_capacity: userProfile.learningCapacity || 0.5
        };

        // Get skill recommendations
        const skillResponse = await mlService.prioritizeSkills(mlUserProfile, targetCareer, 15);
        setRecommendations(skillResponse.recommendations);

        // Get career transition roadmap
        const roadmapData = await mlService.getCareerTransitionRoadmap(
          currentSkills,
          targetCareer,
          userProfile
        );
        setRoadmap(roadmapData);

      } catch (err) {
        console.error('Error fetching ML recommendations:', err);
        setError('Failed to load AI-powered skill recommendations');
      } finally {
        setLoading(false);
      }
    };

    if (targetCareer && currentSkills.length > 0) {
      fetchMLRecommendations();
    }
  }, [targetCareer, currentSkills, userProfile]);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">{error}</div>
          </div>
        </div>
      </div>
    );
  }

  const getPriorityColor = (score: number) => {
    if (score >= 0.7) return 'bg-red-500';
    if (score >= 0.5) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getEffortBadgeColor = (effort: string) => {
    switch (effort) {
      case 'Low': return 'bg-green-100 text-green-800';
      case 'Medium': return 'bg-yellow-100 text-yellow-800';
      case 'High': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderRecommendations = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {recommendations.map((rec, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <h4 className="font-semibold text-gray-900">{rec.skill}</h4>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getEffortBadgeColor(rec.learning_effort)}`}>
                {rec.learning_effort}
              </span>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Priority Score</span>
                <span className="font-medium">{(rec.priority_score * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-300 ${getPriorityColor(rec.priority_score)}`}
                  style={{ width: `${rec.priority_score * 100}%` }}
                />
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Importance</span>
                <span className="font-medium">{(rec.importance * 100).toFixed(0)}%</span>
              </div>
              
              <div className="text-xs text-gray-500 capitalize">
                Category: {rec.category.replace('_', ' ')}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderRoadmap = () => (
    <div className="space-y-6">
      {roadmap && (
        <>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-blue-900">Career Transition Timeline</h3>
                <p className="text-blue-700">Estimated time to transition: {roadmap.estimated_months} months</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-blue-600">{roadmap.total_skills}</div>
                <div className="text-sm text-blue-600">skills to learn</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Immediate (0-3 months) */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-900 mb-3 flex items-center">
                <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                Immediate (0-3 months)
              </h4>
              <div className="space-y-2">
                {roadmap.roadmap.immediate.map((skill: SkillRecommendation, index: number) => (
                  <div key={index} className="bg-white rounded p-3 border border-green-100">
                    <div className="font-medium text-gray-900">{skill.skill}</div>
                    <div className="text-sm text-gray-600">Priority: {(skill.priority_score * 100).toFixed(0)}%</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Short-term (3-6 months) */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h4 className="font-semibold text-yellow-900 mb-3 flex items-center">
                <span className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
                Short-term (3-6 months)
              </h4>
              <div className="space-y-2">
                {roadmap.roadmap.shortTerm.map((skill: SkillRecommendation, index: number) => (
                  <div key={index} className="bg-white rounded p-3 border border-yellow-100">
                    <div className="font-medium text-gray-900">{skill.skill}</div>
                    <div className="text-sm text-gray-600">Priority: {(skill.priority_score * 100).toFixed(0)}%</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Long-term (6+ months) */}
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h4 className="font-semibold text-red-900 mb-3 flex items-center">
                <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
                Long-term (6+ months)
              </h4>
              <div className="space-y-2">
                {roadmap.roadmap.longTerm.map((skill: SkillRecommendation, index: number) => (
                  <div key={index} className="bg-white rounded p-3 border border-red-100">
                    <div className="font-medium text-gray-900">{skill.skill}</div>
                    <div className="text-sm text-gray-600">Priority: {(skill.priority_score * 100).toFixed(0)}%</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">AI-Powered Skill Gap Analysis</h2>
            <p className="text-gray-600">Personalized recommendations for {targetCareer}</p>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>AI-Enhanced</span>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('recommendations')}
              className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'recommendations'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Skill Recommendations
            </button>
            <button
              onClick={() => setActiveTab('roadmap')}
              className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'roadmap'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Learning Roadmap
            </button>
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'recommendations' ? renderRecommendations() : renderRoadmap()}
      </div>

      {/* Current Skills Summary */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Your Current Skills</h3>
        <div className="flex flex-wrap gap-2">
          {currentSkills.map((skill, index) => (
            <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
              {skill}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EnhancedSkillGapAnalyzer;
