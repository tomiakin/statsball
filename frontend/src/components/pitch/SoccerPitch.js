import React from 'react';
import BasePitch from './BasePitch';
import { ORIENTATIONS, COLOR_SCHEMES } from './constants';

const SoccerPitch = ({ children, onPitchClick }) => (
  <BasePitch
    orientation={ORIENTATIONS.HORIZONTAL}
    {...COLOR_SCHEMES.LIGHT}
    onPitchClick={onPitchClick}
  >
    {children}
  </BasePitch>
);

export default SoccerPitch;
