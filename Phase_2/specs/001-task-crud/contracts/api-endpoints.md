# API Contract: Task CRUD Operations

**Branch**: `001-task-crud` | **Date**: 2026-01-07 | **Phase**: 1

## Overview

This document defines the complete API contract for the Task CRUD Operations feature. It includes all endpoints, request/response formats, error codes, and examples for the 6 REST API endpoints.

## Base URL

```
http://localhost:8000/api
```

## Common Response Format

### Success Responses

All successful responses return JSON data:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "test-user-1",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z"
}
```

### Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT/PATCH request |
| 201 | Created | Task successfully created |
| 204 | No Content | Task successfully deleted |
| 404 | Not Found | Task ID doesn't exist |
| 422 | Validation Error | Invalid request data |
| 500 | Server Error | Unexpected server error |

## Authentication

**Current Phase**: No authentication required
- All endpoints are publicly accessible
- `user_id` is a path parameter (fixed to "test-user-1")

**Future Phases**: JWT Bearer token authentication
- Authorization header required: `Authorization: Bearer <token>`
- `user_id` extracted from token, not path parameter

## Endpoints

### 1. Create Task

**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Creates a new task for the specified user.

**Request**:

```http
POST /api/test-user-1/tasks
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write technical documentation for the Task CRUD feature"
}
```

**Request Body Schema**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| title | string | Yes | 1-200 characters | Task title |
| description | string \| null | No | 0-1000 characters | Task description (optional) |

**Success Response** (201 Created):

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "test-user-1",
  "title": "Complete project documentation",
  "description": "Write technical documentation for the Task CRUD feature",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z"
}
```

**Error Responses**:

**422 Validation Error** - Empty title:
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": "Title is required"
}
```

**422 Validation Error** - Title too long:
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": "Title must be 200 characters or less"
}
```

**422 Validation Error** - Description too long:
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": "Description must be 1000 characters or less"
}
```

**500 Server Error**:
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "detail": "Failed to create task"
}
```

---

### 2. List All Tasks

**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieves all tasks for the specified user.

**Request**:

```http
GET /api/test-user-1/tasks
```

**Request Parameters**:

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| user_id | string | Path | Yes | User identifier ("test-user-1") |

**Success Response** (200 OK):

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "test-user-1",
    "title": "Complete project documentation",
    "description": "Write technical documentation",
    "completed": false,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T10:00:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "test-user-1",
    "title": "Review pull request",
    "description": null,
    "completed": true,
    "created_at": "2026-01-07T09:00:00Z",
    "updated_at": "2026-01-07T12:00:00Z"
  }
]
```

**Note**: Tasks are ordered by `created_at` descending (newest first).

**Error Responses**:

**500 Server Error**:
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "detail": "Failed to retrieve tasks"
}
```

**Empty Array** (Success - no tasks):
```http
HTTP/1.1 200 OK
Content-Type: application/json

[]
```

---

### 3. Get Single Task

**Endpoint**: `GET /api/{user_id}/tasks/{task_id}`

**Description**: Retrieves a specific task by ID.

**Request**:

```http
GET /api/test-user-1/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Request Parameters**:

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| user_id | string | Path | Yes | User identifier ("test-user-1") |
| task_id | string | Path | Yes | Task UUID identifier |

**Success Response** (200 OK):

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "test-user-1",
  "title": "Complete project documentation",
  "description": "Write technical documentation",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z"
}
```

**Error Responses**:

**404 Not Found** - Task doesn't exist:
```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Task not found"
}
```

**500 Server Error**:
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "detail": "Failed to retrieve task"
}
```

---

### 4. Update Task

**Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`

**Description**: Updates an existing task. All fields are optional; only provided fields are updated.

**Request**:

```http
PUT /api/test-user-1/tasks/550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Request Parameters**:

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| user_id | string | Path | Yes | User identifier ("test-user-1") |
| task_id | string | Path | Yes | Task UUID identifier |

**Request Body Schema**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| title | string | No | 1-200 characters | New task title |
| description | string \| null | No | 0-1000 characters | New task description |

**Success Response** (200 OK):

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "test-user-1",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T13:00:00Z"
}
```

**Note**: `updated_at` timestamp is automatically updated.

**Error Responses**:

**404 Not Found** - Task doesn't exist:
```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Task not found"
}
```

**422 Validation Error** - Title empty:
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": "Title is required"
}
```

**500 Server Error**:
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "detail": "Failed to update task"
}
```

---

### 5. Delete Task

**Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`

**Description**: Permanently deletes a task.

**Request**:

```http
DELETE /api/test-user-1/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Request Parameters**:

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| user_id | string | Path | Yes | User identifier ("test-user-1") |
| task_id | string | Path | Yes | Task UUID identifier |

**Success Response** (204 No Content):

```http
HTTP/1.1 204 No Content
```

**Note**: Response body is empty. Success is indicated by 204 status code.

**Error Responses**:

**404 Not Found** - Task doesn't exist:
```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Task not found"
}
```

**500 Server Error**:
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "detail": "Failed to delete task"
}
```

---

### 6. Toggle Completion Status

**Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`

**Description**: Toggles the `completed` status of a task (true ↔ false).

**Request**:

```http
PATCH /api/test-user-1/tasks/550e8400-e29b-41d4-a716-446655440000/complete
```

