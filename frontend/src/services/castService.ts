/**
 * CAST Framework API Service
 * Provides easy-to-use functions for CAST Framework endpoints
 */

import api from './api';

export interface TranslationRequest {
  content: string;
  source_language?: string;
  target_language: string;
  cultural_region?: string;
  content_type?: string;
  preserve_cultural_nuances?: boolean;
}

export interface TranslationResult {
  original_text: string;
  translated_text: string;
  confidence_score: number;
  cultural_adaptations: string[];
  bias_warnings: string[];
  alternative_translations: string[];
  language: string;
  cultural_region: string;
}

export interface BiasAnalysisRequest {
  content: string;
  cultural_context?: string;
  content_type?: string;
}

export interface BiasAnalysisResult {
  overall_bias_score: number;
  detected_biases: Array<{
    text_segment: string;
    bias_type: string;
    confidence: number;
    severity: string;
    suggested_replacement: string;
    explanation: string;
  }>;
  bias_categories: Record<string, number>;
  risk_level: string;
  mitigation_strategies: string[];
  warnings: string[];
}

export interface SkillMappingRequest {
  skills: string[];
  source_language?: string;
  target_language: string;
  cultural_context?: string;
  target_industry?: string;
}

export interface SkillMappingResult {
  mapped_skills: Array<{
    original: string;
    translated: string;
    cultural_relevance: number;
    industry_match: number;
    alternatives?: string[];
  }>;
  skill_gaps: string[];
  cultural_alignment: number;
  industry_relevance: number;
  recommendations: string[];
  enhanced_skills: Array<{
    name: string;
    enhancement: string;
    priority: string;
  }>;
}

export const castService = {
  /**
   * Get supported languages
   */
  async getSupportedLanguages(): Promise<{ supported_languages: string[]; count: number }> {
    try {
      const response = await api.get('/api/cast/languages');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch supported languages:', error);
      return {
        supported_languages: ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'or', 'as', 'ur', 'sd', 'ne', 'gom'],
        count: 16
      };
    }
  },

  /**
   * Get cultural regions
   */
  async getCulturalRegions(): Promise<{ cultural_regions: string[]; count: number }> {
    try {
      const response = await api.get('/api/cast/cultural-regions');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch cultural regions:', error);
      return {
        cultural_regions: ['north', 'south', 'east', 'west', 'northeast', 'central', 'metro', 'urban', 'rural'],
        count: 9
      };
    }
  },

  /**
   * Translate content with cultural awareness
   */
  async translateContent(request: TranslationRequest): Promise<TranslationResult> {
    try {
      const response = await api.post('/api/cast/translate', {
        content: request.content,
        source_language: request.source_language || 'en',
        target_language: request.target_language,
        cultural_region: request.cultural_region || 'general',
        content_type: request.content_type || 'career',
        preserve_cultural_nuances: request.preserve_cultural_nuances ?? true
      });
      return response.data;
    } catch (error) {
      console.error('Translation failed:', error);
      // Return fallback result
      return {
        original_text: request.content,
        translated_text: `[Translation to ${request.target_language}] ${request.content}`,
        confidence_score: 0.5,
        cultural_adaptations: ['Fallback translation - API unavailable'],
        bias_warnings: [],
        alternative_translations: [],
        language: request.target_language,
        cultural_region: request.cultural_region || 'general'
      };
    }
  },

  /**
   * Analyze content for bias
   */
  async analyzeBias(request: BiasAnalysisRequest): Promise<BiasAnalysisResult> {
    try {
      const response = await api.post('/api/cast/analyze-bias', {
        content: request.content,
        cultural_context: request.cultural_context || 'general',
        content_type: request.content_type || 'general'
      });
      return response.data;
    } catch (error) {
      console.error('Bias analysis failed:', error);
      // Return fallback result
      return {
        overall_bias_score: 0.3,
        detected_biases: [
          {
            text_segment: request.content.substring(0, 50),
            bias_type: "general",
            confidence: 0.6,
            severity: "low",
            suggested_replacement: "Consider more inclusive language",
            explanation: "Demo result - API unavailable"
          }
        ],
        bias_categories: { gender: 0.3, cultural: 0.2, age: 0.1 },
        risk_level: "low",
        mitigation_strategies: ["Use inclusive language", "Consider cultural context"],
        warnings: ["API unavailable - showing demo result"]
      };
    }
  },

  /**
   * Map skills across cultures and languages
   */
  async mapSkills(request: SkillMappingRequest): Promise<SkillMappingResult> {
    try {
      const response = await api.post('/api/cast/map-skills', {
        skills: request.skills,
        source_language: request.source_language || 'en',
        target_language: request.target_language,
        cultural_context: request.cultural_context || 'general',
        target_industry: request.target_industry || 'technology'
      });
      return response.data;
    } catch (error) {
      console.error('Skills mapping failed:', error);
      // Return fallback result
      return {
        mapped_skills: request.skills.map(skill => ({
          original: skill,
          translated: `[${request.target_language}] ${skill}`,
          cultural_relevance: 0.8,
          industry_match: 0.7,
          alternatives: [`${skill} (alternative)`]
        })),
        skill_gaps: ['Communication skills', 'Cultural awareness'],
        cultural_alignment: 0.75,
        industry_relevance: 0.80,
        recommendations: ['Focus on local market needs', 'Develop cultural competency'],
        enhanced_skills: request.skills.map(skill => ({
          name: skill,
          enhancement: `Enhanced ${skill} with cultural context`,
          priority: 'medium'
        }))
      };
    }
  }
};

export default castService;
