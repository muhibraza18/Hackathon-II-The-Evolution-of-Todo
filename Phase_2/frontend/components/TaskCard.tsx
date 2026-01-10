'use client';

import { useState } from 'react';
import { Task } from '../lib/types';
import { updateTask, deleteTask, toggleComplete } from '../lib/api';
import { PencilIcon, TrashIcon, CalendarIcon, BellIcon } from '@heroicons/react/24/outline';
import Toast from './Toast';

interface Props {
  task: Task;
  onEdit: (task: Task) => void;
  onUpdate: () => void;
  onDelete: () => void;
}

export default function TaskCard({ task, onEdit, onUpdate, onDelete }: Props) {
  const [showToast, setShowToast] = useState(false);

  const handleToggle = async () => {
    await toggleComplete(task.id);
    onUpdate();

    if (!task.completed) {
      setShowToast(true);
    }
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      await deleteTask(task.id);
      onDelete();
    }
  };

  const getPriorityLevel = () => {
    if (!task.due_date) return 'low';

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const dueDate = new Date(task.due_date);
    dueDate.setHours(0, 0, 0, 0);

    const diffTime = dueDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return 'high';
    if (diffDays === 0) return 'high';
    if (diffDays <= 3) return 'medium';
    return 'low';
  };

  const priority = getPriorityLevel();

  const getPriorityColor = () => {
    switch (priority) {
      case 'high': return 'bg-red-500';
      case 'medium': return 'bg-amber-500';
      case 'low': return 'bg-emerald-500';
      default: return 'bg-gray-300';
    }
  };

  const getPriorityBorderColor = () => {
    switch (priority) {
      case 'high': return 'border-red-200 hover:border-red-300';
      case 'medium': return 'border-amber-200 hover:border-amber-300';
      case 'low': return 'border-emerald-200 hover:border-emerald-300';
      default: return 'border-gray-200';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const formatTime = (dateTimeString?: string) => {
    if (!dateTimeString) return '';
    const date = new Date(dateTimeString);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`group relative rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden ${
      task.completed
        ? 'bg-gray-50 border-2 border-gray-200 opacity-70'
        : `bg-white border-2 ${getPriorityBorderColor()} hover:-translate-y-1`
    }`}>
      {/* Priority indicator stripe */}
      <div className={`absolute top-0 left-0 w-2 h-full ${
        priority === 'high' ? 'bg-gradient-to-b from-red-500 to-red-600' :
        priority === 'medium' ? 'bg-gradient-to-b from-amber-500 to-amber-600' : 
        'bg-gradient-to-b from-emerald-500 to-green-600'
      }`}></div>

      <div className="p-5 pl-7">
        {/* Header */}
        <div className="flex justify-between items-start gap-3 mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 mb-2">
              <div className={`w-3 h-3 rounded-full ${getPriorityColor()} shadow-sm flex-shrink-0`} title={`Priority: ${priority}`}></div>
              <h3 className={`font-bold text-lg truncate ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h3>
            </div>

            {task.description && (
              <p className={`text-sm mt-2 line-clamp-2 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
          </div>

          {/* Checkbox */}
          <div className="flex-shrink-0">
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggle}
                className="sr-only peer"
              />
              <div className={`w-11 h-11 rounded-xl border-2 flex items-center justify-center transition-all duration-200 ${
                task.completed 
                  ? 'bg-gradient-to-br from-emerald-500 to-green-600 border-emerald-500' 
                  : 'bg-white border-gray-300 hover:border-emerald-400'
              }`}>
                {task.completed && (
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>
            </label>
          </div>
        </div>

        {/* Meta Information */}
        <div className="flex flex-wrap items-center gap-2 mb-4">
          {task.due_date && (
            <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium ${
              priority === 'high' 
                ? 'bg-red-50 text-red-700 border border-red-200' 
                : priority === 'medium'
                ? 'bg-amber-50 text-amber-700 border border-amber-200'
                : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
            }`}>
              <CalendarIcon className="w-4 h-4" />
              <span>{formatDate(task.due_date)}</span>
            </div>
          )}
          {task.reminder_datetime && (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium bg-blue-50 text-blue-700 border border-blue-200" title={`Reminder: ${formatDate(task.reminder_datetime)} at ${formatTime(task.reminder_datetime)}`}>
              <BellIcon className="w-4 h-4" />
              <span>{formatTime(task.reminder_datetime)}</span>
            </div>
          )}
          {!task.completed && priority === 'high' && (
            <span className="inline-flex items-center px-3 py-1 rounded-lg text-xs font-bold bg-gradient-to-r from-red-500 to-red-600 text-white shadow-sm">
              ⚠️ Urgent
            </span>
          )}
          {!task.completed && priority === 'medium' && (
            <span className="inline-flex items-center px-3 py-1 rounded-lg text-xs font-bold bg-gradient-to-r from-amber-500 to-amber-600 text-white shadow-sm">
              ⏰ Soon
            </span>
          )}
        </div>

        {/* Actions */}
        <div className="flex justify-between items-center pt-3 border-t border-gray-100">
          <div className="flex gap-2">
            <button
              onClick={() => onEdit(task)}
              className="flex items-center gap-1.5 text-gray-600 hover:text-emerald-600 transition-colors duration-200 px-3 py-2 rounded-lg hover:bg-emerald-50 focus:outline-none focus:ring-2 focus:ring-emerald-300 focus:ring-offset-1"
              title="Edit task"
            >
              <PencilIcon className="w-4 h-4" />
              <span className="text-sm font-medium">Edit</span>
            </button>
            <button
              onClick={handleDelete}
              className="flex items-center gap-1.5 text-gray-600 hover:text-red-600 transition-colors duration-200 px-3 py-2 rounded-lg hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-1"
              title="Delete task"
            >
              <TrashIcon className="w-4 h-4" />
              <span className="text-sm font-medium">Delete</span>
            </button>
          </div>

          {task.completed && (
            <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">
              ✓ Completed
            </span>
          )}
        </div>
      </div>

      <Toast
        message="Task completed! 🎉"
        isVisible={showToast}
        onClose={() => setShowToast(false)}
      />
    </div>
  );
}