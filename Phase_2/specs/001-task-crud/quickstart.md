# Quickstart Guide: Task CRUD Operations

**Branch**: `001-task-crud` | **Date**: 2026-01-07 | **Phase**: 1

## Overview

This guide provides step-by-step instructions for setting up the development environment and implementing the Task CRUD Operations feature. It covers prerequisites, installation, configuration, and a complete walkthrough of the development workflow.

## Prerequisites

### Required Software

| Software | Version | Purpose | Installation Link |
|----------|---------|---------|-------------------|
| Python | 3.11+ | Backend runtime | https://www.python.org/downloads/ |
| Node.js | 18+ | Frontend runtime | https://nodejs.org/ |
| npm | 9+ | Package manager | Included with Node.js |
| Git | Latest | Version control | https://git-scm.com/downloads |
| PostgreSQL Client | Any | Database connection | Included with PostgreSQL |

### Required Accounts

- **Neon Database Account**: Free PostgreSQL database
  - Sign up: https://neon.tech
  - Create a new project
  - Copy connection string

### Optional Tools

- **VS Code**: Recommended IDE with extensions
  - Python extension
  - TypeScript extension
  - Tailwind CSS IntelliSense extension
- **Postman**: API testing tool (or use curl)
- **TablePlus** or **DBeaver**: Database GUI

## Project Structure

```
Phase_2/
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # SQLModel Task definition
│   ├── db.py            # Database connection
│   └── routes/
│       └── tasks.py     # Task API endpoints
├── frontend/            # Next.js frontend
│   ├── app/
│   │   └── page.tsx     # Main tasks page
│   ├── lib/
│   │   ├── api.ts       # API client
│   │   └── types.ts     # TypeScript types
│   └── components/
│       ├── TaskList.tsx
│       ├── TaskForm.tsx
│       └── TaskItem.tsx
├── specs/
│   └── 001-task-crud/   # Feature specifications
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md
│       └── contracts/
│           ├── api-endpoints.md
│           └── frontend-types.md
└── .specify/            # Spec-Kit Plus configuration
```

## Setup Instructions

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Phase_2
git checkout 001-task-crud
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlmodel psycopg2-binary

# Create environment file
echo "DATABASE_URL=postgresql://username:password@host:port/database" > .env
```

**Configure DATABASE_URL**:

Replace the placeholder with your Neon database connection string:
```bash
DATABASE_URL=postgresql://username:password@ep-xyz.aws.neon.tech:5432/neondb?sslmode=require
```

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
```

### Step 4: Verify Setup

**Start Backend**:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 8000
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Start Frontend**:
```bash
cd frontend
npm run dev
```

Expected output:
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
  - Environments: .env.local

✓ Starting...
✓ Ready in 2.3s
```

**Test Services**:
- Backend: http://localhost:8000/docs (Swagger UI)
- Frontend: http://localhost:3000

## Development Workflow

### 1. Implement Backend Model

**File**: `backend/models.py`

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

class TaskCreate(TaskBase):
    user_id: str = "test-user-1"

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Test**:
```python
from models import TaskCreate

task = TaskCreate(title="Test task", description="Test description")
print(task)  # Should print TaskCreate object
```

### 2. Implement Database Connection

**File**: `backend/db.py`

```python
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

**Test Connection**:
```python
from db import engine

try:
    with engine.connect() as conn:
        print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
```

### 3. Create Database Tables

```bash
cd backend

# Run Python script to create tables
python -c "
from models import Task
from db import engine
from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
print('✓ Tables created successfully')
"
```

### 4. Implement API Endpoints

