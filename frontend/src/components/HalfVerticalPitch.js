// HalfVerticalPitch.js
import React from 'react';

const HalfVerticalPitch = ({ children, onPitchClick }) => {
  return (
    <div className='relative aspect-[4/3] w-full max-w-xl border-2 border-slate-400 bg-white'>
      <svg
        viewBox='-2 -2 84 64' // 80 width and 60 height
        className='absolute inset-0 h-full w-full'
        style={{
          strokeWidth: '0.2',
          stroke: '#CBD5E1',
          fill: 'none',
        }}
        onClick={onPitchClick}
      >
        {/* Outer border */}
        <rect x='0' y='0' width='80' height='60' />

        {/* Halfway line (now bottom border) */}
        <line x1='0' y1='60' x2='80' y2='60' />

        {/* Half of Center circle */}
        <path d='M 30,60 A 10,10 0 0 1 50,60' />
        <circle cx='40' cy='60' r='0.3' fill='#CBD5E1' />

        {/* Top penalty area */}
        <rect x='18' y='0' width='44' height='18' />
        <rect x='30' y='0' width='20' height='6' />

        {/* Top goal */}
        <rect
          x='36'
          y='-0.5'
          width='8'
          height='0.5'
          style={{ fill: '#CBD5E1' }}
        />

        {/* Top penalty arc */}
        <path d='M 32.5,18 A 10,10 0 0,0 48,18' />
        <circle cx='40' cy='12' r='0.3' fill='#CBD5E1' />

        {/* Corner arcs */}
        <path d='M 0,1 A 3,3 0 0,0 1,0' />
        <path d='M 79,0 A 3,3 0 0,0 80,1' />

        {children}
      </svg>
    </div>
  );
};

export default HalfVerticalPitch;