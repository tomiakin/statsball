import React from 'react';

const LoadingSpinner = ({ fullScreen = false }) => {
  const baseClasses = 'flex items-center justify-center';
  const containerClasses = fullScreen ? `${baseClasses} h-screen` : baseClasses;

  return (
    <div className={containerClasses} role='status'>
      <div
        className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent'
        aria-label='Loading'
      />
      <span className='sr-only'>Loading...</span>
    </div>
  );
};

export default LoadingSpinner;
