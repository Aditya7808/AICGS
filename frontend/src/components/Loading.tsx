import React from 'react';

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
}

const Loading: React.FC<LoadingProps> = ({ size = 'md', text = 'Loading...' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  return (
    <div className="flex items-center justify-center space-x-2">
      <div className={`${sizeClasses[size]} animate-spin`}>
        <div className="w-full h-full border-2 border-primary-200 border-t-primary-600 rounded-full"></div>
      </div>
      {text && <span className="text-gray-600 text-sm">{text}</span>}
    </div>
  );
};

export default Loading;
