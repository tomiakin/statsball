export const STAT_TYPES = {
  SUMMARY: 'summary',
  SHOOTING: 'shooting',
  PASSING: 'passing',
  DEFENDING: 'defending',
};

// If you need specific sub-stat types, you can add them here too
export const SUB_STAT_TYPES = {
  SUMMARY: {
    TOUCHES: 'touches',
    HEATMAP: 'heatmap',
  },
  SHOOTING: {
    ALL_SHOTS: 'shots',
  },
  PASSING: {
    PASS_MAP: 'passMap',
  },
  DEFENDING: {
    DEFENSIVE_ACTIONS: 'defensiveActions',
  },
};

// Helper function to get all sub-stats for a given stat type
export const getSubStatTypes = (statType) => {
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

// Helper function to get default sub-stat for a stat type
export const getDefaultSubStat = (statType) => {
  switch (statType) {
    case STAT_TYPES.SUMMARY:
      return SUB_STAT_TYPES.SUMMARY.TOUCHES;
    case STAT_TYPES.SHOOTING:
      return SUB_STAT_TYPES.SHOOTING.ALL_SHOTS;
    case STAT_TYPES.PASSING:
      return SUB_STAT_TYPES.PASSING.PASS_MAP;
    case STAT_TYPES.DEFENDING:
      return SUB_STAT_TYPES.DEFENDING.DEFENSIVE_ACTIONS;
    default:
      return '';
  }
};