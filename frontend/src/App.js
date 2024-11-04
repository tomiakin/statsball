import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TouchesInMatch from "./components/TouchesInMatch";
import Home from "./components/Home";
import LeagueOverview from "./components/LeagueOverview";
import ThemeProvider from "react-bootstrap/ThemeProvider";

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/league/:leagueId/:seasonId"
            element={<LeagueOverview />}
          />
          <Route
            path="/touches/:matchId/:playerName"
            element={<TouchesInMatch />}
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
