import React, { useCallback } from 'react';
import './FootballPitch.css';

const PitchWithTouches = ({ touches = [], onTouchClick, selectedTouch }) => {
  const handleTouchClick = useCallback(
    (touch) => {
      if (onTouchClick) {
        onTouchClick(touch);
      }
    },
    [onTouchClick]
  );

  const getTouchStyle = (touch) => {
    const xPercent = (touch.location[0] / 120) * 100;
    const yPercent = (touch.location[1] / 80) * 100;

    const touchColors = {
      Shot: 'rgb(59 130 246 / 0.5)', // blue-500 with 50% opacity
      assist: 'rgb(234 179 8 / 0.5)', // yellow-500 with 50% opacity
      default: 'rgb(234 179 8 / 0.5)', // yellow-500 with 50% opacity
    };

    const borderColors = {
      Shot: 'rgb(59 130 246)', // solid blue-500
      assist: 'rgb(234 179 8)', // solid yellow-500
      default: 'rgb(234 179 8)', // solid yellow-500
    };

    const touchColor = touchColors[touch.type] || touchColors.default;
    const borderColor = borderColors[touch.type] || borderColors.default;

    return {
      left: `${xPercent}%`,
      top: `${yPercent}%`,
      backgroundColor: touchColor,
      border: `1px solid ${borderColor}`,
      outline: selectedTouch === touch ? '2px solid rgb(239 68 68)' : 'none',
      outlineOffset: '2px',
    };
  };

  return (
    <div className="pitch-container">
      <div className="field">
        {/* Field Markings */}
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
        {touches.map((touch, index) => (
          <div
            key={`${index}-${touch.type}-${touch.location.join('-')}`}
            className="absolute h-3 w-3 -translate-x-1/2 -translate-y-1/2 cursor-pointer rounded-full transition-all"
            style={getTouchStyle(touch)}
            onClick={() => handleTouchClick(touch)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                handleTouchClick(touch);
              }
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default PitchWithTouches;