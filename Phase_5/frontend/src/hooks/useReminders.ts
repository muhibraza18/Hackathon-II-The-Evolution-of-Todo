'use client';

import { useState, useEffect, useRef } from 'react';
import api from '../services/api';

interface Reminder {
  task_id: string;
  title: string;
  user_id: string;
  due_date: string;
  timestamp: string;
}

interface UseRemindersResult {
  reminders: Reminder[];
  isLoading: boolean;
  error: string | null;
  checkReminders: () => Promise<void>;
}

const STORAGE_KEY = 'seenReminderIds';
const REMINDER_WINDOW_MS = 5 * 60 * 1000; // 5 minutes - show reminders for tasks due within 5 minutes

/**
 * Load seen reminder IDs from localStorage
 */
const loadSeenReminderIds = (): Set<string> => {
  if (typeof window === 'undefined') return new Set();
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      // Clean up old reminder IDs (older than 24 hours) to prevent unlimited growth
      const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);
      const cleaned = parsed.filter((item: { id: string; timestamp: number }) =>
        item.timestamp > oneDayAgo
      );
      if (cleaned.length !== parsed.length) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(cleaned));
      }
      return new Set(cleaned.map((item: { id: string; timestamp: number }) => item.id));
    }
  } catch (e) {
    console.error('Error loading seen reminder IDs:', e);
  }
  return new Set();
};

/**
 * Save a seen reminder ID to localStorage
 */
const saveSeenReminderId = (id: string) => {
  if (typeof window === 'undefined') return;
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    const current = stored ? JSON.parse(stored) : [];
    current.push({ id, timestamp: Date.now() });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
  } catch (e) {
    console.error('Error saving seen reminder ID:', e);
  }
};

/**
 * Hook to poll for reminders from the backend
 * Checks every 10 seconds for new reminders
 * Shows notifications for tasks due within 5 minutes or already overdue
 */
export const useReminders = (): UseRemindersResult => {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const seenReminderIdsRef = useRef<Set<string>>(new Set());

  // Initialize seen reminder IDs from localStorage on mount
  useEffect(() => {
    seenReminderIdsRef.current = loadSeenReminderIds();
  }, []);

  /**
   * Check for reminders from the backend
   * Shows reminders for tasks due within REMINDER_WINDOW_MS or already overdue
   */
  const checkReminders = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Get current user's tasks
      const response = await api.get<{ tasks: any[] }>('/api/tasks');

      if (response.tasks && Array.isArray(response.tasks)) {
        const now = Date.now();
        const newReminders: Reminder[] = [];

        for (const task of response.tasks) {
          // Skip completed tasks
          if (task.completed) continue;

          // Skip tasks without due dates
          if (!task.due_date) continue;

          // Check if task is due soon or already overdue
          const dueDate = new Date(task.due_date).getTime();
          const timeUntilDue = dueDate - now;

          // Show reminder if task is due within REMINDER_WINDOW_MS or already overdue
          if (timeUntilDue <= REMINDER_WINDOW_MS) {
            const reminderId = `reminder-${task.id}-${task.due_date}`;

            // Only show if we haven't seen this reminder yet
            if (!seenReminderIdsRef.current.has(reminderId)) {
              newReminders.push({
                task_id: String(task.id),
                title: task.title,
                user_id: String(task.user_id),
                due_date: task.due_date,
                timestamp: new Date().toISOString(),
              });

              // Mark as seen in memory
              seenReminderIdsRef.current.add(reminderId);

              // Persist to localStorage
              saveSeenReminderId(reminderId);
            }
          }
        }

        setReminders(newReminders);
      }
    } catch (err: any) {
      console.error('Error checking reminders:', err);
      setError(err.message || 'Failed to check reminders');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Check immediately on mount
    checkReminders();

    // Poll every 10 seconds (more frequent than before)
    const interval = setInterval(() => {
      checkReminders();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  return {
    reminders,
    isLoading,
    error,
    checkReminders,
  };
};
