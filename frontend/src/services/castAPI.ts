/**
 * CAST Framework API Service
 * Handles all interactions with the Context-Aware Skills Translation Framework
 */

interface TranslationRequest {
  text: string;
  source_language: string;
  target_language: string;
  cultural_region: string;
  content_type: string;
  user_demographics?: Record<string, any>;
  preserve_cultural_nuances?: boolean;
}

interface TranslationResult {
  original_text: string;
  translated_text: string;
  confidence_score: number;
  cultural_adaptations: string[];
  bias_warnings: string[];
  alternative_translations: string[];
  language: string;
  cultural_region: string;
}

interface BiasAnalysisRequest {
  content: string;
  language?: string;
  content_type?: string;
  cultural_context?: string;
}

interface BiasAnalysis {
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

interface SkillsMappingRequest {
  skills: string[];
  source_culture: string;
  target_culture: string;
  domain?: string;
}

interface SkillsMappingResult {
  original_skills: string[];
  mapped_skills: Array<{
    original: string;
    mapped: string;
    cultural_context: string;
    confidence: number;
    alternatives: string[];
  }>;
  cultural_insights: string[];
  mapping_confidence: number;
}

class CASTAPIService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api/cast') {
    this.baseUrl = baseUrl;
  }

  /**
   * Get supported languages
   */
  async getSupportedLanguages(): Promise<{ supported_languages: string[]; count: number }> {
    const response = await fetch(`${this.baseUrl}/languages`);
    if (!response.ok) {
      throw new Error(`Failed to fetch supported languages: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get cultural regions
   */
  async getCulturalRegions(): Promise<{ cultural_regions: string[] }> {
    const response = await fetch(`${this.baseUrl}/cultural-regions`);
    if (!response.ok) {
      throw new Error(`Failed to fetch cultural regions: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get framework information
   */
  async getFrameworkInfo(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/framework-info`);
    if (!response.ok) {
      throw new Error(`Failed to fetch framework info: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Translate text with cultural context
   */
  async translateText(request: TranslationRequest): Promise<TranslationResult> {
    const response = await fetch(`${this.baseUrl}/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Translation failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Analyze bias in content
   */
  async analyzeBias(request: BiasAnalysisRequest): Promise<BiasAnalysis> {
    const response = await fetch(`${this.baseUrl}/analyze-bias`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Bias analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Map skills across cultures
   */
  async mapSkills(request: SkillsMappingRequest): Promise<SkillsMappingResult> {
    const response = await fetch(`${this.baseUrl}/map-skills`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Skills mapping failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get multilingual career recommendations
   */
  async getMultilingualRecommendations(userId: string, preferences: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        preferences,
      }),
    });

    if (!response.ok) {
      throw new Error(`Recommendations failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Validate translation quality
   */
  async validateTranslation(originalText: string, translatedText: string, targetLanguage: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/validate-translation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        original_text: originalText,
        translated_text: translatedText,
        target_language: targetLanguage,
      }),
    });

    if (!response.ok) {
      throw new Error(`Translation validation failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Check framework health
   */
  async checkHealth(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Clear translation cache
   */
  async clearCache(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/cache`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`Cache clear failed: ${response.statusText}`);
    }
    return response.json();
  }
}

// Export a singleton instance
export const castAPI = new CASTAPIService();

// Export types for use in components
export type {
  TranslationRequest,
  TranslationResult,
  BiasAnalysisRequest,
  BiasAnalysis,
  SkillsMappingRequest,
  SkillsMappingResult,
};

export default CASTAPIService;
