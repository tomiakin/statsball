import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { STAT_TYPES, getDefaultSubStat } from './config/statTypes';
import { useStatData } from './hooks/useStatData';
import { PlayerProfile } from './components/PlayerProfile';
import { StatNavigation } from './components/StatNavigation';
import { StatOverview } from './components/StatOverview';
import { SubStatNavigation } from './components/SubStatNavigation';
import { ItemDetails } from './components/ItemDetails';
import { Visualization } from './components/Visualization';
import MatchHeader from '../../match/MatchHeader';
import * as api from '../../../services/api';

const LOADING_DELAY = 500;
const MAX_RETRY_ATTEMPTS = 2;
const RETRY_DELAY = 1000;

const PlayerMatchPerformance = () => {
  const { competitionId, seasonId, matchId, playerName } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [playerInfo, setPlayerInfo] = useState(
    location.state?.playerInfo || null,
  );
  const [matchData, setMatchData] = useState(location.state?.matchData || null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const [selectedStat, setSelectedStat] = useState(STAT_TYPES.SUMMARY);
  const [selectedSubStat, setSelectedSubStat] = useState(
    getDefaultSubStat(STAT_TYPES.SUMMARY),
  );
  const [selectedTeam, setSelectedTeam] = useState('team1');
  const [selectedItem, setSelectedItem] = useState(null);

  // Initial loading delay
  useEffect(() => {
    const timer = setTimeout(() => {
      if (!location.state) {
        setIsLoading(false);
      }
    }, LOADING_DELAY);

    return () => clearTimeout(timer);
  }, [location.state]);

  // Load match data with retries
  useEffect(() => {
    const getMatch = async () => {
      if (!matchData && !isLoading) {
        try {
          const matches = await api.getCompetitionMatches(
            competitionId,
            seasonId,
          );
          const match = matches.find(m => m.match_id.toString() === matchId);

          if (!match) {
            throw new Error('Match not found');
          }

          setMatchData(match);
          setError(null);
        } catch (error) {
          console.error('Error fetching match:', error);

          if (retryCount < MAX_RETRY_ATTEMPTS) {
            setTimeout(() => {
              setRetryCount(prev => prev + 1);
            }, RETRY_DELAY);
          } else {
            setError('Unable to load match data. Please try again later.');
          }
        }
      }
    };
    getMatch();
  }, [matchData, competitionId, seasonId, matchId, isLoading, retryCount]);

  // Load player info with validation
  useEffect(() => {
    const getPlayer = async () => {
      if (!playerInfo && matchData) {
        try {
          const lineupsData = await api.getMatchLineups(matchId);

          if (!lineupsData || Object.keys(lineupsData).length === 0) {
            throw new Error('No lineup data available');
          }

          const allPlayers = [
            ...(Object.values(lineupsData)[0] || []),
            ...(Object.values(lineupsData)[1] || []),
          ];

          const decodedPlayerName = decodeURIComponent(playerName);
          const player = allPlayers.find(
            p =>
              p.player_name === decodedPlayerName ||
              p.nickname === decodedPlayerName,
          );

          if (!player) {
            throw new Error('Player not found in match lineup');
          }

          setPlayerInfo({
            playerId: player.player_id,
            playerName: player.player_name,
            nickname: player.nickname,
            jerseyNumber: player.jersey_number,
            team: Object.keys(lineupsData).find(team =>
              lineupsData[team].some(p => p.player_id === player.player_id),
            ),
            position: player.positions?.[0]?.position,
          });
          setError(null);
        } catch (error) {
          console.error('Error fetching player:', error);
          setError(
            error.message === 'Player not found in match lineup'
              ? 'Player not found in match lineup. Please check the player name and try again.'
              : 'Unable to load player data. Please try again later.',
          );
        }
      }
    };
    getPlayer();
  }, [playerInfo, matchData, matchId, playerName]);

  const {
    data,
    loading: statsLoading,
    error: statsError,
  } = useStatData(
    matchData && playerInfo ? matchId : null,
    playerInfo?.playerName || null,
    selectedStat,
  );

  const handleStatChange = category => {
    setSelectedStat(category.id);
    setSelectedSubStat(getDefaultSubStat(category.id));
    setSelectedItem(null);
  };

  const handleSubStatChange = subStatId => {
    setSelectedSubStat(subStatId);
    setSelectedItem(null);
  };

  const handleItemClick = item => {
    setSelectedItem(prev => (prev === item ? null : item));
  };

  const handleRetry = () => {
    setError(null);
    setRetryCount(0);
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), LOADING_DELAY);
  };

  // Error UI
  if (error) {
    return (
      <div className='flex h-screen flex-col items-center justify-center bg-gray-100'>
        <div className='rounded-lg bg-white p-8 shadow-lg'>
          <h2 className='mb-4 text-xl font-bold text-red-600'>Error</h2>
          <p className='mb-6 text-gray-700'>{error}</p>
          <div className='flex gap-4'>
            <button
              onClick={handleRetry}
              className='rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600'
            >
              Try Again
            </button>
            <button
              onClick={() => navigate(-1)}
              className='rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600'
            >
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Loading UI
  if (isLoading || !matchData || !playerInfo) {
    return (
      <div className='flex h-screen flex-col items-center justify-center bg-gray-100'>
        <div className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent' />
        <p className='mt-4 text-gray-600'>Loading match data...</p>
      </div>
    );
  }

  return (
    <div className='min-h-screen bg-gray-100'>
      <div className='container mx-auto px-4 py-8'>
        <div className='mb-6'>
          <MatchHeader matchData={matchData} />
        </div>

        <div className='grid grid-cols-12 gap-4'>
          <div className='col-span-12 grid grid-cols-12 gap-4'>
            <PlayerProfile playerInfo={playerInfo} />
            <StatNavigation
              selectedStat={selectedStat}
              onStatChange={handleStatChange}
            />
          </div>

          <div className='col-span-12 lg:col-span-3'>
            <StatOverview selectedStat={selectedStat} data={data} />
          </div>

          <div className='col-span-12 lg:col-span-9'>
            <div className='rounded-lg bg-white shadow-lg'>
              <div className='px-6 pt-4'>
                <SubStatNavigation
                  selectedStat={selectedStat}
                  selectedSubStat={selectedSubStat}
                  onSubStatChange={handleSubStatChange}
                />
              </div>

              <div className='px-6 pb-6'>
                {statsLoading ? (
                  <div className='flex h-64 items-center justify-center'>
                    <div className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent' />
                  </div>
                ) : statsError ? (
                  <div className='flex h-64 items-center justify-center'>
                    <div className='text-center'>
                      <p className='mb-4 text-red-500'>{statsError}</p>
                      <button
                        onClick={handleRetry}
                        className='rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600'
                      >
                        Retry
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <Visualization
                      selectedStat={selectedStat}
                      selectedSubStat={selectedSubStat}
                      data={data}
                      selectedItem={selectedItem}
                      onItemClick={handleItemClick}
                    />

                    <div className='mt-4 rounded-lg bg-gray-50 p-4'>
                      <ItemDetails
                        selectedStat={selectedStat}
                        selectedItem={selectedItem}
                      />
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className='mt-4 flex justify-center'>
          <button
            className='rounded-full bg-gray-800 px-6 py-2 text-white shadow-lg hover:bg-gray-700'
            onClick={() =>
              setSelectedTeam(prev => (prev === 'team1' ? 'team2' : 'team1'))
            }
          >
            Switch to {selectedTeam === 'team1' ? 'Team 2' : 'Team 1'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default PlayerMatchPerformance;
