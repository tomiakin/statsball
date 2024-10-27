// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Players from "./components/Players";
import PremierLeagueStandings from "./components/PremierLeagueStandings";
import TouchesInMatch from "./components/TouchesInMatch"; // Importing TouchesInMatch component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<h1>Welcome to the Football API</h1>} />
        <Route path="/players" element={<Players />} />
        <Route path="/home" element={<PremierLeagueStandings />} />
        <Route path="/touches/:matchId/:playerName" element={<TouchesInMatch />} /> {/* Route for touches */}
      </Routes>
    </Router>
  );
}

export default App;


