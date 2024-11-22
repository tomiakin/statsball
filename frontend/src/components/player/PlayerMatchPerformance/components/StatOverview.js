import { STAT_TYPES, STAT_TITLES } from '../config/statTypes';
import { ShootingStatsOverview } from './statoverview/ShootingStatsOverview';
import { SummaryStatsOverview } from './statoverview/SummaryStatsOverview';

export const StatOverview = ({ selectedStat, data }) => {
  const renderStats = () => {
    switch (selectedStat) {
      case STAT_TYPES.SHOOTING:
        return <ShootingStatsOverview statistics={data?.statistics} />;
      case STAT_TYPES.SUMMARY:
        return <SummaryStatsOverview touches={data?.touches} />;
      default:
        return null;
    }
  };

  return (
    <div className='mb-4 rounded-lg bg-white p-4 shadow-lg'>
      <h3 className='mb-3 text-lg font-semibold'>
        {STAT_TITLES[selectedStat] || 'Overview'}
      </h3>
      {renderStats()}
    </div>
  );
};
