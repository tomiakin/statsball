import React from 'react';

export const StatOverview = ({ selectedStat, shootingData, touches }) => {
  const renderStats = () => {
    if (selectedStat === 'shooting' && shootingData?.statistics) {
      const stats = shootingData.statistics;
      return (
        <div className='grid grid-cols-3 gap-2 lg:grid-cols-1'>
          <div className='rounded-lg bg-gray-50 p-3'>
            <p className='text-xs text-gray-500'>Shot Conversion</p>
            <p className='text-lg font-bold'>{`${stats.goals}/${stats.total_shots}`}</p>
          </div>
          <div className='rounded-lg bg-gray-50 p-3'>
            <p className='text-xs text-gray-500'>On Target</p>
            <p className='text-lg font-bold'>{`${stats.shots_on_target}/${stats.total_shots}`}</p>
          </div>
          <div className='rounded-lg bg-gray-50 p-3'>
            <p className='text-xs text-gray-500'>Shot Accuracy</p>
            <p className='text-lg font-bold'>{`${stats.shot_accuracy}%`}</p>
          </div>
          <div className='rounded-lg bg-gray-50 p-3'>
            <p className='text-xs text-gray-500'>Total xG</p>
            <p className='text-lg font-bold'>{stats.total_xg}</p>
          </div>
          <div className='rounded-lg bg-gray-50 p-3'>
            <p className='text-xs text-gray-500'>Goals per xG</p>
            <p className='text-lg font-bold'>{stats.goals_per_xg}</p>
          </div>
        </div>
      );
    }

    return (
      <div className='grid grid-cols-3 gap-2 lg:grid-cols-1'>
        <div className='rounded-lg bg-gray-50 p-3'>
          <p className='text-xs text-gray-500'>Touches</p>
          <p className='text-lg font-bold'>{touches.length}</p>
        </div>
        <div className='rounded-lg bg-gray-50 p-3'>
          <p className='text-xs text-gray-500'>Shots</p>
          <p className='text-lg font-bold'>
            {touches.filter(t => t.type === 'Shot').length}
          </p>
        </div>
        <div className='rounded-lg bg-gray-50 p-3'>
          <p className='text-xs text-gray-500'>Assists</p>
          <p className='text-lg font-bold'>
            {touches.filter(t => t.type === 'assist').length}
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className='mb-4 rounded-lg bg-white p-4 shadow-lg'>
      <h3 className='mb-3 text-lg font-semibold'>
        {selectedStat === 'shooting' ? 'Shooting Overview' : 'Match Overview'}
      </h3>
      {renderStats()}
    </div>
  );
};
