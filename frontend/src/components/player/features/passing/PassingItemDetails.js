import React from 'react';

export const PassingItemDetails = ({ selectedItem }) => {
  if (!selectedItem) {
    return (
      <div className='text-center text-gray-500'>
        Select a pass to see details
      </div>
    );
  }

  return (
    <div className='grid grid-cols-3 gap-4'>
      <div>
        <p className='text-xs text-gray-500'>Pass Type</p>
        <p className='text-sm font-bold'>{selectedItem.pass_type}</p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Length</p>
        <p className='text-sm font-bold'>
          {selectedItem.pass_length?.toFixed(1)}m
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Outcome</p>
        <p className='text-sm font-bold'>
          {selectedItem.pass_outcome || 'Complete'}
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Height</p>
        <p className='text-sm font-bold'>
          {selectedItem.pass_height || 'Ground'}
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Progressive</p>
        <p className='text-sm font-bold'>
          {selectedItem.progressive ? 'Yes' : 'No'}
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Assist</p>
        <p className='text-sm font-bold'>
          {selectedItem.assist ? 'Yes' : 'No'}
        </p>
      </div>
    </div>
  );
};
