// src/components/common/BaseLayout.js
import React from 'react';
import Navbar from './Navbar';

const BaseLayout = ({ children, className = '' }) => {
  return (
    <div className='min-h-screen bg-gray-100'>
      <Navbar />
      <main
        className={`container mx-auto min-h-[calc(100vh-4rem)] px-4 py-6 sm:px-6 lg:px-8 ${className}`}
      >
        {children}
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
