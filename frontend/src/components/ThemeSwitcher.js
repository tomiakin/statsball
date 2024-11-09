import React, { useEffect } from 'react';
import { themeChange } from 'theme-change';

const ThemeSwitcher = () => {
  useEffect(() => {
    themeChange(false); // Initialize theme change without transitions
  }, []);

  return (
    <div className='p-4'>
      <select
        data-choose-theme
        className='select select-bordered w-full max-w-xs'
      >
        <option value='light'>Light</option>
        <option value='dark'>Dark</option>
      </select>
    </div>
  );
};

export default ThemeSwitcher;
