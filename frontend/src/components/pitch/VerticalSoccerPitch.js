import React from 'react';
import BasePitch from './BasePitch';
import { ORIENTATIONS, COLOR_SCHEMES } from './constants';

const VerticalSoccerPitch = ({ children, onPitchClick }) => (
  <BasePitch
    orientation={ORIENTATIONS.VERTICAL}
    {...COLOR_SCHEMES.LIGHT}
    maxWidth="max-w-xl"
    onPitchClick={onPitchClick}
  >
    {children}
  </BasePitch>
);

export default VerticalSoccerPitch;