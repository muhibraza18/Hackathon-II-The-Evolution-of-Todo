'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useChat } from '../hooks/useChat';
import { useAuth } from '../contexts/AuthProvider';

// Simple XSS prevention function to sanitize user-generated content
const sanitizeMessage = (content: string) => {
  if (!content) return '';
  const tempDiv = document.createElement('div');
  tempDiv.textContent = content;
  return tempDiv.textContent || tempDiv.innerText || content;
};

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
  status: 'sent' | 'delivered' | 'error';
}

const ChatInterface: React.FC = () => {
  const router = useRouter();
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();
  const { user, logout } = useAuth();
  const [inputMessage, setInputMessage] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;
    await sendMessage(inputMessage);
    setInputMessage('');
  };

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <div className="chat-interface" role="main" aria-label="Chat interface">
      {/* Header */}
      <div className="chat-header" role="banner">
        <div className="header-content">
          <div className="logo-area">
            <div className="bot-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" />
              </svg>
            </div>
            <h2>Todo AI</h2>
          </div>
          
          <div className="header-actions">
            {user && user.email && (
              <div className="user-pill">
                <span className="user-avatar">
                  {user.email.charAt(0).toUpperCase()}
                </span>
                <span className="user-email-text">{user.email}</span>
              </div>
            )}
            <button
              onClick={handleLogout}
              className="logout-button"
              aria-label="Logout from chat application"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" y1="12" x2="9" y2="12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div
        className="chat-messages"
        aria-live="polite"
        aria-relevant="additions"
        role="log"
      >
        {/* Empty State / Hero Center Text */}
        {messages.length === 0 && !isLoading && (
          <div className="empty-state">
            <h1>Todo AI Assistant</h1>
            <p>How can I help you manage your tasks today?</p>
          </div>
        )}

        <div className="messages-container">
          {messages.map((message: Message) => (
            <div
              key={message.id}
              className={`message-wrapper ${message.sender}`}
            >
              <div className={`message ${message.sender}-message ${message.status}`} role="listitem">
                <div className="message-content">
                  {sanitizeMessage(message.content)}
                </div>
                <div className="message-meta" aria-hidden="true">
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message-wrapper assistant">
              <div className="message assistant-message" role="status" aria-label="Assistant is typing">
                <div className="message-content">
                  <div className="typing-indicator" aria-hidden="true">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} aria-hidden="true" />
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div role="alert" className="error-message chat-error">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {error}
        </div>
      )}

      {/* Input Area - Fixed Center Box Style */}
      <div className="input-area-wrapper">
        <form onSubmit={handleSendMessage} className="chat-input-form" role="form" aria-label="Message input form">
          <div className="input-container-box">
            <div className="input-left-icon">
              {/* Plus Icon or Paperclip */}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </div>
            
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Message Todo AI..."
              className="chat-input-box"
              disabled={isLoading}
              aria-label="Type your message"
              role="textbox"
              aria-multiline="false"
              autoComplete="off"
            />
            
            <button
              type="submit"
              className="send-button-box"
              disabled={isLoading || !inputMessage.trim()}
              aria-label="Send message"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </form>
        <div className="footer-text">
          AI-generated content may be inaccurate. Please verify important details.
        </div>
      </div>

      {/* Embedded Styles for the Component */}
      <style jsx>{`
        /* --- Reset & Base --- */
        .chat-interface {
          display: flex;
          flex-direction: column;
          height: 100%;
          max-width: 100%;
          margin: 0 auto;
          background-color: #ffffff;
          position: relative;
        }

        /* --- Header --- */
        .chat-header {
          background-color: rgba(255, 255, 255, 0.85);
          backdrop-filter: blur(12px);
          -webkit-backdrop-filter: blur(12px);
          border-bottom: 1px solid #e2e8f0;
          padding: 0;
          flex-shrink: 0;
          z-index: 50;
        }

        .header-content {
          max-width: 900px;
          margin: 0 auto;
          padding: 16px 24px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
        }

        .logo-area {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .bot-icon {
          background-color: #0f172a;
          color: white;
          width: 36px;
          height: 36px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .chat-header h2 {
          margin: 0;
          font-size: 1.1rem;
          font-weight: 600;
          color: #0f172a;
        }

        .header-actions {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .user-pill {
          display: flex;
          align-items: center;
          gap: 8px;
          background-color: #f8fafc;
          padding: 6px 12px;
          border-radius: 24px;
          border: 1px solid #e2e8f0;
        }

        .user-avatar {
          width: 20px;
          height: 20px;
          background: linear-gradient(135deg, #334155, #0f172a);
          color: white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 10px;
          font-weight: 600;
        }

        .user-email-text {
          font-size: 0.8rem;
          color: #475569;
          font-weight: 500;
          display: none;
        }

        @media (min-width: 640px) {
          .user-email-text {
            display: block;
          }
        }

        .logout-button {
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

        .logout-button:hover {
          background-color: #f1f5f9;
          color: #0f172a;
        }

        /* --- Messages Area --- */
        .chat-messages {
          flex: 1;
          overflow-y: auto;
          scroll-behavior: smooth;
          padding-bottom: 160px; /* Space for the fixed bottom input */
          display: flex;
          flex-direction: column;
          justify-content: center; /* Center empty state */
        }

        .chat-messages::-webkit-scrollbar {
          width: 6px;
        }
        .chat-messages::-webkit-scrollbar-thumb {
          background-color: #cbd5e1;
          border-radius: 3px;
        }

        /* Empty State Styling */
        .empty-state {
          text-align: center;
          margin: auto;
          padding: 20px;
        }

        .empty-state h1 {
          font-size: 2rem;
          font-weight: 600;
          color: #0f172a;
          margin-bottom: 12px;
          letter-spacing: -0.03em;
        }

        .empty-state p {
          font-size: 1.1rem;
          color: #64748b;
          margin: 0;
        }

        .messages-container {
          max-width: 768px;
          margin: 0 auto;
          padding: 0 24px;
          display: flex;
          flex-direction: column;
          gap: 32px;
        }

        .message-wrapper {
          display: flex;
          width: 100%;
        }

        .message-wrapper.user {
          justify-content: flex-end;
        }

        .message-wrapper.assistant {
          justify-content: flex-start;
        }

        .message {
          max-width: 85%;
          padding: 14px 20px;
          position: relative;
          font-size: 0.95rem;
          line-height: 1.6;
          transition: all 0.2s ease;
        }

        /* User Message Bubble */
        .user-message {
          background-color: #0f172a;
          color: #f8fafc;
          border-radius: 24px 24px 4px 24px;
          box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
        }

        /* Assistant Message Bubble */
        .assistant-message {
          background-color: #ffffff;
          color: #334155;
          border: 1px solid #e2e8f0;
          border-radius: 24px 24px 24px 4px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        }

        .message-content {
          word-wrap: break-word;
          font-weight: 400;
        }

        .message-meta {
          font-size: 0.65rem;
          margin-top: 6px;
          text-align: right;
          opacity: 0.6;
          font-weight: 500;
          letter-spacing: 0.05em;
        }

        .user-message .message-meta {
          color: #94a3b8;
        }

        .assistant-message .message-meta {
          color: #94a3b8;
        }

        /* Typing Indicator */
        .typing-indicator {
          display: flex;
          align-items: center;
          gap: 5px;
          height: 20px;
        }

        .typing-indicator span {
          width: 5px;
          height: 5px;
          background-color: #94a3b8;
          border-radius: 50%;
          animation: bounce 1.2s infinite ease-in-out both;
        }

        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
          40% { transform: scale(1); opacity: 1; }
        }

        /* --- Error Message --- */
        .chat-error {
          position: absolute;
          bottom: 160px; /* Above input */
          left: 50%;
          transform: translateX(-50%);
          background-color: #fef2f2;
          color: #991b1b;
          padding: 10px 20px;
          border-radius: 50px;
          border: 1px solid #fecaca;
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 0.85rem;
          font-weight: 500;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
          z-index: 100;
          width: max-content;
          max-width: 90%;
        }

        /* --- Input Area --- */
        .input-area-wrapper {
          position: fixed;
          bottom: 0;
          left: 0;
          width: 100%;
          padding: 24px;
          background: linear-gradient(to top, #ffffff 60%, transparent);
          z-index: 40;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }

        .chat-input-form {
          width: 100%;
          max-width: 768px; /* Same as message width */
          display: flex;
          justify-content: center;
        }

        /* Box Shape Input */
        .input-container-box {
          position: relative;
          width: 100%;
          display: flex;
          align-items: center;
          background-color: #ffffff;
          border: 1px solid #e2e8f0;
          border-radius: 12px; /* Squared with slight rounding */
          padding: 12px 16px;
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
          transition: all 0.2s ease;
        }

        .input-container-box:focus-within {
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
          border-color: #cbd5e1;
        }

        .input-left-icon {
          color: #94a3b8;
          margin-right: 12px;
          display: flex;
          align-items: center;
        }

        .chat-input-box {
          flex: 1;
          border: none;
          background: transparent;
          font-size: 1rem;
          color: #1e293b;
          outline: none;
          padding: 0;
          font-family: inherit;
        }

        .chat-input-box::placeholder {
          color: #94a3b8;
        }

        .send-button-box {
          width: 36px;
          height: 36px;
          border-radius: 8px;
          border: none;
          background-color: #0f172a;
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.2s ease;
          flex-shrink: 0;
          margin-left: 8px;
        }

        .send-button-box:hover:not(:disabled) {
          background-color: #334155;
          transform: translateY(-1px);
        }

        .send-button-box:disabled {
          background-color: #e2e8f0;
          cursor: not-allowed;
          color: #94a3b8;
        }

        .footer-text {
          text-align: center;
          color: #cbd5e1;
          font-size: 0.7rem;
          margin-top: 12px;
          font-weight: 500;
          pointer-events: none; /* Let clicks pass through */
        }
      `}</style>
    </div>
  );
};

export default ChatInterface;