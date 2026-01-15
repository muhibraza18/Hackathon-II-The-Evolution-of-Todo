'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '../../contexts/AuthProvider';
import { useEffect } from 'react';
import ChatInterface from '../../components/ChatInterface';

export default function ChatPage() {
  const router = useRouter();
  const { user, loading } = useAuth();

  // Redirect to login if not authenticated and auth state is loaded
  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  // Don't render anything while checking auth status
  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-box">
          <div className="spinner"></div>
        </div>
        <p className="loading-text">Verifying identity...</p>
        <style jsx>{`
          .loading-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #ffffff;
            color: #334155;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          }

          .spinner-box {
            margin-bottom: 24px;
          }

          .spinner {
            width: 32px;
            height: 32px;
            border: 2.5px solid #f1f5f9;
            border-top: 2.5px solid #0f172a; /* Premium Dark Slate */
            border-radius: 50%;
            animation: spin 0.8s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
          }

          .loading-text {
            font-size: 0.9rem;
            letter-spacing: 0.025em;
            color: #64748b;
            font-weight: 500;
            margin: 0;
          }

          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  // Redirect if not authenticated
  if (!user) {
    return null;
  }

  return (
    <div className="chat-page">
      <ChatInterface />
      <style jsx global>{`
        body, html {
          margin: 0;
          padding: 0;
          height: 100%;
          background-color: #fcfcfc; /* Very subtle off-white */
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          -webkit-font-smoothing: antialiased;
        }
        .chat-page {
          height: 100vh;
          width: 100vw;
          overflow: hidden;
        }
      `}</style>
    </div>
  );
}