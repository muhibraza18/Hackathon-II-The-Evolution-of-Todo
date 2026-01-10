"use client";

import { useState, useEffect } from "react";
import { Task } from "../lib/types";
import { fetchTasks } from "../lib/api";
import TaskForm from "./TaskForm";
import TaskCard from "./TaskCard";
import RemindersHandler from "./RemindersHandler";
import { PlusIcon } from '@heroicons/react/24/outline';
import { useAuth } from '@/contexts/AuthContext';

export default function TaskTabs() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [activeTab, setActiveTab] = useState<"today" | "pending" | "overdue" | "completed">("today");
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('newest');
  const { user } = useAuth();

  const loadTasks = async () => {
    setLoading(true);
    setError("");
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

  const getPriorityLevel = (task: Task): string => {
    if (!task.due_date) return 'low';
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const dueDate = new Date(task.due_date);
    dueDate.setHours(0, 0, 0, 0);
    const diffTime = dueDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays < 0 || diffDays === 0) return 'high';
    if (diffDays <= 3) return 'medium';
    return 'low';
  };

  // Filter tasks based on active tab and filters
  const getFilteredTasks = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let filtered = tasks;

    // Tab filtering
    if (activeTab === "today") {
      // Show ALL tasks due today (both completed and not completed)
      filtered = tasks.filter((task) => {
        if (task.due_date) {
          const taskDueDate = new Date(task.due_date);
          taskDueDate.setHours(0, 0, 0, 0);
          return taskDueDate.getTime() === today.getTime();
        }
        // Also show tasks without due date
        return true;
      });
    } else if (activeTab === "pending") {
      filtered = tasks.filter((task) => !task.completed);
    } else if (activeTab === "overdue") {
      // Show overdue tasks (not completed and past due date)
      filtered = tasks.filter((task) => {
        if (task.completed) return false;
        if (task.due_date) {
          const taskDueDate = new Date(task.due_date);
          taskDueDate.setHours(0, 0, 0, 0);
          return taskDueDate.getTime() < today.getTime();
        }
        return false;
      });
    } else if (activeTab === "completed") {
      filtered = tasks.filter((task) => task.completed);
    }

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.description?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(task =>
        statusFilter === 'completed' ? task.completed : !task.completed
      );
    }

    // Priority filter
    if (priorityFilter !== 'all') {
      filtered = filtered.filter(task => {
        const priority = getPriorityLevel(task);
        return priority === priorityFilter;
      });
    }

    // Sort
    if (sortBy === 'newest') {
      filtered.sort((a, b) => {
        const aId = typeof a.id === 'number' ? a.id : 0;
        const bId = typeof b.id === 'number' ? b.id : 0;
        return bId - aId;
      });
    } else if (sortBy === 'oldest') {
      filtered.sort((a, b) => {
        const aId = typeof a.id === 'number' ? a.id : 0;
        const bId = typeof b.id === 'number' ? b.id : 0;
        return aId - bId;
      });
    } else if (sortBy === 'dueDate') {
      filtered.sort((a, b) => {
        if (!a.due_date) return 1;
        if (!b.due_date) return -1;
        return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
      });
    }

    return filtered;
  };

  const filteredTasks = getFilteredTasks();

  const handleTaskSuccess = () => {
    loadTasks();
    setShowForm(false);
    setEditingTask(null);
  };

  // Calculate counts
  const todayCount = tasks.filter((task) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (task.due_date) {
      const taskDueDate = new Date(task.due_date);
      taskDueDate.setHours(0, 0, 0, 0);
      return taskDueDate.getTime() === today.getTime();
    }
    // Count tasks without due date as today tasks
    return true;
  }).length;

  const pendingCount = tasks.filter((task) => !task.completed).length;
  const completedCount = tasks.filter((task) => task.completed).length;

  const overdueCount = tasks.filter((task) => {
    if (task.completed) return false;
    if (task.due_date) {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const taskDueDate = new Date(task.due_date);
      taskDueDate.setHours(0, 0, 0, 0);
      return taskDueDate < today;
    }
    return false;
  }).length;

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Header Section */}
        <div className="mb-6 sm:mb-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white/60 backdrop-blur-sm rounded-2xl shadow-md border border-emerald-100 p-4 sm:p-6">
            <div>
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900">
                Welcome back, <span className="text-emerald-600">{user?.name || 'User'}</span> 👋
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {completedCount} of {tasks.length} tasks completed
              </p>
            </div>
            <div className="flex gap-2 sm:gap-3">
              <button
                onClick={() => setShowForm(!showForm)}
                className="flex items-center gap-2 px-4 sm:px-6 py-2.5 sm:py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white font-semibold rounded-xl hover:from-emerald-600 hover:to-green-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
              >
                <PlusIcon className="w-5 h-5" />
                <span className="hidden sm:inline">{showForm ? 'Close' : 'New Task'}</span>
                <span className="sm:hidden">{showForm ? 'Close' : 'New'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Task Form */}
        {showForm && (
          <div className="mb-6 animate-fadeIn">
            <TaskForm
              mode={editingTask ? "edit" : "create"}
              task={editingTask ?? undefined}
              onSuccess={handleTaskSuccess}
              onCancel={() => {
                setShowForm(false);
                setEditingTask(null);
              }}
            />
          </div>
        )}

        {/* Search and Filters */}
        <div className="mb-6 bg-white/80 backdrop-blur-sm rounded-2xl shadow-md border border-emerald-100 p-4">
          <div className="flex flex-col lg:flex-row gap-3 lg:gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
              />
            </div>

            {/* Filters */}
            <div className="flex gap-2 overflow-x-auto pb-2 lg:pb-0">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-3 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white text-sm font-medium whitespace-nowrap"
              >
                <option value="all">Status</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
              </select>

              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="px-3 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white text-sm font-medium whitespace-nowrap"
              >
                <option value="all">Priority</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white text-sm font-medium whitespace-nowrap"
              >
                <option value="newest">Newest</option>
                <option value="oldest">Oldest</option>
                <option value="dueDate">Due Date</option>
              </select>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-6 overflow-x-auto scrollbar-hide">
          <div className="flex gap-2 min-w-max pb-2">
            {[
              { key: 'today', label: 'Today', icon: '📅', count: todayCount },
              { key: 'pending', label: 'Pending', icon: '⏳', count: pendingCount },
              { key: 'overdue', label: 'Overdue', icon: '🔴', count: overdueCount },
              { key: 'completed', label: 'Completed', icon: '✅', count: completedCount }
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`flex items-center gap-2 px-4 sm:px-6 py-3 rounded-xl font-semibold transition-all duration-200 whitespace-nowrap ${
                  activeTab === tab.key
                    ? 'bg-gradient-to-r from-emerald-500 to-green-600 text-white shadow-lg'
                    : 'bg-white/80 text-gray-700 hover:bg-white hover:shadow-md'
                }`}
              >
                <span className="text-lg">{tab.icon}</span>
                <span className="text-sm sm:text-base">{tab.label}</span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                  activeTab === tab.key
                    ? 'bg-white/20 text-white'
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  {tab.count}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="relative w-16 h-16 mb-4">
              <div className="absolute inset-0 border-4 border-emerald-200 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-emerald-600 rounded-full border-t-transparent animate-spin"></div>
            </div>
            <p className="text-gray-600 font-medium">Loading your tasks...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-r-xl shadow-sm">
            <div className="flex items-center gap-3">
              <svg className="w-6 h-6 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span className="text-red-700 font-medium">{error}</span>
            </div>
          </div>
        )}

        {/* Tasks Grid */}
        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {filteredTasks.length > 0 ? (
              filteredTasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onEdit={(task) => {
                    setEditingTask(task);
                    setShowForm(true);
                  }}
                  onUpdate={loadTasks}
                  onDelete={loadTasks}
                />
              ))
            ) : (
              <div className="col-span-full">
                <div className="bg-white/60 backdrop-blur-sm rounded-3xl shadow-lg border border-emerald-100 p-8 sm:p-12 text-center">
                  <div className="inline-flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 bg-gradient-to-br from-emerald-100 to-green-100 rounded-full mb-6">
                    <svg className="w-10 h-10 sm:w-12 sm:h-12 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-xl sm:text-2xl font-bold text-gray-900 mb-3">
                    {activeTab === 'today' && 'No tasks due today'}
                    {activeTab === 'pending' && 'No pending tasks'}
                    {activeTab === 'overdue' && 'No overdue tasks'}
                    {activeTab === 'completed' && 'No completed tasks yet'}
                  </h3>
                  <p className="text-sm sm:text-base text-gray-600 mb-6 max-w-md mx-auto">
                    {activeTab === 'today' && 'You have no tasks scheduled for today. Great work!'}
                    {activeTab === 'pending' && 'Awesome! You have completed all your tasks.'}
                    {activeTab === 'overdue' && 'Excellent! You are on top of everything.'}
                    {activeTab === 'completed' && 'Start completing tasks to see them here!'}
                  </p>
                  <button
                    onClick={() => setShowForm(true)}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white font-semibold rounded-xl hover:from-emerald-600 hover:to-green-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
                  >
                    <PlusIcon className="w-5 h-5" />
                    Create Your First Task
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Reminders Handler */}
        <RemindersHandler tasks={tasks} />
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
        .scrollbar-hide {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </div>
  );
}