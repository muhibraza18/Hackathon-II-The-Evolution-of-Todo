/**
 * TypeScript types for Task CRUD Operations
 */

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  due_date?: string | null;
  reminder_datetime?: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string | null;
  due_date?: string | null;
  reminder_datetime?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  due_date?: string | null;
  reminder_datetime?: string;
}

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}