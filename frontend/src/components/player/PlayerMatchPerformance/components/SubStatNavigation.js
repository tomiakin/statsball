import React from 'react';
import { statCategories } from '../config/statConfig';

export const SubStatNavigation = ({ selectedStat, selectedSubStat, onSubStatChange }) => {
  const subStats = statCategories.find(cat => cat.id === selectedStat)?.subStats || [];
  
  return (
    <div className='mb-4 flex space-x-4 overflow-x-auto'>
      {subStats.map(subStat => (
        <button
          key={subStat.id}
          className={`whitespace-nowrap rounded-md px-4 py-2 ${
            selectedSubStat === subStat.id
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
          onClick={() => onSubStatChange(subStat.id)}
        >
          {subStat.name}
        </button>
      ))}
    </div>
  );
};