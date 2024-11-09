import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TouchesInMatch from './components/TouchesInMatch';
import Home from './components/Home';
import LeagueOverview from './components/LeagueOverview';
import MatchDetails from './components/MatchDetails';
import BaseLayout from './components/BaseLayout';
import './index.css';
// import ThemeProvider from 'react-bootstrap/ThemeProvider';

// import './App.css'; // Make sure this imports Tailwind styles from App.css

function App() {
  return (
    // <ThemeProvider>
    <Router>
      {/* <Navigation /> */}
      <Routes>
        <Route path='/base' element={<BaseLayout />} />
        <Route path='/' element={<Home />} />
        <Route
          path='/league/:leagueId/:seasonId'
          element={<LeagueOverview />}
        />
        <Route path='/match/:matchId' element={<MatchDetails />} />
        <Route
          path='/touches/:matchId/:playerName'
          element={<TouchesInMatch />}
        />
      </Routes>
    </Router>
    // </ThemeProvider>
  );
}

export default App;
