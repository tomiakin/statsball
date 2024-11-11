import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import * as api from '../services/api';
import PitchWithTouches from './PitchWithTouches';

const PlayerPerformance = () => {
  const { matchId, playerName } = useParams();
  const [selectedStat, setSelectedStat] = useState('possession');
  const [selectedSubStat, setSelectedSubStat] = useState('touches');
  const [selectedTeam, setSelectedTeam] = useState('team1');
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [touches, setTouches] = useState([]);
  const [selectedTouch, setSelectedTouch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock data for demonstration
  const players = [
    { id: 1, name: 'John Doe', position: 'FW', goals: 5, assists: 3 },
    { id: 2, name: 'Jane Smith', position: 'MF', goals: 2, assists: 6 },
    // Add more players as needed
  ];

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
        const data = await api.getTouchData(matchId, playerName);
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

  const handleTouchClick = (touch) => {
    setSelectedTouch((prev) => (prev === touch ? null : touch));
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-12 gap-4">
          {/* Player Info */}
          <div className="col-span-12 rounded-lg bg-white p-6 shadow-lg lg:col-span-3">
            <h2 className="text-2xl font-bold">Player Information</h2>
            <div className="flex flex-col items-center">
              <div className="h-32 w-32 rounded-full bg-gray-200"></div>
              <h3 className="mt-4 text-xl font-semibold">
                {playerName || 'Player Name'}
              </h3>
              <p className="text-gray-600">Team • Nationality</p>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="col-span-12 lg:col-span-9">
            {/* Stat Navigation */}
            <div className="mb-4 flex overflow-x-auto rounded-lg bg-white p-4 shadow-lg">
              {statCategories.map((category) => (
                <button
                  key={category.id}
                  className={`mr-4 whitespace-nowrap rounded-full px-6 py-2 ${
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

            <div className="grid grid-cols-12 gap-4">
              {/* Player Lineups */}
              <div className="col-span-12 rounded-lg bg-white p-6 shadow-lg lg:col-span-3">
                <h3 className="mb-4 text-xl font-semibold">Team Lineup</h3>
                <div className="divide-y">
                  {players.map((player) => (
                    <div
                      key={player.id}
                      className={`cursor-pointer p-3 hover:bg-gray-50 ${
                        selectedPlayer?.id === player.id ? 'bg-blue-50' : ''
                      }`}
                      onClick={() => setSelectedPlayer(player)}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="font-medium">{player.name}</span>
                          <span className="ml-2 text-sm text-gray-500">
                            {player.position}
                          </span>
                        </div>
                        <div className="text-sm text-gray-600">
                          <span className="mr-2">{player.goals}G</span>
                          <span>{player.assists}A</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Stats Area */}
              <div className="col-span-12 space-y-4 lg:col-span-9">
                {/* Pitch Visualization */}
                <div className="rounded-lg bg-white p-6 shadow-lg">
                  <div className="mb-4 flex space-x-4 overflow-x-auto">
                    {statCategories
                      .find((cat) => cat.id === selectedStat)
                      ?.subStats.map((subStat) => (
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

                  <div className="relative h-96">
                    {loading ? (
                      <div className="flex h-full items-center justify-center">
                        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
                      </div>
                    ) : error ? (
                      <div className="flex h-full items-center justify-center text-red-500">
                        {error}
                      </div>
                    ) : (
                      selectedStat === 'possession' &&
                      selectedSubStat === 'touches' && (
                        <PitchWithTouches
                          touches={touches}
                          onTouchClick={handleTouchClick}
                          selectedTouch={selectedTouch}
                        />
                      )
                    )}
                  </div>
                </div>

                {/* Detailed Stats */}
                <div className="rounded-lg bg-white p-6 shadow-lg">
                  <h3 className="mb-4 text-xl font-semibold">
                    Detailed Statistics
                  </h3>
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                    {selectedTouch ? (
                      <>
                        <div className="rounded-lg bg-gray-50 p-4">
                          <p className="text-sm text-gray-500">Touch Type</p>
                          <p className="text-2xl font-bold">
                            {selectedTouch.type}
                          </p>
                        </div>
                        <div className="rounded-lg bg-gray-50 p-4">
                          <p className="text-sm text-gray-500">X Location</p>
                          <p className="text-2xl font-bold">
                            {selectedTouch.location[0].toFixed(1)}
                          </p>
                        </div>
                        <div className="rounded-lg bg-gray-50 p-4">
                          <p className="text-sm text-gray-500">Y Location</p>
                          <p className="text-2xl font-bold">
                            {selectedTouch.location[1].toFixed(1)}
                          </p>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="rounded-lg bg-gray-50 p-4">
                          <p className="text-sm text-gray-500">Total Touches</p>
                          <p className="text-2xl font-bold">{touches.length}</p>
                        </div>
                        <div className="rounded-lg bg-gray-50 p-4">
                          <p className="text-sm text-gray-500">Shots</p>
                          <p className="text-2xl font-bold">
                            {touches.filter((t) => t.type === 'Shot').length}
                          </p>
                        </div>
                        <div className="rounded-lg bg-gray-50 p-4">
                          <p className="text-sm text-gray-500">Assists</p>
                          <p className="text-2xl font-bold">
                            {touches.filter((t) => t.type === 'assist').length}
                          </p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Team Switch */}
        <div className="mt-4 flex justify-center">
          <button
            className="rounded-full bg-gray-800 px-6 py-2 text-white shadow-lg hover:bg-gray-700"
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