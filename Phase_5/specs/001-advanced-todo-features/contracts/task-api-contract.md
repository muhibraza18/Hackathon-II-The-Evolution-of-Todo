# API Contract: Advanced Todo Features

## Overview
This document defines the API contracts for the advanced todo features including recurring tasks, due dates, priorities, tags, and enhanced filtering capabilities.

## Base URL
`/api/tasks`

## Task Creation
### POST /api/tasks

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "status": "pending|completed",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "low|medium|high|urgent",
  "tags": ["string"],
  "recurring_config": {
    "type": "daily|weekly|monthly",
    "interval": 1,
    "end_condition": {
      "type": "never|after_date|after_occurrences",
      "value": "2024-12-31|5"
    }
  }
}
```

**Response:**
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "pending|completed",
  "created_at": "2023-12-31T23:59:59Z",
  "updated_at": "2023-12-31T23:59:59Z",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "low|medium|high|urgent",
  "tags": ["string"],
  "recurring_config": {
    "type": "daily|weekly|monthly",
    "interval": 1,
    "end_condition": {
      "type": "never|after_date|after_occurrences",
      "value": "2024-12-31|5"
    }
  },
  "next_occurrence_id": "string|null",
  "parent_task_id": "string|null",
  "original_task_id": "string|null"
}
```

## Task Retrieval with Filtering
### GET /api/tasks

**Query Parameters:**
- `priority`: Filter by priority (low|medium|high|urgent)
- `tag`: Filter by tag (can be used multiple times)
- `status`: Filter by status (pending|completed)
- `due_before`: Filter tasks with due date before specified date
- `due_after`: Filter tasks with due date after specified date
- `sort_by`: Sort by field (created_at|updated_at|due_date|priority)
- `order`: Sort order (asc|desc)
- `limit`: Number of results to return
- `offset`: Offset for pagination

**Response:**
```json
{
  "items": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "status": "pending|completed",
      "created_at": "2023-12-31T23:59:59Z",
      "updated_at": "2023-12-31T23:59:59Z",
      "due_date": "2023-12-31T23:59:59Z",
      "priority": "low|medium|high|urgent",
      "tags": ["string"],
      "recurring_config": {
        "type": "daily|weekly|monthly",
        "interval": 1,
        "end_condition": {
          "type": "never|after_date|after_occurrences",
          "value": "2024-12-31|5"
        }
      },
      "next_occurrence_id": "string|null",
      "parent_task_id": "string|null",
      "original_task_id": "string|null"
    }
  ],
  "total": 100,
  "offset": 0,
  "limit": 10
}
```

## Task Update
### PUT /api/tasks/{id}

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "status": "pending|completed",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "low|medium|high|urgent",
  "tags": ["string"],
  "recurring_config": {
    "type": "daily|weekly|monthly",
    "interval": 1,
    "end_condition": {
      "type": "never|after_date|after_occurrences",
      "value": "2024-12-31|5"
    }
  }
}
```

**Response:**
Same as GET /api/tasks/{id}

## Task Completion
### PATCH /api/tasks/{id}/complete

**Response:**
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "completed",
  "completed_at": "2023-12-31T23:59:59Z",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "low|medium|high|urgent",
  "tags": ["string"],
  "recurring_config": {
    "type": "daily|weekly|monthly",
    "interval": 1,
    "end_condition": {
      "type": "never|after_date|after_occurrences",
      "value": "2024-12-31|5"
    }
  },
  "next_occurrence_id": "string|null",
  "parent_task_id": "string|null",
  "original_task_id": "string|null"
}
```

**Special Behavior:**
- If the task has recurring_config, creates the next occurrence automatically
- Returns the completed task and the ID of the newly created occurrence (if applicable)

## Event Publishing Contract

When tasks are created, updated, or completed, the system will prepare the following events for future processing:

### TaskCreatedEvent
```json
{
  "event_type": "task.created",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "2023-12-31T23:59:59Z",
  "data": {
    "title": "string",
    "due_date": "2023-12-31T23:59:59Z",
    "priority": "low|medium|high|urgent",
    "tags": ["string"]
  }
}
```

### TaskUpdatedEvent
```json
{
  "event_type": "task.updated",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "2023-12-31T23:59:59Z",
  "data": {
    "title": "string",
    "due_date": "2023-12-31T23:59:59Z",
    "priority": "low|medium|high|urgent",
    "tags": ["string"],
    "status": "pending|completed"
  }
}
```

### TaskCompletedEvent
```json
{
  "event_type": "task.completed",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "2023-12-31T23:59:59Z",
  "data": {
    "title": "string",
    "due_date": "2023-12-31T23:59:59Z",
    "priority": "low|medium|high|urgent",
    "tags": ["string"],
    "next_occurrence_id": "string|null"
  }
}
```

### TaskDeletedEvent
```json
{
  "event_type": "task.deleted",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "2023-12-31T23:59:59Z",
  "data": {}
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "validation_failed",
  "message": "Validation error details",
  "details": [
    {
      "field": "due_date",
      "message": "Must be in the future"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_server_error",
  "message": "An unexpected error occurred"
}
```