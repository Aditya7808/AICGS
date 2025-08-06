import React, { useState, useEffect } from 'react';
import { X, Target, Plus, Trash2, ExternalLink } from 'lucide-react';
import { progressAPI } from '../services/api';

interface CareerGoalModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  goal?: {
    id: number;
    career_id: number;
    goal_type: string;
    target_timeline: string;
    priority_level: number;
    status: string;
    progress_percentage: number;
    next_action?: string;
    links?: Array<{
      title: string;
      url: string;
      type: string;
    }>;
  };
}

interface GoalLink {
  title: string;
  url: string;
  type: string;
}

const CareerGoalModal: React.FC<CareerGoalModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  goal
}) => {
  const [isUpdateMode, setIsUpdateMode] = useState(!!goal);
  const [formData, setFormData] = useState({
    career_id: goal?.career_id || 1,
    goal_type: goal?.goal_type || 'primary',
    target_timeline: goal?.target_timeline || '1_year',
    priority_level: goal?.priority_level || 1,
    progress_percentage: goal?.progress_percentage || 0,
    next_action: goal?.next_action || ''
  });
  const [links, setLinks] = useState<GoalLink[]>(goal?.links || []);
  const [newLink, setNewLink] = useState<GoalLink>({
    title: '',
    url: '',
    type: 'resource'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const goalTypes = [
    { value: 'primary', label: 'Primary Goal' },
    { value: 'secondary', label: 'Secondary Goal' },
    { value: 'exploratory', label: 'Exploratory Goal' }
  ];

  const timelines = [
    { value: '6_months', label: '6 Months' },
    { value: '1_year', label: '1 Year' },
    { value: '2_years', label: '2 Years' },
    { value: '5_years', label: '5 Years' }
  ];

  const linkTypes = [
    { value: 'resource', label: 'Resource' },
    { value: 'course', label: 'Course' },
    { value: 'article', label: 'Article' },
    { value: 'tool', label: 'Tool' },
    { value: 'other', label: 'Other' }
  ];

  const priorities = [1, 2, 3, 4, 5];

  useEffect(() => {
    if (goal) {
      setIsUpdateMode(true);
      setFormData({
        career_id: goal.career_id,
        goal_type: goal.goal_type,
        target_timeline: goal.target_timeline,
        priority_level: goal.priority_level,
        progress_percentage: goal.progress_percentage,
        next_action: goal.next_action || ''
      });
      setLinks(goal.links || []);
    } else {
      setIsUpdateMode(false);
      setLinks([]);
    }
  }, [goal]);

  const addLink = () => {
    if (newLink.title.trim() && newLink.url.trim()) {
      setLinks([...links, { ...newLink }]);
      setNewLink({ title: '', url: '', type: 'resource' });
    }
  };

  const removeLink = (index: number) => {
    setLinks(links.filter((_, i) => i !== index));
  };

  const isValidUrl = (url: string) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isUpdateMode && goal) {
        // Update existing goal
        await progressAPI.updateCareerGoal(goal.id, {
          progress_percentage: formData.progress_percentage,
          next_action: formData.next_action,
          links: links
        });
      } else {
        // Create new goal
        await progressAPI.createCareerGoal({
          career_id: formData.career_id,
          goal_type: formData.goal_type,
          target_timeline: formData.target_timeline,
          priority_level: formData.priority_level,
          links: links
        });
      }

      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save career goal');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Target className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              {isUpdateMode ? 'Update Career Goal' : 'Add New Career Goal'}
            </h3>
          </div>
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

          {!isUpdateMode && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Career ID
                </label>
                <input
                  type="number"
                  required
                  min="1"
                  value={formData.career_id}
                  onChange={(e) => setFormData({ ...formData, career_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Enter career ID"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Refer to the career recommendations or results page for the career ID
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Goal Type
                </label>
                <select
                  value={formData.goal_type}
                  onChange={(e) => setFormData({ ...formData, goal_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  {goalTypes.map(type => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Timeline
                  </label>
                  <select
                    value={formData.target_timeline}
                    onChange={(e) => setFormData({ ...formData, target_timeline: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    {timelines.map(timeline => (
                      <option key={timeline.value} value={timeline.value}>
                        {timeline.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Priority (1=High)
                  </label>
                  <select
                    value={formData.priority_level}
                    onChange={(e) => setFormData({ ...formData, priority_level: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    {priorities.map(priority => (
                      <option key={priority} value={priority}>
                        {priority} {priority === 1 ? '(Highest)' : priority === 5 ? '(Lowest)' : ''}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </>
          )}

          {isUpdateMode && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Progress ({formData.progress_percentage}%)
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={formData.progress_percentage}
                onChange={(e) => setFormData({ ...formData, progress_percentage: parseInt(e.target.value) })}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
              </div>
            </div>
          )}

          {/* Links Section */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Helpful Links
            </label>
            
            {/* Existing Links */}
            {links.length > 0 && (
              <div className="space-y-2 mb-3">
                {links.map((link, index) => (
                  <div key={index} className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                    <ExternalLink className="w-4 h-4 text-gray-400 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-sm text-gray-900 truncate">
                          {link.title}
                        </span>
                        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                          {link.type}
                        </span>
                      </div>
                      <a
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-blue-600 hover:text-blue-800 truncate block"
                      >
                        {link.url}
                      </a>
                    </div>
                    <button
                      type="button"
                      onClick={() => removeLink(index)}
                      className="p-1 text-red-400 hover:text-red-600 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Add New Link */}
            <div className="border border-gray-200 rounded-lg p-3 space-y-3">
              <div className="grid grid-cols-1 gap-3">
                <div>
                  <input
                    type="text"
                    value={newLink.title}
                    onChange={(e) => setNewLink({ ...newLink, title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                    placeholder="Link title (e.g., 'Python Course', 'Industry Article')"
                  />
                </div>
                <div>
                  <input
                    type="url"
                    value={newLink.url}
                    onChange={(e) => setNewLink({ ...newLink, url: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                    placeholder="https://example.com"
                  />
                </div>
                <div className="flex gap-2">
                  <select
                    value={newLink.type}
                    onChange={(e) => setNewLink({ ...newLink, type: e.target.value })}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                  >
                    {linkTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                  <button
                    type="button"
                    onClick={addLink}
                    disabled={!newLink.title.trim() || !newLink.url.trim() || !isValidUrl(newLink.url)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                  >
                    <Plus className="w-4 h-4" />
                    Add
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Next Action
            </label>
            <textarea
              value={formData.next_action}
              onChange={(e) => setFormData({ ...formData, next_action: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={3}
              placeholder="What's your next step towards this goal?"
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
              {loading ? 'Saving...' : (isUpdateMode ? 'Update Goal' : 'Add Goal')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CareerGoalModal;
