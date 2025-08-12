import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import EnhancedSkillGapAnalyzer from '../components/EnhancedSkillGapAnalyzer';
import { mlService } from '../services/mlService';
import { 
  Brain, Target, TrendingUp, BookOpen, Users, 
  BarChart3, Lightbulb, Zap, ChevronRight, Star
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [availableSkills, setAvailableSkills] = useState<any>(null);
  const [selectedCareer, setSelectedCareer] = useState<string>('');
  const [userSkills, setUserSkills] = useState<string[]>([]);
  const [showSkillAnalyzer, setShowSkillAnalyzer] = useState(false);
  const [loading, setLoading] = useState(true);

  const [userProfile, setUserProfile] = useState({
    experienceYears: 2,
    academicScore: 85,
    learningCapacity: 0.7
  });

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const skills = await mlService.getAvailableSkills();
        setAvailableSkills(skills);
        
        // Mock user skills - in production, get from user profile
        setUserSkills(['Python', 'Excel', 'Communication', 'Problem Solving']);
        
        // Set default career if available
        if (skills.careers && skills.careers.length > 0) {
          setSelectedCareer(skills.careers[0]);
        }
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadInitialData();
  }, []);

  const quickActions = [
    {
      icon: Brain,
      title: 'AI Skill Analysis',
      description: 'Get personalized skill recommendations',
      action: () => setShowSkillAnalyzer(true),
      color: 'bg-blue-500',
      featured: true
    },
    {
      icon: Target,
      title: 'Advanced Skills Setup',
      description: 'Detailed skill gap analysis',
      action: () => window.location.href = '/smart-skills',
      color: 'bg-green-500'
    },
    {
      icon: BookOpen,
      title: 'Learning Pathways',
      description: 'Explore educational routes',
      action: () => console.log('Open learning pathways'),
      color: 'bg-purple-500'
    },
    {
      icon: Users,
      title: 'Peer Intelligence',
      description: 'Learn from similar users',
      action: () => console.log('Open peer intelligence'),
      color: 'bg-orange-500'
    }
  ];

  const handleCareerChange = (career: string) => {
    setSelectedCareer(career);
    setShowSkillAnalyzer(true);
  };

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
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Welcome back, {user?.email?.split('@')[0] || 'User'}! 👋
              </h1>
              <p className="text-gray-600 mt-1">
                Ready to advance your career with AI-powered insights?
              </p>
            </div>
            <div className="flex items-center space-x-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg">
              <Zap className="w-5 h-5" />
              <span className="font-medium">AI-Enhanced</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Featured AI Skill Analyzer */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center mb-3">
                  <Brain className="w-8 h-8 mr-3" />
                  <h2 className="text-2xl font-bold">AI-Powered Skill Gap Analysis</h2>
                  <Star className="w-6 h-6 ml-2 text-yellow-300" />
                </div>
                <p className="text-blue-100 mb-4 text-lg">
                  Get personalized skill recommendations based on machine learning analysis of your profile and career goals.
                </p>
                <div className="flex flex-wrap gap-2 mb-4">
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm">✨ Personalized</span>
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm">🎯 Priority Scoring</span>
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm">🗺️ Learning Roadmap</span>
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm">⚡ Real-time</span>
                </div>
              </div>
              <div className="ml-6">
                <button
                  onClick={() => setShowSkillAnalyzer(true)}
                  className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors flex items-center"
                >
                  Get AI Analysis
                  <ChevronRight className="w-5 h-5 ml-2" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Current Skills</dt>
                  <dd className="text-lg font-medium text-gray-900">{userSkills.length}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Target className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Experience</dt>
                  <dd className="text-lg font-medium text-gray-900">{userProfile.experienceYears} years</dd>
                </dl>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BarChart3 className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Academic Score</dt>
                  <dd className="text-lg font-medium text-gray-900">{userProfile.academicScore}%</dd>
                </dl>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Lightbulb className="h-8 w-8 text-yellow-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Learning Capacity</dt>
                  <dd className="text-lg font-medium text-gray-900">{Math.round(userProfile.learningCapacity * 100)}%</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        {/* Career Selection */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Your Target Career</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {availableSkills?.careers?.map((career: string) => (
              <button
                key={career}
                onClick={() => handleCareerChange(career)}
                className={`p-4 rounded-lg border-2 text-left transition-all hover:shadow-md ${
                  selectedCareer === career
                    ? 'border-blue-500 bg-blue-50 text-blue-900'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">{career}</div>
                <div className="text-sm text-gray-500 mt-1">
                  Get AI analysis for this career
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={action.action}
              className={`p-6 rounded-lg shadow-md text-white text-left hover:shadow-lg transition-all transform hover:scale-105 ${
                action.featured ? 'ring-2 ring-yellow-400 ring-offset-2' : ''
              } ${action.color}`}
            >
              <action.icon className="h-8 w-8 mb-3" />
              <h3 className="font-semibold mb-2">{action.title}</h3>
              <p className="text-sm opacity-90">{action.description}</p>
              {action.featured && (
                <div className="mt-3 inline-flex items-center text-yellow-200">
                  <Star className="w-4 h-4 mr-1" />
                  <span className="text-xs">NEW</span>
                </div>
              )}
            </button>
          ))}
        </div>

        {/* AI Analysis Ready State */}
        {selectedCareer && userSkills.length > 0 && !showSkillAnalyzer && (
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-6 mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-green-900 mb-2">✅ Ready for AI Analysis!</h3>
                <p className="text-green-800">
                  You have {userSkills.length} skills selected and {selectedCareer} as your target career.
                  Get personalized recommendations now!
                </p>
              </div>
              <button
                onClick={() => setShowSkillAnalyzer(true)}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors flex items-center"
              >
                Start Analysis
                <Brain className="w-5 h-5 ml-2" />
              </button>
            </div>
          </div>
        )}

        {/* Getting Started Guide */}
        {(!selectedCareer || userSkills.length === 0) && (
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 mb-8">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">🚀 Getting Started with AI Skill Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-blue-800">
              <div className="flex items-start space-x-3">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</span>
                <div>
                  <p className="font-medium">Add Your Skills</p>
                  <p className="text-sm text-blue-700">Select from {availableSkills?.all_skills?.length || 50}+ available skills</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</span>
                <div>
                  <p className="font-medium">Choose Target Career</p>
                  <p className="text-sm text-blue-700">Select from {availableSkills?.careers?.length || 15} career paths</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">3</span>
                <div>
                  <p className="font-medium">Get AI Analysis</p>
                  <p className="text-sm text-blue-700">Receive personalized learning roadmap</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Current Skills Overview - Interactive */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Your Current Skills</h3>
            <Link
              to="/smart-skills"
              className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center"
            >
              Advanced Setup
              <ChevronRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Current Skills Display */}
            <div>
              <h4 className="font-medium text-gray-700 mb-3">Selected Skills ({userSkills.length})</h4>
              <div className="flex flex-wrap gap-2 min-h-[60px] p-3 border-2 border-dashed border-gray-200 rounded-lg">
                {userSkills.length > 0 ? (
                  userSkills.map((skill, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full flex items-center"
                    >
                      {skill}
                      <button
                        onClick={() => handleSkillToggle(skill)}
                        className="ml-2 text-blue-600 hover:text-blue-800"
                      >
                        ×
                      </button>
                    </span>
                  ))
                ) : (
                  <div className="text-gray-400 text-sm flex items-center justify-center w-full">
                    No skills selected yet. Add some skills to get started!
                  </div>
                )}
              </div>
            </div>

            {/* Quick Add Skills */}
            <div>
              <h4 className="font-medium text-gray-700 mb-3">Quick Add Skills</h4>
              <div className="max-h-48 overflow-y-auto">
                {availableSkills?.skills_by_category && Object.entries(availableSkills.skills_by_category).slice(0, 2).map(([category, skills]: [string, any]) => (
                  <div key={category} className="mb-3">
                    <h5 className="text-sm font-medium text-gray-600 mb-2 capitalize">
                      {category.replace('_', ' ')}
                    </h5>
                    <div className="flex flex-wrap gap-1">
                      {skills.slice(0, 8).map((skill: string) => (
                        <button
                          key={skill}
                          onClick={() => handleSkillToggle(skill)}
                          className={`px-2 py-1 rounded text-xs font-medium transition-colors ${
                            userSkills.includes(skill)
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {userSkills.includes(skill) ? '✓ ' : '+ '}{skill}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
                <div className="text-xs text-gray-500 mt-2">
                  <Link to="/smart-skills" className="text-blue-600 hover:text-blue-800">
                    View all skills categories →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* User Profile Quick Settings */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile Settings</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
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
                <span>Slow</span>
                <span>Fast</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* AI Skill Gap Analyzer Modal/Section */}
      {showSkillAnalyzer && selectedCareer && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">
                AI Skill Gap Analysis: {selectedCareer}
              </h2>
              <button
                onClick={() => setShowSkillAnalyzer(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-6">
              <EnhancedSkillGapAnalyzer
                currentSkills={userSkills}
                targetCareer={selectedCareer}
                userProfile={userProfile}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
