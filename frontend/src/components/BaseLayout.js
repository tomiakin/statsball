import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ThemeSwitcher from './ThemeSwitcher';

const BaseLayout = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="mx-auto flex min-h-screen max-w-[50rem] flex-col">
      <header className="z-50 mb-auto flex flex-wrap py-4">
        <nav className="w-full px-4 sm:flex sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <Link to="/" className="text-xl font-semibold text-white hover:opacity-80">Statsball</Link>
            <button
              type="button"
              className="relative flex items-center justify-center rounded-lg border border-white/10 text-sm text-gray-200 hover:bg-white/10 sm:hidden"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
          <div className={`${isMobileMenuOpen ? 'block' : 'hidden'} basis-full sm:block`}>
            <div className="mt-5 flex flex-col gap-5 sm:mt-0 sm:flex-row sm:items-center sm:pl-5">
              <Link to="/" className="font-medium text-white">Home</Link>
              <Link to="/leagues" className="font-medium text-white/70 hover:text-white">Leagues</Link>
              <Link to="/teams" className="font-medium text-white/70 hover:text-white">Teams</Link>
              <Link to="/matches" className="font-medium text-white/70 hover:text-white">Matches</Link>
            </div>
          </div>
        </nav>
        <ThemeSwitcher />
      </header>

      <main className="px-4 sm:px-6 lg:px-8">
        {children}
        {/* Add DaisyUI card for testing */}
        <div className="card card-compact bg-base-100 w-96 shadow-xl mt-8">
          <figure>
            <img src="https://img.daisyui.com/images/stock/photo-1606107557195-0e29a4b5b4aa.webp" alt="Shoes" />
          </figure>
          <div className="card-body">
            <h2 className="card-title">Shoes!</h2>
            <p>If a dog chews shoes whose shoes does he choose?</p>
            <div className="card-actions justify-end">
              <button className="btn btn-primary">Buy Now</button>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-auto py-5 text-center">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <p className="text-sm text-white/70">© {new Date().getFullYear()} Statsball</p>
        </div>
      </footer>
    </div>
  );
};

export default BaseLayout;
