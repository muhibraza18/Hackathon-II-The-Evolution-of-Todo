'use client';

import { useState, useEffect, useRef, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../contexts/AuthProvider';
import { useTasks } from '../../hooks/useTasks';
import { TaskFilters as TaskFiltersType, Task } from '../../services/tasks';
import Navbar from '../../components/Navbar';
import TaskForm from '../../components/tasks/TaskForm';
import TaskFilters from '../../components/tasks/TaskFilters';
import TaskList from '../../components/tasks/TaskList';
import toast, { Toaster } from 'react-hot-toast';

export default function TasksPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [filters, setFilters] = useState<TaskFiltersType>({});
  const [editingTask, setEditingTask] = useState<number | null>(null);
  const [completingTaskId, setCompletingTaskId] = useState<number | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Redirect to login if not authenticated
  if (!authLoading && !user) {
    router.push('/login');
    return null;
  }

  if (authLoading) {
    return (
      <div className="loading-container">
        <div className="spinner-box">
          <div className="spinner"></div>
        </div>
        <p className="loading-text">Loading your tasks...</p>
        <style jsx>{`
          .loading-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #f8fafc;
          }

          .spinner-box {
            margin-bottom: 16px;
          }

          .spinner {
            width: 32px;
            height: 32px;
            border: 2.5px solid #e2e8f0;
            border-top-color: #0f172a;
            border-radius: 50%;
            animation: spin 0.8s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
          }

          .loading-text {
            font-size: 0.9rem;
            color: #64748b;
            font-weight: 500;
          }

          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  const { tasks, loading, error, createTask, updateTask, completeTask, optimisticComplete, deleteTask, refresh, getOverdueTasks } =
    useTasks(filters);

  // Track notified tasks to avoid duplicate notifications
  const notifiedTasksRef = useRef<Set<number>>(new Set());

  // Previous tasks ref to detect changes
  const prevTasksRef = useRef<Task[]>([]);

  // Create a stable string representation of filters for polling dependency
  const filtersKey = useMemo(() => JSON.stringify(filters), [filters]);

  // Polling for real-time updates (every 15 seconds - more responsive)
  useEffect(() => {
    const doPoll = async () => {
      const pollTime = new Date().toLocaleTimeString();
      console.log(`🔄 Polling task list at ${pollTime}`);
      setIsRefreshing(true);
      try {
        await refresh();
        setLastUpdated(new Date());
        console.log(`✅ Task list refreshed at ${pollTime}`);
      } catch (err) {
        console.error(`❌ Error refreshing tasks:`, err);
      } finally {
        setIsRefreshing(false);
      }
    };

    // Initial poll on mount
    doPoll();

    // Poll every 15 seconds
    const pollInterval = setInterval(doPoll, 15000); // 15 seconds - more responsive

    return () => clearInterval(pollInterval);
  }, [filtersKey]);  // Use stable string key instead of object reference

  // Check for due/overdue tasks and show notifications
  useEffect(() => {
    const checkDueTasks = () => {
      const now = new Date();
      const oneMinuteFromNow = new Date(now.getTime() + 60 * 1000);

      tasks.forEach(task => {
        if (task.completed || !task.due_date) return;

        const dueDate = new Date(task.due_date);
        const taskId = task.id;

        // Check if task is overdue OR due within 1 minute
        const isOverdue = dueDate < now;
        const isDueSoon = dueDate <= oneMinuteFromNow;

        if ((isOverdue || isDueSoon) && !notifiedTasksRef.current.has(taskId)) {
          // Mark as notified
          notifiedTasksRef.current.add(taskId);

          if (dueDate < now) {
            // Overdue
            console.log(`⚠️ Task "${task.title}" is OVERDUE!`);
            toast.error(`⚠️ "${task.title}" is overdue!`, {
              duration: 5000,
              icon: '⚠️',
            });
          } else {
            // Due now or within 1 minute
            const secondsUntilDue = Math.round((dueDate.getTime() - now.getTime()) / 1000);
            console.log(`🔔 Task "${task.title}" is due in ${secondsUntilDue} seconds`);
            toast(`🔔 Reminder: "${task.title}" is due now!`, {
              duration: 5000,
              icon: '🔔',
            });
          }
        }
      });
    };

    // Run check immediately
    checkDueTasks();

    // Check every 15 seconds (aligned with polling)
    const checkInterval = setInterval(checkDueTasks, 15000);

    return () => clearInterval(checkInterval);
  }, [tasks]);

  const handleCreateTask = async (data: any) => {
    await createTask(data);
    setShowCreateForm(false);
    await refresh();
    setLastUpdated(new Date());
  };

  const handleUpdateTask = async (taskId: number, data: any) => {
    await updateTask(taskId, data);
    setEditingTask(null);
    await refresh();
    setLastUpdated(new Date());
  };

  const handleCompleteTask = async (taskId: number) => {
    setCompletingTaskId(taskId);
    try {
      await optimisticComplete(taskId);
      setLastUpdated(new Date());
      // No need to refresh - optimistic update already handled UI
    } finally {
      setCompletingTaskId(null);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (confirm('Are you sure you want to delete this task?')) {
      await deleteTask(taskId);
      await refresh();
      setLastUpdated(new Date());
    }
  };

  // Safety check: ensure tasks is an array before filtering
  const tasksList = Array.isArray(tasks) ? tasks : [];
  const pendingTasks = tasksList.filter((t) => !t.completed);
  const completedTasks = tasksList.filter((t) => t.completed);

  return (
    <>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#fff',
            color: '#1e293b',
            borderRadius: '12px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
            padding: '12px 16px',
            fontSize: '0.9rem',
            fontWeight: '500',
          },
          success: {
            iconTheme: {
              primary: '#22c55e',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      <Navbar />
      <div className="tasks-page">
        <div className="tasks-container">
          {/* Header */}
          <div className="tasks-header">
            <div className="header-left">
              <div className="title-section">
                <h1>My Tasks</h1>
                <div className="task-stats">
                  <div className="stat-item">
                    <span className="stat-value">{tasksList.length}</span>
                    <span className="stat-label">Total</span>
                  </div>
                  <div className="stat-divider"></div>
                  <div className="stat-item pending">
                    <span className="stat-value">{pendingTasks.length}</span>
                    <span className="stat-label">Pending</span>
                  </div>
                  <div className="stat-divider"></div>
                  <div className="stat-item completed">
                    <span className="stat-value">{completedTasks.length}</span>
                    <span className="stat-label">Completed</span>
                  </div>
                </div>
              </div>
              <p className="last-updated">
                <span className="pulse-dot"></span>
                Last updated: {lastUpdated.toLocaleTimeString()}
              </p>
            </div>
            <div className="header-actions">
              <button
                onClick={() => {
                  refresh();
                  setLastUpdated(new Date());
                }}
                className="btn-secondary"
                disabled={isRefreshing}
                title="Refresh tasks"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className={isRefreshing ? 'spinning' : ''}
                >
                  <polyline points="23 4 23 10 17 10"></polyline>
                  <polyline points="1 20 1 14 7 14"></polyline>
                  <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
                </svg>
                <span className="btn-text">Refresh</span>
              </button>
              <button onClick={() => setShowCreateForm(true)} className="btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span className="btn-text">Add Task</span>
              </button>
            </div>
          </div>

          {/* Filters */}
          <TaskFilters filters={filters} setFilters={setFilters} />

          {/* Error */}
          {error && (
            <div className="error-banner">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              {error}
            </div>
          )}

          {/* Loading indicator */}
          {loading && tasksList.length === 0 && (
            <div className="loading-tasks">
              <div className="spinner-small"></div>
              <p>Loading your tasks...</p>
            </div>
          )}

          {/* Pending Tasks */}
          {pendingTasks.length > 0 && (
            <>
              <div className="section-header">
                <h2 className="section-title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  Pending Tasks
                </h2>
                <span className="section-count">{pendingTasks.length}</span>
              </div>
              <TaskList
                tasks={pendingTasks}
                onComplete={handleCompleteTask}
                onEdit={(taskId) => setEditingTask(taskId)}
                onDelete={handleDeleteTask}
                isLoading={loading}
                completingTaskId={completingTaskId}
              />
            </>
          )}

          {/* Completed Tasks */}
          {completedTasks.length > 0 && (
            <>
              <div className="section-header">
                <h2 className="section-title completed">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                  Completed Tasks
                </h2>
                <span className="section-count">{completedTasks.length}</span>
              </div>
              <TaskList
                tasks={completedTasks}
                onComplete={handleCompleteTask}
                onEdit={(taskId) => setEditingTask(taskId)}
                onDelete={handleDeleteTask}
                isLoading={loading}
                completingTaskId={completingTaskId}
              />
            </>
          )}

          {/* Empty State */}
          {tasksList.length === 0 && !loading && (
            <div className="empty-state">
              <div className="empty-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M9 11l3 3L22 4"></path>
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                </svg>
              </div>
              <h3>No tasks yet</h3>
              <p>Create your first task to get started organizing your work!</p>
              <button onClick={() => setShowCreateForm(true)} className="btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Create Your First Task
              </button>
            </div>
          )}
        </div>

        {/* Create Task Modal */}
        {showCreateForm && (
          <div className="modal-overlay" onClick={() => setShowCreateForm(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <TaskForm
                onSubmit={handleCreateTask}
                onCancel={() => setShowCreateForm(false)}
              />
            </div>
          </div>
        )}

        {/* Edit Task Modal */}
        {editingTask && (
          <div className="modal-overlay" onClick={() => setEditingTask(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <TaskForm
                task={tasksList.find((t) => t.id === editingTask)}
                onSubmit={(data) => handleUpdateTask(editingTask, data)}
                onCancel={() => setEditingTask(null)}
              />
            </div>
          </div>
        )}
      </div>

      <style jsx global>{`
        body {
          margin: 0;
          padding: 0;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
          background-color: #f8fafc;
          -webkit-font-smoothing: antialiased;
        }
      `}</style>

      <style jsx>{`
        .tasks-page {
          min-height: calc(100vh - 60px);
          padding: 32px 24px;
        }

        .tasks-container {
          max-width: 1000px;
          margin: 0 auto;
        }

        /* Header */
        .tasks-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 32px;
          gap: 24px;
        }

        .header-left {
          flex: 1;
        }

        .title-section {
          margin-bottom: 12px;
        }

        .tasks-header h1 {
          font-size: 2.25rem;
          font-weight: 700;
          margin: 0 0 16px 0;
          color: #0f172a;
          letter-spacing: -0.02em;
        }

        .task-stats {
          display: flex;
          align-items: center;
          gap: 16px;
          margin-top: 12px;
        }

        .stat-item {
          display: flex;
          flex-direction: column;
          gap: 2px;
        }

        .stat-value {
          font-size: 1.5rem;
          font-weight: 700;
          color: #0f172a;
          line-height: 1;
        }

        .stat-label {
          font-size: 0.75rem;
          color: #64748b;
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .stat-item.pending .stat-value {
          color: #f59e0b;
        }

        .stat-item.completed .stat-value {
          color: #10b981;
        }

        .stat-divider {
          width: 1px;
          height: 32px;
          background-color: #e2e8f0;
        }

        .last-updated {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 0.85rem;
          color: #64748b;
          margin: 0;
          font-weight: 500;
        }

        .pulse-dot {
          width: 8px;
          height: 8px;
          background-color: #22c55e;
          border-radius: 50%;
          animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }

        /* Header Actions */
        .header-actions {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }

        .btn-primary,
        .btn-secondary {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 12px 20px;
          border-radius: 12px;
          font-size: 0.9rem;
          font-weight: 600;
          cursor: pointer;
          border: none;
          transition: all 0.2s ease;
          white-space: nowrap;
        }

        .btn-primary {
          background-color: #0f172a;
          color: white;
        }

        .btn-primary:hover {
          background-color: #1e293b;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        }

        .btn-primary:active {
          transform: translateY(0);
        }

        .btn-secondary {
          background-color: white;
          color: #0f172a;
          border: 1px solid #e2e8f0;
        }

        .btn-secondary:hover {
          background-color: #f8fafc;
          border-color: #cbd5e1;
        }

        .btn-secondary:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .btn-secondary:disabled:hover {
          background-color: white;
          border-color: #e2e8f0;
          transform: none;
        }

        .btn-text {
          display: none;
        }

        @media (min-width: 640px) {
          .btn-text {
            display: inline;
          }
        }

        .spinning {
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        /* Section Headers */
        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin: 32px 0 16px 0;
        }

        .section-title {
          display: flex;
          align-items: center;
          gap: 10px;
          font-size: 1rem;
          font-weight: 600;
          color: #475569;
          margin: 0;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .section-title.completed {
          color: #10b981;
        }

        .section-count {
          display: flex;
          align-items: center;
          justify-content: center;
          min-width: 28px;
          height: 28px;
          padding: 0 8px;
          background-color: #f1f5f9;
          color: #475569;
          font-size: 0.85rem;
          font-weight: 600;
          border-radius: 14px;
        }

        /* Error Banner */
        .error-banner {
          display: flex;
          align-items: center;
          gap: 10px;
          background-color: #fef2f2;
          color: #991b1b;
          padding: 14px 18px;
          border-radius: 12px;
          border: 1px solid #fecaca;
          margin-bottom: 24px;
          font-size: 0.9rem;
          font-weight: 500;
        }

        /* Loading States */
        .loading-tasks {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 80px 20px;
          gap: 16px;
        }

        .spinner-small {
          width: 28px;
          height: 28px;
          border: 2.5px solid #e2e8f0;
          border-top-color: #0f172a;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        .loading-tasks p {
          color: #64748b;
          margin: 0;
          font-size: 0.95rem;
          font-weight: 500;
        }

        /* Empty State */
        .empty-state {
          text-align: center;
          padding: 80px 20px;
        }

        .empty-icon {
          width: 96px;
          height: 96px;
          margin: 0 auto 24px;
          background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
          border-radius: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #64748b;
        }

        .empty-state h3 {
          font-size: 1.5rem;
          color: #0f172a;
          margin: 0 0 8px 0;
          font-weight: 600;
        }

        .empty-state p {
          color: #64748b;
          margin: 0 0 28px 0;
          font-size: 1rem;
          max-width: 400px;
          margin-left: auto;
          margin-right: auto;
        }

        /* Modal */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: rgba(15, 23, 42, 0.6);
          backdrop-filter: blur(4px);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          animation: fadeIn 0.2s ease;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        .modal-content {
          background: white;
          border-radius: 16px;
          max-width: 600px;
          width: 90%;
          max-height: 90vh;
          overflow-y: auto;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
          animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        /* Responsive */
        @media (max-width: 768px) {
          .tasks-page {
            padding: 24px 16px;
          }

          .tasks-header {
            flex-direction: column;
            gap: 20px;
          }

          .tasks-header h1 {
            font-size: 1.75rem;
          }

          .header-actions {
            width: 100%;
          }

          .btn-primary,
          .btn-secondary {
            flex: 1;
            justify-content: center;
          }

          .task-stats {
            gap: 12px;
          }

          .stat-value {
            font-size: 1.25rem;
          }
        }
      `}</style>
    </>
  );
}