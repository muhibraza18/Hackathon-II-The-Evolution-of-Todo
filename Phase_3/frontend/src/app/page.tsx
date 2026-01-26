'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthProvider';

export default function HomePage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [isRedirecting, setIsRedirecting] = useState(false);

  useEffect(() => {
    if (!loading) {
      // Set a short artificial delay to allow the user to see the landing page
      // and to ensure assets are loaded/transition is smooth
      const timer = setTimeout(() => {
        setIsRedirecting(true);
        if (user) {
          router.push('/chat');
        } else {
          router.push('/register');
        }
      }, 800); // 800ms delay

      return () => clearTimeout(timer);
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="loading-wrapper">
        <div className="spinner-large"></div>
        <p>Authenticating...</p>
        <style jsx>{`
          .loading-wrapper {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
          }
          .spinner-large {
            width: 48px;
            height: 48px;
            border: 3px solid #e2e8f0;
            border-top-color: #0f172a;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-bottom: 20px;
          }
          p {
            color: #64748b;
            font-weight: 500;
            font-size: 0.95rem;
          }
          @keyframes spin { to { transform: rotate(360deg); } }
        `}</style>
      </div>
    );
  }

  return (
    <div className="home-page">
      <div className="content-container">
        {/* Hero Section */}
        <div className="hero-section">
          <div className="brand-mark">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" />
            </svg>
          </div>
          
          <h1 className="hero-title">
            Todo AI
          </h1>
          
          <p className="hero-subtitle">
            Intelligent task management. Simplified workflow.
          </p>

          <div className="cta-group">
            {isRedirecting ? (
              <div className="loader-mini"></div>
            ) : (
              <>
                <button 
                  onClick={() => router.push('/register')}
                  className="btn-primary"
                >
                  Get Started
                </button>
                <button 
                  onClick={() => router.push('/login')}
                  className="btn-secondary"
                >
                  Sign In
                </button>
              </>
            )}
          </div>
        </div>

        {/* Features Grid (Visual Decoration) */}
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
            </div>
            <h3>Smart Assist</h3>
            <p>Natural language processing for your tasks.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              </svg>
            </div>
            <h3>Secure Data</h3>
            <p>Your data is encrypted and private.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
            </div>
            <h3>Real-time</h3>
            <p>Instant updates and sync across devices.</p>
          </div>
        </div>
      </div>

      {/* Styling */}
      <style jsx global>{`
        body {
          margin: 0;
          padding: 0;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          background-color: #f8fafc;
          color: #0f172a;
        }
      `}</style>
      
      <style jsx>{`
        .home-page {
          display: flex;
          flex-direction: column;
          min-height: 100vh;
          overflow: hidden;
          background: radial-gradient(circle at 50% 0%, #f1f5f9 0%, #f8fafc 60%);
        }

        .content-container {
          max-width: 1000px;
          margin: 0 auto;
          padding: 40px 24px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          flex: 1;
          text-align: center;
        }

        /* Hero Styles */
        .hero-section {
          margin-bottom: 60px;
          animation: fadeIn 0.8s ease-out;
        }

        .brand-mark {
          width: 64px;
          height: 64px;
          background-color: #0f172a;
          color: white;
          border-radius: 16px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 24px;
          box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.2);
        }

        .hero-title {
          font-size: 3.5rem;
          font-weight: 800;
          letter-spacing: -0.04em;
          line-height: 1.1;
          margin: 0 0 16px 0;
          background: -webkit-linear-gradient(45deg, #0f172a, #334155);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
          font-size: 1.25rem;
          color: #64748b;
          margin: 0 0 40px 0;
          font-weight: 400;
          max-width: 500px;
          margin-left: auto;
          margin-right: auto;
        }

        /* CTA Buttons */
        .cta-group {
          display: flex;
          gap: 16px;
          justify-content: center;
          align-items: center;
        }

        .btn-primary, .btn-secondary {
          padding: 14px 32px;
          font-size: 1rem;
          font-weight: 600;
          border-radius: 12px;
          cursor: pointer;
          transition: all 0.2s ease;
          border: none;
        }

        .btn-primary {
          background-color: #0f172a;
          color: white;
          box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.1);
        }

        .btn-primary:hover {
          background-color: #1e293b;
          transform: translateY(-2px);
          box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.2);
        }

        .btn-secondary {
          background-color: white;
          color: #334155;
          border: 1px solid #e2e8f0;
        }

        .btn-secondary:hover {
          background-color: #f8fafc;
          border-color: #cbd5e1;
          color: #0f172a;
        }

        /* Features Grid */
        .features-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 24px;
          width: 100%;
          margin-top: 40px;
          animation: fadeIn 1s ease-out 0.2s backwards;
        }

        .feature-card {
          background: white;
          padding: 24px;
          border-radius: 16px;
          border: 1px solid #e2e8f0;
          text-align: left;
          transition: transform 0.2s;
        }

        .feature-card:hover {
          transform: translateY(-4px);
        }

        .feature-icon {
          width: 40px;
          height: 40px;
          background-color: #f1f5f9;
          color: #475569;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 16px;
        }

        .feature-card h3 {
          margin: 0 0 8px 0;
          font-size: 1rem;
          color: #0f172a;
        }

        .feature-card p {
          margin: 0;
          font-size: 0.875rem;
          color: #64748b;
          line-height: 1.5;
        }

        /* Loader Mini */
        .loader-mini {
          width: 24px;
          height: 24px;
          border: 2px solid #e2e8f0;
          border-top-color: #0f172a;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        /* Animations */
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        /* Responsive */
        @media (max-width: 768px) {
          .hero-title {
            font-size: 2.5rem;
          }
          .features-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}