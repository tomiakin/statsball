import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoadingSpinner, ErrorMessage } from '../common';
import * as api from '../../services/api';

const Home = () => {
  const [leagues, setLeagues] = useState([]);
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [seasons, setSeasons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const modalRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLeagues = async () => {
      try {
        const competitionsData = await api.getCompetitions();
        const uniqueLeagues = Object.values(
          competitionsData.reduce((acc, comp) => {
            if (
              !acc[comp.competition_id] ||
              new Date(comp.season_name) >
                new Date(acc[comp.competition_id].season_name)
            ) {
              acc[comp.competition_id] = {
                id: comp.competition_id,
                name: comp.competition_name,
                country: comp.country_name,
                gender: comp.competition_gender,
                international: comp.competition_international,
                logoUrl: `/api/placeholder/100/100`,
              };
            }
            return acc;
          }, {}),
        ).sort((a, b) => a.name.localeCompare(b.name));

        setLeagues(uniqueLeagues);
        setError(null);
      } catch (err) {
        setError('Failed to load leagues');
      } finally {
        setLoading(false);
      }
    };

    fetchLeagues();
  }, []);

  useEffect(() => {
    const handleClickOutside = event => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        setShowModal(false);
      }
    };

    if (showModal) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showModal]);

  const handleLeagueClick = async league => {
    try {
      const seasonsData = await api.getSeasons(league.id);
      const sortedSeasons = seasonsData.sort(
        (a, b) => new Date(b.season_name) - new Date(a.season_name),
      );
      setSeasons(sortedSeasons);
      setSelectedLeague(league);
      setShowModal(true);
      setError(null);
    } catch (err) {
      setError('Failed to load seasons for this league');
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading leagues..." />;
  }

  if (error) {
    return (
      <ErrorMessage 
        message={error} 
        action={{
          label: 'Try Again',
          onClick: () => window.location.reload()
        }}
      />
    );
  }

  return (
    <div className='container mx-auto bg-gray-100 py-8'>
      <h1 className='mb-6 text-center text-3xl font-semibold'>
        Select a League
      </h1>

      {error && (
        <div className='mb-6 rounded border border-red-400 bg-red-100 px-4 py-3 text-center text-red-700'>
          {error}
        </div>
      )}

      <div className='grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4'>
        {leagues.map(league => (
          <div
            key={league.id}
            className='transform cursor-pointer rounded-lg bg-white p-6 text-center shadow-lg transition-transform hover:scale-105'
            onClick={() => handleLeagueClick(league)}
          >
            <img
              src={league.logoUrl}
              alt={`${league.name} logo`}
              className='mx-auto mb-4 h-24 w-24 object-contain'
            />
            <h3 className='text-xl font-semibold'>{league.name}</h3>
            <p className='text-gray-500'>
              {league.country} {league.international && '• International'}
            </p>
          </div>
        ))}
      </div>

      {showModal && (
        <div className='fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50'>
          <div
            ref={modalRef}
            className='w-full max-w-lg overflow-hidden rounded-lg bg-white shadow-lg'
          >
            <div className='flex items-center justify-between border-b p-4'>
              <h2 className='text-xl font-semibold'>
                {selectedLeague?.name} - Select Season
              </h2>
              <button
                className='text-gray-500 hover:text-gray-700'
                onClick={() => setShowModal(false)}
              >
                &times;
              </button>
            </div>
            <div className='p-6'>
              <div className='grid gap-4 sm:grid-cols-2'>
                {seasons.map(season => (
                  <div
                    key={season.season_id}
                    className='cursor-pointer rounded-lg bg-gray-100 p-4 text-center hover:bg-gray-200'
                    onClick={() =>
                      navigate(
                        `/league/${selectedLeague.id}/${season.season_id}`,
                      )
                    }
                  >
                    <h3 className='text-lg'>{season.season_name}</h3>
                  </div>
                ))}
              </div>
            </div>
            <div className='border-t p-4 text-right'>
              <button
                className='rounded-lg bg-gray-200 px-4 py-2 hover:bg-gray-300'
                onClick={() => setShowModal(false)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
