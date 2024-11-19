import React from 'react';
import { ORIENTATIONS } from './constants';

const getViewBox = (orientation) => {
  switch (orientation) {
    case ORIENTATIONS.VERTICAL:
      return '0 -2 80 124';
    case ORIENTATIONS.HALF_VERTICAL:
      return '-2 -2 84 64';
    case ORIENTATIONS.HORIZONTAL:
    default:
      return '-2 -2 124 84';
  }
};

const getAspectRatio = (orientation) => {
  switch (orientation) {
    case ORIENTATIONS.VERTICAL:
      return 'aspect-[2/3]';
    case ORIENTATIONS.HALF_VERTICAL:
      return 'aspect-[4/3]';
    case ORIENTATIONS.HORIZONTAL:
    default:
      return 'aspect-[3/2]';
  }
};

const BasePitch = ({ 
  children, 
  onPitchClick, 
  orientation = ORIENTATIONS.HORIZONTAL,
  background = 'bg-white',
  stroke = '#CBD5E1',
  fill = 'none',
  maxWidth = 'max-w-3xl'
}) => {
  const isVertical = orientation === ORIENTATIONS.VERTICAL;
  const isHalfVertical = orientation === ORIENTATIONS.HALF_VERTICAL;
  
  const renderPitchElements = () => {
    if (isHalfVertical) {
      return (
        <>
          <rect x='0' y='0' width='80' height='60' />
          <line x1='0' y1='60' x2='80' y2='60' />
          <path d='M 30,60 A 10,10 0 0 1 50,60' />
          <circle cx='40' cy='60' r='0.3' fill={stroke} />
          <rect x='18' y='0' width='44' height='18' />
          <rect x='30' y='0' width='20' height='6' />
          <rect x='36' y='-0.5' width='8' height='0.5' style={{ fill: stroke }} />
          <path d='M 32.5,18 A 10,10 0 0,0 48,18' />
          <circle cx='40' cy='12' r='0.3' fill={stroke} />
          <path d='M 0,1 A 3,3 0 0,0 1,0' />
          <path d='M 79,0 A 3,3 0 0,0 80,1' />
        </>
      );
    }

    const standardElements = (
      <>
        <rect 
          x='0' 
          y='0' 
          width={isVertical ? '80' : '120'} 
          height={isVertical ? '120' : '80'} 
          style={{ fill }}
        />
        {isVertical ? (
          <line x1='0' y1='60' x2='80' y2='60' />
        ) : (
          <line x1='60' y1='0' x2='60' y2='80' />
        )}
        <circle 
          cx={isVertical ? '40' : '60'} 
          cy={isVertical ? '60' : '40'} 
          r='10' 
        />
        <circle 
          cx={isVertical ? '40' : '60'} 
          cy={isVertical ? '60' : '40'} 
          r='0.3' 
          fill={stroke} 
        />
        {/* Penalty areas and other elements */}
        {isVertical ? (
          <>
            {/* Vertical orientation penalty areas */}
            <rect x='18' y='0' width='44' height='18' />
            <rect x='30' y='0' width='20' height='6' />
            <rect x='18' y='102' width='44' height='18' />
            <rect x='30' y='114' width='20' height='6' />
            {/* Goals */}
            <rect x='36' y='-0.5' width='8' height='0.5' style={{ fill: stroke }} />
            <rect x='36' y='120' width='8' height='0.5' style={{ fill: stroke }} />
            {/* Penalty arcs */}
            <path d='M 32.5,18 A 10,10 0 0,0 48,18' />
            <path d='M 32.5,102 A 10,10 0 0,1 48,102' />
          </>
        ) : (
          <>
            {/* Horizontal orientation penalty areas */}
            <rect x='0' y='18' width='18' height='44' />
            <rect x='0' y='30' width='6' height='20' />
            <rect x='102' y='18' width='18' height='44' />
            <rect x='114' y='30' width='6' height='20' />
            {/* Goals */}
            <rect x='-0.5' y='36' width='0.5' height='8' style={{ fill: stroke }} />
            <rect x='120' y='36' width='0.5' height='8' style={{ fill: stroke }} />
            {/* Penalty arcs */}
            <path d='M 18,32.5 A 10,10 0 0,1 18,48' />
            <path d='M 102,32.5 A 10,10 0 0,0 102,48' />
          </>
        )}
      </>
    );

    return standardElements;
  };

  return (
    <div className={`relative ${getAspectRatio(orientation)} w-full ${maxWidth} border-2 border-slate-400 ${background}`}>
      <svg
        viewBox={getViewBox(orientation)}
        className='absolute inset-0 h-full w-full'
        style={{
          strokeWidth: '0.2',
          stroke,
          fill: 'none',
        }}
        onClick={onPitchClick}
      >
        {renderPitchElements()}
        {children}
      </svg>
    </div>
  );
};

export default BasePitch;