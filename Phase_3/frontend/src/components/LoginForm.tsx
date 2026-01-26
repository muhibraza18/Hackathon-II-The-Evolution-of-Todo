'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthProvider';
import { validateLogin } from '../utils/validation';
import { authService } from '../services/auth';

const LoginForm: React.FC = () => {
  const router = useRouter();
  const { login } = useAuth();
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate form
    const validation = validateLogin(formData.email, formData.password);

    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    setIsLoading(true);
    try {
      console.log('🔐 LoginForm.handleSubmit() - initiating login process');

      // authService.login() already saves to localStorage
      const result = await authService.login(formData);
      console.log('✅ AuthService login result:', result);

      if (result.success && result.data) {
        if (!result.data.token) {
          console.error('❌ Login result missing token');
          setErrors({ general: 'Login response missing authentication token' });
          return;
        }

        login(result.data);

        const savedToken = localStorage.getItem('auth_token');
        const savedUserId = localStorage.getItem('user_id');
        console.log('✅ Token verification after AuthProvider.login():', {
          tokenExists: !!savedToken,
          userIdExists: !!savedUserId,
          tokenPreview: savedToken ? savedToken.substring(0, 20) + '...' : null
        });

        if (!savedToken || !savedUserId) {
          console.error('❌ Token or User ID was not saved to localStorage!');
          setErrors({ general: 'Failed to save authentication session' });
          return;
        }

        router.push('/chat');
      } else {
        console.error('❌ Login failed at authService level:', result.error);
        setErrors({ general: result.error || 'Login failed' });
      }
    } catch (error: any) {
      console.error('❌ Login error in LoginForm:', error);
      setErrors({ general: error.message || 'An error occurred during login' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form" aria-label="Login form">
      {errors.general && (
        <div className="alert-error" role="alert">
          {errors.general}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="email" className="form-label">Email Address</label>
        <div className="input-wrapper">
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={`form-input ${errors.email ? 'is-error' : ''}`}
            placeholder="name@company.com"
            autoComplete="email"
            required
          />
        </div>
        {errors.email && <div className="field-error">{errors.email}</div>}
      </div>

      <div className="form-group">
        <label htmlFor="password" className="form-label">Password</label>
        <div className="input-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className={`form-input ${errors.password ? 'is-error' : ''}`}
            placeholder="••••••••"
            autoComplete="current-password"
            required
          />
          <button
            type="button"
            className="password-toggle"
            onClick={() => setShowPassword(!showPassword)}
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            )}
          </button>
        </div>
        {errors.password && <div className="field-error">{errors.password}</div>}
      </div>

      <button type="submit" className="btn-submit" disabled={isLoading}>
        {isLoading ? (
          <span className="spinner-text">
            <span className="spinner"></span> Signing in...
          </span>
        ) : (
          'Sign In'
        )}
      </button>
      
      <div className="auth-footer">
        Don't have an account? <a href="/register">Create account</a>
      </div>

      <style jsx>{`
        .login-form {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .form-label {
          font-size: 0.85rem;
          font-weight: 600;
          color: #334155;
        }

        .input-wrapper {
          position: relative;
          display: flex;
          align-items: center;
        }

        .form-input {
          width: 100%;
          padding: 12px 16px;
          font-size: 0.95rem;
          border-radius: 12px;
          border: 1px solid #e2e8f0;
          background-color: #f8fafc;
          color: #0f172a;
          outline: none;
          transition: all 0.2s ease;
          font-family: inherit;
        }

        .form-input::placeholder {
          color: #94a3b8;
        }

        .form-input:focus {
          background-color: #ffffff;
          border-color: #0f172a;
          box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.05);
        }

        .form-input.is-error {
          border-color: #ef4444;
          background-color: #fef2f2;
        }

        .password-toggle {
          position: absolute;
          right: 14px;
          background: none;
          border: none;
          color: #64748b;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: color 0.2s;
        }

        .password-toggle:hover {
          color: #0f172a;
        }

        .field-error {
          font-size: 0.8rem;
          color: #ef4444;
          margin-top: 4px;
        }

        .alert-error {
          padding: 12px;
          background-color: #fef2f2;
          color: #991b1b;
          border-radius: 8px;
          border: 1px solid #fecaca;
          font-size: 0.9rem;
          text-align: center;
        }

        .btn-submit {
          padding: 14px;
          background-color: #0f172a;
          color: white;
          border: none;
          border-radius: 12px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: background-color 0.2s, transform 0.1s;
          margin-top: 8px;
        }

        .btn-submit:hover:not(:disabled) {
          background-color: #1e293b;
        }

        .btn-submit:active:not(:disabled) {
          transform: scale(0.98);
        }

        .btn-submit:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .spinner-text {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
        }

        .spinner {
          width: 18px;
          height: 18px;
          border: 2px solid rgba(255,255,255,0.3);
          border-radius: 50%;
          border-top-color: white;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        .auth-footer {
          text-align: center;
          font-size: 0.85rem;
          color: #64748b;
          margin-top: 10px;
        }

        .auth-footer a {
          color: #0f172a;
          font-weight: 600;
          text-decoration: none;
        }

        .auth-footer a:hover {
          text-decoration: underline;
        }
      `}</style>
    </form>
  );
};

export default LoginForm;