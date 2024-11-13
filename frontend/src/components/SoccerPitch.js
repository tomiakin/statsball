import React from 'react';

const SoccerPitch = ({ children, onPitchClick }) => {
  return (
    <div className='relative aspect-[3/2] w-full max-w-3xl border-2 border-slate-400 bg-white'>
      <svg
        viewBox='-2 0 124 80'
        className='absolute inset-0 h-full w-full'
        style={{
          strokeWidth: '0.2',
          stroke: '#CBD5E1',
          fill: 'none',
        }}
        onClick={onPitchClick}
      >
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
