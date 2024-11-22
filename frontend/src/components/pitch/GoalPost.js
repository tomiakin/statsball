import React from 'react';

export const GoalPostVisualization = ({ children }) => {
  const goalStroke = 'grey'; // color of posts
  const lineStroke = 'black'; // ground color
  const goalStrokeWidth = 0.4; // Stroke width of the goal frame
  const lineStrokeWidth = 0.1; // Stroke width of the ground line
  const lineBottom = 2.67 + 2.67 + goalStrokeWidth / 2; // Calculate Y post of ground line (affected by width of the goal)

  //     viewBox="30 -1 20 7" ONLY SHOWING THE SIX YARD BOX CAN LATER MAP BACK TO OG COORD TO FIND MAX HEIGHT SHOWING
  //         |<---20--->|
  // 30      36    44      50
  // |       |     |       |
  // |       ╭─────╮       |
  // |       │     │       |
  // |       │     │       |
  // |   ────┴─────┴────   |
  //     32         48

  // Y coordinate
  //    -1 ─ ─ ─ Above origin (top of view)
  //     0 ──── Origin
  //     1 ────
  //     2 ────
  //     3 ──── ╭─────╮  Goal posts start at Y=2.67
  //     4 ──── │     │
  //     5 ──── │     │  Goal posts end at Y=5.34
  //     6 ──── ┴─────┴  Ground line at Y=5.74
  //     |
  //    7 units
  //    total
  //    height

  return (
    <div className='h-[300px] w-full'>
      <svg
        viewBox='30 -1 20 7'
        className='h-full w-full'
        preserveAspectRatio='xMidYMid meet'
      >
        {/* Goal frame as a path - only top and sides */}
        <path
          d='M36 5.34 L36 2.67 L44 2.67 L44 5.34'
          fill='none'
          stroke={goalStroke}
          strokeWidth={goalStrokeWidth}
          strokeLinejoin='round'
          strokeLinecap='square'
        />

        {/* Ground line */}
        <line
          x1='30'
          y1={lineBottom}
          x2='50'
          y2={lineBottom}
          stroke={lineStroke}
          strokeWidth={lineStrokeWidth}
          strokeLinecap='square'
        />

        {children}
      </svg>
    </div>
  );
};

export default GoalPostVisualization;
