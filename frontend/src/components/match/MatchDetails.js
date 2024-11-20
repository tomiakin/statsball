import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LoadingSpinner, ErrorMessage } from '../common';
import * as api from '../../services/api';

const TeamLineup = ({ teamName, players, onPlayerClick }) => {
  const getPlayerPosition = player => {
    if (!player.positions || player.positions.length === 0) return '-';
    const position = player.positions[0];
    return position.position || '-';
  };

  const getPlayerStatus = player => {
    if (!player.positions || player.positions.length === 0) return 'Unknown';
    const position = player.positions[0];
    if (position.start_reason === 'Starting XI') {
      return 'Starting XI';
    } else if (position.start_reason === 'Substitution - On') {
      return 'Substitute';
    }
    return position.start_reason || 'Unknown';
  };

  return (
    <div className='mb-6 overflow-hidden rounded-lg bg-white shadow'>
      <div className='border-b border-gray-200 bg-gray-50 px-4 py-3'>
        <h5 className='m-0 font-semibold'>{teamName}</h5>
      </div>
      <div className='p-0'>
        <table className='w-full'>
          <thead className='bg-gray-50'>
            <tr>
              <th className='px-4 py-2 text-left text-sm font-medium text-gray-500'>
                #
              </th>
              <th className='px-4 py-2 text-left text-sm font-medium text-gray-500'>
                Player
              </th>
              <th className='px-4 py-2 text-left text-sm font-medium text-gray-500'>
                Position
              </th>
              <th className='px-4 py-2 text-left text-sm font-medium text-gray-500'>
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            {players.map(player => (
              <tr
                key={player.player_id}
                onClick={() => onPlayerClick(player)}
                className='cursor-pointer hover:bg-gray-50'
              >
                <td className='px-4 py-2'>{player.jersey_number || '-'}</td>
                <td className='px-4 py-2'>
                  {player.nickname || player.player_name}
                </td>
                <td className='px-4 py-2'>{getPlayerPosition(player)}</td>
                <td className='px-4 py-2'>
                  <span
                    className={
                      getPlayerStatus(player) === 'Starting XI'
                        ? 'text-green-600'
                        : 'text-gray-500'
                    }
                  >
                    {getPlayerStatus(player)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const MatchDetails = () => {
  const { matchId } = useParams();
  const navigate = useNavigate();
  const [lineups, setLineups] = useState({ home: [], away: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLineups = async () => {
      try {
        setLoading(true);
        const lineupsData = await api.getMatchLineups(matchId);
        const teamNames = Object.keys(lineupsData);

        setLineups({
          home: lineupsData[teamNames[0]] || [],
          away: lineupsData[teamNames[1]] || [],
          homeTeam: teamNames[0],
          awayTeam: teamNames[1],
        });

        setError(null);
      } catch (err) {
        console.error('Error fetching lineups:', err);
        setError('Failed to load lineup data');
      } finally {
        setLoading(false);
      }
    };

    fetchLineups();
  }, [matchId]);

  const handlePlayerClick = (player) => {
    if (!player || !player.player_name) {
      console.error('Invalid player data:', player);
      return;
    }

    navigate(
      `/player-performance/${matchId}/${encodeURIComponent(player.player_name)}`,
      {
        state: {
          playerInfo: {
            playerId: player.player_id,
            playerName: player.player_name,
            nickname: player.nickname,
            jerseyNumber: player.jersey_number,
            team: player.team_name,
            position: player.positions?.[0]?.position,
          }
        }
      }
    );
  };

  if (loading) {
    return <LoadingSpinner message="Loading match lineup..." />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <div className='container mx-auto px-4 py-4'>
      <div className='mb-4 overflow-hidden rounded-lg bg-white shadow'>
        <div className='border-b border-gray-200 bg-gray-50 px-4 py-3'>
          <h4 className='m-0 font-semibold'>Match Details</h4>
        </div>
        <div className='px-4 py-4'>
          <div className='grid grid-cols-3 text-center'>
            <div>
              <h5 className='text-lg font-medium'>{lineups.homeTeam}</h5>
            </div>
            <div>
              <h5 className='text-lg font-medium'>vs</h5>
            </div>
            <div>
              <h5 className='text-lg font-medium'>{lineups.awayTeam}</h5>
            </div>
          </div>
        </div>
      </div>

      <div className='grid gap-6 md:grid-cols-2'>
        <TeamLineup
          teamName={lineups.homeTeam}
          players={lineups.home.map(player => ({
            ...player,
            team_name: lineups.homeTeam
          }))}
          onPlayerClick={handlePlayerClick}
        />
        <TeamLineup
          teamName={lineups.awayTeam}
          players={lineups.away.map(player => ({
            ...player,
            team_name: lineups.awayTeam
          }))}
          onPlayerClick={handlePlayerClick}
        />
      </div>
    </div>
  );
};

export default MatchDetails;