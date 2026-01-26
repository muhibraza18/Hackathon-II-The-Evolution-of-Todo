'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '../../contexts/AuthProvider';
import { useEffect } from 'react';
import RegisterForm from '../../components/RegisterForm';

export default function RegisterPage() {
  const router = useRouter();
  const { user } = useAuth();

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      router.push('/chat');
    }
  }, [user, router]);

  if (user) {
    return null; 
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <div className="auth-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" />
            </svg>
          </div>
          <h1>Create Account</h1>
          <p>Join Todo AI today</p>
        </div>
        <RegisterForm />
      </div>
      
      <style jsx>{`
        .auth-page {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 100vh;
          background-color: #f8fafc;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
          padding: 20px;
        }

        .auth-container {
          width: 100%;
          max-width: 420px;
          background: #ffffff;
          padding: 40px;
          border-radius: 24px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
          border: 1px solid #e2e8f0;
        }

        .auth-header {
          text-align: center;
          margin-bottom: 32px;
        }

        .auth-icon {
          width: 48px;
          height: 48px;
          background-color: #0f172a;
          color: white;
          border-radius: 12px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 16px;
          box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        }

        .auth-header h1 {
          font-size: 1.5rem;
          font-weight: 600;
          color: #0f172a;
          margin: 0 0 8px 0;
          letter-spacing: -0.025em;
        }

        .auth-header p {
          font-size: 0.95rem;
          color: #64748b;
          margin: 0;
        }
      `}</style>
    </div>
  );
}