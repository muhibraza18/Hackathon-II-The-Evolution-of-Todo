'use client';

import { useEffect, useRef } from 'react';
import { Task } from '../lib/types';

interface RemindersHandlerProps {
  tasks: Task[];
}

const RemindersHandler = ({ tasks }: RemindersHandlerProps) => {
  const activeNotifications = useRef<Set<string>>(new Set());

  useEffect(() => {
    // Function to check for upcoming reminders
    const checkForReminders = () => {
      const now = new Date();

      tasks.forEach(task => {
        if (task.reminder_datetime && !task.completed) {
          const reminderTime = new Date(task.reminder_datetime);

          // Check if reminder time has arrived and we haven't shown it yet
          if (reminderTime <= now && !activeNotifications.current.has(task.id)) {
            // Check if browser supports notifications
            if ('Notification' in window) {
              // Request permission if not already granted
              if (Notification.permission === 'granted') {
                // Create notification
                const notification = new Notification(`Task Reminder: ${task.title}`, {
                  body: task.description || 'You have a task to complete!',
                  icon: '/favicon.ico', // Use your app's favicon
                  tag: task.id // Prevent duplicate notifications for the same task
                });

                // Mark this notification as shown
                activeNotifications.current.add(task.id);

                // Auto-close notification after 5 seconds
                setTimeout(() => {
                  if (notification.close) {
                    notification.close();
                  }
                }, 5000);
              } else if (Notification.permission !== 'denied') {
                // Request permission to show notifications
                Notification.requestPermission().then(permission => {
                  if (permission === 'granted') {
                    // Show the notification after getting permission
                    const notification = new Notification(`Task Reminder: ${task.title}`, {
                      body: task.description || 'You have a task to complete!',
                      icon: '/favicon.ico',
                      tag: task.id
                    });

                    activeNotifications.current.add(task.id);

                    setTimeout(() => {
                      if (notification.close) {
                        notification.close();
                      }
                    }, 5000);
                  }
                });
              }
            } else {
              // Browser doesn't support notifications, fallback to alert
              // (In a real app, you might want to use a custom toast notification)
              console.log(`Reminder: ${task.title} - ${task.description || 'You have a task to complete!'}`);
            }
          }
        }
      });
    };

    // Check for reminders every 10 seconds to be more responsive
    const interval = setInterval(checkForReminders, 10000); // Check every 10 seconds

    // Initial check
    checkForReminders();

    return () => {
      clearInterval(interval);
    };
  }, [tasks]);

  return null; // This component doesn't render anything visible
};

export default RemindersHandler;