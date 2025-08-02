import React from 'react';
import { useTranslation } from 'react-i18next';
import { CareerMatch } from '../services/api';

interface ResultCardProps {
  match: CareerMatch;
}

const ResultCard: React.FC<ResultCardProps> = ({ match }) => {
  const { t } = useTranslation();

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-700 bg-green-100 border-green-200';
    if (score >= 0.6) return 'text-yellow-700 bg-yellow-100 border-yellow-200';
    return 'text-red-700 bg-red-100 border-red-200';
  };

  const getDemandColor = (demand: string) => {
    if (demand === 'High') return 'text-emerald-700 bg-emerald-100 border-emerald-200';
    if (demand === 'Medium') return 'text-amber-700 bg-amber-100 border-amber-200';
    return 'text-rose-700 bg-rose-100 border-rose-200';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 0.8) return '🎯';
    if (score >= 0.6) return '✨';
    return '💡';
  };

  const getDemandIcon = (demand: string) => {
    if (demand === 'High') return '🔥';
    if (demand === 'Medium') return '📈';
    return '📊';
  };

  return (
    <div className="p-6">
      <div className="flex flex-col md:flex-row md:items-start justify-between mb-6">
        <div className="flex-1 mb-4 md:mb-0">
          <h3 className="text-2xl font-bold text-gray-900 mb-2 flex items-center">
            {getScoreIcon(match.score)}
            <span className="ml-2">{match.career}</span>
          </h3>
          <p className="text-gray-600 leading-relaxed text-lg">
            {match.description}
          </p>
        </div>
        
        <div className="flex flex-col space-y-3 md:ml-6">
          <div className={`px-4 py-2 rounded-xl text-sm font-semibold border ${getScoreColor(match.score)} inline-flex items-center`}>
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            {(match.score * 100).toFixed(0)}% Match
          </div>
          
          <div className={`px-4 py-2 rounded-xl text-sm font-semibold border ${getDemandColor(match.local_demand)} inline-flex items-center`}>
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            {getDemandIcon(match.local_demand)} {match.local_demand} Demand
          </div>
        </div>
      </div>

      {/* Additional career insights */}
      <div className="border-t border-gray-100 pt-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-primary-50 rounded-lg p-4 text-center">
            <div className="text-2xl mb-2">💼</div>
            <div className="text-sm font-semibold text-primary-700">Growth Potential</div>
            <div className="text-lg font-bold text-primary-800">
              {match.score >= 0.8 ? 'Excellent' : match.score >= 0.6 ? 'Good' : 'Moderate'}
            </div>
          </div>
          
          <div className="bg-secondary-50 rounded-lg p-4 text-center">
            <div className="text-2xl mb-2">📍</div>
            <div className="text-sm font-semibold text-secondary-700">Local Market</div>
            <div className="text-lg font-bold text-secondary-800">{match.local_demand}</div>
          </div>
          
          <div className="bg-accent-50 rounded-lg p-4 text-center">
            <div className="text-2xl mb-2">🎓</div>
            <div className="text-sm font-semibold text-accent-700">Match Level</div>
            <div className="text-lg font-bold text-accent-800">
              {match.score >= 0.8 ? 'Perfect' : match.score >= 0.6 ? 'Great' : 'Good'}
            </div>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="border-t border-gray-100 pt-6 mt-6">
        <div className="flex flex-wrap gap-3">
          <button className="btn-primary flex items-center space-x-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Learn More</span>
          </button>
          
          <button className="btn-secondary flex items-center space-x-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span>Find Courses</span>
          </button>
          
          <button className="btn-secondary flex items-center space-x-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>Connect</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
