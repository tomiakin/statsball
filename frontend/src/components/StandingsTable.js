// src/components/StandingsTable.js
import React from "react";

const StandingsTable = ({ standings }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Position</th>
          <th>Team</th>
          <th>Played</th>
          <th>Won</th>
          <th>Draw</th>
          <th>Lost</th>
          <th>Points</th>
          <th>Goal Difference</th>
        </tr>
      </thead>
      <tbody>
        {standings.map((team, index) => (
          <tr key={index}>
            <td>{team.position}</td>
            <td>
              <img
                src={team.team.crest}
                alt={team.team.name}
                style={{ width: "30px", marginRight: "10px" }}
              />
              {team.team.name}
            </td>
            <td>{team.playedGames}</td>
            <td>{team.won}</td>
            <td>{team.draw}</td>
            <td>{team.lost}</td>
            <td>{team.points}</td>
            <td>{team.goalDifference}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default StandingsTable;
