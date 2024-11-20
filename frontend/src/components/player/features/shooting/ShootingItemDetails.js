import React from 'react';

export const ShootingItemDetails = ({ selectedItem }) => {
 if (!selectedItem) {
   return (
     <div className='text-center text-gray-500'>
       Select a shot to see details
     </div>
   );
 }

 return (
   <div className='grid grid-cols-3 gap-4'>
     <div>
       <p className='text-xs text-gray-500'>Shot Outcome</p>
       <p className='text-sm font-bold'>{selectedItem.shot_outcome}</p>
     </div>
     <div>
       <p className='text-xs text-gray-500'>Expected Goals (xG)</p>
       <p className='text-sm font-bold'>
         {selectedItem.shot_statsbomb_xg?.toFixed(2)}
       </p>
     </div>
     <div>
       <p className='text-xs text-gray-500'>Shot Type</p>
       <p className='text-sm font-bold'>{selectedItem.shot_type}</p>
     </div>
   </div>
 );
};