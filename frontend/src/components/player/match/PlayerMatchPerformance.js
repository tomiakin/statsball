import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import * as api from '../../../services/api';

// Pitch imports
import SoccerPitch from '../../pitch/SoccerPitch';
import VerticalSoccerPitch from '../../pitch/VerticalSoccerPitch';
import HalfVerticalPitch from '../../pitch/HalfVerticalPitch';

// To render on pitch
import PlayerMatchTouches from './visualizations/PlayerMatchTouches';
import PlayerVertMatchTouches from './visualizations/PlayerVertMatchTouches';
import PlayerMatchShots from './visualizations/PlayerMatchShots';

const statCategories = [
  {
    id: 'summary',
    name: 'Summary',
    subStats: [
      {
        id: 'touches',
        name: 'Touches',
        container: ({ children }) => (
          <div className='w-full'>
            <SoccerPitch>{children}</SoccerPitch>
          </div>
        ),
        component: PlayerMatchTouches,
      },
      {
        id: 'heatmap',
        name: 'Heatmap',
        container: ({ children }) => (
          <div className='mx-auto w-full max-w-xl'>
            <VerticalSoccerPitch>{children}</VerticalSoccerPitch>
          </div>
        ),
        component: PlayerVertMatchTouches,
      },
    ],
  },
  {
    id: 'shooting',
    name: 'Shooting',
    subStats: [
      {
        id: 'shots',
        name: 'All Shots',
        container: ({ children }) => (
          <div className='mx-auto w-full max-w-xl'>
            <HalfVerticalPitch>{children}</HalfVerticalPitch>
          </div>
        ),
        component: PlayerMatchShots,
      },
    ],
  },
];

