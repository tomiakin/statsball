import { STAT_TYPES } from './statTypes';
import SoccerPitch from '../../../pitch/SoccerPitch';
import VerticalSoccerPitch from '../../../pitch/VerticalSoccerPitch';
import HalfVerticalPitch from '../../../pitch/HalfVerticalPitch';
import { GoalPostVisualization } from '../../../pitch/GoalPost';
import PlayerMatchTouches from '../visualizations/PlayerMatchTouches';
import PlayerMatchShots from '../visualizations/PlayerMatchShots';

export const statCategories = [
  {
    id: STAT_TYPES.SUMMARY, // Using new enum
    name: 'Summary',
    subStats: [
      {
        id: 'touches',
        name: 'Touches',
        container: ({ children }) => (
          <div className='w-full'>
            <SoccerPitch>{children}</SoccerPitch>
          </div>
        ),
        component: props => (
          <PlayerMatchTouches {...props} orientation='horizontal' />
        ),
      },
      {
        id: 'heatmap',
        name: 'Heatmap',
        container: ({ children }) => (
          <div className='mx-auto w-full max-w-xl'>
            <VerticalSoccerPitch>{children}</VerticalSoccerPitch>
          </div>
        ),
        component: props => (
          <PlayerMatchTouches {...props} orientation='vertical' />
        ),
      },
    ],
  },
  {
    id: STAT_TYPES.SHOOTING,
    name: 'Shooting',
    subStats: [
      {
        id: 'shots-vertical',
        name: 'Shots (Vertical)',
        container: ({ children }) => (
          <div className='mx-auto w-full max-w-xl'>
            <HalfVerticalPitch>{children}</HalfVerticalPitch>
          </div>
        ),
        component: props => (
          <PlayerMatchShots {...props} orientation='vertical' />
        ),
      },
      {
        id: 'shots-horizontal',
        name: 'Shots (Horizontal)',
        container: ({ children }) => (
          <div className='w-full'>
            <SoccerPitch>{children}</SoccerPitch>
          </div>
        ),
        component: props => (
          <PlayerMatchShots {...props} orientation='horizontal' />
        ),
      },
      {
        id: 'shots-goalview',
        name: 'Shots (Goal View)',
        container: ({ children }) => (
          <div className='w-full'>
            <GoalPostVisualization>{children}</GoalPostVisualization>
          </div>
        ),
        component: props => (
          <PlayerMatchShots {...props} orientation='goalview' />
        ),
      },
    ],
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
            <GoalPostVisualization>{children}</GoalPostVisualization>
          </div>
        ),
        component: PlayerMatchTouches, // You'll need to create passing specific components
      },
    ],
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
    ],
  },
];

export const getStatConfig = statType => {
  return statCategories.find(config => config.id === statType);
};
