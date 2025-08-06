import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, Target, BookOpen, Award, Calendar,
  CheckCircle, Activity, Plus, Edit3, ExternalLink
} from 'lucide-react';
import { progressAPI } from '../services/api';
import SkillProgressModal from '../components/SkillProgressModal';
import CareerGoalModal from '../components/CareerGoalModal';

interface ProgressData {
  user_id: number;
  total_assessments_completed: number;
  last_assessment_date: string | null;
  career_goals_set: number;
  skills_tracked: number;
  current_streak_days: number;
  longest_streak_days: number;
  profile_completeness: number;
  skill_development_score: number;
  career_clarity_score: number;
  milestones_achieved: string[];
}

interface SkillProgress {
  id: number;
  skill_name: string;
  current_level: string;
  proficiency_score: number;
  target_level: string;
  time_invested_hours: number;
  progress_history: Array<{date: string, score: number, level: string}>;
}

interface CareerGoal {
  id: number;
  career_id: number;
  goal_type: string;
  target_timeline: string;
  priority_level: number;
  status: string;
  progress_percentage: number;
  next_action?: string;
  links?: Array<{
    title: string;
    url: string;
    type: string;
  }>;
  created_at: string;
}

const ProgressDashboard: React.FC = () => {
  const [progressData, setProgressData] = useState<ProgressData | null>(null);
  const [skills, setSkills] = useState<SkillProgress[]>([]);
  const [goals, setGoals] = useState<CareerGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal states
  const [isSkillModalOpen, setIsSkillModalOpen] = useState(false);
  const [isGoalModalOpen, setIsGoalModalOpen] = useState(false);
  const [selectedSkill, setSelectedSkill] = useState<SkillProgress | undefined>();
  const [selectedGoal, setSelectedGoal] = useState<CareerGoal | undefined>();

  useEffect(() => {
    fetchProgressData();
  }, []);

  const fetchProgressData = async () => {
    try {
      setLoading(true);
      setError(''); // Clear any previous errors
      
      // Check if user is authenticated
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Not authenticated. Please log in.');
        return;
      }
      
      // Fetch all progress data using our API with timeout
      const fetchPromise = Promise.all([
        progressAPI.getDashboard(),
        progressAPI.getSkillProgress(),
        progressAPI.getCareerGoals()
      ]);
      
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout')), 10000)
      );
      
      const results = await Promise.race([fetchPromise, timeoutPromise]) as [any, any, any];
      const [dashboardData, skillsData, goalsData] = results;

      setProgressData(dashboardData);
      setSkills(skillsData);
      setGoals(goalsData);

    } catch (err: any) {
      console.error('Progress fetch error:', err);
      
      if (err.code === 'ECONNABORTED' || err.message === 'Request timeout') {
        setError('Cannot connect to server. Please make sure the backend server is running on http://localhost:8000');
      } else if (err.response?.status === 401) {
        setError('Authentication failed. Please log in again.');
        localStorage.removeItem('token');
        window.location.href = '/login';
      } else if (err.response?.status === 404) {
        setError('Progress tracking feature not available. Server may need to be updated.');
      } else {
        setError(`Failed to load progress data: ${err.message || 'Unknown error'}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleModalSuccess = () => {
    // Close modals and refresh data
    setIsSkillModalOpen(false);
    setIsGoalModalOpen(false);
    setSelectedSkill(undefined);
    setSelectedGoal(undefined);
    fetchProgressData();
  };

  const openSkillModal = (skill?: SkillProgress) => {
    setSelectedSkill(skill);
    setIsSkillModalOpen(true);
  };

  const openGoalModal = (goal?: CareerGoal) => {
    setSelectedGoal(goal);
    setIsGoalModalOpen(true);
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-blue-500';
    if (percentage >= 40) return 'bg-yellow-500';
    return 'bg-gray-400';
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your progress...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Progress Dashboard</h1>
          <p className="text-gray-600">Track your career development journey</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Assessments</p>
                <p className="text-2xl font-bold text-gray-900">
                  {progressData?.total_assessments_completed || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Career Goals</p>
                <p className="text-2xl font-bold text-gray-900">
                  {progressData?.career_goals_set || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Skills Tracked</p>
                <p className="text-2xl font-bold text-gray-900">
                  {progressData?.skills_tracked || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Current Streak</p>
                <p className="text-2xl font-bold text-gray-900">
                  {progressData?.current_streak_days || 0} days
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Progress Bars Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile Completion</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Profile Completeness</span>
                  <span className="font-medium">{Math.round((progressData?.profile_completeness || 0) * 100)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getProgressColor((progressData?.profile_completeness || 0) * 100)}`}
                    style={{ width: `${(progressData?.profile_completeness || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Skill Development</span>
                  <span className="font-medium">{Math.round((progressData?.skill_development_score || 0) * 100)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getProgressColor((progressData?.skill_development_score || 0) * 100)}`}
                    style={{ width: `${(progressData?.skill_development_score || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Career Clarity</span>
                  <span className="font-medium">{Math.round((progressData?.career_clarity_score || 0) * 100)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getProgressColor((progressData?.career_clarity_score || 0) * 100)}`}
                    style={{ width: `${(progressData?.career_clarity_score || 0) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
            <div className="space-y-3">
              <div className="flex items-center text-sm text-gray-600">
                <Calendar className="w-4 h-4 mr-2" />
                Last Assessment: {formatDate(progressData?.last_assessment_date || null)}
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <Award className="w-4 h-4 mr-2" />
                Longest Streak: {progressData?.longest_streak_days || 0} days
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <CheckCircle className="w-4 h-4 mr-2" />
                Milestones: {progressData?.milestones_achieved?.length || 0} achieved
              </div>
            </div>
          </div>
        </div>

        {/* Skills Progress */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Skill Progress</h3>
            <button
              onClick={() => openSkillModal()}
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Skill
            </button>
          </div>
          
          {skills.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {skills.map((skill) => (
                <div key={skill.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-medium text-gray-900">{skill.skill_name}</h4>                      <div className="flex items-center space-x-2">
                        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                          {skill.current_level}
                        </span>
                        <button
                          onClick={() => openSkillModal(skill)}
                          className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                          title="Edit skill"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    <div className="mb-2">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Proficiency</span>
                        <span className="font-medium">{Math.round(skill.proficiency_score * 100)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getProgressColor(skill.proficiency_score * 100)}`}
                          style={{ width: `${skill.proficiency_score * 100}%` }}
                        ></div>
                      </div>
                    </div>
                    <div className="text-xs text-gray-500">
                      Target: {skill.target_level} • {skill.time_invested_hours}h invested
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <TrendingUp className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">No skills tracked yet</p>
                <button
                  onClick={() => openSkillModal()}
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Your First Skill
                </button>
              </div>
            )}
          </div>

          {/* Career Goals */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 mb-8">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Career Goals</h3>
              <button
                onClick={() => openGoalModal()}
                className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Goal
              </button>
            </div>
            
            {goals.length > 0 ? (
              <div className="space-y-4">
                {goals.map((goal) => (
                  <div key={goal.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-medium text-gray-900">Career Goal #{goal.id}</h4>
                        <p className="text-sm text-gray-600">
                          {goal.goal_type} • Timeline: {goal.target_timeline.replace('_', ' ')}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`text-xs px-2 py-1 rounded ${
                          goal.status === 'active' ? 'bg-green-100 text-green-800' :
                          goal.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {goal.status}
                        </span>
                        <button
                          onClick={() => openGoalModal(goal)}
                          className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                          title="Edit goal"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    <div className="mb-2">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Progress</span>
                        <span className="font-medium">{Math.round(goal.progress_percentage)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getProgressColor(goal.progress_percentage)}`}
                          style={{ width: `${goal.progress_percentage}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    {/* Display Links */}
                    {goal.links && goal.links.length > 0 && (
                      <div className="mb-2">
                        <p className="text-xs font-medium text-gray-600 mb-1">Helpful Links:</p>
                        <div className="flex flex-wrap gap-1">
                          {goal.links.map((link, linkIndex) => (
                            <a
                              key={linkIndex}
                              href={link.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors"
                            >
                              <ExternalLink className="w-3 h-3 mr-1" />
                              {link.title}
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {goal.next_action && (
                      <div className="text-sm text-gray-600">
                        <strong>Next Action:</strong> {goal.next_action}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Target className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">No career goals set yet</p>
                <button
                  onClick={() => openGoalModal()}
                  className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Set Your First Goal
                </button>
              </div>
            )}
          </div>

        {/* Empty State */}
        {!progressData?.total_assessments_completed && (
          <div className="bg-white rounded-xl shadow-sm p-8 border border-gray-100 text-center">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Start Your Journey</h3>
            <p className="text-gray-600 mb-4">
              Take your first assessment to begin tracking your progress and career development.
            </p>
            <button 
              onClick={() => window.location.href = '/assessment'}
              className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
            >
              Take Assessment
            </button>
          </div>
        )}
      </div>

      {/* Modals */}
      <SkillProgressModal
        isOpen={isSkillModalOpen}
        onClose={() => setIsSkillModalOpen(false)}
        onSuccess={handleModalSuccess}
        skill={selectedSkill}
      />
      
      <CareerGoalModal
        isOpen={isGoalModalOpen}
        onClose={() => setIsGoalModalOpen(false)}
        onSuccess={handleModalSuccess}
        goal={selectedGoal}
      />
    </div>
  );
};

export default ProgressDashboard;
