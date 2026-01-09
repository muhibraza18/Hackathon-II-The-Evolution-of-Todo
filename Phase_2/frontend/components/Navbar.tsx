'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const pathname = usePathname();
  const { user, loading, logout } = useAuth();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (path: string) => pathname === path;

  const handleLogout = async () => {
    await logout();
    setIsMobileMenuOpen(false);
  };

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled
        ? 'bg-white shadow-lg py-2'
        : 'bg-white/90 backdrop-blur-md py-4'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <div className="flex-shrink-0 flex items-center">
            <Link href="/" className="flex items-center group">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl flex items-center justify-center mr-3 shadow-md group-hover:shadow-lg transform group-hover:scale-105 transition-all duration-200">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
                Taskify
              </span>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-4">
              {!loading && user ? (
                <>
                  <Link
                    href="/tasks"
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                      isActive('/tasks')
                        ? 'bg-gradient-to-r from-emerald-500 to-green-600 text-white shadow-md'
                        : 'text-gray-700 hover:bg-emerald-50 hover:text-emerald-700'
                    }`}
                  >
                    Tasks
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 hover:bg-red-50 hover:text-red-700 transition-all duration-200"
                  >
                    Logout
                  </button>
                  <div className="ml-2 flex items-center bg-emerald-50 rounded-full px-4 py-2 border border-emerald-200">
                    <span className="text-sm font-medium text-emerald-900 mr-2">
                      {user.name || user.email}
                    </span>
                    <div className="w-9 h-9 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center shadow-md">
                      <span className="text-white font-bold text-sm">
                        {user.name?.charAt(0).toUpperCase() || user.email?.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                      isActive('/login')
                        ? 'bg-emerald-50 text-emerald-700'
                        : 'text-gray-700 hover:bg-emerald-50 hover:text-emerald-700'
                    }`}
                  >
                    Log in
                  </Link>
                  <Link
                    href="/signup"
                    className="px-5 py-2 rounded-lg text-sm font-bold text-white bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-lg text-gray-700 hover:text-emerald-600 hover:bg-emerald-50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-emerald-500 transition-colors duration-200"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              <svg
                className={`${isMobileMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg
                className={`${isMobileMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className={`${isMobileMenuOpen ? 'md:hidden' : 'hidden'}`}>
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t border-gray-100 shadow-lg">
          {!loading && user ? (
            <>
              <div className="px-3 py-3 mb-2 bg-emerald-50 rounded-lg border border-emerald-200">
                <div className="flex items-center">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center shadow-md mr-3">
                    <span className="text-white font-bold">
                      {user.name?.charAt(0).toUpperCase() || user.email?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="text-sm font-medium text-emerald-900">
                    {user.name || user.email}
                  </span>
                </div>
              </div>
              <Link
                href="/tasks"
                className={`block px-3 py-2 rounded-lg text-base font-semibold transition-colors duration-200 ${
                  isActive('/tasks')
                    ? 'bg-gradient-to-r from-emerald-500 to-green-600 text-white'
                    : 'text-gray-700 hover:bg-emerald-50 hover:text-emerald-700'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Tasks
              </Link>
              <button
                onClick={handleLogout}
                className="w-full text-left px-3 py-2 rounded-lg text-base font-semibold text-gray-700 hover:bg-red-50 hover:text-red-700 transition-colors duration-200"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className={`block px-3 py-2 rounded-lg text-base font-semibold transition-colors duration-200 ${
                  isActive('/login')
                    ? 'bg-emerald-50 text-emerald-700'
                    : 'text-gray-700 hover:bg-emerald-50 hover:text-emerald-700'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Log in
              </Link>
              <Link
                href="/signup"
                className={`block px-3 py-2 rounded-lg text-base font-semibold transition-colors duration-200 ${
                  isActive('/signup')
                    ? 'bg-gradient-to-r from-emerald-500 to-green-600 text-white'
                    : 'text-gray-700 hover:bg-emerald-50 hover:text-emerald-700'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;