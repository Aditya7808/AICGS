import React, { useState } from 'react';
import Button from './Button';
import SkillSelector from './SkillSelector';
import { mareApi, MARERecommendationRequest } from '../services/mare-api';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';

interface FormData extends Partial<MARERecommendationRequest> {
  // Additional UI state
  skillsInput?: string;
  interestsInput?: string;
}

const MAREAssessmentForm: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<string[]>([]);
  
  const [formData, setFormData] = useState<FormData>({
    age: 22,
    education_level: '',
    location: '',
    cultural_context: '',
    family_background: '',
    language_preference: 'en',
    economic_context: '',
    financial_constraints: '',
    geographic_constraints: '',
    urban_rural_type: 'urban',
    infrastructure_level: 'good',
    family_expectations: '',
    peer_influence_score: 0.5,
    community_values: '',
    skills: [],
    interests: [],
    skill_weights: {},
    career_goals: '',
    preferred_industries: [],
    work_environment_preference: 'office',
    salary_expectations: '',
    work_life_balance_priority: 5
  });

  const totalSteps = 5;
  const stepTitles = [
    t('assessment.personal_info'),
    t('assessment.cultural_context'),
    t('assessment.economic_geographic'),
    t('assessment.social_preferences'),
    t('assessment.skills_interests')
  ];

  const updateFormData = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setErrors([]);
  };

  const validateCurrentStep = (): boolean => {
    const newErrors: string[] = [];

    switch (currentStep) {
      case 1:
        if (!formData.age || formData.age < 13 || formData.age > 100) {
          newErrors.push(t('validation.age_required'));
        }
        if (!formData.education_level) {
          newErrors.push(t('validation.education_required'));
        }
        if (!formData.location) {
          newErrors.push(t('validation.location_required'));
        }
        break;
      case 2:
        if (!formData.cultural_context) {
          newErrors.push(t('validation.cultural_context_required'));
        }
        if (!formData.family_background) {
          newErrors.push(t('validation.family_background_required'));
        }
        break;
      case 3:
        if (!formData.economic_context) {
          newErrors.push(t('validation.economic_context_required'));
        }
        if (!formData.geographic_constraints) {
          newErrors.push(t('validation.geographic_constraints_required'));
        }
        break;
      case 4:
        if (!formData.family_expectations) {
          newErrors.push(t('validation.family_expectations_required'));
        }
        break;
      case 5:
        if (!formData.skills || formData.skills.length === 0) {
          newErrors.push(t('validation.skills_required'));
        }
        if (!formData.interests || formData.interests.length === 0) {
          newErrors.push(t('validation.interests_required'));
        }
        break;
    }

    setErrors(newErrors);
    return newErrors.length === 0;
  };

  const handleNext = () => {
    if (validateCurrentStep() && currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    if (!validateCurrentStep()) return;

    setLoading(true);
    try {
      console.log('Form submission started');
      console.log('Current user:', user);
      console.log('Form data to submit:', formData);
      
      // Create profile first
      await mareApi.createProfile(formData as MARERecommendationRequest);
      console.log('Profile created successfully');
      
      // Get enhanced recommendations (includes both standard and Groq-enhanced)
      const enhancedResponse = await fetch('/api/v1/mare/recommendations/enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      console.log('Enhanced API response status:', enhancedResponse.status);

      if (enhancedResponse.ok) {
        const enhancedData = await enhancedResponse.json();
        console.log('Enhanced data received:', enhancedData);
        
        // Navigate to enhanced results page
        navigate('/results', { 
          state: { 
            enhancedRecommendations: enhancedData,
            formData,
            source: 'MARE_ENHANCED'
          } 
        });
      } else {
        console.log('Enhanced API failed, falling back to standard recommendations');
        // Fallback to standard recommendations
        const recommendations = await mareApi.getRecommendations(formData as MARERecommendationRequest);
        
        console.log('Standard MARE recommendations received:', recommendations);
        console.log('Recommendations count:', recommendations?.length);
        console.log('First recommendation:', recommendations?.[0]);
        console.log('Navigation state being passed:', { 
          recommendations, 
          formData,
          source: 'MARE'
        });
        
        navigate('/results', { 
          state: { 
            recommendations, 
            formData,
            source: 'MARE'
          } 
        });
      }
      
    } catch (error) {
      console.error('Error getting MARE recommendations:', error);
      setErrors([t('error.recommendation_failed')]);
    } finally {
      setLoading(false);
    }
  };

  const addInterest = (interest: string) => {
    if (interest && !formData.interests?.includes(interest)) {
      updateFormData('interests', [...(formData.interests || []), interest]);
    }
  };

  const removeInterest = (interestToRemove: string) => {
    updateFormData('interests', formData.interests?.filter(interest => interest !== interestToRemove) || []);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {t('assessment.mare_title')}
          </h1>
          <p className="text-gray-600">
            {t('assessment.mare_subtitle')}
          </p>
        </div>

        {/* Progress indicator */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            {Array.from({ length: totalSteps }, (_, i) => i + 1).map(step => (
              <div key={step} className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold ${
                    step <= currentStep
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {step}
                </div>
                <div className="text-xs text-gray-600 mt-2 text-center max-w-20">
                  {stepTitles[step - 1]}
                </div>
              </div>
            ))}
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / totalSteps) * 100}%` }}
            />
          </div>
        </div>

        {/* Error display */}
        {errors.length > 0 && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <ul className="list-disc list-inside text-red-700">
              {errors.map((error, index) => (
                <li key={index}>{error}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Step content */}
        <div className="min-h-[500px]">
          {currentStep === 1 && (
            <PersonalInfoStep formData={formData} updateFormData={updateFormData} />
          )}
          {currentStep === 2 && (
            <CulturalContextStep formData={formData} updateFormData={updateFormData} />
          )}
          {currentStep === 3 && (
            <EconomicGeographicStep formData={formData} updateFormData={updateFormData} />
          )}
          {currentStep === 4 && (
            <SocialPreferencesStep formData={formData} updateFormData={updateFormData} />
          )}
          {currentStep === 5 && (
            <SkillsInterestsStep
              formData={formData}
              updateFormData={updateFormData}
              onAddInterest={addInterest}
              onRemoveInterest={removeInterest}
            />
          )}
        </div>

        {/* Navigation buttons */}
        <div className="flex justify-between mt-8 pt-6 border-t">
          <Button
            variant="outline"
            onClick={handlePrev}
            disabled={currentStep === 1}
          >
            {t('common.previous')}
          </Button>
          
          {currentStep === totalSteps ? (
            <Button
              onClick={handleSubmit}
              disabled={loading}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8"
            >
              {loading ? t('common.analyzing') : t('assessment.get_recommendations')}
            </Button>
          ) : (
            <Button
              onClick={handleNext}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              {t('common.next')}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

// Individual step components
const PersonalInfoStep: React.FC<{
  formData: FormData;
  updateFormData: (field: string, value: any) => void;
}> = ({ formData, updateFormData }) => {
  const { t } = useTranslation();

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        {t('assessment.personal_information')}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.age')} *
          </label>
          <input
            type="number"
            min="13"
            max="100"
            value={formData.age || ''}
            onChange={(e) => updateFormData('age', parseInt(e.target.value) || 0)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            placeholder={t('assessment.age_placeholder') || 'Enter your age'}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.education_level')} *
          </label>
          <select
            value={formData.education_level || ''}
            onChange={(e) => updateFormData('education_level', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">{t('assessment.select_education')}</option>
            <option value="below_10th">{t('education.below_10th')}</option>
            <option value="10th_pass">{t('education.10th_pass')}</option>
            <option value="12th_pass">{t('education.12th_pass')}</option>
            <option value="diploma">{t('education.diploma')}</option>
            <option value="bachelors">{t('education.bachelors')}</option>
            <option value="masters">{t('education.masters')}</option>
            <option value="phd">{t('education.phd')}</option>
            <option value="professional">{t('education.professional')}</option>
          </select>
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.location')} *
          </label>
          <input
            type="text"
            value={formData.location || ''}
            onChange={(e) => updateFormData('location', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            placeholder={t('assessment.location_placeholder') || 'Enter your location'}
          />
        </div>
      </div>
    </div>
  );
};

const CulturalContextStep: React.FC<{
  formData: FormData;
  updateFormData: (field: string, value: any) => void;
}> = ({ formData, updateFormData }) => {
  const { t } = useTranslation();

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        {t('assessment.cultural_social_context')}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.cultural_context')} *
          </label>
          <select
            value={formData.cultural_context || ''}
            onChange={(e) => updateFormData('cultural_context', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">{t('assessment.select_cultural_context')}</option>
            <option value="traditional">{t('cultural.traditional')}</option>
            <option value="conservative">{t('cultural.conservative')}</option>
            <option value="balanced">{t('cultural.balanced')}</option>
            <option value="modern">{t('cultural.modern')}</option>
            <option value="progressive">{t('cultural.progressive')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.family_background')} *
          </label>
          <select
            value={formData.family_background || ''}
            onChange={(e) => updateFormData('family_background', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">{t('assessment.select_family_background')}</option>
            <option value="business">{t('family.business')}</option>
            <option value="government">{t('family.government')}</option>
            <option value="farming">{t('family.farming')}</option>
            <option value="technical">{t('family.technical')}</option>
            <option value="education">{t('family.education')}</option>
            <option value="healthcare">{t('family.healthcare')}</option>
            <option value="middle_class">{t('family.middle_class')}</option>
            <option value="other">{t('family.other')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.preferred_language')}
          </label>
          <select
            value={formData.language_preference || 'en'}
            onChange={(e) => updateFormData('language_preference', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="en">{t('languages.english')}</option>
            <option value="hi">{t('languages.hindi')}</option>
            <option value="bn">{t('languages.bengali')}</option>
            <option value="te">{t('languages.telugu')}</option>
            <option value="mr">{t('languages.marathi')}</option>
            <option value="ta">{t('languages.tamil')}</option>
            <option value="gu">{t('languages.gujarati')}</option>
            <option value="kn">{t('languages.kannada')}</option>
            <option value="ml">{t('languages.malayalam')}</option>
            <option value="pa">{t('languages.punjabi')}</option>
            <option value="or">{t('languages.odia')}</option>
            <option value="as">{t('languages.assamese')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.community_values')}
          </label>
          <textarea
            value={formData.community_values || ''}
            onChange={(e) => updateFormData('community_values', e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            placeholder={t('assessment.community_values_placeholder') || 'Describe your community values'}
          />
        </div>
      </div>
    </div>
  );
};

const EconomicGeographicStep: React.FC<{
  formData: FormData;
  updateFormData: (field: string, value: any) => void;
}> = ({ formData, updateFormData }) => {
  const { t } = useTranslation();

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        {t('assessment.economic_geographic_factors')}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.economic_context')} *
          </label>
          <select
            value={formData.economic_context || ''}
            onChange={(e) => updateFormData('economic_context', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">{t('assessment.select_economic_context')}</option>
            <option value="low_income">{t('economic.low_income')}</option>
            <option value="lower_middle">{t('economic.lower_middle')}</option>
            <option value="middle_income">{t('economic.middle_income')}</option>
            <option value="upper_middle">{t('economic.upper_middle')}</option>
            <option value="high_income">{t('economic.high_income')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.urban_rural_type')}
          </label>
          <select
            value={formData.urban_rural_type || 'urban'}
            onChange={(e) => updateFormData('urban_rural_type', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="urban">{t('location.urban')}</option>
            <option value="semi_urban">{t('location.semi_urban')}</option>
            <option value="rural">{t('location.rural')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.infrastructure_level')}
          </label>
          <select
            value={formData.infrastructure_level || 'good'}
            onChange={(e) => updateFormData('infrastructure_level', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="poor">{t('infrastructure.poor')}</option>
            <option value="fair">{t('infrastructure.fair')}</option>
            <option value="good">{t('infrastructure.good')}</option>
            <option value="very_good">{t('infrastructure.very_good')}</option>
            <option value="excellent">{t('infrastructure.excellent')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.salary_expectations')}
          </label>
          <select
            value={formData.salary_expectations || ''}
            onChange={(e) => updateFormData('salary_expectations', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">{t('assessment.select_salary_range')}</option>
            <option value="below_3_lakh">{t('salary.below_3_lakh')}</option>
            <option value="3_to_5_lakh">{t('salary.3_to_5_lakh')}</option>
            <option value="5_to_8_lakh">{t('salary.5_to_8_lakh')}</option>
            <option value="8_to_12_lakh">{t('salary.8_to_12_lakh')}</option>
            <option value="12_to_20_lakh">{t('salary.12_to_20_lakh')}</option>
            <option value="above_20_lakh">{t('salary.above_20_lakh')}</option>
          </select>
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.geographic_constraints')} *
          </label>
          <textarea
            value={formData.geographic_constraints || ''}
            onChange={(e) => updateFormData('geographic_constraints', e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            placeholder={t('assessment.geographic_constraints_placeholder') || 'Enter geographic constraints'}
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.financial_constraints')}
          </label>
          <textarea
            value={formData.financial_constraints || ''}
            onChange={(e) => updateFormData('financial_constraints', e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            placeholder={t('assessment.financial_constraints_placeholder') || 'Enter financial constraints'}
          />
        </div>
      </div>
    </div>
  );
};

const SocialPreferencesStep: React.FC<{
  formData: FormData;
  updateFormData: (field: string, value: any) => void;
}> = ({ formData, updateFormData }) => {
  const { t } = useTranslation();

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        {t('assessment.social_career_preferences')}
      </h2>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.family_expectations')} *
          </label>
          <textarea
            value={formData.family_expectations || ''}
            onChange={(e) => updateFormData('family_expectations', e.target.value)}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            placeholder={t('assessment.family_expectations_placeholder') || 'Enter family expectations'}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.career_goals')}
          </label>
          <textarea
            value={formData.career_goals || ''}
            onChange={(e) => updateFormData('career_goals', e.target.value)}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            placeholder={t('assessment.career_goals_placeholder') || 'Enter your career goals'}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('assessment.work_environment')}
            </label>
            <select
              value={formData.work_environment_preference || 'office'}
              onChange={(e) => updateFormData('work_environment_preference', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="office">{t('work_env.office')}</option>
              <option value="remote">{t('work_env.remote')}</option>
              <option value="hybrid">{t('work_env.hybrid')}</option>
              <option value="field">{t('work_env.field')}</option>
              <option value="travel">{t('work_env.travel')}</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('assessment.work_life_balance')} ({formData.work_life_balance_priority || 5}/10)
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.work_life_balance_priority || 5}
              onChange={(e) => updateFormData('work_life_balance_priority', parseInt(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>{t('common.low')}</span>
              <span>{t('common.high')}</span>
            </div>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('assessment.peer_influence')} ({Math.round((formData.peer_influence_score || 0.5) * 100)}%)
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={formData.peer_influence_score || 0.5}
            onChange={(e) => updateFormData('peer_influence_score', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>{t('influence.independent')}</span>
            <span>{t('influence.influenced')}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const SkillsInterestsStep: React.FC<{
  formData: FormData;
  updateFormData: (field: string, value: any) => void;
  onAddInterest: (interest: string) => void;
  onRemoveInterest: (interest: string) => void;
}> = ({ 
  formData, 
  updateFormData, 
  onAddInterest,
  onRemoveInterest
}) => {
  const { t } = useTranslation();
  const [interestInput, setInterestInput] = useState('');

  const commonInterests = [
    'Technology', 'Sports', 'Arts', 'Music', 'Reading', 'Travel',
    'Cooking', 'Photography', 'Writing', 'Gaming', 'Fitness',
    'Movies', 'Nature', 'Science', 'History', 'Languages'
  ];

  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        {t('assessment.skills_interests')}
      </h2>

      {/* Skills Section */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-4">
          {t('assessment.skills')} *
        </label>
        <SkillSelector
          selectedSkills={formData.skills || []}
          onSkillsChange={(skills) => updateFormData('skills', skills)}
          maxSkills={15}
          showCategories={true}
          placeholder={t('assessment.skills_placeholder') || 'Search for skills...'}
        />
      </div>

      {/* Interests Section */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {t('assessment.interests')} *
        </label>
        <input
          type="text"
          value={interestInput}
          onChange={(e) => setInterestInput(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          placeholder={t('assessment.interests_placeholder') || 'Enter your interests'}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && interestInput.trim()) {
              onAddInterest(interestInput.trim());
              setInterestInput('');
              e.preventDefault();
            }
          }}
        />

        {/* Common interests buttons */}
        <div className="mt-3 mb-4">
          <p className="text-sm text-gray-600 mb-2">{t('assessment.common_interests')}</p>
          <div className="flex flex-wrap gap-2">
            {commonInterests.map((interest) => (
              <button
                key={interest}
                type="button"
                onClick={() => onAddInterest(interest)}
                className="px-3 py-1 text-sm border border-gray-300 rounded-full hover:bg-gray-100 focus:bg-gray-100"
                disabled={formData.interests?.includes(interest)}
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        {/* Selected interests */}
        <div className="flex flex-wrap gap-2">
          {formData.interests?.map((interest, index) => (
            <span
              key={index}
              className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800"
            >
              {interest}
              <button
                type="button"
                onClick={() => onRemoveInterest(interest)}
                className="ml-2 text-green-600 hover:text-green-800"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Preferred Industries */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {t('assessment.preferred_industries')}
        </label>
        <select
          multiple
          value={formData.preferred_industries || []}
          onChange={(e) => {
            const selectedOptions = Array.from(e.target.selectedOptions, option => option.value);
            updateFormData('preferred_industries', selectedOptions);
          }}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          size={6}
        >
          <option value="Technology">{t('industries.technology')}</option>
          <option value="Healthcare">{t('industries.healthcare')}</option>
          <option value="Education">{t('industries.education')}</option>
          <option value="Finance">{t('industries.finance')}</option>
          <option value="Manufacturing">{t('industries.manufacturing')}</option>
          <option value="Agriculture">{t('industries.agriculture')}</option>
          <option value="Government">{t('industries.government')}</option>
          <option value="Non-Profit">{t('industries.non_profit')}</option>
          <option value="Media">{t('industries.media')}</option>
          <option value="Retail">{t('industries.retail')}</option>
          <option value="Transportation">{t('industries.transportation')}</option>
          <option value="Construction">{t('industries.construction')}</option>
        </select>
        <p className="text-xs text-gray-500 mt-1">{t('assessment.hold_ctrl_select')}</p>
      </div>
    </div>
  );
};

export default MAREAssessmentForm;
