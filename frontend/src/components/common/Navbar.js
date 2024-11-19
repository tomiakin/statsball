import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Menu, Trophy, Activity, X } from 'lucide-react';

const navigation = [
  { name: 'Home', href: '/', icon: Home },
  { name: 'Competitions', href: '/competitions', icon: Trophy },
  { name: 'Match Center', href: '/matches', icon: Activity },
];

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const isActive = path => location.pathname === path;

  return (
    <header>
      <nav className='bg-blue-600 shadow-lg' aria-label='Main navigation'>
        <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
          <div className='flex h-16 justify-between'>
            <div className='flex'>
              <div className='flex flex-shrink-0 items-center'>
                <Link to='/' className='flex items-center space-x-2'>
                  <img
                    src='/api/placeholder/32/32'
                    alt='Logo'
                    className='h-8 w-8 rounded-full'
                  />
                  <span className='hidden text-xl font-bold text-white sm:block'>
                    Statsball
                  </span>
                </Link>
              </div>

              <div className='hidden sm:ml-6 sm:flex sm:space-x-8'>
                {navigation.map(item => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`inline-flex items-center space-x-2 border-b-2 px-1 pt-1 text-sm font-medium ${
                      isActive(item.href)
                        ? 'border-white text-white'
                        : 'border-transparent text-blue-100 hover:border-blue-200 hover:text-white'
                    }`}
                  >
                    <item.icon className='h-4 w-4' />
                    <span>{item.name}</span>
                  </Link>
                ))}
              </div>
            </div>

            <div className='flex items-center sm:hidden'>
              <button
                onClick={() => setIsOpen(!isOpen)}
                className='inline-flex items-center justify-center rounded-md p-2 text-blue-100 hover:bg-blue-700 hover:text-white'
              >
                {isOpen ? (
                  <X className='h-6 w-6' aria-hidden='true' />
                ) : (
                  <Menu className='h-6 w-6' aria-hidden='true' />
                )}
              </button>
            </div>
          </div>
        </div>

        {isOpen && (
          <div className='sm:hidden'>
            <div className='space-y-1 pb-3 pt-2'>
              {navigation.map(item => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 border-l-4 py-2 pl-3 pr-4 text-base font-medium ${
                    isActive(item.href)
                      ? 'border-white bg-blue-700 text-white'
                      : 'border-transparent text-blue-100 hover:border-blue-300 hover:bg-blue-700 hover:text-white'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <item.icon className='h-5 w-5' />
                  <span>{item.name}</span>
                </Link>
              ))}
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Navbar;