**File**: `backend/routes/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate
from db import get_session
from typing import List

router = APIRouter()

@router.post("/{user_id}/tasks", response_model=Task)
def create_task(task_data: TaskCreate, user_id: str, session: Session = Depends(get_session)):
    task = Task.model_validate(task_data)
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{user_id}/tasks", response_model=List[Task])
def get_tasks(user_id: str, session: Session = Depends(get_session)):
    return select(Task).where(Task.user_id == user_id).all()

@router.get("/{user_id}/tasks/{task_id}", response_model=Task)
def get_task(user_id: str, task_id: str, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{user_id}/tasks/{task_id}", response_model=Task)
def update_task(user_id: str, task_id: str, task_update: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: str, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=Task)
def toggle_complete(user_id: str, task_id: str, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Register Routes**: `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.tasks import router as tasks_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
```

### 5. Test Backend with Swagger UI

1. Start backend: `uvicorn main:app --reload`
2. Open: http://localhost:8000/docs
3. Test each endpoint:
   - POST `/api/test-user-1/tasks` - Create task
   - GET `/api/test-user-1/tasks` - List tasks
   - GET `/api/test-user-1/tasks/{id}` - Get single task
   - PUT `/api/test-user-1/tasks/{id}` - Update task
   - DELETE `/api/test-user-1/tasks/{id}` - Delete task
   - PATCH `/api/test-user-1/tasks/{id}/complete` - Toggle complete

### 6. Implement Frontend Types

**File**: `frontend/lib/types.ts`

```typescript
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
}

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}
```

### 7. Implement API Client

**File**: `frontend/lib/api.ts`

```typescript
import { Task, TaskCreate, TaskUpdate, ApiResponse } from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
const USER_ID = 'test-user-1';

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return { data, error: null };
  } catch (err) {
    return {
      data: null,
      error: err instanceof Error ? err.message : 'Unknown error',
    };
  }
}

export async function fetchTasks(): Promise<ApiResponse<Task[]>> {
  return fetchApi<Task[]>(`/${USER_ID}/tasks`);
}

export async function createTask(task: TaskCreate): Promise<ApiResponse<Task>> {
  return fetchApi<Task>(`/${USER_ID}/tasks`, {
    method: 'POST',
    body: JSON.stringify(task),
  });
}

export async function updateTask(
  id: string,
  task: TaskUpdate
): Promise<ApiResponse<Task>> {
  return fetchApi<Task>(`/${USER_ID}/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(task),
  });
}

export async function deleteTask(id: string): Promise<ApiResponse<void>> {
  return fetchApi<void>(`/${USER_ID}/tasks/${id}`, {
    method: 'DELETE',
  });
}

export async function toggleComplete(id: string): Promise<ApiResponse<Task>> {
  return fetchApi<Task>(`/${USER_ID}/tasks/${id}/complete`, {
    method: 'PATCH',
  });
}
```

### 8. Implement Frontend Components

**File**: `frontend/components/TaskForm.tsx`

```typescript
'use client';

import { useState } from 'react';
import { TaskCreate, TaskUpdate } from '../lib/types';
import { createTask, updateTask } from '../lib/api';

interface Props {
  mode: 'create' | 'edit';
  task?: TaskUpdate;
  onSuccess: () => void;
  onCancel?: () => void;
}

export default function TaskForm({ mode, task, onSuccess, onCancel }: Props) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const data: TaskCreate = { title, description };

    if (mode === 'create') {
      const result = await createTask(data);
      if (result.error) {
        setError(result.error);
      } else {
        setTitle('');
        setDescription('');
        onSuccess();
      }
    } else if (task) {
      const result = await updateTask(task.id || '', data);
      if (result.error) {
        setError(result.error);
      } else {
        onSuccess();
      }
    }

    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 bg-gray-50 rounded">
      <div>
        <label className="block text-sm font-medium mb-1">Title *</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full p-2 border rounded"
          placeholder="Task title"
          required
          maxLength={200}
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-2 border rounded"
          placeholder="Task description"
          rows={3}
          maxLength={1000}
        />
      </div>
      {error && <div className="text-red-500 text-sm">{error}</div>}
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          {loading ? 'Saving...' : mode === 'create' ? 'Create' : 'Update'}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-300 rounded"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
```

**File**: `frontend/components/TaskItem.tsx`

```typescript
'use client';

import { Task } from '../lib/types';
import { updateTask, deleteTask, toggleComplete } from '../lib/api';

interface Props {
  task: Task;
  onEdit: (task: Task) => void;
  onUpdate: () => void;
  onDelete: () => void;
}

export default function TaskItem({ task, onEdit, onUpdate, onDelete }: Props) {
  const handleToggle = async () => {
    await toggleComplete(task.id);
    onUpdate();
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      await deleteTask(task.id);
      onDelete();
    }
  };

  return (
    <div className={`p-4 border rounded ${task.completed ? 'bg-gray-100 opacity-60' : 'bg-white'}`}>
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <h3 className={`font-semibold ${task.completed ? 'line-through' : ''}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className="text-gray-600 mt-1">{task.description}</p>
          )}
        </div>
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          className="ml-4 mt-1"
        />
      </div>
      <div className="flex gap-2 mt-3">
        <button
          onClick={() => onEdit(task)}
          className="text-blue-500 text-sm hover:underline"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="text-red-500 text-sm hover:underline"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
