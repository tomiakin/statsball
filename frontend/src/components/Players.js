import React, { useEffect, useState } from "react";
import axios from "axios";

const Players = () => {
  const [players, setPlayers] = useState([]); // State to store player data
  const [loading, setLoading] = useState(true); // State to track loading status

  useEffect(() => {
    // Fetch player data from the Django API
    const fetchPlayers = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/players/");
        setPlayers(response.data); // Store the fetched data in state
        setLoading(false); // Update loading state
      } catch (error) {
        console.error("Error fetching players:", error);
        setLoading(false); // Update loading state
      }
    };

    fetchPlayers(); // Call the fetch function when the component mounts
  }, []); // Empty dependency array means this effect runs once after the initial render

  if (loading) {
    return <div>Loading players...</div>; // Loading message while fetching data
  }

  return (
    <div>
      <h1>Football Players</h1>
      <ul>
        {players.map((player) => (
          <li key={player.id}>
            {player.name} - {player.nationality}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Players;
