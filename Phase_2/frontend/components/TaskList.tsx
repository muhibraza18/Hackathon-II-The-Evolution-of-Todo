'use client';

import { useState, useEffect } from 'react';
import { Task, TaskUpdate } from '../lib/types';
import { fetchTasks } from '../lib/api';
import TaskForm from './TaskForm';
import TaskItem from './TaskItem';
import { PlusIcon } from '@heroicons/react/24/outline';

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState(false);

  const loadTasks = async () => {
    setLoading(true);
    setError('');
    const result = await fetchTasks();
    if (result.error) {
      setError(result.error);
    } else if (result.data) {
      setTasks(result.data);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleCancel = () => {
    setEditingTask(null);
    setShowForm(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 py-8">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
              Tasks
            </h1>
            <p className="text-gray-600 mt-2 text-sm sm:text-base">Manage your daily tasks</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="flex items-center gap-2 px-5 sm:px-6 py-2.5 sm:py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white font-semibold rounded-xl hover:from-emerald-600 hover:to-green-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
          >
            <PlusIcon className="w-5 h-5" />
            <span>{showForm ? 'Close' : 'New Task'}</span>
          </button>
        </div>

        {/* Task Form */}
        {showForm && (
          <div className="mb-8 animate-slideDown">
            <TaskForm
              mode={editingTask ? 'edit' : 'create'}
              task={editingTask || undefined}
              onSuccess={() => {
                loadTasks();
                handleCancel();
              }}
              onCancel={handleCancel}
            />
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-20">
            <div className="relative w-16 h-16 mx-auto mb-4">
              <div className="absolute inset-0 border-4 border-emerald-200 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-emerald-600 rounded-full border-t-transparent animate-spin"></div>
            </div>
            <p className="text-gray-600 font-medium">Loading tasks...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-r-xl shadow-sm mb-6">
            <div className="flex items-center gap-3">
              <svg className="w-6 h-6 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span className="text-red-700 font-medium">{error}</span>
            </div>
          </div>
        )}

        {/* Tasks */}
        {!loading && (
          <div className="space-y-4">
            {tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={handleEdit}
                onUpdate={loadTasks}
                onDelete={loadTasks}
              />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && tasks.length === 0 && (
          <div className="text-center py-20 bg-white/60 backdrop-blur-sm rounded-3xl border-2 border-dashed border-emerald-200 shadow-lg">
            <div className="inline-flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 bg-gradient-to-br from-emerald-100 to-green-100 rounded-full mb-6">
              <svg className="w-10 h-10 sm:w-12 sm:h-12 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2">No tasks yet</h3>
            <p className="text-sm sm:text-base text-gray-600 mb-6 px-4">Create your first task to get started!</p>
            <button
              onClick={() => setShowForm(true)}
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white font-semibold rounded-xl hover:from-emerald-600 hover:to-green-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
            >
              <PlusIcon className="w-5 h-5" />
              Create Your First Task
            </button>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-slideDown {
          animation: slideDown 0.3s ease-out;
        }
      `}</style>
    </div>
  );
}