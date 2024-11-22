import React, { useCallback } from 'react';

const PlayerMatchTouches = ({
  touches = [],
  onTouchClick,
  selectedTouch,
  showLabels = true,
  orientation = 'horizontal', // New prop to control orientation
}) => {
  const handleTouchClick = useCallback(
    (touch, event) => {
      if (onTouchClick) {
        event.stopPropagation();
        onTouchClick(touch);
      }
    },
    [onTouchClick],
  );

  const getTouchStyle = touch => {
    const touchColors = {
      Shot: 'rgba(59, 130, 246, 0.5)',
      assist: 'rgba(234, 179, 8, 0.5)',
      default: 'rgba(234, 179, 8, 0.5)',
    };

    const borderColors = {
      Shot: 'rgb(59, 130, 246)',
      assist: 'rgb(234, 179, 8)',
      default: 'rgb(234, 179, 8)',
    };

    return {
      fill: touchColors[touch.type] || touchColors.default,
      stroke: borderColors[touch.type] || borderColors.default,
      strokeWidth: selectedTouch === touch ? '0.4' : '0.2',
    };
  };

  const getCoordinates = touch => {
    const [originalX, originalY] = touch.location;
    if (orientation === 'vertical') {
      return {
        x: originalY,
        y: 120 - originalX, // Assuming 120 is the pitch height
      };
    }
    return {
      x: originalX,
      y: originalY,
    };
  };

  return (
    <>
      {touches.map((touch, index) => {
        const { x, y } = getCoordinates(touch);
        const touchStyle = getTouchStyle(touch);

        return (
          <g
            key={`${index}-${touch.type}-${x}-${y}`}
            onClick={e => handleTouchClick(touch, e)}
            style={{ cursor: 'pointer' }}
          >
            {selectedTouch === touch && (
              <circle
                cx={x}
                cy={y}
                r='1.5'
                fill='none'
                stroke='rgb(239, 68, 68)'
                strokeWidth='0.2'
                strokeDasharray='0.5'
              />
            )}

            <circle cx={x} cy={y} r='1' {...touchStyle} />

            {showLabels && (
              <text
                x={x}
                y={y - 1.5}
                fontSize='2'
                fill={touchStyle.stroke}
                textAnchor='middle'
                alignmentBaseline='bottom'
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

export default PlayerMatchTouches;
