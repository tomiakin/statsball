import React, { useState, useEffect } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { STAT_TYPES, getDefaultSubStat } from './config/statTypes';
import { useStatData } from './hooks/useStatData';
import { PlayerProfile } from './components/PlayerProfile';
import { StatNavigation } from './components/StatNavigation';
import { StatOverview } from './components/StatOverview';
import { SubStatNavigation } from './components/SubStatNavigation';
import { ItemDetails } from './components/ItemDetails';
import { Visualization } from './components/Visualization';
import * as api from '../../../services/api';

const PlayerMatchPerformance = () => {
  const { matchId, playerName } = useParams();
  const location = useLocation();
  const [playerInfo, setPlayerInfo] = useState(
    location.state?.playerInfo || null,
  );
  const [loadingPlayerInfo, setLoadingPlayerInfo] = useState(
    !location.state?.playerInfo,
  );

  const [selectedStat, setSelectedStat] = useState(STAT_TYPES.SUMMARY);
  const [selectedSubStat, setSelectedSubStat] = useState(
    getDefaultSubStat(STAT_TYPES.SUMMARY),
  );
  const [selectedTeam, setSelectedTeam] = useState('team1');
  const [selectedItem, setSelectedItem] = useState(null);

  // Fetch player info if not available in state
  useEffect(() => {
    const fetchPlayerInfo = async () => {
      if (!playerInfo && matchId && playerName) {
        try {
          const lineupsData = await api.getMatchLineups(matchId);

          // Search through both teams' lineups
          const allPlayers = [
            ...(Object.values(lineupsData)[0] || []),
            ...(Object.values(lineupsData)[1] || []),
          ];

          const player = allPlayers.find(
            p =>
              p.player_name === decodeURIComponent(playerName) ||
              p.nickname === decodeURIComponent(playerName),
          );

          if (player) {
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
          }
        } catch (error) {
          console.error('Error fetching player info:', error);
        } finally {
          setLoadingPlayerInfo(false);
        }
      }
    };

    fetchPlayerInfo();
  }, [matchId, playerName, playerInfo]);

  // Use our custom hook to fetch data
  const { data, loading, error } = useStatData(
    matchId,
    playerInfo?.playerName || playerName,
    selectedStat,
  );

  const handleStatChange = category => {
    setSelectedStat(category.id);
    // Reset to default sub-stat when changing main stat
    setSelectedSubStat(getDefaultSubStat(category.id));
    // Clear selected item when changing stats
    setSelectedItem(null);
  };

  const handleSubStatChange = subStatId => {
    setSelectedSubStat(subStatId);
    // Optionally clear selected item when changing sub-stat
    setSelectedItem(null);
  };

  const handleItemClick = item => {
    setSelectedItem(prev => (prev === item ? null : item));
  };

  if (loadingPlayerInfo) {
    return (
      <div className='flex h-screen items-center justify-center'>
        <div className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent' />
      </div>
    );
  }

  return (
    <div className='min-h-screen bg-gray-100'>
      <div className='container mx-auto px-4 py-8'>
        <div className='grid grid-cols-12 gap-4'>
          {/* Profile and Navigation Section */}
          <div className='col-span-12 grid grid-cols-12 gap-4'>
            <PlayerProfile playerInfo={playerInfo} />
            <StatNavigation
              selectedStat={selectedStat}
              onStatChange={handleStatChange}
            />
          </div>

          {/* Stats Overview Section */}
          <div className='col-span-12 lg:col-span-3'>
            <StatOverview selectedStat={selectedStat} data={data} />
          </div>

          {/* Main Visualization Section */}
          <div className='col-span-12 lg:col-span-9'>
            <div className='rounded-lg bg-white shadow-lg'>
              {/* Sub-stat Navigation */}
              <div className='px-6 pt-4'>
                <SubStatNavigation
                  selectedStat={selectedStat}
                  selectedSubStat={selectedSubStat}
                  onSubStatChange={handleSubStatChange}
                />
              </div>

              {/* Visualization and Details */}
              <div className='px-6 pb-6'>
                {loading ? (
                  <div className='flex h-full items-center justify-center'>
                    <div className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent' />
                  </div>
                ) : error ? (
                  <div className='flex h-full items-center justify-center text-red-500'>
                    {error}
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

        {/* Team Switch Button */}
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
