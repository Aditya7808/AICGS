import axios from 'axios';
import { config } from '../config/api';

const API_BASE_URL = config.apiUrl;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only redirect to login if we're not already on login/signup pages
      const currentPath = window.location.pathname;
      if (!currentPath.includes('/login') && !currentPath.includes('/signup')) {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  full_name?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  refresh_token: string;
  expires_in: number;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name?: string;
  created_at: string;
}

export interface SignupResponse {
  message: string;
  user_id: string;
  email_confirmed: boolean;
  requires_email_verification: boolean;
}

export interface RecommendationRequest {
  age: number;
  location: string;
  skills: string[];
  interests: string[];
  language: string;
  educationLevel?: string;
  familyBackground?: string;
  economicContext?: string;
  culturalContext?: string;
  careerGoals?: string;
  familyExpectations?: string;
  geographicConstraints?: string;
  languagePreference?: string;
  infrastructureLevel?: string;
}

export interface CareerMatch {
  career: string;
  score: number;
  local_demand: string;
  description: string;
}

export interface RecommendationResponse {
  matches: CareerMatch[];
}

// Phase 3: Peer Intelligence interfaces
export interface PeerIntelligenceResponse {
  user_id: number;
  similar_students: Array<{
    student_id: string;
    similarity_score: number;
    education_level: string;
    current_marks: number;
    career_outcomes: string[];
    similarity_reasons: string[];
  }>;
  success_stories: Array<{
    student_profile: any;
    career_choice: string;
    success_factors: string[];
    inspiration_message: string;
  }>;
  popular_choices: Array<{
    career_name: string;
    popularity_count: number;
    recommendation_strength: string;
    avg_success_rate: number;
  }>;
  peer_comparison: {
    user_position: string;
    academic_standing: string;
    career_diversity: number;
    insights: string[];
  };
  peer_insights: {
    trending_careers: string[];
    success_patterns: string[];
    recommendations: string[];
  };
  generated_at: string;
}

// Phase 3: Skill Gap Analysis interfaces
export interface SkillGapRequest {
  user_id: number;
  target_career_id: number;
  current_skills: string[];
  current_education_level: string;
  time_horizon_months?: number;
}

export interface SkillGapResponse {
  career_analyses: Record<string, {
    skill_gaps: {
      missing_skills: string[];
      available_skills: string[];
      skill_categories: Record<string, any>;
    };
    learning_roadmap: {
      phases: Array<{
        phase: string;
        duration_weeks: number;
        skills: string[];
        resources: Array<{
          title: string;
          type: string;
          duration: string;
          difficulty: string;
          url?: string;
        }>;
      }>;
    };
    overall_gaps: {
      completion_percentage: number;
      readiness_level: string;
      high_priority_missing: number;
    };
    time_estimate: {
      total_weeks: number;
      study_schedule: Record<string, any>;
    };
    readiness_score: number;
    recommendations: string[];
  }>;
  overall_recommendations: string[];
  skill_priorities: Array<{
    skill: string;
    priority: string;
    careers_requiring: string[];
  }>;
}

// Education Pathways Types
export interface Course {
  id: number;
  name: string;
  code?: string;
  credits?: number;
  semester?: number;
  description?: string;
  topics_covered?: string[];
  skills_gained?: string[];
  course_type?: string;
  delivery_mode?: string;
  assessment_methods?: string[];
}

export interface Institution {
  id: number;
  name: string;
  short_name?: string;
  institution_type?: string;
  category?: string;
  city?: string;
  state?: string;
  website?: string;
  ranking_national?: number;
  ranking_global?: number;
  facilities?: string[];
}

export interface EducationPathway {
  id: number;
  career_id: number;
  pathway_name: string;
  pathway_type: string;
  description?: string;
  duration_months?: number;
  difficulty_level?: string;
  min_education_level?: string;
  required_subjects?: string[];
  min_percentage?: number;
  entrance_exams?: string[];
  estimated_cost_min?: number;
  estimated_cost_max?: number;
  financial_aid_available: boolean;
  scholarship_opportunities?: string[];
  average_placement_rate?: number;
  average_starting_salary?: number;
  top_recruiting_companies?: string[];
  popularity_score: number;
  success_rate: number;
}

