import React from 'react';

export const PlayerProfile = ({ playerName }) => (
  <div className='col-span-12 rounded-lg bg-white p-4 shadow-lg lg:col-span-3'>
    <div className='flex items-center space-x-4'>
      <div className='h-16 w-16 rounded-full bg-gray-200'></div>
      <div>
        <h3 className='font-semibold'>{playerName || 'Player Name'}</h3>
        <p className='text-sm text-gray-600'>Team • Nationality</p>
      </div>
    </div>
  </div>
);