'use client';

import { Task } from '../../services/tasks';
import PriorityBadge from './PriorityBadge';

interface TaskListProps {
  tasks: Task[];
  onComplete: (taskId: number) => void;
  onEdit: (taskId: number) => void;
  onDelete: (taskId: number) => void;
  isLoading?: boolean;
  completingTaskId?: number | null;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onComplete, onEdit, onDelete, isLoading, completingTaskId }) => {
  const isOverdue = (dateString: string): boolean => {
    const date = new Date(dateString);
    const now = new Date();
    return date < now;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    // Check if same day
    const isToday = date.toDateString() === today.toDateString();
    const isTomorrow = date.toDateString() === tomorrow.toDateString();
    const isPast = date < today;

    // Format time
    const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (isToday) {
      return `Today at ${time}`;
    } else if (isTomorrow) {
      return `Tomorrow at ${time}`;
    } else if (isPast) {
      return `Overdue (${date.toLocaleDateString()} ${time})`;
    } else {
      return `${date.toLocaleDateString()} ${time}`;
    }
  };

  const getDueDateColor = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    date.setHours(0, 0, 0, 0);

    if (date < today) return '#ef4444'; // Red - overdue
    if (date.getTime() === today.getTime()) return '#f59e0b'; // Orange - today
    return '#64748b'; // Gray - future
  };

  if (tasks.length === 0) {
    return null;
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <div key={task.id} className={`task-card ${task.completed ? 'completed' : ''} ${task.due_date && isOverdue(task.due_date) && !task.completed ? 'overdue' : ''}`}>
          {task.due_date && isOverdue(task.due_date) && !task.completed && (
            <div className="overdue-badge">⚠️ OVERDUE</div>
          )}
          <div className="task-checkbox">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onComplete(task.id)}
              id={`task-${task.id}`}
              disabled={completingTaskId === task.id}
            />
            <label htmlFor={`task-${task.id}`}>
              {completingTaskId === task.id && (
                <span className="checkbox-spinner"></span>
              )}
            </label>
          </div>

          <div className="task-content">
            <h3 className="task-title">{task.title}</h3>
            {task.description && <p className="task-description">{task.description}</p>}

            <div className="task-meta">
              {/* Due Date */}
              {task.due_date && (
                <div className="task-due-date" style={{ color: getDueDateColor(task.due_date) }}>
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  {formatDate(task.due_date)}
                </div>
              )}

              {/* Priority */}
              {task.priority && <PriorityBadge priority={task.priority} />}

              {/* Tags */}
              {task.tags && task.tags.length > 0 && (
                <div className="task-tags">
                  {task.tags.slice(0, 3).map((tag) => (
                    <span key={tag} className="tag-chip">
                      #{tag}
                    </span>
                  ))}
                  {task.tags.length > 3 && (
                    <span className="tag-more">+{task.tags.length - 3}</span>
                  )}
                </div>
              )}

              {/* Recurring */}
              {task.recurring_config?.enabled && (
                <div className="task-recurring" title="Recurring task">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="23 4 23 10 17 10"></polyline>
                    <polyline points="1 20 1 14 7 14"></polyline>
                    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
                  </svg>
                  {task.recurring_config.frequency}
                </div>
              )}
            </div>
          </div>

          <div className="task-actions">
            <button
              onClick={() => onEdit(task.id)}
              className="task-action-btn"
              aria-label="Edit task"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="task-action-btn task-action-delete"
              aria-label="Delete task"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
      ))}

      <style jsx>{`
        .task-list {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .task-card {
          position: relative;
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 16px;
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          transition: all 0.2s ease;
        }

        .task-card:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
          border-color: #cbd5e1;
        }

        .task-card.completed {
          opacity: 0.6;
        }

        .task-card.overdue {
          border-color: #ef4444;
          background: #fef2f2;
        }

        .task-card.overdue:hover {
          border-color: #dc2626;
        }

        .overdue-badge {
          position: absolute;
          top: -8px;
          right: -8px;
          background: #ef4444;
          color: white;
          font-size: 0.7rem;
          font-weight: 600;
          padding: 4px 8px;
          border-radius: 12px;
          box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
          z-index: 10;
          animation: pulse 2s infinite;
        }

        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }

        .task-card.completed .task-title {
          text-decoration: line-through;
          color: #94a3b8;
        }

        .task-checkbox {
          padding-top: 2px;
        }

        .task-checkbox input {
          display: none;
        }

        .task-checkbox label {
          width: 20px;
          height: 20px;
          border: 2px solid #cbd5e1;
          border-radius: 6px;
          cursor: pointer;
          display: block;
          transition: all 0.2s ease;
          position: relative;
        }

        .task-checkbox input:checked + label {
          background-color: #0f172a;
          border-color: #0f172a;
        }

        .task-checkbox input:checked + label::after {
          content: '';
          position: absolute;
          left: 5px;
          top: 2px;
          width: 6px;
          height: 10px;
          border: solid white;
          border-width: 0 2px 2px 0;
          transform: rotate(45deg);
        }

        .task-checkbox input:disabled + label {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .checkbox-spinner {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 12px;
          height: 12px;
          border: 2px solid transparent;
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.6s linear infinite;
        }

        @keyframes spin {
          to { transform: translate(-50%, -50%) rotate(360deg); }
        }

        .task-content {
          flex: 1;
          min-width: 0;
        }

        .task-title {
          font-size: 0.95rem;
          font-weight: 500;
          color: #1e293b;
          margin: 0 0 4px 0;
          line-height: 1.4;
        }

        .task-description {
          font-size: 0.85rem;
          color: #64748b;
          margin: 0 0 8px 0;
          line-height: 1.4;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .task-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          align-items: center;
          font-size: 0.8rem;
        }

        .task-due-date {
          display: flex;
          align-items: center;
          gap: 4px;
          font-weight: 500;
        }

        .task-due-date svg {
          flex-shrink: 0;
        }

        .task-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 4px;
        }

        .tag-chip {
          padding: 2px 6px;
          background-color: #f1f5f9;
          color: #475569;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: 500;
        }

        .tag-more {
          color: #94a3b8;
          font-size: 0.75rem;
          font-weight: 500;
        }

        .task-recurring {
          display: flex;
          align-items: center;
          gap: 4px;
          color: #8b5cf6;
          font-weight: 500;
        }

        .task-actions {
          display: flex;
          gap: 4px;
        }

        .task-action-btn {
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: transparent;
          border: none;
          border-radius: 6px;
          color: #94a3b8;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .task-action-btn:hover {
          background-color: #f1f5f9;
          color: #0f172a;
        }

        .task-action-delete:hover {
          background-color: #fef2f2;
          color: #991b1b;
        }

        @media (max-width: 640px) {
          .task-card {
            padding: 12px;
          }

          .task-actions {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
};

export default TaskList;
