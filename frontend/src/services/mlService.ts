/**
 * ML Service for Smart Skill Gap Prioritization
 * Integrates with CareerBuddy ML API endpoints
 */

import api from './api';

export interface UserProfile {
  current_skills: string[];
  experience_years: number;
  academic_score: number;
  learning_capacity: number;
}

export interface SkillRecommendation {
  skill: string;
  priority_score: number;
  category: string;
  importance: number;
  learning_effort: string;
}

export interface SkillPriorityResponse {
  user_profile: UserProfile;
  target_career: string;
  recommendations: SkillRecommendation[];
  total_recommendations: number;
}

export interface MultiCareerAnalysis {
  user_profile: UserProfile;
  career_analysis: Record<string, SkillRecommendation[]>;
}

export interface CareerDifficultyComparison {
  user_profile: UserProfile;
  career_difficulty_ranking: Array<[string, {
    difficulty_score: number;
    difficulty_level: string;
    skills_needed: number;
    high_effort_skills: number;
    avg_priority: number;
  }]>;
  easiest_transition: string | null;
  hardest_transition: string | null;
}

export interface AvailableSkills {
  skills_by_category: Record<string, string[]>;
  all_skills: string[];
  careers: string[];
}

class MLService {
  private baseUrl = '/api/v1/ml';

  /**
   * Get health status of ML service
   */
  async getHealthStatus() {
    const response = await api.get(`${this.baseUrl}/health`);
    return response.data;
  }

  /**
   * Get all available skills and careers
   */
  async getAvailableSkills(): Promise<AvailableSkills> {
    const response = await api.get(`${this.baseUrl}/skills/available`);
    return response.data;
  }

  /**
   * Get personalized skill priorities for a user
   */
  async prioritizeSkills(
    userProfile: UserProfile,
    targetCareer: string,
    topK: number = 10
  ): Promise<SkillPriorityResponse> {
    const response = await api.post(`${this.baseUrl}/skills/prioritize`, {
      user_profile: userProfile,
      target_career: targetCareer,
      top_k: topK
    });
    return response.data;
  }

  /**
   * Analyze skill gaps for multiple careers
   */
  async analyzeSkillGaps(
    userProfile: UserProfile,
    targetCareers: string[],
    topK: number = 5
  ): Promise<MultiCareerAnalysis> {
    const response = await api.post(`${this.baseUrl}/skills/analyze-gaps`, {
      user_profile: userProfile,
      target_careers: targetCareers,
      top_k: topK
    });
    return response.data;
  }

  /**
   * Compare career transition difficulty
   */
  async compareCareerDifficulty(
    userProfile: UserProfile,
    targetCareers: string[]
  ): Promise<CareerDifficultyComparison> {
    const response = await api.post(`${this.baseUrl}/skills/compare-careers`, {
      user_profile: userProfile,
      target_careers: targetCareers,
      top_k: 20
    });
    return response.data;
  }

  /**
   * Get skill recommendations based on current user data
   */
  async getPersonalizedRecommendations(
    currentSkills: string[],
    targetCareer: string,
    userInfo?: {
      experienceYears?: number;
      academicScore?: number;
      learningCapacity?: number;
    }
  ): Promise<SkillRecommendation[]> {
    const userProfile: UserProfile = {
      current_skills: currentSkills,
      experience_years: userInfo?.experienceYears || 0,
      academic_score: userInfo?.academicScore || 75,
      learning_capacity: userInfo?.learningCapacity || 0.5
    };

    const response = await this.prioritizeSkills(userProfile, targetCareer);
    return response.recommendations;
  }

  /**
   * Get learning roadmap for a career transition
   */
  async getCareerTransitionRoadmap(
    currentSkills: string[],
    targetCareer: string,
    userInfo?: {
      experienceYears?: number;
      academicScore?: number;
      learningCapacity?: number;
    }
  ) {
    const recommendations = await this.getPersonalizedRecommendations(
      currentSkills, 
      targetCareer, 
      userInfo
    );

    // Group by learning effort and priority
    const roadmap = {
      immediate: recommendations
        .filter(r => r.learning_effort === 'Low' && r.priority_score > 0.6)
        .slice(0, 3),
      shortTerm: recommendations
        .filter(r => r.learning_effort === 'Medium' && r.priority_score > 0.5)
        .slice(0, 4),
      longTerm: recommendations
        .filter(r => r.learning_effort === 'High' && r.priority_score > 0.4)
        .slice(0, 3)
    };

    return {
      target_career: targetCareer,
      roadmap,
      total_skills: recommendations.length,
      estimated_months: this.estimateTimeToTransition(roadmap)
    };
  }

  /**
   * Estimate time required for career transition
   */
  private estimateTimeToTransition(roadmap: any): number {
    const effortMonths = {
      'Low': 1,
      'Medium': 3,
      'High': 6
    };

    const immediateTime = roadmap.immediate.length * effortMonths['Low'];
    const shortTermTime = roadmap.shortTerm.length * effortMonths['Medium'];
    const longTermTime = roadmap.longTerm.length * effortMonths['High'];

    return Math.round(immediateTime + shortTermTime + longTermTime);
  }

  /**
   * Get skill category distribution for user
   */
  async getSkillCategoryAnalysis(currentSkills: string[]): Promise<Record<string, number>> {
    const availableSkills = await this.getAvailableSkills();
    const categoryCount: Record<string, number> = {};

    // Initialize all categories
    Object.keys(availableSkills.skills_by_category).forEach(category => {
      categoryCount[category] = 0;
    });

    // Count skills by category
    currentSkills.forEach(skill => {
      Object.entries(availableSkills.skills_by_category).forEach(([category, skills]) => {
        if (skills.includes(skill)) {
          categoryCount[category]++;
        }
      });
    });

    return categoryCount;
  }
}

export const mlService = new MLService();
