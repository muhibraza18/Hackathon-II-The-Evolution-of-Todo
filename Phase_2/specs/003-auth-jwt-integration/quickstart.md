# Quickstart: Authentication with Better Auth + JWT Integration

## Overview
This guide provides step-by-step instructions to implement authentication with Better Auth and JWT tokens for secure user access and task isolation.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Neon PostgreSQL database setup
- Better Auth compatible environment

## Step 1: Environment Setup

### 1.1 Generate BETTER_AUTH_SECRET
```bash
# Generate a secure secret (32+ characters)
openssl rand -hex 32
```

### 1.2 Update Environment Files
```bash
# Backend (.env)
DATABASE_URL="postgresql://..."
BETTER_AUTH_SECRET="your-generated-secret-here"

# Frontend (.env.local)
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_SECRET="same-secret-as-backend"
```

## Step 2: Install Dependencies

### 2.1 Frontend Dependencies
```bash
cd frontend
npm install better-auth @better-auth/react
```

### 2.2 Backend Dependencies
```bash
cd backend
pip install pyjwt[crypto]
```

## Step 3: Configure Better Auth (Frontend)

### 3.1 Create Auth Configuration
```javascript
// frontend/lib/auth.ts or frontend/src/lib/auth.ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  // Additional configuration as needed
});
```

### 3.2 Update Next.js Configuration
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow cookies to be sent with requests
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Access-Control-Allow-Credentials',
            value: 'true',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

## Step 4: Create Authentication Pages

### 4.1 Signup Page
```tsx
// frontend/app/signup/page.tsx
'use client';

import { useState } from 'react';
import { authClient } from '@/lib/auth';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await authClient.signUp.email({
        email,
        password,
        callbackURL: '/login', // Redirect after signup
      });

      if (!response.error) {
        // Signup successful
        window.location.href = '/login';
      } else {
        setError(response.error.message);
      }
    } catch (err) {
      setError('Signup failed. Please try again.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-5">Sign Up</h1>
      <form onSubmit={handleSignup}>
        <div className="mb-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            required
          />
        </div>
        <div className="mb-4">
          <input
            type="password"
            placeholder="Password (min 8 characters)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            minLength={8}
            required
          />
        </div>
        {error && <div className="text-red-500 mb-4">{error}</div>}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Sign Up
        </button>
      </form>
      <p className="mt-4">
        Already have an account?{' '}
        <a href="/login" className="text-blue-500">Log in</a>
      </p>
    </div>
  );
}
```

### 4.2 Login Page
```tsx
// frontend/app/login/page.tsx
'use client';

import { useState } from 'react';
import { authClient } from '@/lib/auth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await authClient.signIn.email({
        email,
        password,
        callbackURL: '/tasks', // Redirect after login
      });

      if (!response.error) {
        // Login successful, JWT token automatically stored in cookie
        window.location.href = '/tasks';
      } else {
        setError(response.error.message);
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-5">Log In</h1>
      <form onSubmit={handleLogin}>
        <div className="mb-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            required
          />
        </div>
        <div className="mb-4">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            required
          />
        </div>
        {error && <div className="text-red-500 mb-4">{error}</div>}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Log In
        </button>
      </form>
      <p className="mt-4">
        Don't have an account?{' '}
        <a href="/signup" className="text-blue-500">Sign up</a>
      </p>
    </div>
  );
}
```

## Step 5: Create Authentication Context

