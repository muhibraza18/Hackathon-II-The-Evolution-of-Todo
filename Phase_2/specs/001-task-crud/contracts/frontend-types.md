# Frontend Types: Task CRUD Operations

**Branch**: `001-task-crud` | **Date**: 2026-01-07 | **Phase**: 1

## Overview

This document defines the TypeScript type definitions used across the frontend application for the Task CRUD Operations feature. These types ensure type safety between the frontend and backend API.

## Type Definitions

### Task Interface

```typescript
/**
 * Represents a single task in the system
 */
export interface Task {
  /** Unique identifier (UUID) */
  id: string;

  /** Owner of the task (user identifier) */
  user_id: string;

  /** Task title/name (1-200 characters) */
  title: string;

  /** Detailed task description (0-1000 characters or null) */
  description: string | null;

  /** Task completion status */
  completed: boolean;

  /** Timestamp when task was created (ISO 8601) */
  created_at: string;

  /** Timestamp when task was last updated (ISO 8601) */
  updated_at: string;
}
```

**Usage Example**:
```typescript
const task: Task = {
  id: "550e8400-e29b-41d4-a716-446655440000",
  user_id: "test-user-1",
  title: "Complete project documentation",
  description: "Write technical documentation",
  completed: false,
  created_at: "2026-01-07T10:00:00Z",
  updated_at: "2026-01-07T10:00:00Z"
};
```

### TaskCreate Interface

```typescript
/**
 * Data required to create a new task
 */
export interface TaskCreate {
  /** Task title/name (1-200 characters, required) */
  title: string;

  /** Detailed task description (0-1000 characters, optional) */
  description?: string | null;
}
```

**Usage Example**:
```typescript
const newTask: TaskCreate = {
  title: "Buy groceries",
  description: "Milk, eggs, bread"
};
```

### TaskUpdate Interface

```typescript
/**
 * Data for updating an existing task
 * All fields are optional - only provided fields will be updated
 */
export interface TaskUpdate {
  /** New task title (1-200 characters, optional) */
  title?: string;

  /** New task description (0-1000 characters, optional) */
  description?: string | null;

  /** Task ID (included for reference) */
  id?: string;
}
```

**Usage Example**:
```typescript
const update: TaskUpdate = {
  id: "task-uuid-1",
  title: "Updated title"
};

// Or update only description
const descUpdate: TaskUpdate = {
  id: "task-uuid-1",
  description: "New description"
};
```

### ApiResponse Interface

```typescript
/**
 * Standard API response wrapper
 * All API client functions return this type
 */
export interface ApiResponse<T> {
  /** Response data on success, null on failure */
  data: T | null;

  /** Error message on failure, null on success */
  error: string | null;
}
```

**Usage Example**:
```typescript
// Success response
const success: ApiResponse<Task[]> = {
  data: [task1, task2],
  error: null
};

// Error response
const failure: ApiResponse<Task> = {
  data: null,
  error: "Failed to connect to server"
};

// Checking response
const result: ApiResponse<Task> = await createTask(newTaskData);
if (result.error) {
  console.error("Error:", result.error);
} else if (result.data) {
  console.log("Created task:", result.data);
}
```

### TaskState Interface (Component State)

```typescript
/**
 * Component state for task management
 * Used in TaskList and TaskForm components
 */
export interface TaskState {
  /** All loaded tasks */
  tasks: Task[];

  /** Loading indicator */
  loading: boolean;

  /** Error message */
  error: string | null;

  /** Task currently being edited */
  editingTask: Task | null;

  /** Whether task form is visible */
  showForm: boolean;
}
```

**Usage Example**:
```typescript
const [state, setState] = useState<TaskState>({
  tasks: [],
  loading: true,
  error: null,
  editingTask: null,
  showForm: false
});
```

### FormState Interface

```typescript
/**
 * State for task creation/editing form
 */
export interface FormState {
  /** Task title input */
  title: string;

  /** Task description input */
  description: string;

  /** Form submission in progress */
  submitting: boolean;

  /** Form validation error */
  error: string | null;
}
```

**Usage Example**:
```typescript
const [formState, setFormState] = useState<FormState>({
  title: "",
  description: "",
  submitting: false,
  error: null
});
```

## Type Guards

### isValidTask

```typescript
/**
 * Type guard to check if an object is a valid Task
 */
export function isValidTask(obj: unknown): obj is Task {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    typeof obj.id === 'string' &&
    'user_id' in obj &&
    typeof obj.user_id === 'string' &&
    'title' in obj &&
    typeof obj.title === 'string' &&
    'completed' in obj &&
    typeof obj.completed === 'boolean' &&
    'created_at' in obj &&
    typeof obj.created_at === 'string' &&
    'updated_at' in obj &&
    typeof obj.updated_at === 'string'
  );
}
```

