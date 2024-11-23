import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/homepage/Home';
import CompetitionOverview from './components/competition/CompetitionOverview';
import BaseLayout from './components/common/BaseLayout';
import MatchDetails from './components/match/MatchDetails';
import PlayerMatchPerformance from './components/player/PlayerMatchPerformance/PlayerMatchPerformance';
import './index.css';

function App() {
  return (
    <Router>
      <BaseLayout>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route
            path='/league/:competitionId/:seasonId'
            element={<CompetitionOverview />}
          />
          {/* Updated match route to include competition and season IDs */}
          <Route
            path='/match/:competitionId/:seasonId/:matchId'
            element={<MatchDetails />}
          />
          {/* Updated player performance route */}
          <Route
            path='/player-performance/:competitionId/:seasonId/:matchId/:playerName'
            element={<PlayerMatchPerformance />}
          />
        </Routes>
      </BaseLayout>
    </Router>
  );
}

export default App;
