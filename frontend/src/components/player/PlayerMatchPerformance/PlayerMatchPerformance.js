import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import * as api from '../../../services/api';
import { PlayerProfile } from './components/PlayerProfile';
import { StatNavigation } from './components/StatNavigation';
import { StatOverview } from './components/StatOverview';
import { SubStatNavigation } from './components/SubStatNavigation';
import { ItemDetails } from './components/ItemDetails';
import { Visualization } from './components/Visualization';

const PlayerMatchPerformance = () => {
  const { matchId, playerName } = useParams();
  const [selectedStat, setSelectedStat] = useState('summary');
  const [selectedSubStat, setSelectedSubStat] = useState('touches');
  const [selectedTeam, setSelectedTeam] = useState('team1');
  const [touches, setTouches] = useState([]);
  const [shootingData, setShootingData] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
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

  const handleStatChange = category => {
    setSelectedStat(category.id);
    setSelectedSubStat(category.subStats[0].id);
    setSelectedItem(null);
  };

  const handleItemClick = item => {
    setSelectedItem(prev => (prev === item ? null : item));
  };

  return (
    <div className='min-h-screen bg-gray-100'>
      <div className='container mx-auto px-4 py-8'>
        <div className='grid grid-cols-12 gap-4'>
          <div className='col-span-12 grid grid-cols-12 gap-4'>
            <PlayerProfile playerName={playerName} />
            <StatNavigation
              selectedStat={selectedStat}
              onStatChange={handleStatChange}
            />
          </div>

          <div className='col-span-12 lg:col-span-3'>
            <StatOverview
              selectedStat={selectedStat}
              shootingData={shootingData}
              touches={touches}
            />
          </div>

          <div className='col-span-12 lg:col-span-9'>
            <div className='rounded-lg bg-white shadow-lg'>
              <div className='px-6 pt-4'>
                <SubStatNavigation
                  selectedStat={selectedStat}
                  selectedSubStat={selectedSubStat}
                  onSubStatChange={setSelectedSubStat}
                />
              </div>

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
                      shootingData={shootingData}
                      touches={touches}
                      selectedTouch={
                        selectedStat === 'summary' ? selectedItem : null
                      }
                      selectedShot={
                        selectedStat === 'shooting' ? selectedItem : null
                      }
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
