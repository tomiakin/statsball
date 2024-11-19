import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/homepage/Home';
import CompetitionOverview from './components/competition/CompetitionOverview';
import BaseLayout from './components/common/BaseLayout';
import MatchDetails from './components/match/MatchDetails';
import PlayerMatchPerformance from './components/player/PlayerMatchPerformance/PlayerMatchPerformance'
import './index.css';

function App() {
  return (
    <Router>
      <BaseLayout>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route
            path='/player-performance/:matchId/:playerName'
            element={<PlayerMatchPerformance />}
          />
          <Route
            path='/league/:competitionId/:seasonId'
            element={<CompetitionOverview />}
          />
          <Route path='/match/:matchId' element={<MatchDetails />} />
        </Routes>
      </BaseLayout>
    </Router>
  );
}

export default App;
