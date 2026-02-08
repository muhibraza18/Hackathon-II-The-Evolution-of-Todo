'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthProvider';

interface NavbarProps {
  showAuthLinks?: boolean;
}

const Navbar: React.FC<NavbarProps> = ({ showAuthLinks = true }) => {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="navbar-container">
        {/* Logo */}
        <Link href="/" className="navbar-logo">
          <div className="logo-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" />
            </svg>
          </div>
          <span className="logo-text">Todo AI</span>
        </Link>

        {/* Navigation Links */}
        <div className="navbar-nav">
          {user ? (
            <>
              <Link
                href="/chat"
                className={`nav-link ${pathname === '/chat' ? 'active' : ''}`}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                <span>Chat</span>
              </Link>
              <Link
                href="/tasks"
                className={`nav-link ${pathname === '/tasks' ? 'active' : ''}`}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M9 11l3 3L22 4"></path>
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                </svg>
                <span>Tasks</span>
              </Link>
            </>
          ) : (
            showAuthLinks && (
              <>
                <Link
                  href="/login"
                  className={`nav-link ${pathname === '/login' ? 'active' : ''}`}
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className={`nav-link nav-link-primary ${pathname === '/register' ? 'active' : ''}`}
                >
                  Get Started
                </Link>
              </>
            )
          )}
        </div>

        {/* User Actions */}
        {user && (
          <div className="navbar-actions">
            <div className="user-pill">
              <span className="user-avatar">
                {user.email?.charAt(0).toUpperCase() || '?'}
              </span>
              <span className="user-email">{user.email}</span>
            </div>
            <button
              onClick={handleLogout}
              className="logout-btn"
              aria-label="Logout"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" y1="12" x2="9" y2="12" />
              </svg>
            </button>
          </div>
        )}
      </div>

      <style jsx>{`
        .navbar {
          background-color: rgba(255, 255, 255, 0.85);
          backdrop-filter: blur(12px);
          -webkit-backdrop-filter: blur(12px);
          border-bottom: 1px solid #e2e8f0;
          position: sticky;
          top: 0;
          z-index: 100;
          box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        }

        .navbar-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 24px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        /* Logo Styles */
        .navbar-logo {
          display: flex;
          align-items: center;
          gap: 10px;
          text-decoration: none;
          color: #0f172a;
          font-weight: 600;
          font-size: 1.1rem;
          transition: opacity 0.2s ease;
        }

        .navbar-logo:hover {
          opacity: 0.8;
        }

        .logo-icon {
          width: 36px;
          height: 36px;
          background-color: #0f172a;
          color: white;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }

        .logo-text {
          font-size: 1.1rem;
          font-weight: 600;
          letter-spacing: -0.025em;
          color: #0f172a;
        }

        /* Navigation Links */
        .navbar-nav {
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .nav-link {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 8px 14px;
          border-radius: 8px;
          text-decoration: none;
          color: #475569;
          font-size: 0.9rem;
          font-weight: 500;
          transition: all 0.2s ease;
          position: relative;
        }

        .nav-link svg {
          flex-shrink: 0;
        }

        .nav-link:hover {
          background-color: #f1f5f9;
          color: #0f172a;
        }

        .nav-link.active {
          background-color: #f1f5f9;
          color: #0f172a;
          font-weight: 600;
        }

        .nav-link.active::after {
          content: '';
          position: absolute;
          bottom: -1px;
          left: 14px;
          right: 14px;
          height: 2px;
          background-color: #0f172a;
          border-radius: 2px 2px 0 0;
        }

        .nav-link-primary {
          background-color: #0f172a;
          color: white;
        }

        .nav-link-primary:hover {
          background-color: #1e293b;
          color: white;
        }

        .nav-link-primary.active {
          background-color: #334155;
        }

        .nav-link-primary.active::after {
          display: none;
        }

        /* User Actions */
        .navbar-actions {
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .user-pill {
          display: flex;
          align-items: center;
          gap: 8px;
          background-color: #f8fafc;
          padding: 6px 12px;
          border-radius: 24px;
          border: 1px solid #e2e8f0;
          transition: all 0.2s ease;
        }

        .user-pill:hover {
          border-color: #cbd5e1;
          background-color: #f1f5f9;
        }

        .user-avatar {
          width: 24px;
          height: 24px;
          background: linear-gradient(135deg, #334155, #0f172a);
          color: white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 11px;
          font-weight: 600;
          flex-shrink: 0;
        }

        .user-email {
          font-size: 0.85rem;
          color: #475569;
          font-weight: 500;
          max-width: 150px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          display: none;
        }

        @media (min-width: 640px) {
          .user-email {
            display: block;
          }
        }

        .logout-btn {
          background: transparent;
          border: none;
          color: #64748b;
          padding: 8px;
          border-radius: 8px;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s ease;
        }

        .logout-btn:hover {
          background-color: #f1f5f9;
          color: #ef4444;
        }

        .logout-btn:active {
          transform: scale(0.95);
        }

        /* Responsive Styles */
        @media (max-width: 640px) {
          .navbar-container {
            padding: 0 16px;
            height: 56px;
          }

          .nav-link {
            padding: 8px 12px;
            font-size: 0.85rem;
          }

          .nav-link span {
            display: none;
          }

          .nav-link svg {
            margin: 0;
          }

          .logo-text {
            display: none;
          }

          .logo-icon {
            width: 32px;
            height: 32px;
          }

          .navbar-nav {
            gap: 4px;
          }

          .navbar-actions {
            gap: 8px;
          }
        }

        @media (max-width: 480px) {
          .user-pill {
            padding: 6px 8px;
          }

          .logout-btn {
            padding: 6px;
          }
        }
      `}</style>
    </nav>
  );
};

export default Navbar;