import axios from 'axios';

const API_URL = "http://localhost:8000/api/";

export const getTouchData = async (matchId, playerName) => {
  const response = await axios.get(`${API_URL}touches/${matchId}/${playerName}/`);
  return response.data;
};
