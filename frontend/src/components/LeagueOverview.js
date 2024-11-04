import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Table,
  Badge,
  Spinner,
} from "react-bootstrap";
import { useParams } from "react-router-dom";
import { format } from "date-fns";
import * as api from "../services/api";

const LeagueOverview = () => {
  const { leagueId, seasonId } = useParams();
  const [matches, setMatches] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [leagueInfo, setLeagueInfo] = useState(null);

  // Simple function to load data
  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // First get league info
      const leagueData = await api.getCompetitionInfo(leagueId, seasonId);
      setLeagueInfo(leagueData);

      // Small delay before next request
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Then get matches
      const matchesData = await api.getLeagueMatches(leagueId, seasonId);

      // Process matches
      const sortedMatches = matchesData
        .filter((match) => match?.match_date)
        .sort((a, b) => new Date(b.match_date) - new Date(a.match_date))
        .slice(0, 5);

      // Extract unique teams
      const uniqueTeams = Array.from(
        new Set(
          matchesData
            .filter((match) => match?.home_team && match?.away_team)
            .flatMap((match) => [match.home_team, match.away_team])
        )
      ).sort();

      setMatches(sortedMatches);
      setTeams(uniqueTeams);
    } catch (err) {
      console.error("Error loading data:", err);
      setError("Failed to load data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Add debounced effect to prevent rapid reloads
  useEffect(() => {
    if (leagueId && seasonId) {
      const timer = setTimeout(loadData, 100);
      return () => clearTimeout(timer);
    }
  }, [leagueId, seasonId]);

  if (loading) {
    return (
      <Container
        className="d-flex justify-content-center align-items-center"
        style={{ minHeight: "60vh" }}
      >
        <div className="text-center">
          <Spinner animation="border" variant="primary" />
          <p className="mt-2">Loading...</p>
        </div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-4">
        <div className="alert alert-danger">
          <p>{error}</p>
          <button className="btn btn-primary" onClick={loadData}>
            Try Again
          </button>
        </div>
      </Container>
    );
  }

  return (
    <Container className="py-4">
      {/* League Header */}
      <Card className="mb-4 bg-primary text-white">
        <Card.Body>
          <Row className="align-items-center">
            <Col>
              <h2 className="mb-0">{leagueInfo?.competition || "League"}</h2>
              <p className="mb-0 opacity-75">
                {leagueInfo?.season || "Season"}
              </p>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <Row className="g-4">
        {/* Recent Matches */}
        <Col xs={12}>
          <Card className="h-100">
            <Card.Header className="bg-light">
              <h4 className="mb-0">Recent Matches</h4>
            </Card.Header>
            <Card.Body className="p-0">
              <div className="table-responsive">
                <Table hover className="mb-0">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Home Team</th>
                      <th>Score</th>
                      <th>Away Team</th>
                      <th>Week</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {matches.map((match) => (
                      <tr
                        key={match.match_id}
                        style={{ cursor: "pointer" }}
                        onClick={() => console.log("Match clicked:", match)}
                      >
                        <td>
                          {format(new Date(match.match_date), "MMM d, yyyy")}
                          <br />
                          <small className="text-muted">{match.kick_off}</small>
                        </td>
                        <td>{match.home_team}</td>
                        <td className="text-center">
                          <strong>
                            {match.home_score} - {match.away_score}
                          </strong>
                        </td>
                        <td>{match.away_team}</td>
                        <td>Week {match.match_week || "N/A"}</td>
                        <td>
                          <Badge
                            bg={
                              match.match_status === "available"
                                ? "success"
                                : "secondary"
                            }
                          >
                            {match.match_status}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Card.Body>
          </Card>
        </Col>

        {/* Teams */}
        <Col xs={12}>
          <Card className="h-100">
            <Card.Header className="bg-light">
              <h4 className="mb-0">Teams</h4>
            </Card.Header>
            <Card.Body>
              <Row className="g-3">
                {teams.map((team) => (
                  <Col key={team} xs={12} sm={6} md={4} lg={3}>
                    <Card
                      className="h-100 team-card"
                      style={{ cursor: "pointer" }}
                      onClick={() => console.log("Team clicked:", team)}
                    >
                      <Card.Body className="text-center">
                        <div className="mb-2">
                          <img
                            src={`/api/placeholder/50/50`}
                            alt={`${team} logo`}
                            className="team-logo"
                            style={{
                              width: "50px",
                              height: "50px",
                              objectFit: "contain",
                            }}
                          />
                        </div>
                        <h6 className="mb-0">{team}</h6>
                      </Card.Body>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default LeagueOverview;
