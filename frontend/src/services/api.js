import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/";

// Configure axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add logging
apiClient.interceptors.request.use((request) => {
  console.log("Making request to:", request.url);
  return request;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error?.response?.data || error.message);
    throw error;
  }
);

// API functions
export const getLeagueMatches = async (leagueId, seasonId) => {
  try {
    const response = await apiClient.get(`matches/${leagueId}/${seasonId}/`);
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch matches for league ${leagueId}, season ${seasonId}:`,
      error
    );
    throw new Error("Failed to load matches");
  }
};

export const getCompetitionInfo = async (leagueId, seasonId) => {
  try {
    const response = await apiClient.get(
      `competition-info/${leagueId}/${seasonId}/`
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch competition info for league ${leagueId}, season ${seasonId}:`,
      error
    );
    throw new Error("Failed to load competition information");
  }
};

export const getCompetitions = async () => {
  try {
    const response = await apiClient.get("competitions/");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch competitions:", error);
    throw new Error("Failed to load competitions");
  }
};

export const getSeasons = async (competitionId) => {
  try {
    const response = await apiClient.get(`seasons/${competitionId}/`);
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch seasons for competition ${competitionId}:`,
      error
    );
    throw new Error("Failed to load seasons");
  }
};

export const getTouchData = async (matchId, playerName) => {
  try {
    const response = await apiClient.get(
      `touches/${matchId}/${encodeURIComponent(playerName)}/`
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch touch data for match ${matchId}, player ${playerName}:`,
      error
    );
    throw new Error("Failed to load touch data");
  }
};
