import React from 'react';
import { Users, ChevronDown, ChevronUp } from 'lucide-react';
import TeamLineupTable from './TeamLineupTable';

const TeamLineup = ({
  teamName,
  players,
  onPlayerClick,
  showSubs,
  onToggleSubs,
  side = 'left',
}) => {
  const getPlayerStatus = player => {
    if (!player.positions?.length) return 'Unknown';
    const startReason = player.positions[0].start_reason;
    if (startReason?.includes('Substitution - On')) return 'Substitute';
    if (startReason === 'Starting XI') return 'Starting XI';
    return startReason || 'Unknown';
  };

  const startingXI = players.filter(p => getPlayerStatus(p) === 'Starting XI');
  const substitutes = players.filter(
    p =>
      p.positions?.length > 0 &&
      p.positions[0].start_reason?.includes('Substitution - On'),
  );

  return (
    <div className='mb-6 overflow-hidden rounded-lg bg-white shadow'>
      <div className='border-b border-gray-200 bg-gray-50 px-4 py-3'>
        <div className='flex items-center justify-between'>
          <div className='flex items-center gap-2'>
            <Users className='h-5 w-5 text-gray-500' />
            <h5 className='m-0 font-semibold'>{teamName}</h5>
          </div>
        </div>
      </div>

      <div className='p-0'>
        <div className='border-b border-gray-100 bg-green-50/30 px-4 py-2'>
          <h6 className='m-0 text-sm font-semibold text-gray-600'>
            Starting XI ({startingXI.length})
          </h6>
        </div>

        <TeamLineupTable players={startingXI} onPlayerClick={onPlayerClick} />

        {substitutes.length > 0 && (
          <div className='border-t-2 border-blue-200'>
            <div
              className='flex cursor-pointer items-center justify-between bg-blue-50 px-4 py-3'
              onClick={onToggleSubs}
            >
              <h6 className='m-0 text-sm font-semibold text-gray-600'>
                Substitutes ({substitutes.length})
              </h6>
              {showSubs ? (
                <ChevronUp className='h-5 w-5 text-blue-500' />
              ) : (
                <ChevronDown className='h-5 w-5 text-blue-500' />
              )}
            </div>

            {showSubs && (
              <TeamLineupTable
                players={substitutes}
                onPlayerClick={onPlayerClick}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TeamLineup;
