import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate
import { Container, Row, Col, Card, Table, Spinner } from 'react-bootstrap';
import * as api from '../services/api';

const TeamLineup = ({ teamName, players, onPlayerClick }) => {
  const getPlayerPosition = player => {
    if (!player.positions || player.positions.length === 0) return '-';
    const position = player.positions[0];
    return position.position || '-';
  };

  const getPlayerStatus = player => {
    if (!player.positions || player.positions.length === 0) return 'Unknown';
    const position = player.positions[0];
    if (position.start_reason === 'Starting XI') {
      return 'Starting XI';
    } else if (position.start_reason === 'Substitution - On') {
      return 'Substitute';
    }
    return position.start_reason || 'Unknown';
  };

  return (
    <Card className='mb-4'>
      <Card.Header>
        <h5 className='mb-0'>{teamName}</h5>
      </Card.Header>
      <Card.Body className='p-0'>
        <Table hover className='mb-0'>
          <thead>
            <tr>
              <th>#</th>
              <th>Player</th>
              <th>Position</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {players.map(player => (
              <tr
                key={player.player_id}
                onClick={() => onPlayerClick(player.player_name)}
              >
                <td>{player.jersey_number || '-'}</td>
                <td>{player.nickname || player.player_name}</td>
                <td>{getPlayerPosition(player)}</td>
                <td>
                  <span
                    className={
                      getPlayerStatus(player) === 'Starting XI'
                        ? 'text-success'
                        : 'text-secondary'
                    }
                  >
                    {getPlayerStatus(player)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  );
};

const MatchDetails = () => {
  const { matchId } = useParams();
  const navigate = useNavigate(); // Hook to navigate
  const [lineups, setLineups] = useState({ home: [], away: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLineups = async () => {
      try {
        setLoading(true);
        const lineupsData = await api.getMatchLineups(matchId);
        const teamNames = Object.keys(lineupsData);

        setLineups({
          home: lineupsData[teamNames[0]] || [],
          away: lineupsData[teamNames[1]] || [],
          homeTeam: teamNames[0],
          awayTeam: teamNames[1],
        });

        setError(null);
      } catch (err) {
        console.error('Error fetching lineups:', err);
        setError('Failed to load lineup data');
      } finally {
        setLoading(false);
      }
    };

    fetchLineups();
  }, [matchId]);

  const handlePlayerClick = playerName => {
    navigate(`/touches/${matchId}/${playerName}`);
  };

  if (loading) {
    return (
      <Container
        className='d-flex justify-content-center align-items-center'
        style={{ minHeight: '60vh' }}
      >
        <Spinner animation='border' variant='primary' />
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <div className='alert-danger alert mt-4'>{error}</div>
      </Container>
    );
  }

  return (
    <Container className='py-4'>
      <Card className='mb-4'>
        <Card.Header>
          <h4 className='mb-0'>Match Details</h4>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={4} className='text-center'>
              <h5>{lineups.homeTeam}</h5>
            </Col>
            <Col md={4} className='text-center'>
              <h5>vs</h5>
            </Col>
            <Col md={4} className='text-center'>
              <h5>{lineups.awayTeam}</h5>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <Row>
        <Col md={6}>
          <TeamLineup
            teamName={lineups.homeTeam}
            players={lineups.home}
            onPlayerClick={handlePlayerClick}
          />
        </Col>
        <Col md={6}>
          <TeamLineup
            teamName={lineups.awayTeam}
            players={lineups.away}
            onPlayerClick={handlePlayerClick}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default MatchDetails;
