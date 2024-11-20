// src/components/common/index.js
import React from 'react';
import { AlertCircle, Loader2 } from 'lucide-react';

export const ErrorMessage = ({ 
  message, 
  variant = 'error',
  action,
  className = '' 
}) => {
  const styles = {
    error: 'bg-red-50 text-red-700 border-red-200',
    warning: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    info: 'bg-blue-50 text-blue-700 border-blue-200',
  };

  return (
    <div className={`rounded-lg border p-4 ${styles[variant]} ${className}`}>
      <div className="flex items-center gap-3">
        <AlertCircle className="h-5 w-5" />
        <div className="flex-1">{message}</div>
        {action && (
          <button 
            onClick={action.onClick}
            className="rounded bg-white px-3 py-1 text-sm font-medium shadow-sm hover:bg-gray-50"
          >
            {action.label}
          </button>
        )}
      </div>
    </div>
  );
};

export const LoadingSpinner = ({ 
  fullScreen = false,
  message = 'Loading...',
  className = '' 
}) => {
  const containerStyles = fullScreen 
    ? 'fixed inset-0 bg-white/80 backdrop-blur-sm' 
    : 'w-full';

  return (
    <div className={`flex items-center justify-center p-8 ${containerStyles} ${className}`}>
      <div className="flex flex-col items-center gap-2">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        <p className="text-sm text-gray-500">{message}</p>
      </div>
    </div>
  );
};

export const EmptyState = ({
  title,
  message,
  icon: Icon,
  action,
  className = ''
}) => (
  <div className={`flex flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 bg-white p-8 ${className}`}>
    {Icon && <Icon className="mb-3 h-12 w-12 text-gray-400" />}
    <h3 className="mb-1 text-lg font-medium">{title}</h3>
    <p className="mb-4 text-sm text-gray-500">{message}</p>
    {action && (
      <button
        onClick={action.onClick}
        className="rounded-full bg-blue-500 px-4 py-2 text-sm font-medium text-white hover:bg-blue-600"
      >
        {action.label}
      </button>
    )}
  </div>
);