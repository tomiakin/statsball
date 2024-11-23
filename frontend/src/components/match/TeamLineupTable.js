import React from 'react';

const TeamLineupTable = ({ players, onPlayerClick }) => (
  <table className='w-full'>
    <tbody>
      {players.map(player => (
        <tr
          key={player.player_id}
          onClick={() => onPlayerClick(player)}
          className='cursor-pointer border-b border-gray-50 hover:bg-gray-50'
        >
          <td className='px-4 py-3 text-sm'>{player.jersey_number || '-'}</td>
          <td className='px-4 py-3'>
            <div>
              <div className='font-medium'>
                {player.nickname || player.player_name}
              </div>
              {player.nationality && (
                <div className='text-xs text-gray-500'>
                  {player.nationality}
                </div>
              )}
            </div>
          </td>
          <td className='px-4 py-3 text-sm'>
            {player.positions?.[0]?.position || '-'}
          </td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default TeamLineupTable;
