import React from 'react';
import { format } from 'date-fns';
import { MapPin, User, Clock } from 'lucide-react';

const MatchHeader = ({ matchData }) => {
  if (!matchData) return null;

  const getStatusColor = status => {
    switch (status?.toLowerCase()) {
      case 'available':
        return 'bg-green-100 text-green-800';
      case 'scheduled':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className='mb-6 overflow-hidden rounded-lg bg-white shadow'>
      {/* Competition Info */}
      <div className='border-b border-gray-200 bg-blue-600 p-4 text-white'>
        <h2 className='text-2xl font-bold'>{matchData.competition}</h2>
        <p className='text-sm opacity-80'>
          {matchData.season} - {matchData.competition_stage}
        </p>
      </div>

      {/* Match Status & Date */}
      <div className='border-b border-gray-200 bg-gray-50 p-4'>
        <div className='flex items-center justify-between'>
          <div className='flex items-center gap-2'>
            <Clock className='h-4 w-4 text-gray-500' />
            <span className='text-sm text-gray-600'>
              {format(new Date(matchData.match_date), 'MMMM d, yyyy')} -{' '}
              {matchData.kick_off?.slice(0, 5)}
            </span>
          </div>
          <span
            className={`rounded-full px-3 py-1 text-sm ${getStatusColor(matchData.match_status)}`}
          >
            {matchData.match_status}
          </span>
        </div>
      </div>

      {/* Teams & Score */}
      <div className='grid grid-cols-7 items-center gap-4 p-6'>
        {/* Home Team */}
        <div className='col-span-3 text-right'>
          <h3 className='text-xl font-semibold'>{matchData.home_team}</h3>
          {matchData.home_managers && (
            <div className='mt-2 flex items-center justify-end gap-1 text-sm text-gray-600'>
              <User className='h-4 w-4' />
              {matchData.home_managers}
            </div>
          )}
        </div>

        {/* Score */}
        <div className='col-span-1 text-center'>
          <div className='text-2xl font-bold'>
            {typeof matchData.home_score === 'number' &&
            typeof matchData.away_score === 'number'
              ? `${matchData.home_score} - ${matchData.away_score}`
              : 'vs'}
          </div>
          {matchData.match_week && (
            <div className='mt-1 text-xs text-gray-500'>
              Week {matchData.match_week}
            </div>
          )}
        </div>

        {/* Away Team */}
        <div className='col-span-3 text-left'>
          <h3 className='text-xl font-semibold'>{matchData.away_team}</h3>
          {matchData.away_managers && (
            <div className='mt-2 flex items-center gap-1 text-sm text-gray-600'>
              <User className='h-4 w-4' />
              {matchData.away_managers}
            </div>
          )}
        </div>
      </div>

      {/* Additional Info */}
      {(matchData.stadium || matchData.referee) && (
        <div className='border-t border-gray-200 bg-gray-50 p-4'>
          <div className='flex flex-wrap items-center gap-6'>
            {matchData.stadium && (
              <div className='flex items-center gap-2 text-sm text-gray-600'>
                <MapPin className='h-4 w-4' />
                {matchData.stadium}
              </div>
            )}
            {matchData.referee && (
              <div className='flex items-center gap-2 text-sm text-gray-600'>
                <User className='h-4 w-4' />
                Referee: {matchData.referee}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MatchHeader;
