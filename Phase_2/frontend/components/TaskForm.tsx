'use client';

import { useState } from 'react';
import { Task, TaskCreate, TaskUpdate } from '../lib/types';
import { createTask, updateTask } from '../lib/api';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface Props {
  mode: 'create' | 'edit';
  task?: Task;
  onSuccess: () => void;
  onCancel?: () => void;
}

export default function TaskForm({ mode, task, onSuccess, onCancel }: Props) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [dueDate, setDueDate] = useState(task?.due_date || '');
  const [reminderDateTime, setReminderDateTime] = useState<string>(task?.reminder_datetime || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    const data: TaskCreate = {
      title,
      description: description || null,
      due_date: dueDate || null,
      ...(reminderDateTime && { reminder_datetime: reminderDateTime })
    };

    if (mode === 'create') {
      const result = await createTask(data);
      if (result.error) {
        setError(result.error);
      } else {
        setTitle('');
        setDescription('');
        setDueDate('');
        setReminderDateTime('');
        onSuccess();
      }
    } else if (task?.id) {
      const updateData: TaskUpdate = {
        title,
        description: description || null,
        due_date: dueDate || null,
        ...(reminderDateTime && { reminder_datetime: reminderDateTime })
      };
      const result = await updateTask(task.id, updateData);
      if (result.error) {
        setError(result.error);
      } else {
        onSuccess();
      }
    }

    setLoading(false);
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 px-6 py-4 flex items-center justify-between">
        <h3 className="text-xl font-semibold text-white">
          {mode === 'create' ? '✨ Create New Task' : '✏️ Edit Task'}
        </h3>
        {onCancel && (
          <button
            onClick={onCancel}
            className="text-white hover:bg-white/20 rounded-lg p-1 transition-colors"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        )}
      </div>

      <div className="p-6 space-y-5">
        {/* Title */}
        <div>
          <label className="block text-sm font-semibold mb-2 text-gray-700">
            Task Title <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900 font-medium placeholder-gray-400"
            placeholder="What needs to be done?"
            required
            maxLength={200}
          />
          <p className="mt-1 text-xs text-gray-500">{title.length}/200 characters</p>
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-semibold mb-2 text-gray-700">
            Description
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900 placeholder-gray-400 resize-none"
            placeholder="Add more details about this task..."
            rows={4}
            maxLength={1000}
          />
          <p className="mt-1 text-xs text-gray-500">{description.length}/1000 characters</p>
        </div>

        {/* Due Date and Reminder in Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Due Date */}
          <div>
            <label className="block text-sm font-semibold mb-2 text-gray-700">
              📅 Due Date
            </label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900"
            />
          </div>

          {/* Reminder */}
          <div>
            <label className="block text-sm font-semibold mb-2 text-gray-700">
              🔔 Reminder
            </label>
            <input
              type="datetime-local"
              value={reminderDateTime}
              onChange={(e) => setReminderDateTime(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900"
            />
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="flex items-center gap-2 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
            <svg className="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-sm text-red-700 font-medium">{error}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-3 pt-2">
          <button
            type="button"
            onClick={handleSubmit}
            disabled={loading}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            ) : (
              mode === 'create' ? '✨ Create Task' : '💾 Save Changes'
            )}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="px-6 py-3 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transition-all duration-200"
            >
              Cancel
            </button>
          )}
        </div>
      </div>
    </div>
  );
}