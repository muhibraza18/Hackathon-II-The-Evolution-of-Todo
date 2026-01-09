'use client';

import { useEffect } from 'react';
import { CheckCircleIcon, XMarkIcon } from '@heroicons/react/24/solid';

interface ToastProps {
  message: string;
  isVisible: boolean;
  onClose: () => void;
  type?: 'success' | 'error' | 'info';
}

const Toast = ({ message, isVisible, onClose, type = 'success' }: ToastProps) => {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  if (!isVisible) return null;

  const colors = {
    success: {
      bg: 'bg-gradient-to-r from-green-500 to-emerald-500',
      icon: CheckCircleIcon
    },
    error: {
      bg: 'bg-gradient-to-r from-red-500 to-rose-500',
      icon: XMarkIcon
    },
    info: {
      bg: 'bg-gradient-to-r from-blue-500 to-indigo-500',
      icon: CheckCircleIcon
    }
  };

  const config = colors[type];
  const Icon = config.icon;

  return (
    <div className={`fixed bottom-6 right-6 ${config.bg} text-white px-5 py-4 rounded-xl shadow-2xl z-50 flex items-center gap-3 min-w-[300px] animate-slideIn`}>
      <Icon className="w-6 h-6 flex-shrink-0" />
      <span className="font-medium flex-1">{message}</span>
      <button
        onClick={onClose}
        className="hover:bg-white/20 rounded-lg p-1 transition-colors"
      >
        <XMarkIcon className="w-5 h-5" />
      </button>

      <style jsx>{`
        @keyframes slideIn {
          from {
            transform: translateX(400px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        .animate-slideIn {
          animation: slideIn 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default Toast;