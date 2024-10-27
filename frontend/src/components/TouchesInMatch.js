import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './FootballPitch.css'; // Import the new CSS

const TouchesInMatch = () => {
    const { matchId, playerName } = useParams();
    const [touches, setTouches] = useState([]);
    const [selectedTouch, setSelectedTouch] = useState(null);

    useEffect(() => {
        const fetchTouchData = async () => {
            if (!matchId || !playerName) {
                console.error('matchId or playerName is undefined');
                return;
            }
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/touches/${matchId}/${encodeURIComponent(playerName)}/`);
                setTouches(response.data);
            } catch (error) {
                console.error('Error fetching touch data:', error);
            }
        };

        fetchTouchData();
    }, [matchId, playerName]);

    const handleTouchClick = (touch) => {
        setSelectedTouch(touch);
    };

    return (
        <div className="pitch-container">
            {/* Render the soccer field */}
            <div className="field">
                <div className="center-circle"></div>
                <div className="center-spot"></div>
                <div className="half-line"></div>
                <div className="penalty-area left"></div>
                <div className="penalty-area right"></div>
                <div className="penalty-spot left"></div>
                <div className="penalty-spot right"></div>
                <div className="goal-area left"></div>
                <div className="goal-area right"></div>
                <div className="goal left"></div>
                <div className="goal right"></div>
                <div className="corner-arc top-left"></div>
                <div className="corner-arc top-right"></div>
                <div className="corner-arc bottom-left"></div>
                <div className="corner-arc bottom-right"></div>

                {/* Render touch markers */}
                {touches.map((touch, index) => {
                    const xPercent = (touch.location[0] / 120) * 100;
                    const yPercent = (touch.location[1] / 80) * 100;

                    return (
                        <div
                            key={index}
                            className="marker"
                            style={{
                                left: `${xPercent}%`,
                                top: `${yPercent}%`,
                            }}
                            onClick={() => handleTouchClick(touch)}
                        />
                    );
                })}
            </div>

            {/* Display touch information when a marker is clicked */}
            {selectedTouch && (
                <div className="info-box">
                    <h3>Touch Information</h3>
                    <p>Type: {selectedTouch.type}</p>
                    <p>Location: {selectedTouch.location.join(', ')}</p>
                </div>
            )}
        </div>
    );
};

export default TouchesInMatch;
