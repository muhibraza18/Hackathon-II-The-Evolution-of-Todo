'use client';

import { useEffect, useRef } from 'react';
import { Task } from '../lib/types';

interface RemindersHandlerProps {
  tasks: Task[];
}

const RemindersHandler = ({ tasks }: RemindersHandlerProps) => {
  const activeNotifications = useRef<Set<string | number>>(new Set());
  const hasRequestedPermission = useRef(false);

  useEffect(() => {
    // Request notification permission on mount (only once)
    const requestNotificationPermission = async () => {
      if ('Notification' in window && !hasRequestedPermission.current) {
        hasRequestedPermission.current = true;
        
        if (Notification.permission === 'default') {
          try {
            const permission = await Notification.requestPermission();
            console.log('Notification permission:', permission);
          } catch (error) {
            console.error('Error requesting notification permission:', error);
          }
        }
      }
    };

    requestNotificationPermission();
  }, []);

  useEffect(() => {
    // Function to check for upcoming reminders
    const checkForReminders = () => {
      const now = new Date();
      
      console.log('Checking reminders at:', now.toLocaleString());
      console.log('Total tasks:', tasks.length);

      tasks.forEach(task => {
        if (task.reminder_datetime && !task.completed && task.id) {
          const reminderTime = new Date(task.reminder_datetime);
          
          console.log(`Task: ${task.title}`);
          console.log(`Reminder time: ${reminderTime.toLocaleString()}`);
          console.log(`Current time: ${now.toLocaleString()}`);
          console.log(`Should remind: ${reminderTime <= now && !activeNotifications.current.has(task.id)}`);

          // Check if reminder time has arrived (within 1 minute window) and we haven't shown it yet
          const timeDiff = now.getTime() - reminderTime.getTime();
          const withinWindow = timeDiff >= 0 && timeDiff < 60000; // Within 1 minute after reminder time

          if (withinWindow && !activeNotifications.current.has(task.id)) {
            // Check if browser supports notifications
            if ('Notification' in window && Notification.permission === 'granted') {
              console.log('Showing notification for:', task.title);
              
              try {
                // Create notification
                const notification = new Notification(`🔔 Task Reminder: ${task.title}`, {
                  body: task.description || 'You have a task to complete!',
                  icon: '/favicon.ico',
                  tag: `task-${task.id}`,
                  requireInteraction: false,
                  silent: false
                });

                // Mark this notification as shown
                activeNotifications.current.add(task.id);

                // Handle notification click
                notification.onclick = () => {
                  window.focus();
                  notification.close();
                };

                // Auto-close notification after 10 seconds
                setTimeout(() => {
                  notification.close();
                }, 10000);

                console.log('Notification created successfully');
              } catch (error) {
                console.error('Error creating notification:', error);
              }
            } else if ('Notification' in window && Notification.permission === 'default') {
              console.log('Notification permission not granted, requesting...');
              Notification.requestPermission().then(permission => {
                console.log('Permission result:', permission);
              });
            } else {
              console.log('Notifications not supported or permission denied');
            }
          }
        }
      });
    };

    // Check for reminders every 30 seconds
    const interval = setInterval(checkForReminders, 30000);

    // Initial check after 1 second (to allow component to mount)
    const initialTimeout = setTimeout(checkForReminders, 1000);

    return () => {
      clearInterval(interval);
      clearTimeout(initialTimeout);
    };
  }, [tasks]);

  // Clean up shown notifications when tasks change (e.g., task completed or deleted)
  useEffect(() => {
    const taskIds = new Set<string | number>(tasks.filter(t => t.id).map(t => t.id!));
    const notificationsToRemove: (string | number)[] = [];

    activeNotifications.current.forEach(id => {
      if (!taskIds.has(id)) {
        notificationsToRemove.push(id);
      }
    });

    notificationsToRemove.forEach(id => {
      activeNotifications.current.delete(id);
    });
  }, [tasks]);

  return null; // This component doesn't render anything visible
};

export default RemindersHandler;












// 'use client';

// import { useEffect, useRef } from 'react';
// import { Task } from '../lib/types';

// interface RemindersHandlerProps {
//   tasks: Task[];
// }

// const RemindersHandler = ({ tasks }: RemindersHandlerProps) => {
//   const activeNotifications = useRef<Set<string>>(new Set());

//   useEffect(() => {
//     // Function to check for upcoming reminders
//     const checkForReminders = () => {
//       const now = new Date();

//       tasks.forEach(task => {
//         if (task.reminder_datetime && !task.completed) {
//           const reminderTime = new Date(task.reminder_datetime);

//           // Check if reminder time has arrived and we haven't shown it yet
//           if (reminderTime <= now && !activeNotifications.current.has(task.id)) {
//             // Check if browser supports notifications
//             if ('Notification' in window) {
//               // Request permission if not already granted
//               if (Notification.permission === 'granted') {
//                 // Create notification
//                 const notification = new Notification(`Task Reminder: ${task.title}`, {
//                   body: task.description || 'You have a task to complete!',
//                   icon: '/favicon.ico', // Use your app's favicon
//                   tag: task.id // Prevent duplicate notifications for the same task
//                 });

//                 // Mark this notification as shown
//                 activeNotifications.current.add(task.id);

//                 // Auto-close notification after 5 seconds
//                 setTimeout(() => {
//                   if (notification.close) {
//                     notification.close();
//                   }
//                 }, 5000);
//               } else if (Notification.permission !== 'denied') {
//                 // Request permission to show notifications
//                 Notification.requestPermission().then(permission => {
//                   if (permission === 'granted') {
//                     // Show the notification after getting permission
//                     const notification = new Notification(`Task Reminder: ${task.title}`, {
//                       body: task.description || 'You have a task to complete!',
//                       icon: '/favicon.ico',
//                       tag: task.id
//                     });

//                     activeNotifications.current.add(task.id);

//                     setTimeout(() => {
//                       if (notification.close) {
//                         notification.close();
//                       }
//                     }, 5000);
//                   }
//                 });
//               }
//             } else {
//               // Browser doesn't support notifications, fallback to alert
//               // (In a real app, you might want to use a custom toast notification)
//               console.log(`Reminder: ${task.title} - ${task.description || 'You have a task to complete!'}`);
//             }
//           }
//         }
//       });
//     };

//     // Check for reminders every 10 seconds to be more responsive
//     const interval = setInterval(checkForReminders, 10000); // Check every 10 seconds

//     // Initial check
//     checkForReminders();

//     return () => {
//       clearInterval(interval);
//     };
//   }, [tasks]);

//   return null; // This component doesn't render anything visible
// };

// export default RemindersHandler;