const PlayerMatchPerformance = () => {
  const { matchId, playerName } = useParams();
  const [selectedStat, setSelectedStat] = useState('summary');
  const [selectedSubStat, setSelectedSubStat] = useState('touches');
  const [selectedTeam, setSelectedTeam] = useState('team1');
  const [touches, setTouches] = useState([]);
  const [shootingData, setShootingData] = useState(null);
  const [selectedTouch, setSelectedTouch] = useState(null);
  const [selectedShot, setSelectedShot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!matchId || !playerName) return;

      setLoading(true);
      setError(null);

      try {
        // Always fetch touches as they're used in the summary
        const touchData = await api.getPlayerMatchTouches(matchId, playerName);
        setTouches(touchData);

        // Only fetch shooting data if we're in shooting view
        if (selectedStat === 'shooting') {
          const shotData = await api.getPlayerMatchShooting(
            matchId,
            playerName,
          );
          setShootingData(shotData);
        }
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [matchId, playerName, selectedStat]);

  const handleTouchClick = item => {
    if (selectedStat === 'shooting') {
      setSelectedShot(prev => (prev === item ? null : item));
    } else {
      setSelectedTouch(prev => (prev === item ? null : item));
    }
  };

  const renderStatDetails = () => {
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

    // Default summary stats
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

  const renderSelectedItemDetails = () => {
    if (selectedStat === 'shooting') {
      return selectedShot ? (
        <div className='grid grid-cols-3 gap-4'>
          <div>
            <p className='text-xs text-gray-500'>Shot Outcome</p>
            <p className='text-sm font-bold'>{selectedShot.shot_outcome}</p>
          </div>
          <div>
            <p className='text-xs text-gray-500'>Expected Goals (xG)</p>
            <p className='text-sm font-bold'>
              {selectedShot.shot_statsbomb_xg?.toFixed(2)}
            </p>
          </div>
          <div>
            <p className='text-xs text-gray-500'>Shot Type</p>
            <p className='text-sm font-bold'>{selectedShot.shot_type}</p>
          </div>
        </div>
      ) : (
        <div className='text-center text-gray-500'>
          Select a shot to see details
        </div>
      );
    }

    return selectedTouch ? (
      <div className='grid grid-cols-3 gap-4'>
        <div>
          <p className='text-xs text-gray-500'>Touch Type</p>
          <p className='text-sm font-bold'>{selectedTouch.type}</p>
        </div>
        <div>
          <p className='text-xs text-gray-500'>X Location</p>
          <p className='text-sm font-bold'>
            {selectedTouch.location[0].toFixed(1)}
          </p>
        </div>
        <div>
          <p className='text-xs text-gray-500'>Y Location</p>
          <p className='text-sm font-bold'>
            {selectedTouch.location[1].toFixed(1)}
          </p>
        </div>
      </div>
    ) : (
      <div className='text-center text-gray-500'>
        Select a touch point to see details
      </div>
    );
  };

  const renderVisualization = () => {
    const category = statCategories.find(cat => cat.id === selectedStat);
    const subStat = category?.subStats.find(sub => sub.id === selectedSubStat);

    if (!subStat) return null;

    const { container: Container, component: Component } = subStat;

    const componentProps =
      selectedStat === 'shooting'
        ? {
            shots: shootingData?.shots || [],
            onShotClick: handleTouchClick,
            selectedShot,
            showLabels: false,
          }
        : {
            touches,
            onTouchClick: handleTouchClick,
            selectedTouch,
            showLabels: false,
          };

    return (
      <Container>
        <Component {...componentProps} />
      </Container>
    );
  };

  return (
    <div className='min-h-screen bg-gray-100'>
      <div className='container mx-auto px-4 py-8'>
        <div className='grid grid-cols-12 gap-4'>
          {/* First Row: Player Info + Stat Navigation */}
          <div className='col-span-12 grid grid-cols-12 gap-4'>
            {/* Player Info */}
            <div className='col-span-12 rounded-lg bg-white p-4 shadow-lg lg:col-span-3'>
              <div className='flex items-center space-x-4'>
                <div className='h-16 w-16 rounded-full bg-gray-200'></div>
                <div>
                  <h3 className='font-semibold'>
                    {playerName || 'Player Name'}
                  </h3>
                  <p className='text-sm text-gray-600'>Team • Nationality</p>
                </div>
              </div>
            </div>

            {/* Stat Navigation */}
            <div className='col-span-12 flex items-center rounded-lg bg-white px-6 py-4 shadow-lg lg:col-span-9'>
              <div className='flex space-x-4 overflow-x-auto'>
                {statCategories.map(category => (
                  <button
                    key={category.id}
                    className={`whitespace-nowrap rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                      selectedStat === category.id
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                    onClick={() => {
                      setSelectedStat(category.id);
                      setSelectedSubStat(category.subStats[0].id);
                      setSelectedTouch(null);
                      setSelectedShot(null);
                    }}
                  >
                    {category.name}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Second Row: Stats + Pitch */}
          <div className='col-span-12 lg:col-span-3'>
            {/* Match Overview with conditional rendering based on selectedStat */}
            <div className='mb-4 rounded-lg bg-white p-4 shadow-lg'>
              <h3 className='mb-3 text-lg font-semibold'>
                {selectedStat === 'shooting'
                  ? 'Shooting Overview'
                  : 'Match Overview'}
              </h3>
              {renderStatDetails()}
            </div>
          </div>

          {/* Pitch Visualization */}
          <div className='col-span-12 lg:col-span-9'>
            <div className='rounded-lg bg-white shadow-lg'>
              {/* Sub-stat buttons */}
              <div className='px-6 pt-4'>
                <div className='mb-4 flex space-x-4 overflow-x-auto'>
                  {statCategories
                    .find(cat => cat.id === selectedStat)
                    ?.subStats.map(subStat => (
                      <button
                        key={subStat.id}
                        className={`whitespace-nowrap rounded-md px-4 py-2 ${
                          selectedSubStat === subStat.id
                            ? 'bg-blue-100 text-blue-700'
                            : 'text-gray-600 hover:bg-gray-100'
                        }`}
                        onClick={() => setSelectedSubStat(subStat.id)}
                      >
                        {subStat.name}
                      </button>
                    ))}
                </div>
              </div>

              {/* Pitch container */}
              <div className='px-6 pb-6'>
                {loading ? (
                  <div className='flex h-full items-center justify-center'>
                    <div className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent'></div>
                  </div>
                ) : error ? (
                  <div className='flex h-full items-center justify-center text-red-500'>
                    {error}
                  </div>
                ) : (
                  <>
                    {renderVisualization()}

                    {/* Selected Item Details below pitch */}
                    <div className='mt-4 rounded-lg bg-gray-50 p-4'>
                      {renderSelectedItemDetails()}
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Team Switch */}
        <div className='mt-4 flex justify-center'>
          <button
            className='rounded-full bg-gray-800 px-6 py-2 text-white shadow-lg hover:bg-gray-700'
            onClick={() =>
              setSelectedTeam(selectedTeam === 'team1' ? 'team2' : 'team1')
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
