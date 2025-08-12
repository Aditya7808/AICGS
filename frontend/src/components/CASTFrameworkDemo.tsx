import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { config } from '../config/api';

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

const CASTFrameworkDemo: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<'translate' | 'bias' | 'skills'>('translate');
  const [isLoading, setIsLoading] = useState(false);
  
  // Translation state
  const [translationInput, setTranslationInput] = useState('Software Engineer responsible for developing web applications');
  const [targetLanguage, setTargetLanguage] = useState('hi');
  const [culturalRegion, setCulturalRegion] = useState('north');
  const [translationResult, setTranslationResult] = useState<TranslationResult | null>(null);
  
  // Bias analysis state
  const [biasInput, setBiasInput] = useState('We need young, energetic developers who can work long hours');
  const [biasResult, setBiasResult] = useState<BiasAnalysis | null>(null);
  
  // Skills mapping state
  const [skillsInput, setSkillsInput] = useState('JavaScript, React, Node.js, MongoDB');
  const [skillsResult, setSkillsResult] = useState<any>(null);
  
  const [supportedLanguages, setSupportedLanguages] = useState<string[]>([]);
  const [culturalRegions, setCulturalRegions] = useState<string[]>([]);

  // Language display names
  const languageNames: Record<string, string> = {
    'en': 'English',
    'hi': 'Hindi (हिंदी)',
    'ta': 'Tamil (தமிழ்)',
    'te': 'Telugu (తెలుగు)',
    'bn': 'Bengali (বাংলা)',
    'mr': 'Marathi (मराठी)',
    'gu': 'Gujarati (ગુજરાતી)',
    'kn': 'Kannada (ಕನ್ನಡ)',
    'ml': 'Malayalam (മലയാളം)',
    'pa': 'Punjabi (ਪੰਜਾਬੀ)',
    'or': 'Odia (ଓଡ଼ିଆ)',
    'as': 'Assamese (অসমীয়া)',
    'ur': 'Urdu (اردو)',
    'sd': 'Sindhi (سندھی)',
    'ne': 'Nepali (नेपाली)',
    'gom': 'Konkani (कोंकणी)'
  };

  // Cultural region display names
  const regionNames: Record<string, string> = {
    'north': 'Northern India',
    'south': 'Southern India',
    'east': 'Eastern India', 
    'west': 'Western India',
    'northeast': 'Northeast India',
    'central': 'Central India',
    'metro': 'Metropolitan Cities',
    'urban': 'Urban Areas',
    'rural': 'Rural Areas'
  };

  useEffect(() => {
    fetchSupportedLanguages();
    fetchCulturalRegions();
  }, []);

  const fetchSupportedLanguages = async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/cast/languages`);
      const data = await response.json();
      setSupportedLanguages(data.supported_languages || []);
    } catch (error) {
      console.error('Failed to fetch supported languages:', error);
      // Fallback to predefined languages
      setSupportedLanguages(['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa', 'or', 'as', 'ur', 'sd', 'ne', 'gom']);
    }
  };

  const fetchCulturalRegions = async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/cast/cultural-regions`);
      const data = await response.json();
      setCulturalRegions(data.cultural_regions || []);
    } catch (error) {
      console.error('Failed to fetch cultural regions:', error);
      // Fallback to predefined regions
      setCulturalRegions(['north', 'south', 'east', 'west', 'northeast', 'central', 'metro', 'urban', 'rural']);
    }
  };

  const handleTranslation = async () => {
    if (!translationInput.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await fetch(`${config.apiUrl}/api/cast/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: translationInput,
          source_language: 'en',
          target_language: targetLanguage,
          cultural_region: culturalRegion,
          content_type: 'career',
          preserve_cultural_nuances: true
        })
      });

      if (response.ok) {
        const result = await response.json();
        setTranslationResult(result);
      } else {
        const errorData = await response.json();
        console.error('Translation failed:', errorData);
        // Show fallback result
        setTranslationResult({
          original_text: translationInput,
          translated_text: `[Translation to ${targetLanguage}] ${translationInput}`,
          confidence_score: 0.5,
          cultural_adaptations: ['Fallback translation - API unavailable'],
          bias_warnings: [],
          alternative_translations: [],
          language: targetLanguage,
          cultural_region: culturalRegion
        });
      }
    } catch (error) {
      console.error('Translation error:', error);
      // Show fallback result
      setTranslationResult({
        original_text: translationInput,
        translated_text: `[Translation to ${targetLanguage}] ${translationInput}`,
        confidence_score: 0.5,
        cultural_adaptations: ['Fallback translation - API unavailable'],
        bias_warnings: [],
        alternative_translations: [],
        language: targetLanguage,
        cultural_region: culturalRegion
      });
    }
    setIsLoading(false);
  };

  const handleBiasAnalysis = async () => {
    if (!biasInput.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await fetch(`${config.apiUrl}/api/cast/analyze-bias`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: biasInput,
          cultural_context: culturalRegion,
          content_type: 'general'
        })
      });

      if (response.ok) {
        const result = await response.json();
        setBiasResult(result);
      } else {
        const errorData = await response.json();
        console.error('Bias analysis failed:', errorData);
        // Show fallback result
        setBiasResult({
          overall_bias_score: 0.3,
          detected_biases: [
            {
              text_segment: biasInput.substring(0, 50),
              bias_type: "gender",
              confidence: 0.6,
              severity: "low",
              suggested_replacement: "Use gender-neutral language",
              explanation: "Consider using inclusive language"
            }
          ],
          bias_categories: { gender: 0.3, cultural: 0.2, age: 0.1 },
          risk_level: "low",
          mitigation_strategies: ["Use inclusive language", "Consider cultural context"],
          warnings: ["API unavailable - showing demo result"]
        });
      }
    } catch (error) {
      console.error('Bias analysis error:', error);
      // Show fallback result  
      setBiasResult({
        overall_bias_score: 0.3,
        detected_biases: [],
        bias_categories: { gender: 0.3, cultural: 0.2, age: 0.1 },
        risk_level: "low",
        mitigation_strategies: ["Use inclusive language", "Consider cultural context"],
        warnings: ["API unavailable - showing demo result"]
      });
    }
    setIsLoading(false);
  };

  const handleSkillsMapping = async () => {
    if (!skillsInput.trim()) return;
    
    const skillsList = skillsInput.split(',').map(s => s.trim()).filter(s => s);
    
    setIsLoading(true);
    try {
      const response = await fetch(`${config.apiUrl}/api/cast/map-skills`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          skills: skillsList,
          source_language: 'en',
          target_language: targetLanguage,
          cultural_context: culturalRegion,
          target_industry: 'technology'
        })
      });

      if (response.ok) {
        const result = await response.json();
        setSkillsResult(result);
      } else {
        const errorData = await response.json();
        console.error('Skills mapping failed:', errorData);
        // Show fallback result
        setSkillsResult({
          mapped_skills: skillsList.map(skill => ({
            original: skill,
            translated: `[${targetLanguage}] ${skill}`,
            cultural_relevance: 0.8,
            industry_match: 0.7,
            alternatives: [`${skill} (alternative)`]
          })),
          skill_gaps: ['Communication skills', 'Cultural awareness'],
          cultural_alignment: 0.75,
          industry_relevance: 0.80,
          recommendations: ['Focus on local market needs', 'Develop cultural competency'],
          enhanced_skills: skillsList.map(skill => ({
            name: skill,
            enhancement: `Enhanced ${skill} with cultural context`,
            priority: 'medium'
          }))
        });
      }
    } catch (error) {
      console.error('Skills mapping error:', error);
      // Show fallback result
      setSkillsResult({
        mapped_skills: skillsList.map(skill => ({
          original: skill,
          translated: `[${targetLanguage}] ${skill}`,
          cultural_relevance: 0.8,
          industry_match: 0.7
        })),
        skill_gaps: ['Communication skills', 'Cultural awareness'],
        cultural_alignment: 0.75,
        industry_relevance: 0.80,
        recommendations: ['Focus on local market needs', 'Develop cultural competency'],
        enhanced_skills: []
      });
    }
    setIsLoading(false);
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          {t('cast_framework.multilingual_support')} - CAST Framework Demo
        </h1>
        <p className="text-gray-600">
          Context-Aware Skills Translation Framework for multilingual career guidance
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6">
        <button
          onClick={() => setActiveTab('translate')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'translate'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Translation
        </button>
        <button
          onClick={() => setActiveTab('bias')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'bias'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Bias Detection
        </button>
        <button
          onClick={() => setActiveTab('skills')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'skills'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Skills Mapping
        </button>
      </div>

      {/* Controls */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Language
            </label>
            <select
              value={targetLanguage}
              onChange={(e) => setTargetLanguage(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {supportedLanguages.map(lang => (
                <option key={lang} value={lang}>{languageNames[lang] || lang.toUpperCase()}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cultural Region
            </label>
            <select
              value={culturalRegion}
              onChange={(e) => setCulturalRegion(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {culturalRegions.map(region => (
                <option key={region} value={region}>{regionNames[region] || region.charAt(0).toUpperCase() + region.slice(1)}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Translation Tab */}
      {activeTab === 'translate' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Text to Translate
            </label>
            <textarea
              value={translationInput}
              onChange={(e) => setTranslationInput(e.target.value)}
              placeholder="Enter career-related content to translate..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
            />
            
            <div className="mt-2 mb-3">
              <p className="text-sm text-gray-600 mb-2">Quick samples:</p>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setTranslationInput('Software Engineer responsible for developing web applications')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Job Title
                </button>
                <button
                  onClick={() => setTranslationInput('Looking for skilled candidates with experience in Java programming and database management')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Job Description
                </button>
                <button
                  onClick={() => setTranslationInput('Strong communication skills and team leadership abilities required')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Skills Required
                </button>
              </div>
            </div>

            <button
              onClick={handleTranslation}
              disabled={isLoading || !translationInput.trim()}
              className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50"
            >
              {isLoading ? 'Translating...' : 'Translate'}
            </button>
          </div>

          {translationResult && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold mb-3">Translation Result</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Original</h4>
                  <p className="p-3 bg-white rounded border">{translationResult.original_text}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Translated</h4>
                  <p className="p-3 bg-white rounded border">{translationResult.translated_text}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Confidence Score</h4>
                  <div className="flex items-center">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full"
                        style={{ width: `${translationResult.confidence_score * 100}%` }}
                      ></div>
                    </div>
                    <span className="ml-2 text-sm font-medium">
                      {(translationResult.confidence_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
                
                {translationResult.cultural_adaptations.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Cultural Adaptations</h4>
                    <ul className="text-sm space-y-1">
                      {translationResult.cultural_adaptations.map((adaptation, index) => (
                        <li key={index} className="text-green-600">• {adaptation}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {translationResult.bias_warnings.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Bias Warnings</h4>
                    <ul className="text-sm space-y-1">
                      {translationResult.bias_warnings.map((warning, index) => (
                        <li key={index} className="text-red-600">⚠ {warning}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Bias Analysis Tab */}
      {activeTab === 'bias' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content to Analyze for Bias
            </label>
            <textarea
              value={biasInput}
              onChange={(e) => setBiasInput(e.target.value)}
              placeholder="Enter content to analyze for bias..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
            />
            
            <div className="mt-2 mb-3">
              <p className="text-sm text-gray-600 mb-2">Quick samples:</p>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setBiasInput('We need young, energetic developers who can work long hours')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Ageist Language
                </button>
                <button
                  onClick={() => setBiasInput('Looking for native English speakers only for customer service role')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Language Bias
                </button>
                <button
                  onClick={() => setBiasInput('Female candidates preferred for receptionist position')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Gender Bias
                </button>
              </div>
            </div>

            <button
              onClick={handleBiasAnalysis}
              disabled={isLoading || !biasInput.trim()}
              className="mt-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:opacity-50"
            >
              {isLoading ? 'Analyzing...' : 'Analyze Bias'}
            </button>
          </div>

          {biasResult && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold mb-3">Bias Analysis Result</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Overall Bias Score</h4>
                  <div className="flex items-center">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-red-500 h-2 rounded-full"
                        style={{ width: `${biasResult.overall_bias_score * 100}%` }}
                      ></div>
                    </div>
                    <span className="ml-2 text-sm font-medium">
                      {(biasResult.overall_bias_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Risk Level</h4>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(biasResult.risk_level)}`}>
                    {biasResult.risk_level.toUpperCase()}
                  </span>
                </div>

                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Detected Biases</h4>
                  <span className="text-2xl font-bold text-red-600">
                    {biasResult.detected_biases.length}
                  </span>
                </div>
              </div>

              {biasResult.detected_biases.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Bias Details</h4>
                  <div className="space-y-2">
                    {biasResult.detected_biases.map((bias, index) => (
                      <div key={index} className="p-3 bg-white rounded border border-red-200">
                        <div className="flex justify-between items-start mb-2">
                          <span className="font-medium text-red-700">{bias.bias_type}</span>
                          <span className={`px-2 py-1 rounded text-xs ${
                            bias.severity === 'high' ? 'bg-red-100 text-red-800' :
                            bias.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {bias.severity}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-1">
                          <strong>Text:</strong> "{bias.text_segment}"
                        </p>
                        <p className="text-sm text-gray-600 mb-1">
                          <strong>Suggested:</strong> "{bias.suggested_replacement}"
                        </p>
                        <p className="text-xs text-gray-500">{bias.explanation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {biasResult.mitigation_strategies.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Mitigation Strategies</h4>
                  <ul className="text-sm space-y-1">
                    {biasResult.mitigation_strategies.map((strategy, index) => (
                      <li key={index} className="text-blue-600">• {strategy}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Skills Mapping Tab */}
      {activeTab === 'skills' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Skills to Map (comma-separated)
            </label>
            <textarea
              value={skillsInput}
              onChange={(e) => setSkillsInput(e.target.value)}
              placeholder="Enter skills separated by commas (e.g., programming, communication, leadership, problem solving)"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
            
            <div className="mt-2 mb-3">
              <p className="text-sm text-gray-600 mb-2">Quick samples:</p>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSkillsInput('JavaScript, React, Node.js, MongoDB')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Tech Skills
                </button>
                <button
                  onClick={() => setSkillsInput('Project Management, Leadership, Communication, Problem Solving')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Soft Skills
                </button>
                <button
                  onClick={() => setSkillsInput('Data Analysis, Machine Learning, Python, Statistics')}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
                >
                  Data Science
                </button>
              </div>
            </div>

            <button
              onClick={handleSkillsMapping}
              disabled={isLoading || !skillsInput.trim()}
              className="mt-2 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50"
            >
              {isLoading ? 'Mapping...' : 'Map Skills'}
            </button>
          </div>

          {skillsResult && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold mb-3">Skills Mapping Result</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Cultural Alignment</h4>
                  <div className="flex items-center">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{ width: `${skillsResult.cultural_alignment * 100}%` }}
                      ></div>
                    </div>
                    <span className="ml-2 text-sm font-medium">
                      {(skillsResult.cultural_alignment * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Industry Relevance</h4>
                  <div className="flex items-center">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full"
                        style={{ width: `${skillsResult.industry_relevance * 100}%` }}
                      ></div>
                    </div>
                    <span className="ml-2 text-sm font-medium">
                      {(skillsResult.industry_relevance * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>

              {skillsResult.mapped_skills && skillsResult.mapped_skills.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Mapped Skills</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {skillsResult.mapped_skills.map((skill: any, index: number) => (
                      <div key={index} className="p-3 bg-white rounded border">
                        <div className="flex justify-between items-start">
                          <div>
                            <p className="font-medium">{skill.original}</p>
                            <p className="text-sm text-blue-600">{skill.mapped}</p>
                          </div>
                          <div className="text-xs text-gray-500">
                            <div>Cultural: {(skill.cultural_fit * 100).toFixed(0)}%</div>
                            <div>Relevant: {(skill.industry_relevance * 100).toFixed(0)}%</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {skillsResult.recommendations && skillsResult.recommendations.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Recommendations</h4>
                  <ul className="text-sm space-y-1">
                    {skillsResult.recommendations.map((recommendation: string, index: number) => (
                      <li key={index} className="text-purple-600">• {recommendation}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CASTFrameworkDemo;
