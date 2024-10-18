import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Players from "./components/Players";
import PremierLeagueStandings from "./components/PremierLeagueStandings";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<h1>Welcome to the Football API</h1>} />
        <Route path="/players" element={<Players />} />
        <Route path="/home" element={<PremierLeagueStandings />} />
      </Routes>
    </Router>
  );
}

export default App;
