import { STAT_TYPES } from './statTypes';
import SoccerPitch from '../../../pitch/SoccerPitch';
import VerticalSoccerPitch from '../../../pitch/VerticalSoccerPitch';
import HalfVerticalPitch from '../../../pitch/HalfVerticalPitch';
import PlayerMatchTouches from '../visualizations/PlayerMatchTouches';
import PlayerVertMatchTouches from '../visualizations/PlayerVertMatchTouches';
import PlayerMatchShots from '../visualizations/PlayerMatchShots';

export const statCategories = [
  {
    id: STAT_TYPES.SUMMARY,  // Using new enum
    name: 'Summary',
    subStats: [
      {
        id: 'touches',
        name: 'Touches',
        container: ({ children }) => (  // Keeping your working container setup
          <div className='w-full'>
            <SoccerPitch>{children}</SoccerPitch>
          </div>
        ),
        component: PlayerMatchTouches,
      },
      {
        id: 'heatmap',
        name: 'Heatmap',
        container: ({ children }) => (
          <div className='mx-auto w-full max-w-xl'>
            <VerticalSoccerPitch>{children}</VerticalSoccerPitch>
          </div>
        ),
        component: PlayerVertMatchTouches,
      }
    ]
  },
  {
    id: STAT_TYPES.SHOOTING,  // Using new enum
    name: 'Shooting',
    subStats: [
      {
        id: 'shots',
        name: 'All Shots',
        container: ({ children }) => (
          <div className='mx-auto w-full max-w-xl'>
            <HalfVerticalPitch>{children}</HalfVerticalPitch>
          </div>
        ),
        component: PlayerMatchShots,
      }
    ]
  },
  // New categories
  {
    id: STAT_TYPES.PASSING,
    name: 'Passing',
    subStats: [
      {
        id: 'passMap',
        name: 'Pass Map',
        container: ({ children }) => (
          <div className='w-full'>
            <SoccerPitch>{children}</SoccerPitch>
          </div>
        ),
        component: PlayerMatchTouches, // You'll need to create passing specific components
      },
    ]
  },
  {
    id: STAT_TYPES.DEFENDING,
    name: 'Defending',
    subStats: [
      {
        id: 'defensiveActions',
        name: 'Defensive Actions',
        container: ({ children }) => (
          <div className='w-full'>
            <SoccerPitch>{children}</SoccerPitch>
          </div>
        ),
        component: PlayerMatchTouches, // You'll need to create defending specific components
      },
    ]
  }
];

export const getStatConfig = (statType) => {
  return statCategories.find(config => config.id === statType);
};