**Usage Example**:
```typescript
const data = await response.json();

if (isValidTask(data)) {
  // TypeScript knows data is Task
  console.log(data.title);
}
```

### isValidTaskCreate

```typescript
/**
 * Type guard to check if an object is a valid TaskCreate
 */
export function isValidTaskCreate(obj: unknown): obj is TaskCreate {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'title' in obj &&
    typeof obj.title === 'string' &&
    obj.title.length >= 1 &&
    obj.title.length <= 200
  );
}
```

## Utility Types

### TaskKeys

```typescript
/**
 * Union of all Task property keys
 */
export type TaskKeys = keyof Task;
// "id" | "user_id" | "title" | "description" | "completed" | "created_at" | "updated_at"
```

### PartialTask

```typescript
/**
 * All Task properties optional
 */
export type PartialTask = Partial<Task>;
```

### TaskWithoutId

```typescript
/**
 * Task without id field (for creation)
 */
export type TaskWithoutId = Omit<Task, 'id'>;
```

### TaskDTO

```typescript
/**
 * Task Data Transfer Object (for API communication)
 */
export type TaskDTO = Pick<Task, 'id' | 'title' | 'description' | 'completed'>;
```

## Type Compositions

### TaskWithAction

```typescript
/**
 * Task with associated action handlers
 */
export interface TaskWithAction {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onToggle: (taskId: string) => void;
}
```

### TaskListProps

```typescript
/**
 * Props for TaskList component
 */
export interface TaskListProps {
  /** Initial tasks to display */
  initialTasks?: Task[];

  /** Callback when tasks are updated */
  onUpdate?: (tasks: Task[]) => void;

  /** Callback when task is selected */
  onSelect?: (task: Task) => void;
}
```

### TaskFormProps

```typescript
/**
 * Props for TaskForm component
 */
export interface TaskFormProps {
  /** Form mode: create or edit */
  mode: 'create' | 'edit';

  /** Task data (required for edit mode) */
  task?: Task | TaskUpdate;

  /** Callback on successful submission */
  onSuccess: () => void;

  /** Callback on form cancellation */
  onCancel?: () => void;

  /** Submit button text override */
  submitText?: string;
}
```

## Validation Types

### ValidationError

```typescript
/**
 * Validation error with field and message
 */
export interface ValidationError {
  /** Field that failed validation */
  field: string;

  /** Error message */
  message: string;
}
```

### FormValidationResult

```typescript
/**
 * Result of form validation
 */
export interface FormValidationResult {
  /** Whether validation passed */
  isValid: boolean;

  /** List of validation errors */
  errors: ValidationError[];
}
```

## API Function Types

### FetchTasksFunction

```typescript
/**
 * Type for fetchTasks API function
 */
export type FetchTasksFunction = () => Promise<ApiResponse<Task[]>>;
```

### CreateTaskFunction

```typescript
/**
 * Type for createTask API function
 */
export type CreateTaskFunction = (
  task: TaskCreate
) => Promise<ApiResponse<Task>>;
```

### UpdateTaskFunction

```typescript
/**
 * Type for updateTask API function
 */
export type UpdateTaskFunction = (
  id: string,
  task: TaskUpdate
) => Promise<ApiResponse<Task>>;
```

### DeleteTaskFunction

```typescript
/**
 * Type for deleteTask API function
 */
export type DeleteTaskFunction = (
  id: string
) => Promise<ApiResponse<void>>;
```

### ToggleCompleteFunction

```typescript
/**
 * Type for toggleComplete API function
 */
export type ToggleCompleteFunction = (
  id: string
) => Promise<ApiResponse<Task>>;
```

## API Client Type

### TaskAPIClient

```typescript
/**
 * Complete API client interface for task operations
 */
export interface TaskAPIClient {
  fetchTasks: FetchTasksFunction;
  createTask: CreateTaskFunction;
  updateTask: UpdateTaskFunction;
  deleteTask: DeleteTaskFunction;
  toggleComplete: ToggleCompleteFunction;
}
```

**Usage Example**:
```typescript
const api: TaskAPIClient = {
  fetchTasks: async () => { /* implementation */ },
  createTask: async (task) => { /* implementation */ },
  updateTask: async (id, task) => { /* implementation */ },
  deleteTask: async (id) => { /* implementation */ },
  toggleComplete: async (id) => { /* implementation */ }
};
```

## Constants

### Validation Rules

```typescript
/**
 * Task validation constraints
 */
export const TASK_VALIDATION = {
  /** Minimum title length */
  TITLE_MIN_LENGTH: 1,

  /** Maximum title length */
  TITLE_MAX_LENGTH: 200,

  /** Maximum description length */
  DESCRIPTION_MAX_LENGTH: 1000,

  /** User ID for unauthenticated mode */
  DEFAULT_USER_ID: "test-user-1"
} as const;
```