**Request Parameters**:

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| user_id | string | Path | Yes | User identifier ("test-user-1") |
| task_id | string | Path | Yes | Task UUID identifier |

**Request Body**: Empty (no body required)

**Success Response** (200 OK):

**Task marked complete**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "test-user-1",
  "title": "Complete project documentation",
  "description": "Write technical documentation",
  "completed": true,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T14:00:00Z"
}
```

**Task marked incomplete**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "test-user-1",
  "title": "Complete project documentation",
  "description": "Write technical documentation",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T14:30:00Z"
}
```

**Note**: `updated_at` timestamp is automatically updated.

**Error Responses**:

**404 Not Found** - Task doesn't exist:
```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Task not found"
}
```

**500 Server Error**:
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "detail": "Failed to toggle task completion"
}
```

## Response Data Model

### Task Object

```typescript
interface Task {
  id: string;              // UUID
  user_id: string;         // User identifier
  title: string;           // 1-200 characters
  description: string | null;  // 0-1000 characters or null
  completed: boolean;      // true or false
  created_at: string;      // ISO 8601 datetime
  updated_at: string;      // ISO 8601 datetime
}
```

### DateTime Format

All datetime fields use ISO 8601 format:

```
YYYY-MM-DDTHH:MM:SSZ
```

Example: `2026-01-07T10:00:00Z`

## Request/Response Examples

### Complete CRUD Workflow

**1. Create Task**:
```http
POST /api/test-user-1/tasks
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

Response: 201 Created
{
  "id": "task-uuid-1",
  "user_id": "test-user-1",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z"
}
```

**2. List Tasks**:
```http
GET /api/test-user-1/tasks

Response: 200 OK
[{
  "id": "task-uuid-1",
  "user_id": "test-user-1",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z"
}]
```

**3. Get Task**:
```http
GET /api/test-user-1/tasks/task-uuid-1

Response: 200 OK
{
  "id": "task-uuid-1",
  "user_id": "test-user-1",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z"
}
```

**4. Update Task**:
```http
PUT /api/test-user-1/tasks/task-uuid-1
{
  "title": "Buy groceries and household items"
}

Response: 200 OK
{
  "id": "task-uuid-1",
  "user_id": "test-user-1",
  "title": "Buy groceries and household items",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T11:00:00Z"
}
```

**5. Toggle Completion**:
```http
PATCH /api/test-user-1/tasks/task-uuid-1/complete

Response: 200 OK
{
  "id": "task-uuid-1",
  "user_id": "test-user-1",
  "title": "Buy groceries and household items",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T12:00:00Z"
}
```

**6. Delete Task**:
```http
DELETE /api/test-user-1/tasks/task-uuid-1

Response: 204 No Content
```

## Testing Endpoints with curl

### Create Task
```bash
curl -X POST http://localhost:8000/api/test-user-1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test description"}'
```

### List Tasks
```bash
curl http://localhost:8000/api/test-user-1/tasks
```

### Get Single Task
```bash
curl http://localhost:8000/api/test-user-1/tasks/TASK_UUID
```

### Update Task
```bash
curl -X PUT http://localhost:8000/api/test-user-1/tasks/TASK_UUID \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title"}'
```

### Delete Task
```bash
curl -X DELETE http://localhost:8000/api/test-user-1/tasks/TASK_UUID
```

### Toggle Completion
```bash
curl -X PATCH http://localhost:8000/api/test-user-1/tasks/TASK_UUID/complete
```

## Rate Limiting

**Current Phase**: No rate limiting

**Future Phases**: Rate limits may be implemented:
- 100 requests per minute per user
- 1000 requests per hour per user

## Pagination

**Current Phase**: No pagination (all tasks returned in single response)

**Future Phases**: Pagination may be added:
- Query parameters: `?page=1&limit=20`
- Response headers: `X-Total-Count`, `X-Page`, `X-Limit`

## CORS Configuration

**Allowed Origins**:
- `http://localhost:3000` (frontend dev server)
- `http://localhost:3001` (alternate frontend port)

**Allowed Methods**:
- GET, POST, PUT, DELETE, PATCH, OPTIONS

**Allowed Headers**:
- Content-Type, Authorization

## Versioning

**Current Version**: v1 (implied, not in URL)

**Future Versions**:
- URL-based: `/api/v2/tasks`
- Header-based: `Accept: application/vnd.api+json; version=2`

## OpenAPI Specification

The API includes automatic OpenAPI/Swagger documentation available at:
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

This documentation is auto-generated from FastAPI routes and Pydantic models.

## Notes

1. **Idempotency**:
   - GET requests are idempotent
   - POST requests are NOT idempotent (creates new task)
   - PUT requests are idempotent (full update)
   - DELETE requests are idempotent (deleting non-existent task returns 404)
   - PATCH /complete is idempotent (toggles based on current state)

2. **Timestamps**:
   - `created_at` is set once on creation
   - `updated_at` updates on ANY modification (title, description, completed)
   - Both are in UTC timezone

3. **User Scope**:
   - All operations are scoped to `user_id` path parameter
   - Current implementation: fixed to "test-user-1"
   - Future: extracted from JWT token

4. **Empty Description**:
   - Description can be `null` or empty string
   - Both are valid and treated the same

5. **Task Ordering**:
   - List endpoint returns tasks ordered by `created_at` DESC
   - Newest tasks appear first
