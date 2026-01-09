'use client';

import { useMemo } from 'react';

interface PasswordStrengthIndicatorProps {
  password: string;
  className?: string;
}

const PasswordStrengthIndicator = ({ password, className = '' }: PasswordStrengthIndicatorProps) => {
  const { score, label, color, feedback } = useMemo(() => {
    let score = 0;
    const feedback: string[] = [];

    // Length check
    if (password.length >= 8) {
      score += 1;
    } else {
      feedback.push('Use at least 8 characters');
    }

    // Uppercase check
    if (/[A-Z]/.test(password)) {
      score += 1;
    } else if (password.length >= 8) {
      feedback.push('Add an uppercase letter');
    }

    // Lowercase check
    if (/[a-z]/.test(password)) {
      score += 1;
    } else if (password.length >= 8) {
      feedback.push('Add a lowercase letter');
    }

    // Number check
    if (/\d/.test(password)) {
      score += 1;
    } else if (password.length >= 8) {
      feedback.push('Add a number');
    }

    // Special character check
    if (/[^A-Za-z0-9]/.test(password)) {
      score += 1;
    } else if (password.length >= 8) {
      feedback.push('Add a special character');
    }

    let label: string;
    let color: string;

    switch (score) {
      case 0:
      case 1:
        label = 'Weak';
        color = 'bg-red-500';
        break;
      case 2:
        label = 'Medium';
        color = 'bg-yellow-500';
        break;
      case 3:
      case 4:
        label = 'Strong';
        color = 'bg-green-500';
        break;
      case 5:
        label = 'Very Strong';
        color = 'bg-emerald-600';
        break;
      default:
        label = 'Weak';
        color = 'bg-red-500';
    }

    return { score, label, color, feedback };
  }, [password]);

  return (
    <div className={`mt-2 ${className}`}>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-medium">Password strength:</span>
        <span className={`text-sm font-semibold ${
          score <= 1 ? 'text-red-600' :
          score === 2 ? 'text-yellow-600' :
          score <= 4 ? 'text-green-600' : 'text-emerald-700'
        }`}>
          {label}
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all duration-300 ease-in-out ${color}`}
          style={{ width: `${(score / 5) * 100}%` }}
        ></div>
      </div>
      {feedback.length > 0 && (
        <ul className="mt-2 text-xs text-gray-500 space-y-1">
          {feedback.map((item, index) => (
            <li key={index} className="flex items-start">
              <span className="text-red-500 mr-1">•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PasswordStrengthIndicator;