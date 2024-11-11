import React from 'react';

const BaseLayout = ({ children }) => {
  return (
    <div className='flex min-h-screen bg-gray-100'>
      <div className='mx-auto w-full max-w-6xl p-6'>{children}</div>
    </div>
  );
};

export default BaseLayout;
