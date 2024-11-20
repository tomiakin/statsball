// src/components/Visualization.jsx
import React from 'react';
import { STAT_TYPES } from '../config/statTypes';
import { statCategories } from '../config/statConfig';

export const Visualization = ({
  selectedStat,
  selectedSubStat,
  data,
  selectedItem,
  onItemClick,
}) => {
  const category = statCategories.find(cat => cat.id === selectedStat);
  const subStat = category?.subStats.find(sub => sub.id === selectedSubStat);

  if (!subStat) return null;

  const { container: Container, component: Component } = subStat;

  // Determine props based on stat type
  const getComponentProps = () => {
    switch (selectedStat) {
      case STAT_TYPES.SHOOTING:
        return {
          shots: data?.shots || [],
          onShotClick: onItemClick,
          selectedShot: selectedItem,
          showLabels: false,
        };
      
      case STAT_TYPES.SUMMARY:
        return {
          touches: data?.touches || [], // Fix: Access touches from data object
          onTouchClick: onItemClick,
          selectedTouch: selectedItem,
          showLabels: false,
        };
        
      case STAT_TYPES.PASSING:
        return {
          passes: data?.passes || [],
          onPassClick: onItemClick,
          selectedPass: selectedItem,
          showLabels: false,
        };
        
      case STAT_TYPES.DEFENDING:
        return {
          actions: data?.actions || [],
          onActionClick: onItemClick,
          selectedAction: selectedItem,
          showLabels: false,
        };

      default:
        return {};
    }
  };

  const componentProps = getComponentProps();

  return (
    <Container>
      <Component {...componentProps} />
    </Container>
  );
};