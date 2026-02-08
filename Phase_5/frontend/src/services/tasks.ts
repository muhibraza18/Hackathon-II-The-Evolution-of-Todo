/**
 * Tasks API Service
 * Handles all task-related API calls
 */

import api from './api';

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  tags: string[];
  recurring_config?: {
    enabled: boolean;
    frequency: 'daily' | 'weekly' | 'monthly';
    interval: number;
  };
  next_occurrence_id?: number;
  parent_task_id?: number;
  original_task_id?: number;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  due_date?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  tags?: string[];
  recurring_config?: {
    enabled: boolean;
    frequency: 'daily' | 'weekly' | 'monthly';
    interval: number;
  };
}

export interface UpdateTaskRequest extends Partial<CreateTaskRequest> {
  completed?: boolean;
}

export interface TaskFilters {
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  tag?: string;
  due_date_before?: string;
  due_date_after?: string;
  overdue_only?: boolean;
  search?: string;
  sort_by?: 'created_at' | 'updated_at' | 'due_date' | 'priority';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  page: number;
  limit: number;
}

class TasksService {
  /**
   * Get all tasks with optional filters
   */
  async getTasks(filters?: TaskFilters): Promise<TaskListResponse> {
    const params = new URLSearchParams();

    if (filters?.completed !== undefined) params.append('completed', String(filters.completed));
    if (filters?.priority) params.append('priority', filters.priority);
    if (filters?.tag) params.append('tag', filters.tag);
    if (filters?.due_date_before) params.append('due_before', filters.due_date_before);
    if (filters?.due_date_after) params.append('due_after', filters.due_date_after);
    if (filters?.overdue_only) params.append('overdue_only', 'true');
    if (filters?.search) params.append('search', filters.search);
    if (filters?.sort_by) params.append('sort_by', filters.sort_by);
    if (filters?.sort_order) params.append('sort_order', filters.sort_order);
    if (filters?.page) params.append('page', String(filters.page));
    if (filters?.limit) params.append('limit', String(filters.limit));

    const queryString = params.toString();
    const url = `/api/tasks${queryString ? `?${queryString}` : ''}`;

    return api.get(url);
  }

  /**
   * Get overdue tasks (optimized endpoint)
   */
  async getOverdueTasks(): Promise<Task[]> {
    const response = await this.getTasks({ overdue_only: true, completed: false });
    return response.tasks;
  }

  /**
   * Get a single task by ID
   */
  async getTask(taskId: number): Promise<Task> {
    return api.get(`/api/tasks/${taskId}`);
  }

  /**
   * Create a new task
   */
  async createTask(data: CreateTaskRequest): Promise<Task> {
    return api.post('/api/tasks', data);
  }

  /**
   * Update a task
   */
  async updateTask(taskId: number, data: UpdateTaskRequest): Promise<Task> {
    return api.put(`/api/tasks/${taskId}`, data);
  }

  /**
   * Complete a task (handles recurring tasks)
   */
  async completeTask(taskId: number): Promise<Task> {
    return api.patch(`/api/tasks/${taskId}/complete`);
  }

  /**
   * Delete a task
   */
  async deleteTask(taskId: number): Promise<void> {
    return api.delete(`/api/tasks/${taskId}`);
  }
}

export const tasksService = new TasksService();
