import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { LoadingSpinner, ErrorMessage } from '../common';
import MatchHeader from './MatchHeader';
import MatchLineups from './MatchLineups';
import * as api from '../../services/api';

const MatchDetails = () => {
  const { matchId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [matchData, setMatchData] = useState(location.state?.matchData || null);
  const [lineups, setLineups] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // If we don't have match data from navigation state, fetch it
        let currentMatch = matchData;
        if (!currentMatch) {
          const matchesData = await api.getCompetitionMatches();
          currentMatch = matchesData.find(
            m => m.match_id.toString() === matchId,
          );
          if (!currentMatch) throw new Error('Match not found');
          setMatchData(currentMatch);
        }

        // Fetch lineups
        const lineupsData = await api.getMatchLineups(matchId);
        console.log('Fetched lineups:', lineupsData); // Debug log
        setLineups(lineupsData);
        setError(null);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load match data');
      } finally {
        setLoading(false);
      }
    };

    if (matchId) fetchData();
  }, [matchId, matchData]);

  const handlePlayerClick = player => {
    if (!player?.player_name) {
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
          },
        },
      },
    );
  };

  if (loading) return <LoadingSpinner message='Loading match data...' />;
  if (error) return <ErrorMessage message={error} />;
  if (!matchData || !lineups) return null;

  return (
    <div className='container mx-auto px-4 py-4'>
      <MatchHeader matchData={matchData} />
      <MatchLineups
        lineups={lineups}
        matchData={matchData}
        onPlayerClick={handlePlayerClick}
      />
    </div>
  );
};

export default MatchDetails;
