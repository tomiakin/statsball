import React from 'react';
import { statCategories } from '../config/statConfig';

export const StatNavigation = ({ selectedStat, onStatChange }) => (
  <div className='col-span-12 flex items-center rounded-lg bg-white px-6 py-4 shadow-lg lg:col-span-9'>
    <div className='flex space-x-4 overflow-x-auto'>
      {statCategories.map(category => (
        <button
          key={category.id}
          className={`whitespace-nowrap rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
            selectedStat === category.id
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => onStatChange(category)}
        >
          {category.name}
        </button>
      ))}
    </div>
  </div>
);