import React from 'react';
import { useLocation } from 'react-router-dom';

export const PlayerProfile = () => {
  const location = useLocation();
  const playerInfo = location.state?.playerInfo || {};

  return (
    <div className='col-span-12 rounded-lg bg-white p-4 shadow-lg lg:col-span-3'>
      <div className='flex items-center space-x-4'>
        <div className='h-16 w-16 rounded-full bg-gray-200'>
          {playerInfo.jerseyNumber && (
            <div className='flex h-full w-full items-center justify-center text-xl font-bold text-gray-600'>
              {playerInfo.jerseyNumber}
            </div>
          )}
        </div>
        <div>
          <h3 className='font-semibold'>
            {playerInfo.nickname || playerInfo.playerName || 'Player Name'}
          </h3>
          <p className='text-sm text-gray-600'>
            {playerInfo.team} • {playerInfo.position || 'Position'}
          </p>
        </div>
      </div>
    </div>
  );
};
