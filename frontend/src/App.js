import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import LeagueOverview from './components/LeagueOverview';
import BaseLayout from './components/BaseLayout';
import MatchDetails from './components/MatchDetails';
import PlayerPerformance from './components/PlayerPerformance';
import './index.css';

import SoccerPitch from './components/SoccerPitch';

function App() {
  return (
    <Router>
      <BaseLayout>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route
            path='/player-performance/:matchId/:playerName'
            element={<PlayerPerformance />}
          />
          <Route
            path='/league/:leagueId/:seasonId'
            element={<LeagueOverview />}
          />
          <Route path='/match/:matchId' element={<MatchDetails />} />
          <Route path='/soccerpitch' element={<SoccerPitch />} />
        </Routes>
      </BaseLayout>
    </Router>
  );
}

export default App;