### 5.1 Auth Context Provider
```tsx
// frontend/contexts/AuthContext.tsx
'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authClient } from '@/lib/auth';

interface AuthContextType {
  user: any | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkSession();
  }, []);

  const checkSession = async () => {
    try {
      const session = await authClient.getSession();
      setUser(session?.session ? session.user : null);
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await authClient.signIn.email({
        email,
        password,
      });

      if (!response.error) {
        setUser(response.user);
        return true;
      }
      return false;
    } catch (error) {
      return false;
    }
  };

  const logout = async () => {
    try {
      await authClient.signOut();
      setUser(null);
      window.location.href = '/login';
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

## Step 6: Create Protected Route Component

### 6.1 Protected Route Wrapper
```tsx
// frontend/components/ProtectedRoute.tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  return <>{children}</>;
}
```

## Step 7: Update API Client for JWT

### 7.1 Enhanced API Client
```typescript
// frontend/lib/api.ts
import { Task } from './types'; // Adjust import based on your types

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// Helper to include auth token in requests
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Include cookies in requests
  };

  const response = await fetch(url, config);

  if (response.status === 401) {
    // Redirect to login if unauthorized
    window.location.href = '/login';
    throw new Error('Unauthorized - redirecting to login');
  }

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const taskApi = {
  getAll: (): Promise<Task[]> => apiRequest('/tasks'),

  getById: (id: string): Promise<Task> => apiRequest(`/tasks/${id}`),

  create: (task: Omit<Task, 'id'>): Promise<Task> =>
    apiRequest('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    }),

  update: (id: string, task: Partial<Task>): Promise<Task> =>
    apiRequest(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(task),
    }),

  delete: (id: string): Promise<void> =>
    apiRequest(`/tasks/${id}`, { method: 'DELETE' }),

  toggleComplete: (id: string): Promise<Task> =>
    apiRequest(`/tasks/${id}/toggle-complete`, {
      method: 'PATCH',
    }),
};

export default taskApi;
```

## Step 8: Backend JWT Verification

### 8.1 JWT Utility Functions
```python
# backend/auth.py
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os

# JWT Configuration
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not JWT_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(days=7)  # Token expires in 7 days

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    email: str

def create_access_token(data: dict) -> str:
    """Create a new JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + JWT_EXPIRATION_DELTA
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Verify JWT token and extract user data"""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(user_id=user_id, email=email)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_id(token_data: TokenData = Depends(verify_token)) -> str:
    """Dependency to get current user ID from JWT token"""
    return token_data.user_id
```

## Step 9: Update Backend Routes with Authentication

### 9.1 Protected Task Endpoints
```python
# backend/routers/tasks.py (update existing file)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..models import Task, TaskCreate, TaskUpdate, TaskResponse
from ..db import get_session
from ..auth import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current authenticated user
    """
    statement = select(Task).where(Task.user_id == current_user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the current authenticated user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    return task

@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current authenticated user
    """
    db_task = Task.from_orm(task)
    db_task.user_id = current_user_id  # Assign task to current user
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a task for the current authenticated user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the current authenticated user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/toggle-complete", response_model=TaskResponse)
def toggle_task_complete(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for the current authenticated user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to modify it"
        )

    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

## Step 10: Update Main Application

### 10.1 Update Main App to Include Auth Router
```python
# backend/main.py (update existing file)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import tasks

app = FastAPI(title="Todo API with Authentication")

# Add CORS middleware to allow credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# For development: Initialize database tables
@app.on_event("startup")
def on_startup():
    from .init_db import create_db_and_tables
    create_db_and_tables()
```

## Step 11: Testing the Implementation

### 11.1 Test Authentication Flow
1. Start the backend: `uvicorn backend.main:app --reload`
2. Start the frontend: `npm run dev`
3. Navigate to `http://localhost:3000/signup` to create an account
4. Log in at `http://localhost:3000/login`
5. Access protected task features at `http://localhost:3000/tasks`
6. Verify that without authentication, you're redirected to login

### 11.2 Test User Isolation
1. Create two user accounts
2. Have each user create different tasks
3. Verify that each user can only see their own tasks
4. Attempt to access another user's task directly via API - should return 404

## Step 12: Production Considerations

### 12.1 Security Hardening
- Use HTTPS in production
- Implement proper rate limiting
- Add CSRF protection
- Regular security audits

### 12.2 Performance Optimization
- Implement caching for user sessions
- Optimize database queries with proper indexing
- Monitor JWT verification performance

### 12.3 Monitoring and Logging
- Log authentication events
- Monitor for suspicious activities
- Track token expiration rates