export interface InstitutionPathway {
  id: number;
  institution: Institution;
  pathway: EducationPathway;
  program_name?: string;
  fees_per_year?: number;
  duration_years?: number;
  entrance_exams_accepted?: string[];
  cutoff_scores?: Record<string, any>;
  seats_available?: number;
  placement_statistics?: Record<string, any>;
  application_fee?: number;
}

export interface AdmissionProcess {
  id: number;
  process_name: string;
  process_type: string;
  application_start_date?: string;
  application_end_date?: string;
  exam_dates?: string[];
  result_declaration_date?: string;
  eligibility_criteria?: Record<string, any>;
  required_documents?: string[];
  exam_pattern?: Record<string, any>;
  syllabus?: Record<string, any>;
  recommended_preparation_time?: number;
  preparation_resources?: Record<string, any>;
  difficulty_level?: string;
  success_tips?: string[];
}

export interface EducationRecommendationsResponse {
  recommended_pathways: Array<{
    pathway: EducationPathway;
    top_institutions: Array<{
      institution: Institution;
      fees_per_year?: number;
      entrance_exams?: string[];
      placement_rate?: number;
    }>;
  }>;
  budget_analysis: {
    selected_range: string;
    average_cost: number;
    cost_breakdown: Record<string, string>;
    financial_aid_options: string[];
  };
  timeline_analysis: {
    preparation_phase: string;
    application_phase: string;
    study_duration: string;
    total_timeline: string;
  };
  success_probability?: Record<string, any>;
  alternative_options?: any[];
}

export interface EntranceExamInfo {
  name: string;
  full_name: string;
  conducting_authority: string;
  exam_type: string;
  subjects: string[];
  duration: string;
  total_marks: number;
  exam_dates: string[];
  application_fee: number;
  eligibility: {
    min_education: string;
    min_percentage: number;
    age_limit: string;
    attempts_allowed: string;
  };
  preparation_tips: string[];
  accepted_by: string[];
  difficulty_level: string;
}

export const authAPI = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },
  
  signup: async (data: SignupRequest): Promise<SignupResponse> => {
    const response = await api.post('/auth/signup', data);
    return response.data;
  },
  
  getMe: async (): Promise<UserProfile> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  createProfile: async (): Promise<{ message: string }> => {
    const response = await api.post('/auth/create-profile');
    return response.data;
  },

  updateProfile: async (data: { full_name?: string }): Promise<{ message: string }> => {
    const response = await api.put('/auth/me', data);
    return response.data;
  },

  logout: async (): Promise<{ message: string }> => {
    const response = await api.post('/auth/logout');
    return response.data;
  },

  refreshToken: async (refresh_token: string): Promise<TokenResponse> => {
    const response = await api.post('/auth/refresh', { refresh_token });
    return response.data;
  },

  resendConfirmation: async (email: string): Promise<{ message: string }> => {
    const response = await api.post('/auth/resend-confirmation', { email });
    return response.data;
  },

  googleSignin: async (): Promise<{ url: string; provider: string }> => {
    const response = await api.get('/auth/google/url');
    return response.data;
  },

  googleCallback: async (code: string): Promise<TokenResponse> => {
    const response = await api.post('/auth/google/callback', { code });
    return response.data;
  }
};

export const recommendationAPI = {
  getRecommendations: async (data: RecommendationRequest): Promise<RecommendationResponse> => {
    const response = await api.post('/recommend', data);
    return response.data;
  },

  // Phase 3: Peer Intelligence API
  getPeerIntelligence: async (userId: number): Promise<PeerIntelligenceResponse> => {
    const response = await api.get(`/recommend/v2/peer-intelligence/${userId}`);
    return response.data;
  },

  // Phase 3: Skill Gap Analysis API
  analyzeSkillGap: async (data: SkillGapRequest): Promise<SkillGapResponse> => {
    const response = await api.post('/recommend/v2/skill-gap-analysis', data);
    return response.data;
  },

  getLearningRoadmap: async (userId: number, careerId: number, timeHorizon: number = 12) => {
    const response = await api.get(`/recommend/v2/learning-roadmap/${userId}/${careerId}?time_horizon=${timeHorizon}`);
    return response.data;
  },

  getCareerReadiness: async (userId: number, careerId: number) => {
    const response = await api.get(`/recommend/v2/career-readiness/${userId}/${careerId}`);
    return response.data;
  },

  // Test endpoint for Phase 3
  testPhase3: async () => {
    const response = await api.get('/recommend/v3/test');
    return response.data;
  }
};

