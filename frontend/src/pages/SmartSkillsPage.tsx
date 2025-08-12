import React, { useState, useEffect } from 'react';
import EnhancedSkillGapAnalyzer from '../components/EnhancedSkillGapAnalyzer';
import { mlService } from '../services/mlService';
import { Brain, Target, Users, BarChart3 } from 'lucide-react';

const SmartSkillsPage: React.FC = () => {
  const [availableSkills, setAvailableSkills] = useState<any>(null);
  const [selectedCareer, setSelectedCareer] = useState<string>('');
  const [userSkills, setUserSkills] = useState<string[]>([]);
  const [userProfile, setUserProfile] = useState({
    experienceYears: 0,
    academicScore: 75,
    learningCapacity: 0.5
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const skills = await mlService.getAvailableSkills();
        setAvailableSkills(skills);
        
        // Mock user data - in production, get from user profile/API
        setUserSkills(['Python', 'Excel', 'Communication']);
        setUserProfile({
          experienceYears: 2,
          academicScore: 85,
          learningCapacity: 0.7
        });
        
        if (skills.careers && skills.careers.length > 0) {
          setSelectedCareer(skills.careers[0]);
        }
      } catch (error) {
        console.error('Error loading skills data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const handleSkillToggle = (skill: string) => {
    setUserSkills(prev => 
      prev.includes(skill) 
        ? prev.filter(s => s !== skill)
        : [...prev, skill]
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading AI-powered skill analysis...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <Brain className="w-12 h-12 mr-3" />
              <h1 className="text-4xl font-bold">Smart Skills Analysis</h1>
            </div>
            <p className="text-xl text-blue-100 mb-6">
              AI-powered skill gap analysis and personalized learning recommendations
            </p>
            <div className="flex justify-center space-x-8 text-sm">
              <div className="flex items-center">
                <Target className="w-5 h-5 mr-2" />
                <span>Personalized Recommendations</span>
              </div>
              <div className="flex items-center">
                <BarChart3 className="w-5 h-5 mr-2" />
                <span>Priority Scoring</span>
              </div>
              <div className="flex items-center">
                <Users className="w-5 h-5 mr-2" />
                <span>Peer Insights</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Setup Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Setup Your Profile</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* User Profile Settings */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Personal Information</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Years of Experience
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="50"
                    value={userProfile.experienceYears}
                    onChange={(e) => setUserProfile(prev => ({
                      ...prev,
                      experienceYears: parseInt(e.target.value) || 0
                    }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Academic Performance (%)
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={userProfile.academicScore}
                    onChange={(e) => setUserProfile(prev => ({
                      ...prev,
                      academicScore: parseInt(e.target.value) || 75
                    }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Learning Capacity: {Math.round(userProfile.learningCapacity * 100)}%
                  </label>
                  <input
                    type="range"
                    min="0.1"
                    max="1"
                    step="0.1"
                    value={userProfile.learningCapacity}
                    onChange={(e) => setUserProfile(prev => ({
                      ...prev,
                      learningCapacity: parseFloat(e.target.value)
                    }))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Slow learner</span>
                    <span>Fast learner</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Skills Selection */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Current Skills</h3>
              <div className="max-h-64 overflow-y-auto">
                {availableSkills?.skills_by_category && Object.entries(availableSkills.skills_by_category).map(([category, skills]: [string, any]) => (
                  <div key={category} className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2 capitalize">
                      {category.replace('_', ' ')}
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {skills.map((skill: string) => (
                        <button
                          key={skill}
                          onClick={() => handleSkillToggle(skill)}
                          className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                            userSkills.includes(skill)
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                          }`}
                        >
                          {skill}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Career Selection */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Target Career</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {availableSkills?.careers?.map((career: string) => (
              <button
                key={career}
                onClick={() => setSelectedCareer(career)}
                className={`p-4 rounded-lg border-2 text-left transition-all hover:shadow-md ${
                  selectedCareer === career
                    ? 'border-blue-500 bg-blue-50 text-blue-900'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">{career}</div>
                <div className="text-sm text-gray-500 mt-1">
                  Click to analyze skills needed
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* AI Analysis Results */}
        {selectedCareer && userSkills.length > 0 && (
          <EnhancedSkillGapAnalyzer
            currentSkills={userSkills}
            targetCareer={selectedCareer}
            userProfile={userProfile}
          />
        )}

        {/* Getting Started Guide */}
        {(!selectedCareer || userSkills.length === 0) && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">Getting Started</h3>
            <div className="space-y-2 text-blue-800">
              <p>1. ✅ Select your current skills from the categories above</p>
              <p>2. ✅ Choose your target career</p>
              <p>3. ✅ Get AI-powered skill gap analysis and learning roadmap</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SmartSkillsPage;
