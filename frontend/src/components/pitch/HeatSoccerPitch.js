import React from 'react';
import BasePitch from './BasePitch';
import { ORIENTATIONS, COLOR_SCHEMES } from './constants';

const HeatSoccerPitch = ({ children, onPitchClick }) => (
  <BasePitch
    orientation={ORIENTATIONS.HORIZONTAL}
    {...COLOR_SCHEMES.DARK}
    onPitchClick={onPitchClick}
  >
    {children}
  </BasePitch>
);

export default HeatSoccerPitch;