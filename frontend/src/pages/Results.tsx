import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ResultCard from '../components/ResultCard';
import PeerIntelligence from '../components/PeerIntelligence';
import SkillGapAnalyzer from '../components/SkillGapAnalyzer';
import GroqEnhancedMAREResults from '../components/GroqEnhancedMAREResults';
import { RecommendationResponse, PeerIntelligenceResponse, SkillGapResponse, recommendationAPI } from '../services/api';
import { mareApi } from '../services/mare-api';
import { GraduationCap } from 'lucide-react';

const Results: React.FC = () => {
  const location = useLocation();
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const [mareResults, setMareResults] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'recommendations' | 'peer-intelligence' | 'skill-gaps'>('recommendations');
  const [peerData, setPeerData] = useState<PeerIntelligenceResponse | null>(null);
  const [skillGapData, setSkillGapData] = useState<SkillGapResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [groqLoading, setGroqLoading] = useState(false);
  const [groqError, setGroqError] = useState<string | null>(null);
  const [showGroqResults, setShowGroqResults] = useState(false);
  const [enhancedResults, setEnhancedResults] = useState<any>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    // Check for data passed via navigation state (MARE assessment)
    const navigationState = location.state as any;
    console.log('Results page loaded. Navigation state:', navigationState);
    console.log('Current mareResults:', mareResults);
    console.log('Current results:', results);
    console.log('Current enhancedResults:', enhancedResults);
    
    if (navigationState) {
      console.log('Navigation state received:', navigationState);
      console.log('navigationState.recommendations:', navigationState.recommendations);
      console.log('navigationState.enhancedRecommendations:', navigationState.enhancedRecommendations);
      console.log('Type of recommendations:', typeof navigationState.recommendations);
      console.log('Is array:', Array.isArray(navigationState.recommendations));
      
      if (navigationState.enhancedRecommendations) {
        console.log('Setting enhanced recommendations:', navigationState.enhancedRecommendations);
        setEnhancedResults(navigationState.enhancedRecommendations);
        setMareResults(navigationState.enhancedRecommendations);
      } else if (navigationState.recommendations) {
        console.log('Setting standard recommendations:', navigationState.recommendations);
        setMareResults(navigationState.recommendations);
      }
      
      // Store in localStorage for persistence
      if (navigationState.enhancedRecommendations || navigationState.recommendations) {
        localStorage.setItem('careerResults', JSON.stringify({
          type: navigationState.source || 'MARE',
          data: navigationState.enhancedRecommendations || navigationState.recommendations,
          formData: navigationState.formData,
          timestamp: new Date().toISOString()
        }));
      }
    } else {
      // Fallback: Load results from localStorage
      const savedResults = localStorage.getItem('careerResults');
      if (savedResults) {
        const parsed = JSON.parse(savedResults);
        console.log('Loaded from localStorage:', parsed);
        
        if (parsed.type === 'MARE' || parsed.type === 'MARE_ENHANCED') {
          setMareResults(parsed.data);
          if (parsed.type === 'MARE_ENHANCED') {
            setEnhancedResults(parsed.data);
          }
        } else {
          setResults(parsed);
        }
      } else {
        // No results found, try to load sample data or redirect to assessment
        console.log('No saved results found, checking for fallback options');
        
        // For testing, let's try to create a simple fallback request
        if (user?.id) {
          console.log('User is available, attempting to fetch demo recommendations');
          const loadDemoRecommendations = async () => {
            try {
              // Create a simple demo request
              const demoRequest = {
                age: 22,
                education_level: 'Undergraduate',
                location: 'India',
                cultural_context: 'traditional',
                family_background: 'middle_class',
                language_preference: 'en',
                economic_context: 'middle_income',
                financial_constraints: 'moderate',
                geographic_constraints: 'urban_preferred',
                urban_rural_type: 'urban',
                infrastructure_level: 'good',
                family_expectations: 'supportive_with_guidance',
                peer_influence_score: 0.5,
                community_values: 'traditional',
                skills: ['communication', 'problem_solving'],
                interests: ['technology', 'business'],
                skill_weights: {},
                interest_weights: {},
                career_goals: 'Looking for a stable career with growth potential',
                preferred_industries: ['Technology', 'Business'],
                work_environment_preference: 'office',
                salary_expectations: '500000-1000000',
                work_life_balance_priority: 7
              };
              
              const demoResponse = await mareApi.getRecommendations(demoRequest);
              console.log('Demo recommendations received:', demoResponse);
              console.log('First recommendation structure:', demoResponse[0]);
              if (demoResponse[0]) {
                console.log('overall_score:', demoResponse[0].overall_score);
                console.log('title:', demoResponse[0].title);
                console.log('dimension_scores:', demoResponse[0].dimension_scores);
              }
              setMareResults(demoResponse);
              
              // Store in localStorage
              localStorage.setItem('careerResults', JSON.stringify({
                type: 'MARE_DEMO',
                data: demoResponse,
                timestamp: new Date().toISOString()
              }));
            } catch (error) {
              console.error('Failed to fetch demo recommendations:', error);
              navigate('/mare');
            }
          };
          
          loadDemoRecommendations();
        } else {
          navigate('/mare');
        }
      }
    }
  }, [isAuthenticated, navigate, location]);

  // Load Phase 3 data when user is available
  useEffect(() => {
    const loadPhase3Data = async () => {
      if (!user?.id) return;
      
      try {
        setLoading(true);
        // Load peer intelligence data
        if (activeTab === 'peer-intelligence' && !peerData) {
          const peerResponse = await recommendationAPI.getPeerIntelligence(parseInt(user.id));
          setPeerData(peerResponse);
        }
        // Load skill gap data 
        if (activeTab === 'skill-gaps' && !skillGapData) {
          // For demo, we'll use mock data - in real app you'd have the actual career IDs
          const mockRequest = {
            user_id: parseInt(user.id),
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

  // Function to fetch Groq enhanced results
  const fetchGroqEnhancedResults = async () => {
    if (!user) {
      setGroqError('Please log in to access AI enhancement features.');
      return;
    }

    setGroqLoading(true);
    setGroqError(null);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Authentication token not found. Please login again.');
      }

      // Get the stored assessment data from localStorage
      const savedResults = localStorage.getItem('careerResults');
      let assessmentData = null;
      
      if (savedResults) {
        const parsed = JSON.parse(savedResults);
        assessmentData = parsed.formData;
      }

      // If no assessment data, create a sample one based on current results
      if (!assessmentData) {
        assessmentData = {
          age: 25,
          education_level: "bachelor",
          location: "India",
          cultural_context: "modern_urban",
          family_background: "middle_class",
          language_preference: "en",
          economic_context: "stable_middle_class",
          financial_constraints: "moderate",
          geographic_constraints: "flexible",
          urban_rural_type: "urban",
          infrastructure_level: "good",
          family_expectations: "supportive_with_guidance",
          peer_influence_score: 0.6,
          community_values: "education_focused",
          skills: ["communication", "problem_solving", "analytical_thinking"],
          interests: ["technology", "innovation", "learning"],
          skill_weights: {},
          interest_weights: {},
          career_goals: "Seeking a fulfilling career with growth opportunities",
          preferred_industries: ["Technology", "Business"],
          work_environment_preference: "hybrid",
          salary_expectations: "competitive",
          work_life_balance_priority: 7
        };
      }

      console.log('🤖 Fetching Groq enhanced results with data:', assessmentData);

      const response = await fetch('http://localhost:8000/api/v1/mare/recommendations/enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(assessmentData)
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('AI enhancement service is not available. Please check if the backend is running and Groq API is configured.');
        } else if (response.status === 401 || response.status === 403) {
          // For demo purposes, show demo results when authentication fails
          console.log('🔧 Authentication failed, showing demo Groq results...');
          showDemoGroqResults();
          return;
        } else if (response.status === 500) {
          // If Groq API key is not configured, show demo data
          console.log('Groq API not configured, showing demo enhanced results');
          showDemoGroqResults();
          return;
        } else {
          throw new Error(`Failed to fetch enhanced results: ${response.status} ${response.statusText}`);
        }
      }

      const data = await response.json();
      console.log('✅ Groq enhanced results received:', data);
      
      setEnhancedResults(data);
      setShowGroqResults(true);
      
      // Store enhanced results in localStorage
      const updatedResults = {
        type: 'MARE_ENHANCED',
        data: data,
        formData: assessmentData,
        timestamp: new Date().toISOString()
      };
      localStorage.setItem('careerResults', JSON.stringify(updatedResults));
      
    } catch (error) {
      console.error('❌ Error fetching Groq enhanced results:', error);
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch AI enhancement';
      setGroqError(errorMessage);
    } finally {
      setGroqLoading(false);
    }
  };

  // Demo function to show Groq results without authentication
  const showDemoGroqResults = () => {
    const demoEnhancedResults = {
      enhancement_available: true,
      groq_enhanced_suggestions: [
        {
          career_title: "Data Scientist",
          personalized_insight: "Based on your strong analytical background and interest in technology, data science is an excellent fit. Your computer science education provides a solid foundation for the programming skills required, while your problem-solving abilities will excel in extracting insights from complex datasets.",
          actionable_steps: [
            "Complete an online course in machine learning (Coursera ML Specialization recommended)",
            "Build 3-5 data science projects using real datasets and showcase them on GitHub",
            "Learn key tools: Python pandas, scikit-learn, TensorFlow, and Tableau for visualization",
            "Network with data scientists through LinkedIn and attend local tech meetups",
            "Apply for junior data analyst positions to gain industry experience"
          ],
          skill_development_plan: [
            "Advanced Python programming with focus on data libraries",
            "Statistical analysis and hypothesis testing", 
            "Machine learning algorithms (supervised and unsupervised)",
            "Data visualization and storytelling",
            "SQL for database management",
            "Business acumen to translate data insights to business value"
          ],
          cultural_considerations: "In Indian tech culture, data science is highly respected and offers excellent career growth. The field aligns well with the emphasis on analytical thinking and continuous learning valued in your background.",
          timeline_suggestion: "With focused effort, you can transition into a data science role within 12-18 months. Start with foundational courses (3-6 months), build projects (6-9 months), then begin applying for positions.",
          confidence_score: 0.92
        },
        {
          career_title: "Software Developer", 
          personalized_insight: "Your technical foundation makes software development a natural career progression. The field offers diverse opportunities from web development to mobile apps, allowing you to specialize based on your interests while maintaining strong job security.",
          actionable_steps: [
            "Choose a specialization (web development, mobile apps, or backend systems)",
            "Master a popular framework (React for frontend, Node.js for backend)",
            "Contribute to open-source projects to build your portfolio",
            "Practice coding challenges on platforms like LeetCode and HackerRank",
            "Build 2-3 full-stack applications demonstrating different technologies"
          ],
          skill_development_plan: [
            "Full-stack web development (HTML, CSS, JavaScript)",
            "Modern frameworks and libraries (React, Angular, or Vue.js)",
            "Backend development with Node.js or Python Django",
            "Database design and management (SQL and NoSQL)",
            "Version control with Git and collaborative development",
            "Software testing and deployment practices"
          ],
          cultural_considerations: "Software development is one of the most established and respected careers in Indian tech industry, offering excellent work-life balance and remote work opportunities that align with modern work preferences.",
          timeline_suggestion: "You can become job-ready in 6-12 months with intensive practice. Focus on building a strong portfolio and gaining proficiency in 2-3 key technologies rather than trying to learn everything.",
          confidence_score: 0.87
        },
        {
          career_title: "Product Manager",
          personalized_insight: "Your combination of technical knowledge and business interest positions you well for product management. This role bridges technology and business strategy, requiring both analytical thinking and communication skills you possess.",
          actionable_steps: [
            "Take a product management course (Google PM Certificate or similar)",
            "Analyze successful products and write case studies on product decisions",
            "Learn user experience (UX) principles and customer research methods",
            "Practice product strategy frameworks like RICE prioritization",
            "Network with current product managers and seek mentorship opportunities"
          ],
          skill_development_plan: [
            "Product strategy and roadmap planning",
            "User research and customer interview techniques",
            "Data analysis for product metrics and KPIs",
            "Agile and Scrum methodologies",
            "Cross-functional team leadership",
            "Market research and competitive analysis"
          ],
          cultural_considerations: "Product management is emerging as a prestigious career path in India's growing startup ecosystem. It offers the opportunity to drive innovation while building products that impact millions of users.",
          timeline_suggestion: "Transitioning to product management typically takes 18-24 months, as it requires building both technical credibility and business acumen. Consider starting in a technical role and transitioning internally.",
          confidence_score: 0.78
        }
      ],
      career_pathway_summary: "Your technical background and analytical mindset position you excellently for high-growth careers in the technology sector. The recommended pathway starts with building strong foundational skills in your chosen field, followed by practical experience through projects and internships. Data science offers the highest alignment with your interests and skills, while software development provides the most direct career entry point. Product management represents a longer-term growth opportunity that combines your technical knowledge with business strategy. Focus on continuous learning, building a strong portfolio, and networking within the tech community to accelerate your career growth.",
      standard_recommendations: mareResults || []
    };

    setEnhancedResults(demoEnhancedResults);
    setShowGroqResults(true);
    
    // Store demo results
    localStorage.setItem('careerResults', JSON.stringify({
      type: 'MARE_ENHANCED_DEMO',
      data: demoEnhancedResults,
      timestamp: new Date().toISOString()
    }));
  };

  // Function to toggle between standard and enhanced results
  const toggleGroqResults = () => {
    setShowGroqResults(!showGroqResults);
  };

  if (!isAuthenticated) {
    return null;
  }

  // Show loading if no data is available yet
  if (!results && !mareResults && !enhancedResults) {
    console.log('No data available - showing loading screen');
    console.log('results:', results);
    console.log('mareResults:', mareResults);
    console.log('enhancedResults:', enhancedResults);
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your career recommendations...</p>
          <p className="text-sm text-gray-500 mt-2">
            If this takes too long, please <a href="/mare" className="text-blue-600 underline">retake the assessment</a>
          </p>
        </div>
      </div>
    );
  }

  console.log('About to render results page with:');
  console.log('mareResults:', mareResults);
  console.log('results:', results);
  console.log('enhancedResults:', enhancedResults);

  const renderTabContent = () => {
    switch (activeTab) {
      case 'peer-intelligence':
        return user?.id ? <PeerIntelligence userId={parseInt(user.id)} /> : <div>Please log in to view peer intelligence</div>;
      case 'skill-gaps':
        return user?.id ? <SkillGapAnalyzer userId={parseInt(user.id)} /> : <div>Please log in to view skill gap analysis</div>;
      default:
        console.log('Rendering recommendations tab');
        console.log('mareResults:', mareResults);
        console.log('mareResults type:', typeof mareResults);
        console.log('mareResults is array:', Array.isArray(mareResults));
        console.log('mareResults length:', mareResults?.length);
        
        // Handle MARE results - Check if we should show enhanced or standard
        if (mareResults && Array.isArray(mareResults)) {
          console.log('Rendering MARE results, count:', mareResults.length);
          
          // Show Groq Enhanced Results if available
          if (showGroqResults && enhancedResults) {
            return <GroqEnhancedMAREResults assessmentData={enhancedResults} />;
          }
          
          // Show standard MARE results
          return (
            <div className="space-y-6">
              {mareResults.map((recommendation: any, index: number) => (
                <div
                  key={index}
                  className="bg-white rounded-2xl shadow-soft border border-gray-100 overflow-hidden hover:shadow-medium transition-all duration-300 transform hover:-translate-y-1 p-6"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-800 mb-2">
                        {recommendation.title || 'Career Opportunity'}
                      </h3>
                      <p className="text-gray-600 mb-2">
                        <span className="font-medium">Industry:</span> {recommendation.industry || 'N/A'}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">
                        {Math.round((recommendation.overall_score || 0) * 100)}%
                      </div>
                      <div className="text-sm text-gray-500">Match Score</div>
                    </div>
                  </div>
                  
                  {recommendation.dimension_scores && (
                    <div className="mb-4">
                      <h4 className="text-lg font-medium mb-3">Dimension Scores</h4>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {Object.entries(recommendation.dimension_scores).map(([dimension, score]: [string, any]) => (
                          <div key={dimension} className="bg-gray-50 p-3 rounded-lg">
                            <div className="text-sm font-medium text-gray-700 capitalize">
                              {dimension.replace('_', ' ')}
                            </div>
                            <div className="text-lg font-semibold text-blue-600">
                              {Math.round(score * 100)}%
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {recommendation.explanation && (
                    <div className="mb-4">
                      <h4 className="text-lg font-medium mb-2">Why This Matches You</h4>
                      <div className="space-y-2">
                        {Object.entries(recommendation.explanation).map(([key, value]: [string, any]) => (
                          <div key={key} className="text-sm text-gray-600">
                            <span className="font-medium capitalize">{key.replace('_', ' ')}:</span> {value}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center pt-4 border-t border-gray-200">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      recommendation.confidence_level === 'High' ? 'bg-green-100 text-green-800' :
                      recommendation.confidence_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {recommendation.confidence_level || 'Medium'} Confidence
                    </span>
                  </div>
                </div>
              ))}
            </div>
          );
        }
        
        // Fallback to legacy results format
        if (results && results.matches) {
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
        
        // No results available
        return (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg mb-4">No recommendations available</div>
            <button 
              onClick={() => navigate('/mare-assessment')} 
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Take MARE AI Assessment
            </button>
          </div>
        );
    }
  };

  if (!isAuthenticated) {
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
        {/* Summary Stats - Handle both MARE and legacy formats */}
        {(mareResults && Array.isArray(mareResults)) ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-2xl p-6 text-center shadow-soft border border-gray-100">
              <div className="text-3xl font-bold text-primary-600 mb-2">
                {mareResults.length}
              </div>
              <div className="text-gray-600">Career Matches Found</div>
            </div>
            <div className="bg-white rounded-2xl p-6 text-center shadow-soft border border-gray-100">
              <div className="text-3xl font-bold text-secondary-600 mb-2">
                {(() => {
                  if (!mareResults || mareResults.length === 0) return '0';
                  
                  const scores = mareResults.map((rec: any) => {
                    const score = rec.overall_score || 0;
                    console.log('Processing score for', rec.title, ':', score);
                    return score;
                  });
                  
                  const sum = scores.reduce((acc: number, score: number) => acc + score, 0);
                  const average = sum / mareResults.length;
                  const percentage = Math.round(average * 100);
                  
                  console.log('Score calculation:', { scores, sum, average, percentage });
                  
                  return isNaN(percentage) ? '0' : `${percentage}`;
                })()}%
              </div>
              <div className="text-gray-600">Average Match Score</div>
            </div>
            <div className="bg-white rounded-2xl p-6 text-center shadow-soft border border-gray-100">
              <div className="text-3xl font-bold text-accent-600 mb-2">
                {mareResults.filter((rec: any) => {
                  const score = rec.overall_score || 0;
                  return score >= 0.8;
                }).length}
              </div>
              <div className="text-gray-600">High-Quality Matches</div>
            </div>
          </div>
        ) : results && results.matches ? (
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
        ) : null}          {/* Career Matches */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-900">
              Your Career Analysis
            </h2>
            <Link
              to="/mare-assessment"
              className="btn-secondary flex items-center space-x-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>Retake MARE Assessment</span>
            </Link>
          </div>

          {/* Groq AI Enhancement Section */}
          <div className="mb-8">
            {!showGroqResults && !enhancedResults && (
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-xl">🤖</span>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">Get AI-Enhanced Career Insights</h3>
                      <p className="text-gray-600">
                        Unlock personalized AI-powered recommendations with actionable career steps, cultural insights, and timeline guidance.
                      </p>
                    </div>
                  </div>
                  <div className="flex space-x-3">
                    <button
                      onClick={fetchGroqEnhancedResults}
                      disabled={groqLoading}
                      className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                    >
                      {groqLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                          <span>Getting AI Insights...</span>
                        </>
                      ) : (
                        <>
                          <span>✨ Enhance with AI</span>
                        </>
                      )}
                    </button>
                    
                    <button
                      onClick={showDemoGroqResults}
                      className="bg-gradient-to-r from-green-600 to-teal-600 text-white px-4 py-3 rounded-lg hover:from-green-700 hover:to-teal-700 transition-all transform hover:scale-105 flex items-center space-x-2"
                    >
                      <span>🎯 Try Demo</span>
                    </button>
                  </div>
                </div>
                
                {groqError && (
                  <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                    <div className="flex items-start">
                      <span className="text-red-400 mr-2">⚠️</span>
                      <div>
                        <h4 className="text-sm font-medium text-red-800">AI Enhancement Error</h4>
                        <p className="mt-1 text-sm text-red-700">{groqError}</p>
                        <button
                          onClick={fetchGroqEnhancedResults}
                          className="mt-2 text-sm bg-red-100 text-red-800 px-3 py-1 rounded hover:bg-red-200 transition-colors"
                        >
                          Try Again
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {(showGroqResults && enhancedResults) && (
              <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-xl p-6 mb-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-xl">🤖</span>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">AI Enhancement Active</h3>
                      <p className="text-gray-600">
                        Your results have been enhanced with AI-powered insights and personalized recommendations.
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={toggleGroqResults}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    View Standard Results
                  </button>
                </div>
              </div>
            )}
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

          {/* Groq Enhancement Section */}
          {activeTab === 'recommendations' && !showGroqResults && (
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-xl p-6 mb-8">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-xl">🤖</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Get AI-Enhanced Career Insights
                    </h3>
                    <p className="text-gray-600 text-sm">
                      Unlock personalized career advice, actionable steps, and timeline guidance powered by Groq AI
                    </p>
                  </div>
                </div>
                <button
                  onClick={fetchGroqEnhancedResults}
                  disabled={groqLoading}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {groqLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      Getting AI Insights...
                    </>
                  ) : (
                    <>
                      ✨ Enhance with AI
                    </>
                  )}
                </button>
              </div>
              
              {groqError && (
                <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <span className="text-red-400">⚠️</span>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">Error</h3>
                      <p className="mt-1 text-sm text-red-700">{groqError}</p>
                      <div className="mt-2">
                        <button
                          onClick={fetchGroqEnhancedResults}
                          className="text-sm bg-red-100 text-red-800 px-3 py-1 rounded hover:bg-red-200 transition-colors"
                        >
                          Retry
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Enhanced Results Display */}
          {showGroqResults && enhancedResults && (
            <div className="mb-8">
              {enhancedResults.enhancement_available && (
                <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-4 mb-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">🤖</span>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">AI Enhancement Active</h3>
                        <p className="text-gray-600">Your results have been enhanced with personalized AI insights from Groq.</p>
                      </div>
                    </div>
                    <button
                      onClick={() => setShowGroqResults(false)}
                      className="text-gray-500 hover:text-gray-700 px-3 py-1 rounded border"
                    >
                      View Standard Results
                    </button>
                  </div>
                </div>
              )}
              
              {/* Groq Enhanced Suggestions */}
              {enhancedResults.groq_enhanced_suggestions?.length > 0 && (
                <div className="space-y-6 mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">🎯 AI-Enhanced Career Insights</h3>
                  {enhancedResults.groq_enhanced_suggestions.map((suggestion: any, index: number) => (
                    <div key={index} className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
                      <div className="flex justify-between items-start mb-4">
                        <h4 className="text-xl font-semibold text-gray-900">{suggestion.career_title}</h4>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          suggestion.confidence_score >= 0.8 
                            ? 'bg-green-100 text-green-800'
                            : suggestion.confidence_score >= 0.6
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {Math.round(suggestion.confidence_score * 100)}% confidence
                        </span>
                      </div>

                      <div className="space-y-4">
                        <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
                          <h5 className="font-semibold text-blue-800 mb-2">💡 Personalized Insight</h5>
                          <p className="text-blue-700">{suggestion.personalized_insight}</p>
                        </div>

                        <div>
                          <h5 className="font-semibold text-gray-800 mb-2">🎯 Your Action Plan</h5>
                          <ul className="space-y-1">
                            {suggestion.actionable_steps?.map((step: string, stepIndex: number) => (
                              <li key={stepIndex} className="flex items-start">
                                <span className="text-green-500 mr-2">✅</span>
                                <span className="text-gray-700">{step}</span>
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div>
                          <h5 className="font-semibold text-gray-800 mb-2">📚 Skills to Develop</h5>
                          <div className="flex flex-wrap gap-2">
                            {suggestion.skill_development_plan?.map((skill: string, skillIndex: number) => (
                              <span key={skillIndex} className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-4">
                          <div className="bg-purple-50 p-3 rounded-lg">
                            <h5 className="font-semibold text-gray-800 mb-1">🌍 Cultural Fit</h5>
                            <p className="text-gray-700 text-sm">{suggestion.cultural_considerations}</p>
                          </div>
                          <div className="bg-yellow-50 p-3 rounded-lg">
                            <h5 className="font-semibold text-gray-800 mb-1">⏰ Timeline</h5>
                            <p className="text-gray-700 text-sm">{suggestion.timeline_suggestion}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Career Pathway Summary */}
              {enhancedResults.career_pathway_summary && (
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-xl mb-8">
                  <h3 className="text-xl font-bold mb-3">🚀 Your Career Journey Summary</h3>
                  <p className="text-blue-100">{enhancedResults.career_pathway_summary}</p>
                </div>
              )}
            </div>
          )}

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

        {/* Handle No Results for both formats */}
        {((results && results.matches && results.matches.length === 0) || (mareResults && mareResults.length === 0)) && (
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
              to="/mare-assessment"
              className="btn-primary text-lg px-8 py-3"
            >
              Retake MARE Assessment
            </Link>
          </div>
        )}

        {/* Next Steps - Show for both formats when results exist */}
        {((results && results.matches && results.matches.length > 0) || (mareResults && mareResults.length > 0)) && (
          <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl p-8 text-white text-center">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Take the Next Step?
            </h3>
            <p className="text-lg opacity-90 mb-6 max-w-2xl mx-auto">
              Now that you've discovered your ideal career paths, explore educational opportunities, 
              connect with professionals, and start building your future today.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              {results && results.matches ? (
                <Link
                  to={`/education/${results.matches.map((_, index) => index + 1).join(',')}`}
                  className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors duration-200 flex items-center gap-2"
                >
                  <GraduationCap className="w-5 h-5" />
                  Education Pathways
                </Link>
              ) : (
                <Link
                  to="/education"
                  className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors duration-200 flex items-center gap-2"
                >
                  <GraduationCap className="w-5 h-5" />
                  Education Pathways
                </Link>
              )}
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
