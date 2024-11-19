import React from 'react';
import { statCategories } from '../config/statConfig';

export const Visualization = ({
  selectedStat,
  selectedSubStat,
  shootingData,
  touches,
  selectedTouch,
  selectedShot,
  onItemClick,
}) => {
  const category = statCategories.find(cat => cat.id === selectedStat);
  const subStat = category?.subStats.find(sub => sub.id === selectedSubStat);

  if (!subStat) return null;

  const { container: Container, component: Component } = subStat;

  const componentProps =
    selectedStat === 'shooting'
      ? {
          shots: shootingData?.shots || [],
          onShotClick: onItemClick,
          selectedShot,
          showLabels: false,
        }
      : {
          touches,
          onTouchClick: onItemClick,
          selectedTouch,
          showLabels: false,
        };

  return (
    <Container>
      <Component {...componentProps} />
    </Container>
  );
};
