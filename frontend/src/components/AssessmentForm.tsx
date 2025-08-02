import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { recommendationAPI, RecommendationRequest } from '../services/api';

const skillOptions = [
  'Programming', 'Web Development', 'Data Analysis', 'Design', 'Writing', 
  'Communication', 'Leadership', 'Problem Solving', 'Analytics', 'Marketing',
  'Teaching', 'Research', 'Project Management', 'Public Speaking', 'Creativity',
  'Mathematics', 'Science', 'Art', 'Music', 'Sports'
];

const interestOptions = [
  'Technology', 'Artificial Intelligence', 'Web Development', 'Mobile Apps',
  'Data Science', 'Cybersecurity', 'Art & Design', 'Writing & Content',
  'Business & Entrepreneurship', 'Healthcare', 'Education', 'Environment',
  'Finance', 'Marketing', 'Photography', 'Gaming', 'Travel', 'Fashion',
  'Food & Culinary', 'Sports & Fitness'
];

interface AssessmentFormProps {
  onResults: (results: any) => void;
}

const AssessmentForm: React.FC<AssessmentFormProps> = ({ onResults }) => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    age: '',
    location: '',
    skills: [] as string[],
    interests: [] as string[]
  });
  
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);
  const totalSteps = 3;

  const handleSkillToggle = (skill: string) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }));
  };

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const request: RecommendationRequest = {
        age: parseInt(formData.age),
        location: formData.location,
        skills: formData.skills,
        interests: formData.interests,
        language: i18n.language
      };
      
      const results = await recommendationAPI.getRecommendations(request);
      onResults(results);
      navigate('/results');
    } catch (error) {
      console.error('Error getting recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    if (step < totalSteps) setStep(step + 1);
  };

  const prevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  const isStepValid = () => {
    switch (step) {
      case 1:
        return formData.age && formData.location;
      case 2:
        return formData.skills.length > 0;
      case 3:
        return formData.interests.length > 0;
      default:
        return false;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Career <span className="gradient-text">Assessment</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Discover your perfect career path through our comprehensive AI-powered assessment
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-12">
          <div className="flex justify-center items-center space-x-4 mb-4">
            {[1, 2, 3].map((stepNum) => (
              <React.Fragment key={stepNum}>
                <div className={`
                  w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg transition-all duration-300
                  ${step >= stepNum 
                    ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg transform scale-110' 
                    : step === stepNum 
                      ? 'bg-white border-2 border-primary-500 text-primary-500 animate-pulse-glow'
                      : 'bg-gray-200 text-gray-500'
                  }
                `}>
                  {step > stepNum ? (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    stepNum
                  )}
                </div>
                {stepNum < totalSteps && (
                  <div className={`w-16 h-1 rounded transition-all duration-300 ${
                    step > stepNum ? 'bg-primary-500' : 'bg-gray-200'
                  }`} />
                )}
              </React.Fragment>
            ))}
          </div>
          <div className="text-center">
            <span className="text-sm font-medium text-gray-500">
              Step {step} of {totalSteps}
            </span>
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
          <form onSubmit={handleSubmit}>
            {/* Step 1: Personal Information */}
            {step === 1 && (
              <div className="p-8 md:p-12 animate-fade-in">
                <div className="text-center mb-8">
                  <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    Personal Information
                  </h3>
                  <p className="text-gray-600">
                    Tell us a bit about yourself to get started
                  </p>
                </div>
                
                <div className="space-y-6 max-w-lg mx-auto">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      What's your age?
                    </label>
                    <input
                      type="number"
                      value={formData.age}
                      onChange={(e) => setFormData(prev => ({ ...prev, age: e.target.value }))}
                      className="input-field text-lg"
                      required
                      min="13"
                      max="100"
                      placeholder="Enter your age"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Where are you located?
                    </label>
                    <input
                      type="text"
                      value={formData.location}
                      onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
                      className="input-field text-lg"
                      required
                      placeholder="e.g., Mumbai, Delhi, Bangalore"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Skills */}
            {step === 2 && (
              <div className="p-8 md:p-12 animate-fade-in">
                <div className="text-center mb-8">
                  <div className="w-16 h-16 bg-gradient-to-r from-secondary-500 to-accent-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    Your Skills
                  </h3>
                  <p className="text-gray-600">
                    Select the skills you possess or would like to develop
                  </p>
                </div>
                
                <div className="max-w-4xl mx-auto">
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {skillOptions.map(skill => (
                      <button
                        key={skill}
                        type="button"
                        onClick={() => handleSkillToggle(skill)}
                        className={`
                          px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 transform hover:scale-105
                          ${formData.skills.includes(skill)
                            ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg'
                            : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'
                          }
                        `}
                      >
                        {skill}
                      </button>
                    ))}
                  </div>
                  <div className="text-center mt-6">
                    <p className="text-sm text-gray-500">
                      Selected: {formData.skills.length} skills
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Interests */}
            {step === 3 && (
              <div className="p-8 md:p-12 animate-fade-in">
                <div className="text-center mb-8">
                  <div className="w-16 h-16 bg-gradient-to-r from-accent-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    Your Interests
                  </h3>
                  <p className="text-gray-600">
                    What topics and fields genuinely interest you?
                  </p>
                </div>
                
                <div className="max-w-4xl mx-auto">
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {interestOptions.map(interest => (
                      <button
                        key={interest}
                        type="button"
                        onClick={() => handleInterestToggle(interest)}
                        className={`
                          px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 transform hover:scale-105
                          ${formData.interests.includes(interest)
                            ? 'bg-gradient-to-r from-secondary-500 to-secondary-600 text-white shadow-lg'
                            : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'
                          }
                        `}
                      >
                        {interest}
                      </button>
                    ))}
                  </div>
                  <div className="text-center mt-6">
                    <p className="text-sm text-gray-500">
                      Selected: {formData.interests.length} interests
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Navigation */}
            <div className="bg-gray-50 px-8 md:px-12 py-6 flex justify-between items-center">
              <button
                type="button"
                onClick={prevStep}
                disabled={step === 1}
                className={`
                  flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all duration-200
                  ${step === 1 
                    ? 'text-gray-400 cursor-not-allowed' 
                    : 'text-gray-700 hover:bg-gray-200'
                  }
                `}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>Previous</span>
              </button>

              {step < totalSteps ? (
                <button
                  type="button"
                  onClick={nextStep}
                  disabled={!isStepValid()}
                  className={`
                    flex items-center space-x-2 px-8 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:-translate-y-0.5
                    ${isStepValid()
                      ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-lg hover:shadow-xl'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }
                  `}
                >
                  <span>Continue</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={loading || !isStepValid()}
                  className={`
                    flex items-center space-x-2 px-8 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:-translate-y-0.5
                    ${!loading && isStepValid()
                      ? 'bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg hover:shadow-xl'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }
                  `}
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <span>Processing...</span>
                    </>
                  ) : (
                    <>
                      <span>Get My Results</span>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </>
                  )}
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AssessmentForm;
