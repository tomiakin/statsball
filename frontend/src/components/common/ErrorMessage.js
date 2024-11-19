// ErrorMessage.js
import React from 'react';

const ErrorMessage = ({ message }) => {
  if (!message) return null;
  
  return (
    <div className="mb-6 rounded-lg border border-red-400 bg-red-100 px-4 py-3 text-center text-red-700" role="alert">
      {message}
    </div>
  );
};

export default ErrorMessage;