export const progressAPI = {
  getDashboard: async () => {
    const response = await api.get('/progress/dashboard');
    return response.data;
  },

  getSkillProgress: async () => {
    const response = await api.get('/progress/skills');
    return response.data;
  },

  updateSkillProgress: async (skillData: {
    skill_name: string;
    current_level: string;
    proficiency_score: number;
    target_level?: string;
    time_invested_hours?: number;
  }) => {
    const response = await api.post('/progress/skills', skillData);
    return response.data;
  },

  getCareerGoals: async () => {
    const response = await api.get('/progress/goals');
    return response.data;
  },

  createCareerGoal: async (goalData: {
    career_id: number;
    goal_type?: string;
    target_timeline?: string;
    priority_level?: number;
    links?: Array<{
      title: string;
      url: string;
      type: string;
    }>;
  }) => {
    const response = await api.post('/progress/goals', goalData);
    return response.data;
  },

  updateCareerGoal: async (goalId: number, updateData: {
    progress_percentage: number;
    completed_skills?: string[];
    next_action?: string;
    links?: Array<{
      title: string;
      url: string;
      type: string;
    }>;
  }) => {
    const response = await api.put(`/progress/goals/${goalId}`, updateData);
    return response.data;
  },

  getAssessmentHistory: async () => {
    const response = await api.get('/progress/history');
    return response.data;
  },

  getAnalytics: async () => {
    const response = await api.get('/progress/analytics');
    return response.data;
  }
};

// Education Pathways API
export const educationAPI = {
  getPathways: async (
    careerId: number,
    filters?: {
      education_level?: string;
      budget_max?: number;
      pathway_type?: string;
    }
  ): Promise<EducationPathway[]> => {
    const params = new URLSearchParams();
    if (filters?.education_level) params.append('education_level', filters.education_level);
    if (filters?.budget_max) params.append('budget_max', filters.budget_max.toString());
    if (filters?.pathway_type) params.append('pathway_type', filters.pathway_type);
    
    const response = await api.get(`/api/education/pathways/${careerId}?${params.toString()}`);
    return response.data;
  },

  getPathwayCourses: async (pathwayId: number): Promise<Course[]> => {
    const response = await api.get(`/api/education/pathways/${pathwayId}/courses`);
    return response.data;
  },

  getPathwayInstitutions: async (
    pathwayId: number,
    filters?: {
      location_filter?: string;
      ranking_min?: number;
      fees_max?: number;
    }
  ): Promise<InstitutionPathway[]> => {
    const params = new URLSearchParams();
    if (filters?.location_filter) params.append('location_filter', filters.location_filter);
    if (filters?.ranking_min) params.append('ranking_min', filters.ranking_min.toString());
    if (filters?.fees_max) params.append('fees_max', filters.fees_max.toString());

    const response = await api.get(`/api/education/pathways/${pathwayId}/institutions?${params.toString()}`);
    return response.data;
  },

  getAdmissionProcesses: async (
    institutionId: number,
    pathwayId?: number
  ): Promise<AdmissionProcess[]> => {
    const params = pathwayId ? `?pathway_id=${pathwayId}` : '';
    const response = await api.get(`/api/education/institutions/${institutionId}/admission-process${params}`);
    return response.data;
  },

  getPersonalizedRecommendations: async (
    careerIds: number[],
    currentEducation: string,
    budgetRange: string,
    locationPreference?: string
  ): Promise<EducationRecommendationsResponse> => {
    const params = new URLSearchParams();
    careerIds.forEach(id => params.append('career_ids', id.toString()));
    params.append('current_education', currentEducation);
    params.append('budget_range', budgetRange);
    if (locationPreference) params.append('location_preference', locationPreference);

    const response = await api.get(`/api/education/recommendations?${params.toString()}`);
    return response.data;
  },

  getEntranceExamsInfo: async (examNames?: string[]): Promise<EntranceExamInfo[]> => {
    const params = new URLSearchParams();
    if (examNames) {
      examNames.forEach(name => params.append('exam_names', name));
    }
    
    const response = await api.get(`/api/education/entrance-exams?${params.toString()}`);
    return response.data;
  }
};

export default api;