### Error Messages

```typescript
/**
 * Standard error messages
 */
export const ERROR_MESSAGES = {
  /** Empty title error */
  EMPTY_TITLE: "Title is required",

  /** Title too long error */
  TITLE_TOO_LONG: "Title must be 200 characters or less",

  /** Description too long error */
  DESCRIPTION_TOO_LONG: "Description must be 1000 characters or less",

  /** Task not found error */
  TASK_NOT_FOUND: "Task not found",

  /** Network error */
  NETWORK_ERROR: "Failed to connect to server",

  /** Unknown error */
  UNKNOWN_ERROR: "An unexpected error occurred"
} as const;
```

## Type Exports

```typescript
// Export all types from a single file
export type {
  Task,
  TaskCreate,
  TaskUpdate,
  ApiResponse,
  TaskState,
  FormState,
  TaskKeys,
  PartialTask,
  TaskWithoutId,
  TaskDTO,
  TaskWithAction,
  TaskListProps,
  TaskFormProps,
  ValidationError,
  FormValidationResult,
  FetchTasksFunction,
  CreateTaskFunction,
  UpdateTaskFunction,
  DeleteTaskFunction,
  ToggleCompleteFunction,
  TaskAPIClient
};

export {
  isValidTask,
  isValidTaskCreate,
  TASK_VALIDATION,
  ERROR_MESSAGES
};
```

## Usage Patterns

### Pattern 1: API Response Handling

```typescript
import { ApiResponse, Task } from './types';

async function loadTasks() {
  const result: ApiResponse<Task[]> = await fetchTasks();

  if (result.error) {
    console.error(result.error);
    return;
  }

  if (result.data) {
    // TypeScript knows result.data is Task[]
    setTasks(result.data);
  }
}
```

### Pattern 2: Form Validation

```typescript
import { TaskCreate, TASK_VALIDATION, ERROR_MESSAGES } from './types';

function validateTaskCreate(data: TaskCreate): FormValidationResult {
  const errors: ValidationError[] = [];

  if (!data.title || data.title.length < TASK_VALIDATION.TITLE_MIN_LENGTH) {
    errors.push({
      field: 'title',
      message: ERROR_MESSAGES.EMPTY_TITLE
    });
  }

  if (data.title.length > TASK_VALIDATION.TITLE_MAX_LENGTH) {
    errors.push({
      field: 'title',
      message: ERROR_MESSAGES.TITLE_TOO_LONG
    });
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}
```

### Pattern 3: Component Props with Types

```typescript
import { Task, TaskFormProps } from './types';

function TaskForm({ mode, task, onSuccess, onCancel }: TaskFormProps) {
  // TypeScript ensures mode is 'create' | 'edit'
  // task is optional and type-safe
  // onSuccess and onCancel are functions
}
```

### Pattern 4: Type-Safe API Calls

```typescript
import { CreateTaskFunction, TaskCreate, ApiResponse, Task } from './types';

const createTask: CreateTaskFunction = async (task: TaskCreate): Promise<ApiResponse<Task>> => {
  // Implementation
  // TypeScript ensures task has correct structure
  // Return type is guaranteed
};
```

## Type Compatibility

### Backend to Frontend Mapping

| Backend Type | Frontend Type | Notes |
|--------------|---------------|-------|
| UUID (String) | string | Both use string representation |
| VARCHAR(200) | string | Validated to 1-200 chars |
| TEXT | string \| null | Validated to 0-1000 chars |
| BOOLEAN | boolean | Direct mapping |
| TIMESTAMP | string | ISO 8601 format |
| Optional | \| null | Backend optional = frontend null |

### Serialization Notes

1. **UUIDs**: Transferred as strings, not objects
2. **Dates**: Transferred as ISO 8601 strings, not Date objects
3. **Null vs Undefined**: Backend uses NULL, frontend uses null
4. **Booleans**: JSON true/false, both use boolean type

## Type Testing

```typescript
// Test: Task interface
const task: Task = {
  id: "uuid",
  user_id: "test-user-1",
  title: "Test",
  description: null,
  completed: false,
  created_at: "2026-01-07T10:00:00Z",
  updated_at: "2026-01-07T10:00:00Z"
};

// Test: TaskCreate
const create: TaskCreate = {
  title: "Test"
  // description is optional
};

// Test: ApiResponse
const response: ApiResponse<Task> = {
  data: task,
  error: null
};

// Test: Type guard
if (isValidTask(task)) {
  console.log(task.title); // Type-safe access
}
```

## Conclusion

These TypeScript types provide:
- Type safety across the frontend application
- Clear contracts for API communication
- Runtime validation through type guards
- Self-documenting code through interfaces
- Consistent data structures throughout the application

All types align with the backend Pydantic models and API contracts defined in `api-endpoints.md`.
