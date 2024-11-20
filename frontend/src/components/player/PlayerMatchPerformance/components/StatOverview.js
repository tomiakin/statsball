import React from 'react';
import { STAT_TYPES } from '../config/statTypes';

export const StatOverview = ({ selectedStat, data }) => {
  const renderStats = () => {
    switch (selectedStat) {
      case STAT_TYPES.SHOOTING:
        if (!data?.statistics) return null;
        const stats = data.statistics;
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

      case STAT_TYPES.SUMMARY:
        if (!data?.touches) return null;
        const touches = data.touches;
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
              <p className='text-xs text-gray-500'>Passes</p>
              <p className='text-lg font-bold'>
                {touches.filter(t => t.type === 'Pass').length}
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className='mb-4 rounded-lg bg-white p-4 shadow-lg'>
      <h3 className='mb-3 text-lg font-semibold'>
        {selectedStat === STAT_TYPES.SHOOTING
          ? 'Shooting Overview'
          : 'Match Overview'}
      </h3>
      {renderStats()}
    </div>
  );
};
