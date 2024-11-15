import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import * as api from '../services/api';
import MatchTouches from './MatchTouches';
import SoccerPitch from './SoccerPitch';
import VerticalMatchTouches from './VerticalMatchTouches';
import VerticalSoccerPitch from './VerticalSoccerPitch';

const PlayerPerformance = () => {
  const { matchId, playerName } = useParams();
  const [selectedStat, setSelectedStat] = useState('possession');
  const [selectedSubStat, setSelectedSubStat] = useState('touches');
  const [selectedTeam, setSelectedTeam] = useState('team1');
  const [touches, setTouches] = useState([]);
  const [selectedTouch, setSelectedTouch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isVertical, setIsVertical] = useState(false);

  const statCategories = [
    {
      id: 'possession',
      name: 'Possession',
      subStats: ['touches', 'passes', 'ball control'],
    },
    {
      id: 'attacking',
      name: 'Attacking',
      subStats: ['shots', 'goals', 'assists'],
    },
  ];

  useEffect(() => {
    const fetchTouchData = async () => {
      if (!matchId || !playerName) return;
      try {
        setLoading(true);
        const data = await api.getPlayerMatchTouches(matchId, playerName);
        setTouches(data);
        setError(null);
      } catch (err) {
        setError('Failed to load touch data');
        setTouches([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTouchData();
  }, [matchId, playerName]);

  const handleTouchClick = touch => {
    setSelectedTouch(prev => (prev === touch ? null : touch));
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
                    onClick={() => setSelectedStat(category.id)}
                  >
                    {category.name}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Second Row: Stats + Pitch */}
          <div className='col-span-12 lg:col-span-3'>
            {/* More compact Match Overview */}
            <div className='mb-4 rounded-lg bg-white p-4 shadow-lg'>
              <h3 className='mb-3 text-lg font-semibold'>Match Overview</h3>
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
            </div>

            {/* Selected Touch - Same height as before but starts higher up */}
            <div className='rounded-lg bg-white p-4 shadow-lg'>
              <h3 className='mb-3 text-lg font-semibold'>Selected Touch</h3>
              <div className='grid gap-3'>
                {selectedTouch ? (
                  <>
                    <div className='rounded-lg bg-gray-50 p-3'>
                      <p className='text-xs text-gray-500'>Touch Type</p>
                      <p className='text-lg font-bold'>{selectedTouch.type}</p>
                    </div>
                    <div className='rounded-lg bg-gray-50 p-3'>
                      <p className='text-xs text-gray-500'>X Location</p>
                      <p className='text-lg font-bold'>
                        {selectedTouch.location[0].toFixed(1)}
                      </p>
                    </div>
                    <div className='rounded-lg bg-gray-50 p-3'>
                      <p className='text-xs text-gray-500'>Y Location</p>
                      <p className='text-lg font-bold'>
                        {selectedTouch.location[1].toFixed(1)}
                      </p>
                    </div>
                  </>
                ) : (
                  <div className='text-center text-gray-500'>
                    Select a touch point to see details
                  </div>
                )}
              </div>
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
                        key={subStat}
                        className={`whitespace-nowrap rounded-md px-4 py-2 ${
                          selectedSubStat === subStat
                            ? 'bg-blue-100 text-blue-700'
                            : 'text-gray-600 hover:bg-gray-100'
                        }`}
                        onClick={() => setSelectedSubStat(subStat)}
                      >
                        {subStat}
                      </button>
                    ))}
                </div>
              </div>

              {/* Pitch container */}
              {isVertical ? (
                <div className='px-6 pb-6'>
                  <div className='mx-auto aspect-[2/3] max-w-[400px]'>
                    {loading ? (
                      <div className='flex h-full items-center justify-center'>
                        <div className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent'></div>
                      </div>
                    ) : error ? (
                      <div className='flex h-full items-center justify-center text-red-500'>
                        {error}
                      </div>
                    ) : (
                      selectedStat === 'possession' &&
                      selectedSubStat === 'touches' && (
                        <div className='relative h-full w-full'>
                          <VerticalSoccerPitch>
                            <VerticalMatchTouches
                              touches={touches}
                              onTouchClick={handleTouchClick}
                              selectedTouch={selectedTouch}
                              showLabels={false}
                            />
                          </VerticalSoccerPitch>
                        </div>
                      )
                    )}
                  </div>
                </div>
              ) : (
                <div className='aspect-[3/2] w-full px-6 pb-6'>
                  {loading ? (
                    <div className='flex h-full items-center justify-center'>
                      <div className='h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent'></div>
                    </div>
                  ) : error ? (
                    <div className='flex h-full items-center justify-center text-red-500'>
                      {error}
                    </div>
                  ) : (
                    selectedStat === 'possession' &&
                    selectedSubStat === 'touches' && (
                      <div className='relative h-full w-full'>
                        <SoccerPitch>
                          <MatchTouches
                            touches={touches}
                            onTouchClick={handleTouchClick}
                            selectedTouch={selectedTouch}
                            showLabels={false}
                          />
                        </SoccerPitch>
                      </div>
                    )
                  )}
                </div>
              )}
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

export default PlayerPerformance;
