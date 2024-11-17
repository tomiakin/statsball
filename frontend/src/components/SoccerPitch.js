import React from 'react';

// Main soccer pitch component - accepts children for overlays and click handler
const SoccerPitch = ({ children, onPitchClick }) => {
  return (
    // CONTAINER DIV:
    // - relative: needed for absolute SVG positioning
    // - aspect-[3/2]: forces width:height ratio of 3:2
    // - w-full: takes full width of parent
    // - max-w-3xl: limits max width to 768px (change to max-w-xl for smaller)
    <div className='relative aspect-[3/2] w-full max-w-3xl border-2 border-slate-400 bg-white'>
      {/* SVG ELEMENT:
          viewBox='-6 -4 132 88' breaks down as:
          - -6: adds 6 units padding on left
          - -4: adds 4 units padding on top
          - 132: total width (120 pitch + 6 left + 6 right padding)
          - 88: total height (80 pitch + 4 top + 4 bottom padding)
      */}
      <svg
        viewBox='-2 -2 124 84'
        // SVG positioning: absolute + inset-0 makes it fill container
        className='absolute inset-0 h-full w-full'
        // Basic SVG styling: thin grey lines, no fill
        style={{
          strokeWidth: '0.2',
          stroke: '#CBD5E1',
          fill: 'none',
        }}
        onClick={onPitchClick}
      >
        {/* PITCH ELEMENTS:
            - Pitch is 120x80 units total
            - (0,0) is top-left corner
            - (120,80) is bottom-right corner
        */}
        {/* Outer border */}
        <rect x='0' y='0' width='120' height='80' />

        {/* Halfway line */}
        <line x1='60' y1='0' x2='60' y2='80' />

        {/* Center circle */}
        <circle cx='60' cy='40' r='10' />
        <circle cx='60' cy='40' r='0.3' fill='#CBD5E1' />

        {/* Left penalty area */}
        <rect x='0' y='18' width='18' height='44' />
        <rect x='0' y='30' width='6' height='20' />

        {/* Left goal */}
        <rect
          x='-0.5'
          y='36'
          width='0.5'
          height='8'
          style={{ fill: '#CBD5E1' }}
        />

        {/* Left penalty arc */}
        <path d='M 18,32.5 A 10,10 0 0,1 18,48' />
        <circle cx='12' cy='40' r='0.3' fill='#CBD5E1' />

        {/* Right penalty area */}
        <rect x='102' y='18' width='18' height='44' />
        <rect x='114' y='30' width='6' height='20' />

        {/* Right goal */}
        <rect
          x='120'
          y='36'
          width='0.5'
          height='8'
          style={{ fill: '#CBD5E1' }}
        />

        {/* Right penalty arc */}
        <path d='M 102,32.5 A 10,10 0 0,0 102,48' />
        <circle cx='108' cy='40' r='0.3' fill='#CBD5E1' />

        {/* Corner arcs */}
        <path d='M 1,0 A 3,3 0 0,1 0,1' />
        <path d='M 119,0 A 3,3 0 0,0 120,1' />
        <path d='M 0,79 A 3,3 0 0,1 1,80' />
        <path d='M 119,80 A 3,3 0 0,1 120,79' />

        {children}
      </svg>
    </div>
  );
};

export default SoccerPitch;
