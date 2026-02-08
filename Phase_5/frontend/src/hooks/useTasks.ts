/**
 * useTasks Hook
 * Custom hook for task management with optimistic updates
 */

import { useState, useCallback, useEffect, useRef } from 'react';
import { tasksService, Task, TaskFilters, CreateTaskRequest, UpdateTaskRequest } from '../services/tasks';
import toast from 'react-hot-toast';

export const useTasks = (initialFilters?: TaskFilters) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [limit] = useState(20);

  // Use ref to store filters without causing re-renders
  const filtersRef = useRef<TaskFilters>(initialFilters || {});

  // Update ref when initialFilters changes
  useEffect(() => {
    filtersRef.current = initialFilters || {};
  }, [initialFilters]);

  const fetchTasks = useCallback(async (filters?: TaskFilters) => {
    setLoading(true);
    setError(null);

    try {
      const response = await tasksService.getTasks({
        ...filtersRef.current,
        ...filters,
        page,
        limit,
      });

      setTasks(response.tasks);
      setTotal(response.total);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  }, [page, limit, initialFilters]);  // Add initialFilters to prevent stale closure

  // Initial fetch - run on mount and when filters change
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);  // Changed from [initialFilters] to [fetchTasks]

  const createTask = useCallback(async (data: CreateTaskRequest) => {
    setLoading(true);
    setError(null);

    try {
      const newTask = await tasksService.createTask(data);
      setTasks((prev) => [newTask, ...prev]);
      setTotal((prev) => prev + 1);
      return newTask;
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateTask = useCallback(async (taskId: number, data: UpdateTaskRequest) => {
    setLoading(true);
    setError(null);

    try {
      const updatedTask = await tasksService.updateTask(taskId, data);
      setTasks((prev) =>
        prev.map((task) => (task.id === taskId ? updatedTask : task))
      );
      return updatedTask;
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const completeTask = useCallback(async (taskId: number) => {
    setLoading(true);
    setError(null);

    try {
      const completedTask = await tasksService.completeTask(taskId);
      setTasks((prev) =>
        prev.map((task) => (task.id === taskId ? completedTask : task))
      );
      return completedTask;
    } catch (err: any) {
      setError(err.message || 'Failed to complete task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Optimistic complete - updates UI immediately, then syncs with backend
  const optimisticComplete = useCallback(async (taskId: number) => {
    // Find the task to complete
    const taskToComplete = tasks.find(t => t.id === taskId);
    if (!taskToComplete) return;

    const previousState = taskToComplete.completed;

    // Optimistically update UI immediately
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, completed: !previousState } : task
      )
    );

    try {
      // Sync with backend
      const completedTask = await tasksService.completeTask(taskId);
      setTasks((prev) =>
        prev.map((task) => (task.id === taskId ? completedTask : task))
      );
      toast.success('Task completed!');
      return completedTask;
    } catch (err: any) {
      // Rollback on error
      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId ? { ...task, completed: previousState } : task
        )
      );
      setError(err.message || 'Failed to complete task');
      toast.error('Failed to complete task');
      throw err;
    }
  }, [tasks]);

  const deleteTask = useCallback(async (taskId: number) => {
    setLoading(true);
    setError(null);

    try {
      await tasksService.deleteTask(taskId);
      setTasks((prev) => prev.filter((task) => task.id !== taskId));
      setTotal((prev) => prev - 1);
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const refresh = useCallback((filters?: TaskFilters) => {
    setLoading(true);
    setError(null);

    const currentFilters = filtersRef.current;

    tasksService.getTasks({
      ...currentFilters,
      ...filters,
      page,
      limit,
    }).then(response => {
      setTasks(response.tasks);
      setTotal(response.total);
    }).catch(err => {
      setError(err.message || 'Failed to fetch tasks');
    }).finally(() => {
      setLoading(false);
    });
  }, [page, limit]);  // Add page and limit dependencies

  const nextPage = useCallback(() => {
    setPage((prev) => prev + 1);
  }, []);

  const prevPage = useCallback(() => {
    setPage((prev) => Math.max(1, prev - 1));
  }, []);

  // Check for overdue tasks (for reminder notifications)
  const getOverdueTasks = useCallback((): Task[] => {
    const now = new Date();
    return tasks.filter(task =>
      !task.completed &&
      task.due_date &&
      new Date(task.due_date) < now
    );
  }, [tasks]);

  return {
    tasks,
    loading,
    error,
    total,
    page,
    limit,
    createTask,
    updateTask,
    completeTask,
    optimisticComplete,
    deleteTask,
    refresh,
    nextPage,
    prevPage,
    getOverdueTasks,
  };
};
