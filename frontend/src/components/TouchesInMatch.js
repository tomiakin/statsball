import React, { useEffect, useState, useCallback } from "react";
import { Card, Container, Alert } from "react-bootstrap";
import { useParams } from "react-router-dom";
import * as api from "../services/api";
import "./FootballPitch.css";

const TouchesInMatch = () => {
  const { matchId, playerName } = useParams();
  const [touches, setTouches] = useState([]);
  const [selectedTouch, setSelectedTouch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTouchData = useCallback(async () => {
    if (!matchId || !playerName) {
      setError("Match ID or player name is missing");
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setSelectedTouch(null); // Clear selected touch when fetching new data
      setTouches([]); // Clear existing touches

      const data = await api.getTouchData(matchId, playerName);
      setTouches(data);
      setError(null);
    } catch (error) {
      setError("Failed to load touch data. Please try again.");
      setTouches([]);
    } finally {
      setLoading(false);
    }
  }, [matchId, playerName]);

  useEffect(() => {
    fetchTouchData();

    // Cleanup function
    return () => {
      setTouches([]);
      setSelectedTouch(null);
    };
  }, [fetchTouchData]);

  const handleTouchClick = useCallback((touch) => {
    setSelectedTouch((prev) => (prev === touch ? null : touch));
  }, []);

  return (
    <Container className="mt-4">
      <Card className="shadow-sm">
        <Card.Header className="bg-primary text-white">
          <h4 className="mb-0">Player Touches - {playerName}</h4>
        </Card.Header>
        <Card.Body>
          {error && (
            <Alert variant="danger" className="mb-3">
              {error}
            </Alert>
          )}

          <div className="pitch-container">
            <div className="field">
              {/* Field markings */}
              <div className="center-circle" />
              <div className="center-spot" />
              <div className="half-line" />
              <div className="penalty-area left" />
              <div className="penalty-area right" />
              <div className="goal-area left" />
              <div className="goal-area right" />
              <div className="penalty-spot left" />
              <div className="penalty-spot right" />
              <div className="goal left" />
              <div className="goal right" />
              <div className="corner-arc top-left" />
              <div className="corner-arc top-right" />
              <div className="corner-arc bottom-left" />
              <div className="corner-arc bottom-right" />

              {/* Touch markers */}
              {!loading &&
                touches.map((touch, index) => {
                  const xPercent = (touch.location[0] / 120) * 100;
                  const yPercent = (touch.location[1] / 80) * 100;

                  return (
                    <div
                      key={`${index}-${touch.type}-${touch.location.join("-")}`}
                      className={`marker ${
                        selectedTouch === touch ? "selected" : ""
                      }`}
                      style={{
                        left: `${xPercent}%`,
                        top: `${yPercent}%`,
                      }}
                      onClick={() => handleTouchClick(touch)}
                      role="button"
                      tabIndex={0}
                      onKeyPress={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          handleTouchClick(touch);
                        }
                      }}
                    />
                  );
                })}
            </div>

            {loading && (
              <div className="text-center my-4">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
              </div>
            )}

            {selectedTouch && (
              <Card className="info-box mt-3">
                <Card.Body>
                  <h5 className="mb-3">Touch Information</h5>
                  <p className="mb-2">
                    <strong>Type:</strong> {selectedTouch.type}
                  </p>
                  <p className="mb-0">
                    <strong>Location:</strong>
                    {` X: ${selectedTouch.location[0].toFixed(
                      1
                    )}, Y: ${selectedTouch.location[1].toFixed(1)}`}
                  </p>
                </Card.Body>
              </Card>
            )}
          </div>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default TouchesInMatch;
