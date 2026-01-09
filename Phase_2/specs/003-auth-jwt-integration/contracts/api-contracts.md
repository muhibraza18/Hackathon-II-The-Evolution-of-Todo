# API Contracts: Authentication with Better Auth + JWT Integration

## 1. Authentication Endpoints (Better Auth)

### 1.1 User Registration
```
POST /api/auth/sign-up
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success - 200):**
```json
{
  "user": {
    "id": "user-uuid-here",
    "email": "user@example.com"
  },
  "token": "jwt-token-here"
}
```

**Response (Error - 400/409):**
```json
{
  "error": {
    "message": "Validation error or duplicate email"
  }
}
```

### 1.2 User Login
```
POST /api/auth/sign-in
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success - 200):**
```json
{
  "user": {
    "id": "user-uuid-here",
    "email": "user@example.com"
  },
  "token": "jwt-token-here"
}
```

**Response (Error - 400/401):**
```json
{
  "error": {
    "message": "Invalid credentials"
  }
}
```

### 1.3 User Logout
```
POST /api/auth/sign-out
```

**Request Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (Success - 200):**
```json
{
  "message": "Signed out successfully"
}
```

## 2. Protected Task Endpoints

### 2.1 Get All Tasks
```
GET /api/tasks
```

**Request Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (Success - 200):**
```json
[
  {
    "id": "task-uuid-1",
    "title": "Task 1",
    "description": "Description of task 1",
    "completed": false,
    "user_id": "user-uuid-here",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  },
  {
    "id": "task-uuid-2",
    "title": "Task 2",
    "description": "Description of task 2",
    "completed": true,
    "user_id": "user-uuid-here",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

**Response (Error - 401):**
```json
{
  "detail": "Could not validate credentials"
}
```

### 2.2 Get Task by ID
```
GET /api/tasks/{task_id}
```

**Request Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (Success - 200):**
```json
{
  "id": "task-uuid-1",
  "title": "Task 1",
  "description": "Description of task 1",
  "completed": false,
  "user_id": "user-uuid-here",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (Error - 404):**
```json
{
  "detail": "Task not found or you don't have permission to access it"
}
```

### 2.3 Create Task
```
POST /api/tasks
```

**Request Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Description of new task",
  "completed": false
}
```

**Response (Success - 200):**
```json
{
  "id": "task-uuid-3",
  "title": "New Task",
  "description": "Description of new task",
  "completed": false,
  "user_id": "user-uuid-here",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Could not validate credentials"
}
```

### 2.4 Update Task
```
PUT /api/tasks/{task_id}
```

**Request Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Task Title",
  "completed": true
}
```

**Response (Success - 200):**
```json
{
  "id": "task-uuid-1",
  "title": "Updated Task Title",
  "description": "Description of task 1",
  "completed": true,
  "user_id": "user-uuid-here",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (Error - 404):**
```json
{
  "detail": "Task not found or you don't have permission to update it"
}
```

### 2.5 Delete Task
```
DELETE /api/tasks/{task_id}
```

**Request Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (Success - 200):**
```json
{
  "message": "Task deleted successfully"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (Error - 404):**
```json
{
  "detail": "Task not found or you don't have permission to delete it"
}
```

### 2.6 Toggle Task Completion
```
PATCH /api/tasks/{task_id}/toggle-complete
```

**Request Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (Success - 200):**
```json
{
  "id": "task-uuid-1",
  "title": "Task 1",
  "description": "Description of task 1",
  "completed": true,
  "user_id": "user-uuid-here",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (Error - 404):**
```json
{
  "detail": "Task not found or you don't have permission to modify it"
}
```

## 3. JWT Token Structure

### 3.1 JWT Payload Format
```json
{
  "sub": "user-uuid-here",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Claims:**
- `sub`: User ID (subject)
- `email`: User email address
- `exp`: Token expiration timestamp (Unix time)
- `iat`: Token issued at timestamp (Unix time)

### 3.2 JWT Algorithm
- Algorithm: HS256 (HMAC with SHA-256)
- Secret: BETTER_AUTH_SECRET environment variable

## 4. Error Response Format

### 4.1 Standard Error Format
```json
{
  "detail": "Error message describing the issue"
}
```

### 4.2 Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation error)
- `401`: Unauthorized (invalid/expired JWT)
- `404`: Not Found (resource doesn't exist OR user doesn't own it)
- `409`: Conflict (duplicate email on signup)
- `422`: Unprocessable Entity (validation error)
- `500`: Internal Server Error

## 5. Security Requirements

### 5.1 Authentication Requirements
- All API endpoints (except health check) require valid JWT
- JWT must be included in Authorization header: `Bearer <token>`
- JWT must not be expired
- JWT signature must be valid

### 5.2 User Isolation Requirements
- All task operations filtered by authenticated user's ID
- Users cannot access tasks belonging to other users
- 404 returned for tasks that don't belong to authenticated user (don't leak existence)

### 5.3 Rate Limiting
- TBD: Rate limits for authentication endpoints to prevent brute force