// BaseLayout.js
import React from 'react';
import Navbar from './Navbar';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage'; // Changed from import { ErrorMessage }

// Add prop types documentation
const BaseLayout = ({
  children,
  loading = false,
  error = null,
  fullWidth = false,
  className = '',
}) => {
  // Move this to a component to avoid repetition , dark --- dark:bg-gray-900"
  const containerClass = 'min-h-screen bg-gray-100';

  if (loading) {
    return (
      <div className={containerClass}>
        <Navbar />
        <div className='mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8'>
          <LoadingSpinner fullScreen={false} />
        </div>
        {/* Add footer here too for consistency */}
      </div>
    );
  }

  return (
    <div className={containerClass}>
      <Navbar />
      <main
        className={`min-h-[calc(100vh-4rem)] ${fullWidth ? '' : 'container mx-auto'} px-4 py-6 sm:px-6 lg:px-8`}
      >
        {error && <ErrorMessage message={error} />}
        <div className={className}>{children}</div>
      </main>
      <footer className='mt-auto border-t border-gray-200 bg-white py-4 dark:border-gray-800 dark:bg-gray-800'>
        <div className='container mx-auto px-4 text-center text-sm text-gray-600 dark:text-gray-400'>
          © {new Date().getFullYear()} Statsball. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default BaseLayout;
