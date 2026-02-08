'use client';

import { useState, useEffect } from 'react';
import { Task, CreateTaskRequest } from '../../services/tasks';

interface TaskFormProps {
  task?: Task;
  onSubmit: (data: CreateTaskRequest) => void | Promise<void>;
  onCancel: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');

  // Convert ISO datetime to datetime-local format (YYYY-MM-DDTHH:mm)
  const [dueDate, setDueDate] = useState(() => {
    if (task?.due_date) {
      const d = new Date(task.due_date);
      // Get local date and time
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      const hours = String(d.getHours()).padStart(2, '0');
      const minutes = String(d.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day}T${hours}:${minutes}`;
    }
    return '';
  });
  const [priority, setPriority] = useState<'low' | 'medium' | 'high' | 'urgent'>(
    task?.priority || 'medium'
  );
  const [tags, setTags] = useState<string[]>(task?.tags || []);
  const [tagInput, setTagInput] = useState('');
  const [recurringEnabled, setRecurringEnabled] = useState(
    task?.recurring_config?.enabled || false
  );
  const [recurringFrequency, setRecurringFrequency] = useState<'daily' | 'weekly' | 'monthly'>(
    task?.recurring_config?.frequency || 'weekly'
  );
  const [recurringInterval, setRecurringInterval] = useState(
    task?.recurring_config?.interval || 1
  );
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setSubmitting(true);
    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
        due_date: dueDate || undefined,
        priority,
        tags: tags.length > 0 ? tags : undefined,
        recurring_config: recurringEnabled
          ? {
              enabled: true,
              frequency: recurringFrequency,
              interval: recurringInterval,
            }
          : undefined,
      });
    } finally {
      setSubmitting(false);
    }
  };

  const addTag = () => {
    const tag = tagInput.trim().toLowerCase();
    if (tag && !tags.includes(tag) && tags.length < 10) {
      setTags([...tags, tag]);
      setTagInput('');
    }
  };

  const removeTag = (tag: string) => {
    setTags(tags.filter((t) => t !== tag));
  };

  const handleTagInputKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addTag();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <div className="task-form-header">
        <h2>{task ? 'Edit Task' : 'New Task'}</h2>
        <button type="button" onClick={onCancel} className="close-btn" aria-label="Close">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div className="task-form-body">
        {/* Title */}
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            required
            maxLength={200}
          />
        </div>

        {/* Description */}
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details..."
            rows={3}
            maxLength={1000}
          />
        </div>

        {/* Due Date */}
        <div className="form-group">
          <label htmlFor="dueDate">Due Date & Time</label>
          <input
            id="dueDate"
            type="datetime-local"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            min={new Date().toISOString().slice(0, 16)}
          />
        </div>

        {/* Priority */}
        <div className="form-group">
          <label htmlFor="priority">Priority</label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as any)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>

        {/* Tags */}
        <div className="form-group">
          <label htmlFor="tags">Tags</label>
          <div className="tags-input-container">
            <div className="tags-list">
              {tags.map((tag) => (
                <span key={tag} className="tag-chip">
                  #{tag}
                  <button
                    type="button"
                    onClick={() => removeTag(tag)}
                    className="tag-remove"
                    aria-label={`Remove ${tag} tag`}
                  >
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </span>
              ))}
            </div>
            <input
              id="tags"
              type="text"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyDown={handleTagInputKeyDown}
              placeholder="Add tag..."
              disabled={tags.length >= 10}
            />
          </div>
          <small>{tags.length}/10 tags</small>
        </div>

        {/* Recurring */}
        <div className="form-group">
          <div className="checkbox-group">
            <input
              id="recurring"
              type="checkbox"
              checked={recurringEnabled}
              onChange={(e) => setRecurringEnabled(e.target.checked)}
            />
            <label htmlFor="recurring">Recurring Task</label>
          </div>

          {recurringEnabled && (
            <div className="recurring-options">
              <select
                value={recurringFrequency}
                onChange={(e) => setRecurringFrequency(e.target.value as any)}
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
              <input
                type="number"
                value={recurringInterval}
                onChange={(e) => setRecurringInterval(Math.max(1, parseInt(e.target.value) || 1))}
                min={1}
                max={52}
              />
              <span>times</span>
            </div>
          )}
        </div>
      </div>

      <div className="task-form-footer">
        <button type="button" onClick={onCancel} className="btn-secondary" disabled={submitting}>
          Cancel
        </button>
        <button type="submit" className="btn-primary" disabled={submitting || !title.trim()}>
          {submitting ? 'Saving...' : task ? 'Save Changes' : 'Create Task'}
        </button>
      </div>

      <style jsx>{`
        .task-form {
          display: flex;
          flex-direction: column;
        }

        .task-form-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 24px;
          border-bottom: 1px solid #e2e8f0;
        }

        .task-form-header h2 {
          font-size: 1.25rem;
          font-weight: 600;
          color: #0f172a;
          margin: 0;
        }

        .close-btn {
          background: none;
          border: none;
          color: #64748b;
          cursor: pointer;
          padding: 4px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s ease;
        }

        .close-btn:hover {
          background-color: #f1f5f9;
          color: #0f172a;
        }

        .task-form-body {
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .form-group label {
          font-size: 0.875rem;
          font-weight: 500;
          color: #475569;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
          padding: 10px 12px;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          font-size: 0.95rem;
          color: #1e293b;
          transition: all 0.2s ease;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
          outline: none;
          border-color: #0f172a;
          box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
        }

        .form-group textarea {
          resize: vertical;
          font-family: inherit;
        }

        .form-group small {
          font-size: 0.75rem;
          color: #94a3b8;
        }

        .tags-input-container {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          padding: 8px 12px;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          min-height: 42px;
        }

        .tags-input-container:focus-within {
          border-color: #0f172a;
          box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
        }

        .tags-list {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
        }

        .tag-chip {
          display: flex;
          align-items: center;
          gap: 4px;
          padding: 4px 8px;
          background-color: #f1f5f9;
          color: #475569;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .tag-remove {
          background: none;
          border: none;
          color: #64748b;
          cursor: pointer;
          padding: 0;
          display: flex;
          align-items: center;
          opacity: 0.7;
        }

        .tag-remove:hover {
          opacity: 1;
          color: #0f172a;
        }

        .tags-input-container input {
          flex: 1;
          min-width: 100px;
          border: none;
          outline: none;
          padding: 4px 0;
          font-size: 0.9rem;
        }

        .checkbox-group {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .checkbox-group input[type="checkbox"] {
          width: 18px;
          height: 18px;
          cursor: pointer;
        }

        .checkbox-group label {
          cursor: pointer;
          margin: 0;
        }

        .recurring-options {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 8px;
        }

        .recurring-options select,
        .recurring-options input {
          padding: 8px 12px;
        }

        .recurring-options input {
          width: 70px;
        }

        .task-form-footer {
          display: flex;
          justify-content: flex-end;
          gap: 12px;
          padding: 20px 24px;
          border-top: 1px solid #e2e8f0;
        }

        .btn-primary,
        .btn-secondary {
          padding: 10px 20px;
          border-radius: 8px;
          font-size: 0.9rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-primary {
          background-color: #0f172a;
          color: white;
          border: none;
        }

        .btn-primary:hover:not(:disabled) {
          background-color: #1e293b;
        }

        .btn-primary:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .btn-secondary {
          background-color: white;
          color: #475569;
          border: 1px solid #e2e8f0;
        }

        .btn-secondary:hover:not(:disabled) {
          background-color: #f8fafc;
          border-color: #cbd5e1;
        }
      `}</style>
    </form>
  );
};

export default TaskForm;
