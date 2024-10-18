// src/components/PremierLeagueStandings.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import StandingsTable from "./StandingsTable";

const PremierLeagueStandings = () => {
  const [standings, setStandings] = useState([]);
  const [standingType, setStandingType] = useState("TOTAL");

  useEffect(() => {
    fetchStandings(standingType);
  }, [standingType]);

  const fetchStandings = async (type) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/standings/${type}/`
      );
      setStandings(response.data.standings);
    } catch (error) {
      console.error("Error fetching standings:", error);
    }
  };

  return (
    <div>
      <h1>Premier League Standings</h1>
      <div>
        <button onClick={() => setStandingType("TOTAL")}>Total</button>
        <button onClick={() => setStandingType("HOME")}>Home</button>
        <button onClick={() => setStandingType("AWAY")}>Away</button>
      </div>
      <StandingsTable standings={standings} />
    </div>
  );
};

export default PremierLeagueStandings;
