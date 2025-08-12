import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  SKILL_CATEGORIES, 
  ALL_SKILLS, 
  searchSkills, 
  getCareerKeywordsForSkill 
} from '../config/skills';

interface SkillSelectorProps {
  selectedSkills: string[];
  onSkillsChange: (skills: string[]) => void;
  maxSkills?: number;
  showCategories?: boolean;
  placeholder?: string;
}

const SkillSelector: React.FC<SkillSelectorProps> = ({
  selectedSkills,
  onSkillsChange,
  maxSkills = 20,
  showCategories = true,
  placeholder
}) => {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Filter skills based on search term and category
  const getFilteredSkills = () => {
    let skills = ALL_SKILLS;
    
    if (activeCategory !== 'all') {
      const category = SKILL_CATEGORIES.find(cat => cat.id === activeCategory);
      skills = category ? category.skills : [];
    }
    
    if (searchTerm) {
      skills = skills.filter(skill => 
        skill.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    // Remove already selected skills
    return skills.filter(skill => !selectedSkills.includes(skill));
  };

  // Handle search input change
  const handleSearchChange = (value: string) => {
    setSearchTerm(value);
    if (value.length > 0) {
      const filtered = searchSkills(value).slice(0, 10);
      setSuggestions(filtered.filter(skill => !selectedSkills.includes(skill)));
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  // Add skill
  const addSkill = (skill: string) => {
    if (!selectedSkills.includes(skill) && selectedSkills.length < maxSkills) {
      onSkillsChange([...selectedSkills, skill]);
      setSearchTerm('');
      setShowSuggestions(false);
    }
  };

  // Remove skill
  const removeSkill = (skill: string) => {
    onSkillsChange(selectedSkills.filter(s => s !== skill));
  };

  // Get skill priority level for styling
  const getSkillPriority = (skill: string): 'high' | 'medium' | 'low' => {
    const keywords = getCareerKeywordsForSkill(skill);
    if (keywords.length > 5) return 'high';
    if (keywords.length > 2) return 'medium';
    return 'low';
  };

  // Get skill color based on priority
  const getSkillColor = (priority: 'high' | 'medium' | 'low') => {
    switch (priority) {
      case 'high': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'medium': return 'bg-green-100 text-green-800 border-green-200';
      case 'low': return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const filteredSkills = getFilteredSkills();

  return (
    <div className="space-y-4">
      {/* Search Input */}
      <div className="relative">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => handleSearchChange(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && searchTerm.trim()) {
              addSkill(searchTerm.trim());
              e.preventDefault();
            }
          }}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder={placeholder || (t('assessment.search_skills_placeholder') || 'Search for skills...')}
        />
        
        {/* Search Suggestions */}
        {showSuggestions && suggestions.length > 0 && (
          <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-48 overflow-y-auto">
            {suggestions.map((skill, index) => (
              <button
                key={index}
                type="button"
                onClick={() => addSkill(skill)}
                className="w-full px-4 py-2 text-left hover:bg-gray-100 focus:bg-gray-100 first:rounded-t-lg last:rounded-b-lg"
              >
                <span className="font-medium">{skill}</span>
                <div className="text-xs text-gray-500 mt-1">
                  Career matches: {getCareerKeywordsForSkill(skill).length} categories
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Category Tabs */}
      {showCategories && (
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setActiveCategory('all')}
            className={`px-3 py-1 text-sm rounded-full border transition-colors ${
              activeCategory === 'all'
                ? 'bg-blue-500 text-white border-blue-500'
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            }`}
          >
            All Skills
          </button>
          {SKILL_CATEGORIES.map((category) => (
            <button
              key={category.id}
              type="button"
              onClick={() => setActiveCategory(category.id)}
              className={`px-3 py-1 text-sm rounded-full border transition-colors ${
                activeCategory === category.id
                  ? 'bg-blue-500 text-white border-blue-500'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>
      )}

      {/* Selected Skills */}
      {selectedSkills.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-medium text-gray-700">
              Selected Skills ({selectedSkills.length}/{maxSkills})
            </h4>
            <button
              type="button"
              onClick={() => onSkillsChange([])}
              className="text-xs text-red-600 hover:text-red-800"
            >
              Clear All
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {selectedSkills.map((skill, index) => {
              const priority = getSkillPriority(skill);
              const colorClass = getSkillColor(priority);
              return (
                <span
                  key={index}
                  className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${colorClass}`}
                >
                  {skill}
                  <button
                    type="button"
                    onClick={() => removeSkill(skill)}
                    className="ml-2 text-current hover:text-red-600 focus:text-red-600"
                  >
                    ×
                  </button>
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* Quick Add Skills */}
      {filteredSkills.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            {activeCategory === 'all' 
              ? 'Popular Skills' 
              : SKILL_CATEGORIES.find(cat => cat.id === activeCategory)?.name || 'Skills'
            }
          </h4>
          <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
            {filteredSkills.slice(0, 20).map((skill) => {
              const priority = getSkillPriority(skill);
              return (
                <button
                  key={skill}
                  type="button"
                  onClick={() => addSkill(skill)}
                  disabled={selectedSkills.length >= maxSkills}
                  className={`px-3 py-1 text-sm border rounded-full transition-colors ${
                    selectedSkills.length >= maxSkills
                      ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 hover:border-gray-400'
                  }`}
                >
                  {skill}
                  {priority === 'high' && (
                    <span className="ml-1 text-xs text-blue-600">⭐</span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Skill Selection Tips */}
      <div className="text-xs text-gray-500 space-y-1">
        <div>💡 Tip: Skills marked with ⭐ match more career opportunities</div>
        <div>🎯 Select 5-10 skills for best matching results</div>
        <div>🔍 Use search to find specific skills or add custom ones</div>
      </div>
    </div>
  );
};

export default SkillSelector;
