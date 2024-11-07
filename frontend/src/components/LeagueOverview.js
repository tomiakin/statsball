import React, { useState, useEffect, useCallback } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Table,
  Badge,
  Spinner,
  Button,
  Pagination,
} from "react-bootstrap";
import { useParams, useNavigate } from "react-router-dom";
import { format } from "date-fns";
import * as api from "../services/api";

const LeagueOverview = () => {
  const { leagueId, seasonId } = useParams();
  const [allMatches, setAllMatches] = useState([]); // Store all matches
  const [displayedMatches, setDisplayedMatches] = useState([]); // Matches currently shown
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [leagueInfo, setLeagueInfo] = useState(null);
  const navigate = useNavigate();

  // Pagination states
  const [showAllMatches, setShowAllMatches] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [matchesPerPage] = useState(10);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const leagueData = await api.getCompetitionInfo(leagueId, seasonId);
      setLeagueInfo(leagueData);

      await new Promise((resolve) => setTimeout(resolve, 500));

      const matchesData = await api.getLeagueMatches(leagueId, seasonId);

      // Sort matches by date
      const sortedMatches = matchesData
        .filter((match) => match?.match_date)
        .sort((a, b) => new Date(b.match_date) - new Date(a.match_date));

      setAllMatches(sortedMatches);

      // Set initial displayed matches (last 5)
      setDisplayedMatches(sortedMatches.slice(0, 5));

      // Process teams
      const uniqueTeams = Array.from(
        new Set(
          matchesData
            .filter((match) => match?.home_team && match?.away_team)
            .flatMap((match) => [match.home_team, match.away_team])
        )
      ).sort();

      setTeams(uniqueTeams);
    } catch (err) {
      console.error("Error loading data:", err);
      setError("Failed to load data. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [leagueId, seasonId]);

  useEffect(() => {
    if (leagueId && seasonId) {
      const timer = setTimeout(loadData, 100);
      return () => clearTimeout(timer);
    }
  }, [leagueId, seasonId, loadData]);

  // Calculate pagination
  const indexOfLastMatch = currentPage * matchesPerPage;
  const indexOfFirstMatch = indexOfLastMatch - matchesPerPage;
  const totalPages = Math.ceil(allMatches.length / matchesPerPage);

  // Update displayed matches when pagination or view mode changes
  useEffect(() => {
    if (showAllMatches) {
      setDisplayedMatches(
        allMatches.slice(indexOfFirstMatch, indexOfLastMatch)
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

  // Handle page change
  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  // Toggle between all matches and recent matches
  const toggleMatchesView = () => {
    setShowAllMatches(!showAllMatches);
    setCurrentPage(1); // Reset to first page when toggling
  };

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center vh-100">
        <Spinner animation="border" variant="primary" />
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-4">
        <div className="alert alert-danger">
          <p>{error}</p>
          <Button variant="primary" onClick={loadData}>
            Try Again
          </Button>
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

      {/* Matches Section */}
      <Row className="g-4">
        <Col xs={12}>
          <Card className="h-100">
            <Card.Header className="bg-light d-flex justify-content-between align-items-center">
              <h4 className="mb-0">
                {showAllMatches ? "All Matches" : "Recent Matches"}
              </h4>
              <Button
                variant="outline-primary"
                onClick={toggleMatchesView}
                className="float-end"
              >
                {showAllMatches ? "Show Recent Matches" : "View All Matches"}
              </Button>
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
                    {displayedMatches.map((match) => (
                      <tr
                        key={match.match_id}
                        style={{ cursor: "pointer" }}
                        onClick={() => navigate(`/match/${match.match_id}`)}
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

              {/* Pagination */}
              {showAllMatches && totalPages > 1 && (
                <div className="d-flex justify-content-center p-3">
                  <Pagination>
                    <Pagination.First
                      onClick={() => handlePageChange(1)}
                      disabled={currentPage === 1}
                    />
                    <Pagination.Prev
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                    />

                    {[...Array(totalPages)].map((_, index) => (
                      <Pagination.Item
                        key={index + 1}
                        active={currentPage === index + 1}
                        onClick={() => handlePageChange(index + 1)}
                      >
                        {index + 1}
                      </Pagination.Item>
                    ))}

                    <Pagination.Next
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === totalPages}
                    />
                    <Pagination.Last
                      onClick={() => handlePageChange(totalPages)}
                      disabled={currentPage === totalPages}
                    />
                  </Pagination>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>

        {/* Keep your existing Teams section */}
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
