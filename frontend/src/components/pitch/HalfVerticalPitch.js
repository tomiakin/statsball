import React from 'react';
import BasePitch from './BasePitch';
import { ORIENTATIONS, COLOR_SCHEMES } from './constants';

const HalfVerticalPitch = ({ children, onPitchClick }) => (
  <BasePitch
    orientation={ORIENTATIONS.HALF_VERTICAL}
    {...COLOR_SCHEMES.LIGHT}
    maxWidth='max-w-xl'
    onPitchClick={onPitchClick}
  >
    {children}
  </BasePitch>
);

export default HalfVerticalPitch;
