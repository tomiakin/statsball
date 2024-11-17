import React, { useCallback } from 'react';

const PlayerMatchShots = ({
  shots = [],
  onShotClick,
  selectedShot,
  showLabels = true,
}) => {
  const handleShotClick = useCallback(
    (shot, event) => {
      event.stopPropagation();
      onShotClick?.(shot);
    },
    [onShotClick],
  );

  const getShotRadius = xg => {
    if (!xg) return 1;
    const xgValue = parseFloat(xg);
    if (xgValue <= 0.05) return 0.8;
    if (xgValue <= 0.15) return 1.2;
    if (xgValue <= 0.25) return 1.6;
    if (xgValue <= 0.35) return 2;
    return 2.4;
  };

  const getShotStyle = (shot, isSelected) => {
    const isGoal = shot.shot_outcome === 'Goal';
    return {
      fill: isGoal ? 'rgba(244, 63, 94, 0.6)' : 'rgba(0, 0, 0, 0.1)',
      stroke: isGoal ? 'rgb(244, 63, 94)' : '#000000',
      strokeWidth: isSelected ? '0.4' : '0.2',
      cursor: 'pointer',
    };
  };

  return (
    <>
      {shots.map((shot, index) => {
        const x = shot.location[1];
        const y = 120 - shot.location[0];
        const isSelected = selectedShot?.id === shot.id;
        const shotStyle = getShotStyle(shot, isSelected);
        const radius = getShotRadius(shot.shot_statsbomb_xg);

        return (
          <g
            key={shot.id || `${index}-${x}-${y}`}
            onClick={e => handleShotClick(shot, e)}
          >
            {/* Selection highlight */}
            {isSelected && (
              <circle
                cx={x}
                cy={y}
                r={radius + 0.5}
                fill="none"
                stroke="rgb(239, 68, 68)"
                strokeWidth="0.2"
                strokeDasharray="0.5"
              />
            )}

            {/* Shot circle */}
            <circle
              cx={x}
              cy={y}
              r={radius}
              style={shotStyle}
            />

            {/* Label */}
            {showLabels && (
              <text
                x={x}
                y={y - radius - 0.5}
                fontSize="2"
                fill={shotStyle.stroke}
                textAnchor="middle"
                alignmentBaseline="bottom"
              >
                {index + 1}
              </text>
            )}
          </g>
        );
      })}
    </>
  );
};

export default PlayerMatchShots;