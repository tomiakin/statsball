import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Modal, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import * as api from '../services/api';
import './LeagueSelection.css';

const Home = () => {
  const [leagues, setLeagues] = useState([]);
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [seasons, setSeasons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLeagues = async () => {
      try {
        const competitionsData = await api.getCompetitions();
        // Group competitions by unique competition_id and get latest season info
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
    return (
      <Container className='d-flex justify-content-center align-items-center vh-100'>
        <div className='spinner-border text-primary' role='status'>
          <span className='visually-hidden'>Loading...</span>
        </div>
      </Container>
    );
  }

  return (
    <Container fluid className='py-5' style={{ backgroundColor: '#f8f9fa' }}>
      <h1 className='mb-5 text-center'>Select a League</h1>

      {error && (
        <div className='alert-danger alert mb-4 text-center' role='alert'>
          {error}
        </div>
      )}

      <Row className='g-4'>
        {leagues.map(league => (
          <Col key={league.id} xs={12} sm={6} md={4} lg={3}>
            <Card
              className='h-100 league-card'
              onClick={() => handleLeagueClick(league)}
              style={{
                cursor: 'pointer',
                transition: 'transform 0.2s',
                ':hover': { transform: 'scale(1.03)' },
              }}
            >
              <div className='pt-3 text-center'>
                <img
                  src={league.logoUrl}
                  alt={`${league.name} logo`}
                  className='img-fluid'
                  style={{
                    width: '100px',
                    height: '100px',
                    objectFit: 'contain',
                  }}
                />
              </div>
              <Card.Body className='text-center'>
                <Card.Title>{league.name}</Card.Title>
                <Card.Text className='text-muted'>
                  {league.country}
                  {league.international && ' • International'}
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Modal
        show={showModal}
        onHide={() => setShowModal(false)}
        centered
        size='lg'
      >
        <Modal.Header closeButton>
          <Modal.Title>{selectedLeague?.name} - Select Season</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Row className='g-3'>
            {seasons.map(season => (
              <Col key={season.season_id} xs={12} sm={6}>
                <Card
                  className='season-card h-100'
                  onClick={() => {
                    navigate(
                      `/league/${selectedLeague.id}/${season.season_id}`,
                    );
                  }}
                  style={{ cursor: 'pointer' }}
                >
                  <Card.Body className='text-center'>
                    <h5 className='mb-0'>{season.season_name}</h5>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='secondary' onClick={() => setShowModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default Home;
