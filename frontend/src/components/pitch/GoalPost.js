import React from 'react';

export const GoalPostVisualization = ({ children }) => {
    const goalStroke = "grey"; // color of posts
    const lineStroke = 'black'; // ground color
    const goalStrokeWidth = 0.4; // Stroke width of the goal frame
    const lineStrokeWidth = 0.1; // Stroke width of the ground line
    const lineBottom = 2.67 + 2.67 + (goalStrokeWidth)/ 2; // Calculate Y post of ground line (affected by width of the goal)
  return (
    <div className="w-full h-[300px]">
      <svg 
        viewBox="35 1 10 5"
        className="w-full h-full"
        preserveAspectRatio="xMidYMid meet"
      >
        {/* Goal frame as a path - only top and sides */}
        <path
          d="M36 5.34 L36 2.67 L44 2.67 L44 5.34"
          fill="none"
          stroke={goalStroke}
          strokeWidth={goalStrokeWidth}
          strokeLinejoin="round"
          strokeLinecap="square"
        />
        
        {/* Ground line */}
        <line 
          x1="32"
          y1={lineBottom}
          x2="48"
          y2={lineBottom}
          stroke={lineStroke}
          strokeWidth={lineStrokeWidth}
          strokeLinecap="square"
        />

        {children}
      </svg>
    </div>
  );
};

export default GoalPostVisualization;