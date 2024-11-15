import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

// Configure axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add logging
apiClient.interceptors.request.use(request => {
  console.log('Making request to:', request.url);
  return request;
});

apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error?.response?.data || error.message);
    throw error;
  },
);

// =====================================
// Competition & Season Related Endpoints
// =====================================

export const getCompetitions = async () => {
  try {
    const response = await apiClient.get('competitions/');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch competitions:', error);
    throw new Error('Failed to load competitions');
  }
};

export const getSeasons = async competitionId => {
  try {
    const response = await apiClient.get(`seasons/${competitionId}/`);
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch seasons for competition ${competitionId}:`,
      error,
    );
    throw new Error('Failed to load seasons');
  }
};

export const getCompetitionInfo = async (competitionId, seasonId) => {
  try {
    const response = await apiClient.get(
      `competition-info/${competitionId}/${seasonId}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch competition info for competition ${competitionId}, season ${seasonId}:`,
      error,
    );
    throw new Error('Failed to load competition information');
  }
};

export const getCompetitionMatches = async (competitionId, seasonId) => {
  try {
    const response = await apiClient.get(
      `matches/${competitionId}/${seasonId}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch matches for competition ${competitionId}, season ${seasonId}:`,
      error,
    );
    throw new Error('Failed to load matches');
  }
};

// =====================================
// Match Related Endpoints
// =====================================

export const getMatchInfo = async matchId => {
  try {
    const response = await apiClient.get(`match-info/${matchId}/`);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch match info for match ${matchId}:`, error);
    throw new Error('Failed to load match information');
  }
};

export const getMatchLineups = async matchId => {
  try {
    const response = await apiClient.get(`match-lineups/${matchId}/`);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch lineups for match ${matchId}:`, error);
    throw new Error('Failed to load match lineups');
  }
};

// =====================================
// Player Match Performance Endpoints
// =====================================

export const getPlayerMatchTouches = async (matchId, playerName) => {
  try {
    const response = await apiClient.get(
      `player-match-touches/${matchId}/${encodeURIComponent(playerName)}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch touch data for match ${matchId}, player ${playerName}:`,
      error,
    );
    throw new Error('Failed to load player touch data');
  }
};

export const getPlayerMatchPassing = async (matchId, playerName) => {
  try {
    const response = await apiClient.get(
      `player-match-passing/${matchId}/${encodeURIComponent(playerName)}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch passing data for match ${matchId}, player ${playerName}:`,
      error,
    );
    throw new Error('Failed to load player passing data');
  }
};

export const getPlayerMatchShooting = async (matchId, playerName) => {
  try {
    const response = await apiClient.get(
      `player-match-shooting/${matchId}/${encodeURIComponent(playerName)}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch shooting data for match ${matchId}, player ${playerName}:`,
      error,
    );
    throw new Error('Failed to load player shooting data');
  }
};

export const getPlayerMatchDefending = async (matchId, playerName) => {
  try {
    const response = await apiClient.get(
      `player-match-def/${matchId}/${encodeURIComponent(playerName)}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch defending data for match ${matchId}, player ${playerName}:`,
      error,
    );
    throw new Error('Failed to load player defending data');
  }
};

export const getPlayerMatchPossession = async (matchId, playerName) => {
  try {
    const response = await apiClient.get(
      `player-match-poss/${matchId}/${encodeURIComponent(playerName)}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch possession data for match ${matchId}, player ${playerName}:`,
      error,
    );
    throw new Error('Failed to load player possession data');
  }
};

export const getGoalkeeperMatchStats = async (matchId, playerName) => {
  try {
    const response = await apiClient.get(
      `player-gk/${matchId}/${encodeURIComponent(playerName)}/`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Failed to fetch goalkeeper data for match ${matchId}, player ${playerName}:`,
      error,
    );
    throw new Error('Failed to load goalkeeper data');
  }
};
