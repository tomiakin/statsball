import React from 'react';

export const SummaryItemDetails = ({ selectedItem }) => {
  if (!selectedItem) {
    return (
      <div className='text-center text-gray-500'>
        Select a touch point to see details
      </div>
    );
  }

  return (
    <div className='grid grid-cols-3 gap-4'>
      <div>
        <p className='text-xs text-gray-500'>Touch Type</p>
        <p className='text-sm font-bold'>{selectedItem.type}</p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>X Location</p>
        <p className='text-sm font-bold'>
          {selectedItem.location[0].toFixed(1)}
        </p>
      </div>
      <div>
        <p className='text-xs text-gray-500'>Y Location</p>
        <p className='text-sm font-bold'>
          {selectedItem.location[1].toFixed(1)}
        </p>
      </div>
    </div>
  );
};
