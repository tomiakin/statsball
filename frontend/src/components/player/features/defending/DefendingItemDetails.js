import React from 'react';

export const DefendingItemDetails = ({ selectedItem }) => {
  if (!selectedItem) {
    return (
      <div className='text-center text-gray-500'>
        Select a defensive action to see details
      </div>
    );
  }

  return (
    <div className='grid grid-cols-3 gap-4'>
      <div>
        <p className='text-xs text-gray-500'>Action Type</p>
        <p className='text-sm font-bold'>{selectedItem.type}</p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Outcome</p>
        <p className='text-sm font-bold'>
          {selectedItem.outcome || 'Successful'}
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Pressure Duration</p>
        <p className='text-sm font-bold'>
          {selectedItem.pressure_duration
            ? `${selectedItem.pressure_duration}s`
            : 'N/A'}
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Duel Type</p>
        <p className='text-sm font-bold'>{selectedItem.duel_type || 'N/A'}</p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Recovery Type</p>
        <p className='text-sm font-bold'>
          {selectedItem.recovery_type || 'N/A'}
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Pressure Regain</p>
        <p className='text-sm font-bold'>
          {selectedItem.pressure_regain ? 'Yes' : 'No'}
        </p>
      </div>
    </div>
  );
};
