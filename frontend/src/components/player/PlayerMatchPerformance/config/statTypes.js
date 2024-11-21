export const STAT_TYPES = {
  SUMMARY: 'summary',
  SHOOTING: 'shooting', 
  PASSING: 'passing',
  DEFENDING: 'defending',
 };
 
 export const SUB_STAT_TYPES = {
  SUMMARY: {
    TOUCHES: 'touches',
    HEATMAP: 'heatmap',
  },
  SHOOTING: {
    SHOTS_VERTICAL: 'shots-vertical',
    SHOTS_HORIZONTAL: 'shots-horizontal',
    SHOTS_GOALVIEW: 'shots-goalview'
  },
  PASSING: {
    PASS_MAP: 'passMap',
  },
  DEFENDING: {
    DEFENSIVE_ACTIONS: 'defensiveActions',
  },
 };
 
 export const STAT_TITLES = {
  [STAT_TYPES.SUMMARY]: 'Match Overview',
  [STAT_TYPES.SHOOTING]: 'Shooting Overview',
  [STAT_TYPES.PASSING]: 'Passing Overview',
  [STAT_TYPES.DEFENDING]: 'Defending Overview'
 };
 
 export const getSubStatTypes = statType => {
  switch (statType) {
    case STAT_TYPES.SUMMARY:
      return SUB_STAT_TYPES.SUMMARY;
    case STAT_TYPES.SHOOTING:
      return SUB_STAT_TYPES.SHOOTING;
    case STAT_TYPES.PASSING:
      return SUB_STAT_TYPES.PASSING;
    case STAT_TYPES.DEFENDING:
      return SUB_STAT_TYPES.DEFENDING;
    default:
      return {};
  }
 };
 
 export const getDefaultSubStat = statType => {
  switch (statType) {
    case STAT_TYPES.SUMMARY:
      return SUB_STAT_TYPES.SUMMARY.TOUCHES;
    case STAT_TYPES.SHOOTING:
      return SUB_STAT_TYPES.SHOOTING.SHOTS_VERTICAL;
    case STAT_TYPES.PASSING:
      return SUB_STAT_TYPES.PASSING.PASS_MAP;
    case STAT_TYPES.DEFENDING:
      return SUB_STAT_TYPES.DEFENDING.DEFENSIVE_ACTIONS;
    default:
      return '';
  }
 };