import React, { useState } from 'react';
import { X } from 'lucide-react';
import { progressAPI } from '../services/api';

interface SkillProgressModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  skill?: {
    id: number;
    skill_name: string;
    current_level: string;
    proficiency_score: number;
    target_level: string;
  };
}

const SkillProgressModal: React.FC<SkillProgressModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  skill
}) => {
  const [formData, setFormData] = useState({
    skill_name: skill?.skill_name || '',
    current_level: skill?.current_level || 'beginner',
    proficiency_score: skill?.proficiency_score || 0,
    target_level: skill?.target_level || 'intermediate',
    time_invested_hours: 0
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const skillLevels = ['beginner', 'intermediate', 'advanced', 'expert'];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await progressAPI.updateSkillProgress({
        skill_name: formData.skill_name,
        current_level: formData.current_level,
        proficiency_score: formData.proficiency_score / 100, // Convert percentage to decimal
        target_level: formData.target_level,
        time_invested_hours: formData.time_invested_hours
      });

      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update skill progress');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            {skill ? 'Update Skill Progress' : 'Add New Skill'}
          </h3>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Skill Name
            </label>
            <input
              type="text"
              required
              value={formData.skill_name}
              onChange={(e) => setFormData({ ...formData, skill_name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="e.g., Python Programming, Data Analysis"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Level
              </label>
              <select
                value={formData.current_level}
                onChange={(e) => setFormData({ ...formData, current_level: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                {skillLevels.map(level => (
                  <option key={level} value={level}>
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Level
              </label>
              <select
                value={formData.target_level}
                onChange={(e) => setFormData({ ...formData, target_level: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                {skillLevels.map(level => (
                  <option key={level} value={level}>
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Proficiency Score ({formData.proficiency_score}%)
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={formData.proficiency_score}
              onChange={(e) => setFormData({ ...formData, proficiency_score: parseInt(e.target.value) })}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Time Invested (hours)
            </label>
            <input
              type="number"
              min="0"
              step="0.5"
              value={formData.time_invested_hours}
              onChange={(e) => setFormData({ ...formData, time_invested_hours: parseFloat(e.target.value) || 0 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Hours spent learning this skill"
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : (skill ? 'Update Skill' : 'Add Skill')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SkillProgressModal;
