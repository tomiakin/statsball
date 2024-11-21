import React from 'react';
import { StatCard } from './StatCard';

export const ShootingStatsOverview = ({ statistics }) => {
    if (!statistics) return null;
  
    return (
      <div className="grid grid-cols-2 gap-2">
        {/* First row - Goals and xG side by side */}
        <StatCard 
          label="Goals" 
          value={`${statistics.goals}`} 
        />
        <StatCard 
          label="Expected Goals" 
          value={statistics.total_xg.toFixed(2)} 
        />

        {/* Second row */}
        <StatCard 
          label="Shots on target" 
          value={`${statistics.shots_on_target}`} 
        />
        <StatCard 
          label="Shots off target" 
          value={`${statistics.shots_off_target}`} 
        />

        {/* Only render shots blocked if not zero */}
        {statistics.shots_blocked > 0 && (
          <div className="col-span-2">
            <StatCard 
              label="Shots blocked" 
              value={`${statistics.shots_blocked}`} 
            />
          </div>
        )}

        {/* Accuracy and conversion side by side */}
        <StatCard 
          label="Shooting accuracy" 
          value={`${statistics.shot_accuracy}%`} 
        />
        <StatCard 
          label="Shot conversion" 
          value={`${statistics.shot_conversion}%`} 
        />
      </div>
    );
};