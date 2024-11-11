import React from 'react';
import BaseLayout from './BaseLayout';

const BoxesPage = () => {
  return (
    <BaseLayout>
      <h1 className='mb-8 text-center text-3xl font-bold'>
        Player Performance
      </h1>

      <div className='grid grid-cols-3 grid-rows-2 gap-4 p-6'>
        {/* Left Column */}
        <div className='col-span-1 row-span-1 rounded-lg bg-blue-200 p-4'>
          Box 1 (Left Top) Player first, last name and rating Box 1 (Left Top)
          Player first, last name and rating
        </div>

        {/* Right Column Top - Spans 2 Columns */}
        <div className='col-span-2 row-span-1 h-20 rounded-lg bg-green-200 p-4'>
          Box 2 (Right Top) Navbar, Summary, Shooting, Passing, Defending
        </div>

        {/* Left Column Bottom - Table inside Box 3 */}
        <div className='col-span-1 row-span-1 flex flex-col rounded-lg bg-purple-200 p-4'>
          <div className='overflow-x-auto'>
            <table className='w-full table-auto border-collapse'>
              <thead>
                <tr>
                  <th className='border-b px-4 py-2'>#</th>
                  <th className='border-b px-4 py-2'>Name</th>
                  <th className='border-b px-4 py-2'>Job</th>
                  <th className='border-b px-4 py-2'>Favorite Color</th>
                </tr>
              </thead>
              <tbody>
                {/* row 1 */}
                <tr>
                  <th className='border-b px-4 py-2'>1</th>
                  <td className='border-b px-4 py-2'>Cy Ganderton</td>
                  <td className='border-b px-4 py-2'>
                    Quality Control Specialist
                  </td>
                  <td className='border-b px-4 py-2'>Blue</td>
                </tr>
                {/* row 2 */}
                <tr className='hover:bg-gray-100'>
                  <th className='border-b px-4 py-2'>2</th>
                  <td className='border-b px-4 py-2'>Hart Hagerty</td>
                  <td className='border-b px-4 py-2'>
                    Desktop Support Technician
                  </td>
                  <td className='border-b px-4 py-2'>Purple</td>
                </tr>
                {/* row 3 */}
                <tr>
                  <th className='border-b px-4 py-2'>3</th>
                  <td className='border-b px-4 py-2'>Brice Swyre</td>
                  <td className='border-b px-4 py-2'>Tax Accountant</td>
                  <td className='border-b px-4 py-2'>Red</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Bottom Row - Center */}
        <div className='col-span-1 row-span-1 rounded-lg bg-red-200 p-4'>
          Box 4 (Right Bottom - Top)
        </div>

        {/* Bottom Row - Right */}
        <div className='col-span-1 row-span-1 rounded-lg bg-yellow-200 p-4'>
          Box 5 (Right Bottom - Bottom)
        </div>
      </div>
    </BaseLayout>
  );
};

export default BoxesPage;
