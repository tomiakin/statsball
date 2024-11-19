import SoccerPitch from '../../../pitch/SoccerPitch';
import VerticalSoccerPitch from '../../../pitch/VerticalSoccerPitch';
import HalfVerticalPitch from '../../../pitch/HalfVerticalPitch';
import PlayerMatchTouches from '../visualizations/PlayerMatchTouches';
import PlayerVertMatchTouches from '../visualizations/PlayerVertMatchTouches';
import PlayerMatchShots from '../visualizations/PlayerMatchShots';

export const statCategories = [
  {
    id: 'summary',
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
      },
    ],
  },
  {
    id: 'shooting',
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
      },
    ],
  },
];