```

**File**: `frontend/components/TaskList.tsx`

```typescript
'use client';

import { useState, useEffect } from 'react';
import { Task, TaskUpdate } from '../lib/types';
import { fetchTasks } from '../lib/api';
import TaskForm from './TaskForm';
import TaskItem from './TaskItem';

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
    <div className="max-w-2xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Tasks</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          {showForm ? 'Hide Form' : 'New Task'}
        </button>
      </div>

      {showForm && (
        <TaskForm
          mode={editingTask ? 'edit' : 'create'}
          task={editingTask || undefined}
          onSuccess={() => {
            loadTasks();
            handleCancel();
          }}
          onCancel={handleCancel}
        />
      )}

      {loading && <div className="text-center py-4">Loading tasks...</div>}
      {error && <div className="text-red-500 py-4">{error}</div>}

      <div className="space-y-3">
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

      {!loading && tasks.length === 0 && (
        <div className="text-center text-gray-500 py-8">
          No tasks yet. Create one to get started!
        </div>
      )}
    </div>
  );
}
```

**File**: `frontend/app/page.tsx`

```typescript
import TaskList from '../components/TaskList';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100">
      <TaskList />
    </main>
  );
}
```

### 9. Test Complete Workflow

1. Start both services:
   ```bash
   # Terminal 1: Backend
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload

   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

2. Open http://localhost:3000

3. Test complete CRUD flow:
   - Click "New Task"
   - Enter title: "Test task"
   - Click "Create"
   - Verify task appears in list
   - Click checkbox to mark complete
   - Click "Edit" and modify title
   - Click "Update"
   - Click "Delete" and confirm
   - Verify task is removed

## Troubleshooting

### Backend Issues

**Database Connection Failed**:
```bash
# Check DATABASE_URL in .env
cat backend/.env

# Test connection directly
psql $DATABASE_URL
```

**Module Not Found Error**:
```bash
# Reinstall dependencies
pip install --upgrade fastapi uvicorn sqlmodel psycopg2-binary
```

**CORS Error**:
```bash
# Verify CORS middleware is configured in main.py
# Check allow_origins matches frontend URL
```

### Frontend Issues

**API Connection Refused**:
```bash
# Check NEXT_PUBLIC_API_URL in .env.local
cat frontend/.env.local

# Verify backend is running on port 8000
curl http://localhost:8000/docs
```

**TypeScript Errors**:
```bash
# Clear cache and reinstall
rm -rf frontend/.next frontend/node_modules
cd frontend
npm install
```

**Tailwind Not Working**:
```bash
# Check tailwind.config.js exists
# Restart dev server
npm run dev
```

### Common Errors

**404 Not Found**:
- Task ID doesn't exist
- Route not registered in main.py
- Check URL path matches route definition

**422 Validation Error**:
- Title empty or exceeds 200 characters
- Description exceeds 1000 characters
- Check request body format

**500 Server Error**:
- Database connection issue
- SQLModel validation error
- Check backend logs for stack trace

## Development Tips

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# View API documentation
open http://localhost:8000/docs

# Run with debug output
uvicorn main:app --reload --log-level debug
```

### Frontend Development

```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Test production build
npm run start
```

### Database Operations

```bash
# View tasks in database
psql $DATABASE_URL -c "SELECT * FROM tasks;"

# Clear all tasks (for testing)
psql $DATABASE_URL -c "DELETE FROM tasks;"

# Count tasks
psql $DATABASE_URL -c "SELECT COUNT(*) FROM tasks;"
```

## Next Steps

After completing this quickstart:

1. ✅ Review `specs/001-task-crud/spec.md` for requirements
2. ✅ Review `specs/001-task-crud/plan.md` for architecture
3. ✅ Review `specs/001-task-crud/contracts/api-endpoints.md` for API details
4. ✅ Run `/sp.tasks` to generate implementation tasks
5. ✅ Complete tasks in order specified in `tasks.md`
6. ✅ Test against acceptance criteria in `spec.md`

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Support

For issues or questions:

1. Check the Troubleshooting section
2. Review relevant specification documents
3. Check logs in terminal output
4. Open an issue in the project repository
