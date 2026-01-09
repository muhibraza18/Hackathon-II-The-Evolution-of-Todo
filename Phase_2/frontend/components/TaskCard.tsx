'use client';

import { useState } from 'react';
import { Task } from '../lib/types';
import { updateTask, deleteTask, toggleComplete } from '../lib/api';
import { PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
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

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div className={`group relative p-5 border-2 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 ${
      task.completed
        ? 'bg-gray-50 border-gray-200 opacity-70'
        : 'bg-white border-emerald-100 hover:border-emerald-300 hover:-translate-y-1'
    }`}>
      {/* Priority indicator stripe */}
      <div className={`absolute top-0 left-0 w-1.5 h-full rounded-l-2xl ${
        priority === 'high' ? 'bg-red-500' :
        priority === 'medium' ? 'bg-amber-500' : 'bg-emerald-500'
      }`}></div>

      <div className="flex justify-between items-start pl-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 mb-2">
            <div className={`w-3 h-3 rounded-full ${getPriorityColor()} shadow-sm`} title={`Priority: ${priority}`}></div>
            <h3 className={`font-bold text-lg truncate ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
          </div>

          {task.description && (
            <p className={`text-sm mt-2 ml-6 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}

          <div className="flex items-center mt-3 ml-6 space-x-3 text-sm">
            {task.due_date && (
              <div className="flex items-center bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-200">
                <svg className="w-4 h-4 mr-1.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span className={`font-medium ${
                  priority === 'high' ? 'text-red-600' : 
                  priority === 'medium' ? 'text-amber-600' : 'text-gray-600'
                }`}>
                  {formatDate(task.due_date)}
                </span>
              </div>
            )}
            {task.reminder_datetime && (
              <div className="flex items-center bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200" title={`Reminder: ${task.reminder_datetime}`}>
                <svg className="w-4 h-4 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
                </svg>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 ml-3">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            className="w-6 h-6 text-emerald-600 rounded-md focus:ring-emerald-500 focus:ring-2 border-2 border-gray-300 cursor-pointer transition-all duration-200 hover:border-emerald-400"
          />
        </div>
      </div>

      <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-100 pl-3">
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(task)}
            className="flex items-center gap-1.5 text-gray-600 hover:text-emerald-600 transition-colors duration-200 px-3 py-1.5 rounded-lg hover:bg-emerald-50 focus:outline-none focus:ring-2 focus:ring-emerald-300 focus:ring-offset-1"
            title="Edit task"
          >
            <PencilIcon className="w-4 h-4" />
            <span className="text-sm font-medium">Edit</span>
          </button>
          <button
            onClick={handleDelete}
            className="flex items-center gap-1.5 text-gray-600 hover:text-red-600 transition-colors duration-200 px-3 py-1.5 rounded-lg hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-1"
            title="Delete task"
          >
            <TrashIcon className="w-4 h-4" />
            <span className="text-sm font-medium">Delete</span>
          </button>
        </div>

        {!task.completed && priority === 'high' && (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-red-500 to-red-600 text-white shadow-sm">
            Urgent
          </span>
        )}
        {!task.completed && priority === 'medium' && (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-amber-500 to-amber-600 text-white shadow-sm">
            Soon
          </span>
        )}
      </div>

      <Toast
        message="Task completed! 🎉"
        isVisible={showToast}
        onClose={() => setShowToast(false)}
      />
    </div>
  );
}