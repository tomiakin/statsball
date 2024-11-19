import React, { useCallback } from 'react';

const PlayerMatchTouches = ({
  touches = [],
  onTouchClick,
  selectedTouch,
  showLabels = true,
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
      Shot: 'rgba(59, 130, 246, 0.5)', // blue-500 with 50% opacity
      assist: 'rgba(234, 179, 8, 0.5)', // yellow-500 with 50% opacity
      default: 'rgba(234, 179, 8, 0.5)', // yellow-500 with 50% opacity
    };

    const borderColors = {
      Shot: 'rgb(59, 130, 246)', // solid blue-500
      assist: 'rgb(234, 179, 8)', // solid yellow-500
      default: 'rgb(234, 179, 8)', // solid yellow-500
    };

    return {
      fill: touchColors[touch.type] || touchColors.default,
      stroke: borderColors[touch.type] || borderColors.default,
      strokeWidth: selectedTouch === touch ? '0.4' : '0.2',
    };
  };

  return (
    <>
      {touches.map((touch, index) => {
        const [x, y] = touch.location;
        const touchStyle = getTouchStyle(touch);

        return (
          <g
            key={`${index}-${touch.type}-${x}-${y}`}
            onClick={e => handleTouchClick(touch, e)}
            style={{ cursor: 'pointer' }}
          >
            {/* Selection highlight circle */}
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

            {/* Touch point */}
            <circle cx={x} cy={y} r='1' {...touchStyle} />

            {/* Label */}
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
