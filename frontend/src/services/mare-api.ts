// MARE API Service
// Enhanced API service for Multi-Dimensional Adaptive Recommendation Engine

import api from './api';

export interface MARERecommendationRequest {
  // Personal dimensions
  age: number;
  education_level: string;
  location: string;
  
  // Cultural dimensions
  cultural_context: string;
  family_background: string;
  language_preference: string;
  
  // Economic dimensions
  economic_context: string;
  financial_constraints?: string;
  
  // Geographic dimensions
  geographic_constraints: string;
  urban_rural_type: string;
  infrastructure_level: string;
  
  // Social dimensions
  family_expectations: string;
  peer_influence_score: number;
  community_values?: string;
  
  // Skills and interests
  skills: string[];
  interests: string[];
  skill_weights?: { [key: string]: number };
  interest_weights?: { [key: string]: number };
  
  // Career preferences (optional)
  career_goals?: string;
  preferred_industries?: string[];
  work_environment_preference?: string;
  salary_expectations?: string;
  work_life_balance_priority?: number;
}

export interface MARERecommendation {
  career_id: string;
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
    skills_explanation: string;
    cultural_explanation: string;
    economic_explanation: string;
    geographic_explanation: string;
    social_explanation: string;
    growth_explanation: string;
  };
  confidence_level: string;
  
  // Legacy fields for backward compatibility
  id?: number;
  description?: string;
  confidence_score?: number;
  required_skills?: string[];
  preferred_skills?: string[];
  skill_match_percentage?: number;
  salary_range?: {
    min: number;
    max: number;
  };
  locations?: string[];
  remote_available?: boolean;
  urban_rural_suitability?: string;
  cultural_fit?: number;
  family_friendly_rating?: number;
  traditional_modern_spectrum?: string;
  growth_potential?: number;
  job_security?: number;
  future_outlook?: string;
  adaptability_factors?: {
    personal_fit: number;
    cultural_alignment: number;
    economic_viability: number;
    geographic_accessibility: number;
    social_acceptance: number;
  };
  education_requirements?: string[];
  experience_level?: string;
  mare_compatibility_score?: number;
}

export interface MAREInsights {
  user_profile_completeness: number;
  dominant_skill_categories: string[];
  cultural_career_alignment: number;
  economic_opportunity_score: number;
  geographic_mobility_score: number;
  
  recommendations_summary: {
    total_generated: number;
    avg_confidence: number;
    top_industries: string[];
    growth_potential_avg: number;
  };
  
  learning_progress: {
    feedback_provided: number;
    preferences_learned: string[];
    accuracy_improvement: number;
  };
}

export interface RecommendationFeedback {
  career_opportunity_id: number;
  recommendation_score: number;
  recommendation_rank?: number;
  user_rating?: number; // 1-5 stars
  user_feedback?: string;
  selected: boolean;
  time_spent_viewing?: number; // seconds
  context_snapshot?: any;
  
  // Detailed fit scores
  cultural_fit_score?: number;
  economic_fit_score?: number;
  geographic_fit_score?: number;
  skills_match_score?: number;
}

export interface MAREAnalytics {
  total_recommendations: number;
  positive_ratings: number;
  conversions: number;
  avg_rating: number;
  avg_recommendation_score: number;
  satisfaction_rate: number;
  conversion_rate: number;
  avg_time_spent: number;
}

export interface PopularCareerPath {
  id: number;
  title: string;
  industry: string;
  total_recommendations: number;
  selections: number;
  avg_rating: number;
  avg_mare_score: number;
}

class MAREApiService {
  private baseUrl = '/api/v1/mare';

  // Core recommendation functionality
  async getRecommendations(request: MARERecommendationRequest): Promise<MARERecommendation[]> {
    try {
      console.log('Making MARE API request:', request);
      const response = await api.post(`${this.baseUrl}/recommendations`, request);
      console.log('MARE API response:', response);
      console.log('MARE API response data:', response.data);
      console.log('Response data type:', typeof response.data);
      console.log('Response data is array:', Array.isArray(response.data));
      
      // Backend returns array directly, not wrapped in recommendations property
      const recommendations = Array.isArray(response.data) ? response.data : (response.data.recommendations || []);
      console.log('Processed recommendations:', recommendations);
      console.log('Recommendations count:', recommendations.length);
      
      return recommendations;
    } catch (error) {
      console.error('Error getting MARE recommendations:', error);
      throw new Error('Failed to get recommendations');
    }
  }

  async createProfile(profile: MARERecommendationRequest): Promise<any> {
    try {
      const response = await api.post(`${this.baseUrl}/profile`, profile);
      return response.data;
    } catch (error) {
      console.error('Error creating MARE profile:', error);
      throw new Error('Failed to create profile');
    }
  }

