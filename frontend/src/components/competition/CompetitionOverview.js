import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LoadingSpinner, ErrorMessage, EmptyState } from '../common';
import { Calendar } from 'lucide-react';
import { format } from 'date-fns';
import * as api from '../../services/api';

const CompetitionOverview = () => {
  const { competitionId, seasonId } = useParams();
  const [allMatches, setAllMatches] = useState([]);
  const [displayedMatches, setDisplayedMatches] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [leagueInfo, setLeagueInfo] = useState(null);
  const navigate = useNavigate();

  const [showAllMatches, setShowAllMatches] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [matchesPerPage] = useState(10);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const leagueData = await api.getCompetitionInfo(competitionId, seasonId);
      setLeagueInfo(leagueData);

      await new Promise(resolve => setTimeout(resolve, 500));

      const matchesData = await api.getCompetitionMatches(
        competitionId,
        seasonId,
      );
      const sortedMatches = matchesData
        .filter(match => match?.match_date)
        .sort((a, b) => new Date(b.match_date) - new Date(a.match_date));

      setAllMatches(sortedMatches);
      setDisplayedMatches(sortedMatches.slice(0, 5));

      const uniqueTeams = Array.from(
        new Set(
          matchesData
            .filter(match => match?.home_team && match?.away_team)
            .flatMap(match => [match.home_team, match.away_team]),
        ),
      ).sort();

      setTeams(uniqueTeams);
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to load data. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [competitionId, seasonId]);

  useEffect(() => {
    if (competitionId && seasonId) {
      const timer = setTimeout(loadData, 100);
      return () => clearTimeout(timer);
    }
  }, [competitionId, seasonId, loadData]);

  const indexOfLastMatch = currentPage * matchesPerPage;
  const indexOfFirstMatch = indexOfLastMatch - matchesPerPage;
  const totalPages = Math.ceil(allMatches.length / matchesPerPage);

  useEffect(() => {
    if (showAllMatches) {
      setDisplayedMatches(
        allMatches.slice(indexOfFirstMatch, indexOfLastMatch),
      );
    } else {
      setDisplayedMatches(allMatches.slice(0, 5));
    }
  }, [
    showAllMatches,
    currentPage,
    allMatches,
    indexOfFirstMatch,
    indexOfLastMatch,
  ]);

  const handlePageChange = pageNumber => {
    setCurrentPage(pageNumber);
  };

  const toggleMatchesView = () => {
    setShowAllMatches(!showAllMatches);
    setCurrentPage(1);
  };

  if (loading) {
    return <LoadingSpinner message='Loading competition data...' />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={error}
        action={{
          label: 'Try Again',
          onClick: loadData,
        }}
      />
    );
  }

  if (!allMatches.length) {
    return (
      <EmptyState
        icon={Calendar}
        title='No Matches Found'
        message='There are no matches available for this competition yet.'
      />
    );
  }

  return (
    <div className='container mx-auto py-6'>
      <div className='mb-6 rounded bg-blue-600 p-4 text-white'>
        <h2 className='text-2xl font-bold'>
          {leagueInfo?.competition || 'League'}
        </h2>
        <p className='opacity-80'>{leagueInfo?.season || 'Season'}</p>
      </div>

      <div className='mb-6 rounded bg-white shadow'>
        <div className='flex items-center justify-between rounded-t bg-gray-100 p-4'>
          <h4 className='text-xl font-semibold'>
            {showAllMatches ? 'All Matches' : 'Recent Matches'}
          </h4>
          <button
            className='rounded border border-blue-500 px-3 py-1 text-blue-500 hover:bg-blue-500 hover:text-white'
            onClick={toggleMatchesView}
          >
            {showAllMatches ? 'Show Recent Matches' : 'View All Matches'}
          </button>
        </div>
        <div className='overflow-x-auto'>
          <table className='min-w-full divide-y divide-gray-200'>
            <thead className='bg-gray-50'>
              <tr>
                <th className='px-6 py-3 text-left text-xs font-medium uppercase text-gray-500'>
                  Date
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium uppercase text-gray-500'>
                  Home Team
                </th>
                <th className='px-6 py-3 text-center text-xs font-medium uppercase text-gray-500'>
                  Score
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium uppercase text-gray-500'>
                  Away Team
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium uppercase text-gray-500'>
                  Week
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium uppercase text-gray-500'>
                  Status
                </th>
              </tr>
            </thead>
            <tbody className='divide-y divide-gray-200 bg-white'>
              {displayedMatches.map(match => (
                <tr
                  key={match.match_id}
                  className='cursor-pointer hover:bg-gray-100'
                  onClick={() => navigate(`/match/${match.match_id}`)}
                >
                  <td className='px-6 py-4'>
                    {format(new Date(match.match_date), 'MMM d, yyyy')}
                    <br />
                    <span className='text-xs text-gray-500'>
                      {match.kick_off}
                    </span>
                  </td>
                  <td className='px-6 py-4'>{match.home_team}</td>
                  <td className='px-6 py-4 text-center font-semibold'>
                    {match.home_score} - {match.away_score}
                  </td>
                  <td className='px-6 py-4'>{match.away_team}</td>
                  <td className='px-6 py-4'>
                    Week {match.match_week || 'N/A'}
                  </td>
                  <td className='px-6 py-4'>
                    <span
                      className={`rounded px-2 py-1 ${
                        match.match_status === 'available'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {match.match_status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {showAllMatches && totalPages > 1 && (
          <div className='flex justify-center p-4'>
            <div className='flex gap-2'>
              {[...Array(totalPages)].map((_, index) => (
                <button
                  key={index + 1}
                  onClick={() => handlePageChange(index + 1)}
                  className={`rounded px-3 py-1 ${
                    currentPage === index + 1
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 hover:bg-gray-300'
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className='rounded bg-white shadow'>
        <div className='rounded-t bg-gray-100 p-4'>
          <h4 className='text-xl font-semibold'>Teams</h4>
        </div>
        <div className='grid gap-4 p-4 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-5'>
          {teams.map(team => (
            <div
              key={team}
              className='cursor-pointer rounded-lg bg-white p-4 text-center shadow hover:bg-gray-100'
              onClick={() => console.log('Team clicked:', team)}
            >
              <img
                src='/api/placeholder/50/50'
                alt={`${team} logo`}
                className='mx-auto mb-2 h-12 w-12'
              />
              <h6 className='text-sm font-medium'>{team}</h6>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CompetitionOverview;
