import { useState, useEffect } from 'react';
import { STAT_TYPES } from '../config/statTypes';
import * as api from '../../../../services/api';

export const useStatData = (matchId, playerName, selectedStat) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!matchId || !playerName) {
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        let result;
        
        switch (selectedStat) {
          case STAT_TYPES.SUMMARY: {
            const touchesData = await api.getPlayerMatchTouches(matchId, playerName);
            result = { 
              touches: touchesData 
            };
            break;
          }
            
          case STAT_TYPES.SHOOTING: {
            result = await api.getPlayerMatchShooting(matchId, playerName);
            break;
          }
            
          case STAT_TYPES.PASSING: {
            const passingData = await api.getPlayerMatchPassing(matchId, playerName);
            result = { 
              passes: passingData 
            };
            break;
          }
            
          case STAT_TYPES.DEFENDING: {
            const defendingData = await api.getPlayerMatchDefending(matchId, playerName);
            result = { 
              actions: defendingData 
            };
            break;
          }
            
          default:
            throw new Error(`Invalid stat type: ${selectedStat}`);
        }

        setData(result);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message || 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [matchId, playerName, selectedStat]);

  return {
    data,
    loading,
    error,
    refresh: () => {
      setData(null);
      setLoading(true);
    }
  };
};