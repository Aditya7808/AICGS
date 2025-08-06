import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import ResultCard from '../components/ResultCard';
import PeerIntelligence from '../components/PeerIntelligence';
import SkillGapAnalyzer from '../components/SkillGapAnalyzer';
import { RecommendationResponse, PeerIntelligenceResponse, SkillGapResponse, recommendationAPI } from '../services/api';
import { GraduationCap } from 'lucide-react';

const Results: React.FC = () => {
  const { t } = useTranslation();
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'recommendations' | 'peer-intelligence' | 'skill-gaps'>('recommendations');
  const [peerData, setPeerData] = useState<PeerIntelligenceResponse | null>(null);
  const [skillGapData, setSkillGapData] = useState<SkillGapResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    // Load results from localStorage
    const savedResults = localStorage.getItem('careerResults');
    if (savedResults) {
      setResults(JSON.parse(savedResults));
    } else {
      navigate('/assessment');
    }
  }, [isAuthenticated, navigate]);

  // Load Phase 3 data when user is available
  useEffect(() => {
    const loadPhase3Data = async () => {
      if (!user?.id) return;
      
      try {
        setLoading(true);
        // Load peer intelligence data
        if (activeTab === 'peer-intelligence' && !peerData) {
          const peerResponse = await recommendationAPI.getPeerIntelligence(user.id);
          setPeerData(peerResponse);
        }
        // Load skill gap data 
        if (activeTab === 'skill-gaps' && !skillGapData) {
          // For demo, we'll use mock data - in real app you'd have the actual career IDs
          const mockRequest = {
            user_id: user.id,
            target_career_id: 1,
            current_skills: ['Python', 'Web Development'],
            current_education_level: 'Undergraduate'
          };
          const skillResponse = await recommendationAPI.analyzeSkillGap(mockRequest);
          setSkillGapData(skillResponse);
        }
      } catch (error) {
        console.error('Error loading Phase 3 data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadPhase3Data();
  }, [activeTab, user, peerData, skillGapData]);

  if (!isAuthenticated || !results) {
    return null;
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'peer-intelligence':
        return user?.id ? <PeerIntelligence userId={user.id} /> : <div>Please log in to view peer intelligence</div>;
      case 'skill-gaps':
        return user?.id ? <SkillGapAnalyzer userId={user.id} /> : <div>Please log in to view skill gap analysis</div>;
      default:
        return (
          <div className="space-y-6">
            {results.matches.map((match, index) => (
              <div
                key={index}
                className="bg-white rounded-2xl shadow-soft border border-gray-100 overflow-hidden hover:shadow-medium transition-all duration-300 transform hover:-translate-y-1"
              >
                <ResultCard match={match} />
              </div>
            ))}
          </div>
        );
    }
  };

  if (!isAuthenticated || !results) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <div className="mb-6">
            <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            🎉 Your Career Matches Are Ready!
          </h1>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Based on your skills, interests, and preferences, we've found the perfect career paths for you.
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
              ✨ Personalized Results
            </span>
            <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
              🎯 AI-Powered Matching
            </span>
            <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
              � Peer Intelligence
            </span>
            <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
              📈 Skill Gap Analysis
            </span>
            <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
              �📍 Location-Based
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-2xl p-6 text-center shadow-soft border border-gray-100">
            <div className="text-3xl font-bold text-primary-600 mb-2">
              {results.matches.length}
            </div>
            <div className="text-gray-600">Career Matches Found</div>
          </div>
          <div className="bg-white rounded-2xl p-6 text-center shadow-soft border border-gray-100">
            <div className="text-3xl font-bold text-secondary-600 mb-2">
              {Math.round(results.matches.reduce((acc, match) => acc + (match.score * 100), 0) / results.matches.length)}%
            </div>
            <div className="text-gray-600">Average Match Score</div>
          </div>
          <div className="bg-white rounded-2xl p-6 text-center shadow-soft border border-gray-100">
            <div className="text-3xl font-bold text-accent-600 mb-2">
              {results.matches.filter(match => match.score >= 0.8).length}
            </div>
            <div className="text-gray-600">High-Quality Matches</div>
          </div>
        </div>

        {/* Career Matches */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-900">
              Your Career Analysis
            </h2>
            <Link
              to="/assessment"
              className="btn-secondary flex items-center space-x-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>Retake Assessment</span>
            </Link>
          </div>

          {/* Tab Navigation */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`flex-1 py-4 px-6 text-center font-medium transition-all duration-200 ${
                  activeTab === 'recommendations'
                    ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                🎯 Career Matches
              </button>
              <button
                onClick={() => setActiveTab('peer-intelligence')}
                className={`flex-1 py-4 px-6 text-center font-medium transition-all duration-200 ${
                  activeTab === 'peer-intelligence'
                    ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                👥 Peer Intelligence
              </button>
              <button
                onClick={() => setActiveTab('skill-gaps')}
                className={`flex-1 py-4 px-6 text-center font-medium transition-all duration-200 ${
                  activeTab === 'skill-gaps'
                    ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                📈 Skill Analysis
              </button>
            </div>
          </div>

          {/* Tab Content */}
          <div className="min-h-[400px]">
            {loading ? (
              <div className="flex justify-center items-center py-16">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <div className="text-gray-500">Loading analysis...</div>
                </div>
              </div>
            ) : (
              renderTabContent()
            )}
          </div>
        </div>

        {results.matches.length === 0 && (
          <div className="text-center py-16">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 20.4a7.962 7.962 0 01-5-1.691m0 0V9a3 3 0 015.356-1.857M7 20.4V9a3 3 0 015.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              No Perfect Matches Found
            </h3>
            <p className="text-gray-600 text-lg mb-8 max-w-md mx-auto">
              Don't worry! Let's try again with different preferences to find careers that match your unique profile.
            </p>
            <Link
              to="/assessment"
              className="btn-primary text-lg px-8 py-3"
            >
              Retake Assessment
            </Link>
          </div>
        )}

        {/* Next Steps */}
        {results.matches.length > 0 && (
          <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl p-8 text-white text-center">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Take the Next Step?
            </h3>
            <p className="text-lg opacity-90 mb-6 max-w-2xl mx-auto">
              Now that you've discovered your ideal career paths, explore educational opportunities, 
              connect with professionals, and start building your future today.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                to={`/education/${results.matches.map((_, index) => index + 1).join(',')}`}
                className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors duration-200 flex items-center gap-2"
              >
                <GraduationCap className="w-5 h-5" />
                Education Pathways
              </Link>
              <button className="bg-white/20 backdrop-blur-sm text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/30 transition-colors duration-200 border border-white/30">
                Find Mentors
              </button>
              <button className="bg-white/20 backdrop-blur-sm text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/30 transition-colors duration-200 border border-white/30">
                Join Communities
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Results;
