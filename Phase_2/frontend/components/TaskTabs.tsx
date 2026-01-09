"use client";

import { useState, useEffect } from "react";
import { Task } from "../lib/types";
import { fetchTasks } from "../lib/api";
import TaskForm from "./TaskForm";
import TaskCard from "./TaskCard";
import RemindersHandler from "./RemindersHandler";
import { PlusIcon, HomeIcon } from '@heroicons/react/24/outline';

export default function TaskTabs() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [activeTab, setActiveTab] = useState<"today" | "pending" | "overdue">("today");

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

  // Filter tasks based on active tab
  const filteredTasks = tasks.filter((task) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (activeTab === "today") {
      if (task.due_date) {
        const taskDueDate = new Date(task.due_date);
        taskDueDate.setHours(0, 0, 0, 0);
        return taskDueDate.getTime() === today.getTime();
      }
      return false;
    } else if (activeTab === "pending") {
      return !task.completed;
    } else if (activeTab === "overdue") {
      if (task.completed) return false;
      if (task.due_date) {
        const taskDueDate = new Date(task.due_date);
        taskDueDate.setHours(0, 0, 0, 0);
        return taskDueDate < today;
      }
      return false;
    }
    return true;
  });

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
    return false;
  }).length;

  const pendingCount = tasks.filter((task) => !task.completed).length;

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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <button
                onClick={() => window.location.href = '/'}
                className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-gray-50 text-gray-700 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 border border-gray-200"
              >
                <HomeIcon className="w-5 h-5" />
                <span className="font-medium">Home</span>
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
                <p className="text-gray-600 mt-1">Stay organized and productive</p>
              </div>
            </div>
            <button
              onClick={() => setShowForm(!showForm)}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
            >
              <PlusIcon className="w-5 h-5" />
              {showForm ? "Close" : "New Task"}
            </button>
          </div>

          {/* Task Form */}
          {showForm && (
            <div className="mb-8 animate-fadeIn">
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
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 mb-6">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab("today")}
              className={`flex-1 px-6 py-4 font-semibold transition-all duration-200 relative ${
                activeTab === "today"
                  ? "text-primary-700"
                  : "text-gray-500 hover:text-gray-700 hover:bg-gray-50"
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <span>Today</span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                  activeTab === "today" 
                    ? "bg-primary-100 text-primary-700" 
                    : "bg-gray-100 text-gray-600"
                }`}>
                  {todayCount}
                </span>
              </div>
              {activeTab === "today" && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary-600 to-purple-600 rounded-t"></div>
              )}
            </button>

            <button
              onClick={() => setActiveTab("pending")}
              className={`flex-1 px-6 py-4 font-semibold transition-all duration-200 relative ${
                activeTab === "pending"
                  ? "text-primary-700"
                  : "text-gray-500 hover:text-gray-700 hover:bg-gray-50"
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <span>Pending</span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                  activeTab === "pending" 
                    ? "bg-primary-100 text-primary-700" 
                    : "bg-gray-100 text-gray-600"
                }`}>
                  {pendingCount}
                </span>
              </div>
              {activeTab === "pending" && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary-600 to-purple-600 rounded-t"></div>
              )}
            </button>

            <button
              onClick={() => setActiveTab("overdue")}
              className={`flex-1 px-6 py-4 font-semibold transition-all duration-200 relative ${
                activeTab === "overdue"
                  ? "text-red-700"
                  : "text-gray-500 hover:text-gray-700 hover:bg-gray-50"
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <span>Overdue</span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                  activeTab === "overdue" 
                    ? "bg-red-100 text-red-700" 
                    : overdueCount > 0 
                    ? "bg-red-100 text-red-700"
                    : "bg-gray-100 text-gray-600"
                }`}>
                  {overdueCount}
                </span>
              </div>
              {activeTab === "overdue" && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-red-600 to-orange-600 rounded-t"></div>
              )}
            </button>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-20">
            <div className="relative w-16 h-16 mx-auto mb-4">
              <div className="absolute inset-0 border-4 border-primary-200 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-primary-600 rounded-full border-t-transparent animate-spin"></div>
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

        {/* Tasks List */}
        {!loading && !error && (
          <div className="space-y-4">
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
              <div className="text-center py-20 bg-white rounded-2xl border-2 border-dashed border-gray-200">
                <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center">
                  <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {activeTab === 'today' && 'No tasks due today'}
                  {activeTab === 'pending' && 'No pending tasks'}
                  {activeTab === 'overdue' && 'No overdue tasks'}
                </h3>
                <p className="text-gray-600 mb-6 max-w-sm mx-auto">
                  {activeTab === 'today' && 'You have no tasks scheduled for today. Great work!'}
                  {activeTab === 'pending' && 'Awesome! You have completed all your tasks.'}
                  {activeTab === 'overdue' && 'Excellent! You are on top of everything.'}
                </p>
                <div className="flex gap-3 justify-center">
                  <button
                    onClick={() => setShowForm(true)}
                    className="px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                  >
                    Create Your First Task
                  </button>
                  {(activeTab === 'today' || activeTab === 'overdue') && pendingCount > 0 && (
                    <button
                      onClick={() => setActiveTab('pending')}
                      className="px-6 py-3 bg-white text-gray-700 font-semibold rounded-xl border-2 border-gray-200 hover:border-gray-300 hover:shadow-md transition-all duration-200"
                    >
                      View All Tasks
                    </button>
                  )}
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
      `}</style>
    </div>
  );
}