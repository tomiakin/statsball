import React, { useCallback } from 'react';

const PlayerMatchShots = ({
  shots = [],
  onShotClick,
  selectedShot,
  showLabels = true,
  orientation = 'vertical'
}) => {
  const handleShotClick = useCallback(
    (shot, event) => {
      event.stopPropagation();
      onShotClick?.(shot);
    },
    [onShotClick]
  );

  const getShotRadius = (xg, isGoalView) => {
    if (isGoalView) {
      return 0.2; // Smaller, fixed size for goal view
    }
    
    if (!xg) return 1;
    const xgValue = parseFloat(xg);
    if (xgValue <= 0.05) return 0.8;
    if (xgValue <= 0.15) return 1.2;
    if (xgValue <= 0.25) return 1.6;
    if (xgValue <= 0.35) return 2;
    return 2.4;
  };

  const getShotStyle = (shot, isSelected, isGoalView) => {
    const isGoal = shot.shot_outcome === 'Goal';
    return {
      fill: isGoal ? 'rgba(244, 63, 94, 0.6)' : 'rgba(0, 0, 0, 0.1)',
      stroke: isGoal ? '#000000' : '#000000',
      strokeWidth: isSelected ? (isGoalView ? '0.1' : '0.4') : (isGoalView ? '0.05' : '0.2'),
      cursor: 'pointer',
    };
  };

  const mapRange = (value, a, b, c, d) => {
    return c + (value - a) * (d - c) / (b - a);
  };

  const getCoordinates = (location, isEndLocation = false) => {
    if (!location) return { x: 0, y: 0 };
    
    const [originalX, originalY, originalZ] = location;
    
    if (orientation === 'goalview' && isEndLocation) {
      return {
        x: originalY,
        y: originalZ !== undefined ? mapRange(originalZ, 0, 5.34, 5.34, 0) : 0
      };
    }
    
    if (orientation === 'vertical') {
      return {
        x: originalY,
        y: 120 - originalX
      };
    }
    
    return {
      x: originalX,
      y: originalY
    };
  };

  const getLineStartPoint = (start, end, radius, isSelected) => {
    const startCoord = getCoordinates(start);
    const endCoord = getCoordinates(end);
    
    const dx = endCoord.x - startCoord.x;
    const dy = endCoord.y - startCoord.y;
    const length = Math.sqrt(dx * dx + dy * dy);
    const totalRadius = radius + (isSelected ? 0.5 : 0);

    return {
      x: startCoord.x + (dx / length) * totalRadius,
      y: startCoord.y + (dy / length) * totalRadius,
    };
  };

  return (
    <>
      {shots.map((shot, index) => {
        const isGoalView = orientation === 'goalview';
        const coords = isGoalView 
          ? getCoordinates(shot.shot_end_location, true)
          : getCoordinates(shot.location);
        
        const isSelected = selectedShot?.id === shot.id;
        const shotStyle = getShotStyle(shot, isSelected, isGoalView);
        const radius = getShotRadius(shot.shot_statsbomb_xg, isGoalView);

        // Skip shots without end location for goalview
        if (isGoalView && !shot.shot_end_location) {
          return null;
        }

        return (
          <g
            key={shot.id || `${index}-${coords.x}-${coords.y}`}
            onClick={e => handleShotClick(shot, e)}
          >
            {isSelected && (
              <circle
                cx={coords.x}
                cy={coords.y}
                r={radius + (isGoalView ? 0.14 : 0.6)}
                fill="none"
                stroke="rgb(255, 0, 0)"
                strokeWidth={isGoalView ? "0.1" : "0.4"}
              />
            )}

            <circle 
              cx={coords.x} 
              cy={coords.y} 
              r={radius} 
              style={shotStyle} 
            />

            {showLabels && !isGoalView && (
              <text
                x={coords.x}
                y={coords.y - radius - 0.5}
                fontSize="2"
                fill={shotStyle.stroke}
                textAnchor="middle"
                alignmentBaseline="bottom"
              >
                {index + 1}
              </text>
            )}

            {/* Only show trajectory line for pitch views, not goalview */}
            {isSelected && shot.shot_end_location && !isGoalView && (
              <line
                x1={getLineStartPoint(
                  shot.location,
                  shot.shot_end_location,
                  radius,
                  true
                ).x}
                y1={getLineStartPoint(
                  shot.location,
                  shot.shot_end_location,
                  radius,
                  true
                ).y}
                x2={getCoordinates(shot.shot_end_location).x}
                y2={getCoordinates(shot.shot_end_location).y}
                stroke="rgb(255, 0, 0)"
                strokeWidth="0.4"
              />
            )}
          </g>
        );
      })}
    </>
  );
};

export default PlayerMatchShots;