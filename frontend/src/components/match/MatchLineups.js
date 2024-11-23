import React, { useState } from 'react';
import TeamLineup from './TeamLineup';

const MatchLineups = ({ lineups, matchData, onPlayerClick }) => {
  const [showSubs, setShowSubs] = useState(true);

  // Debug logs
  console.log('Match Data:', matchData);
  console.log('Lineups Data:', lineups);

  // Ensure we have the required data
  if (!matchData?.home_team || !matchData?.away_team || !lineups) {
    return null;
  }

  const handleToggleSubs = () => {
    setShowSubs(!showSubs);
  };

  // Create lineup data for each team
  const homeTeam = {
    teamName: matchData.home_team,
    players: (lineups[matchData.home_team] || []).map(player => ({
      ...player,
      team_name: matchData.home_team,
    })),
  };

  const awayTeam = {
    teamName: matchData.away_team,
    players: (lineups[matchData.away_team] || []).map(player => ({
      ...player,
      team_name: matchData.away_team,
    })),
  };

  return (
    <div className='grid gap-6 md:grid-cols-2'>
      <TeamLineup
        teamName={homeTeam.teamName}
        players={homeTeam.players}
        onPlayerClick={onPlayerClick}
        showSubs={showSubs}
        onToggleSubs={handleToggleSubs}
        side='left'
      />
      <TeamLineup
        teamName={awayTeam.teamName}
        players={awayTeam.players}
        onPlayerClick={onPlayerClick}
        showSubs={showSubs}
        onToggleSubs={handleToggleSubs}
        side='right'
      />
    </div>
  );
};

export default MatchLineups;