  async updateProfile(userId: number, profileUpdates: Partial<MARERecommendationRequest>): Promise<any> {
    try {
      const response = await api.put(`${this.baseUrl}/profile/${userId}`, profileUpdates);
      return response.data;
    } catch (error) {
      console.error('Error updating MARE profile:', error);
      throw new Error('Failed to update profile');
    }
  }

  // Feedback and learning
  async submitFeedback(feedback: RecommendationFeedback): Promise<any> {
    try {
      const response = await api.post(`${this.baseUrl}/feedback`, feedback);
      return response.data;
    } catch (error) {
      console.error('Error submitting feedback:', error);
      throw new Error('Failed to submit feedback');
    }
  }

  async getFeedbackHistory(userId: number, limit: number = 20): Promise<RecommendationFeedback[]> {
    try {
      const response = await api.get(`${this.baseUrl}/feedback/${userId}?limit=${limit}`);
      return response.data.feedback_history || [];
    } catch (error) {
      console.error('Error getting feedback history:', error);
      return [];
    }
  }

  // Insights and analytics
  async getAdaptiveLearningInsights(userId: number): Promise<MAREInsights> {
    try {
      const response = await api.get(`${this.baseUrl}/insights/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting MARE insights:', error);
      throw new Error('Failed to get insights');
    }
  }

  async getRecommendationAnalytics(days: number = 30): Promise<MAREAnalytics> {
    try {
      const response = await api.get(`${this.baseUrl}/analytics?days=${days}`);
      return response.data;
    } catch (error) {
      console.error('Error getting analytics:', error);
      throw new Error('Failed to get analytics');
    }
  }

  async getPopularCareerPaths(limit: number = 10): Promise<PopularCareerPath[]> {
    try {
      const response = await api.get(`${this.baseUrl}/popular-careers?limit=${limit}`);
      return response.data.popular_careers || [];
    } catch (error) {
      console.error('Error getting popular career paths:', error);
      return [];
    }
  }

  // Career opportunities search
  async searchCareerOpportunities(filters: {
    industry?: string;
    location?: string;
    salary_min?: number;
    salary_max?: number;
    remote_available?: boolean;
    urban_rural_type?: string;
    required_skills?: string[];
  }, limit: number = 50): Promise<MARERecommendation[]> {
    try {
      const queryParams = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          if (Array.isArray(value)) {
            value.forEach(item => queryParams.append(key, item));
          } else {
            queryParams.append(key, value.toString());
          }
        }
      });
      queryParams.append('limit', limit.toString());

      const response = await api.get(`${this.baseUrl}/opportunities?${queryParams.toString()}`);
      return response.data.opportunities || [];
    } catch (error) {
      console.error('Error searching career opportunities:', error);
      return [];
    }
  }

  async getCareerOpportunity(opportunityId: number): Promise<MARERecommendation | null> {
    try {
      const response = await api.get(`${this.baseUrl}/opportunities/${opportunityId}`);
      return response.data.opportunity;
    } catch (error) {
      console.error('Error getting career opportunity:', error);
      return null;
    }
  }

  // Utility methods
  async validateProfileData(profileData: Partial<MARERecommendationRequest>): Promise<{
    isValid: boolean;
    errors: string[];
    suggestions: string[];
  }> {
    try {
      const response = await api.post(`${this.baseUrl}/validate-profile`, profileData);
      return response.data;
    } catch (error) {
      console.error('Error validating profile data:', error);
      return {
        isValid: false,
        errors: ['Failed to validate profile data'],
        suggestions: []
      };
    }
  }

  async getSkillSuggestions(partialSkill: string, limit: number = 10): Promise<string[]> {
    try {
      const response = await api.get(`${this.baseUrl}/skills/suggest?q=${encodeURIComponent(partialSkill)}&limit=${limit}`);
      return response.data.suggestions || [];
    } catch (error) {
      console.error('Error getting skill suggestions:', error);
      return [];
    }
  }

  async getLocationSuggestions(partialLocation: string, limit: number = 10): Promise<string[]> {
    try {
      const response = await api.get(`${this.baseUrl}/locations/suggest?q=${encodeURIComponent(partialLocation)}&limit=${limit}`);
      return response.data.suggestions || [];
    } catch (error) {
      console.error('Error getting location suggestions:', error);
      return [];
    }
  }

  // Real-time updates
  async subscribeToRecommendationUpdates(userId: number, callback: (update: any) => void): Promise<() => void> {
    // This would implement WebSocket or Server-Sent Events for real-time updates
    // For now, we'll use polling as a fallback
    
    const pollInterval = 30000; // 30 seconds
    const intervalId = setInterval(async () => {
      try {
        const insights = await this.getAdaptiveLearningInsights(userId);
        callback({ type: 'insights_update', data: insights });
      } catch (error) {
        console.error('Error polling for updates:', error);
      }
    }, pollInterval);

    // Return unsubscribe function
    return () => {
      clearInterval(intervalId);
    };
  }
}

// Export singleton instance
export const mareApi = new MAREApiService();
