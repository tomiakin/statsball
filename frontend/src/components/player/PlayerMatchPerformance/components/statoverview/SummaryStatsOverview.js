import React from 'react';
import { StatCard } from './StatCard';

export const SummaryStatsOverview = ({ touches }) => {
    if (!touches) return null;
  
    return (
      <div className='grid grid-cols-3 gap-2 lg:grid-cols-1'>
        <StatCard label="Touches" value={touches.length} />
        <StatCard 
          label="Shots" 
          value={touches.filter(t => t.type === 'Shot').length} 
        />
        <StatCard 
          label="Passes" 
          value={touches.filter(t => t.type === 'Pass').length} 
        />
      </div>
    );
  };