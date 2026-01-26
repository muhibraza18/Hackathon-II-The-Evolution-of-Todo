# Data Model: MCP Server for Todo AI Chatbot

**Feature**: MCP Server for Todo AI Chatbot
**Date**: 2026-01-13
**Status**: Draft

## MCP Tool: add_task

### Purpose
Create a new task in the database

### Input Parameters
- **user_id** (String, Required)
  - User identifier
  - Used for data isolation
  - Required for all operations
- **title** (String, Required)
  - Task title
  - Maximum 200 characters
  - Cannot be empty
- **description** (String, Optional)
  - Task details
  - Maximum 1000 characters
  - Can be null/empty

### Output Format
```json
{
  "task_id": integer,
  "status": "created",
  "title": string
}
```

### Validation Rules
- user_id must be provided
- title must be provided and not empty
- title must be ≤ 200 characters
- description must be ≤ 1000 characters if provided

### Error Scenarios
- Missing user_id → "user_id is required"
- Missing title → "title is required"
- Empty title → "title cannot be empty"
- Database error → "Failed to create task"

## MCP Tool: list_tasks

### Purpose
Retrieve tasks from database based on filter

### Input Parameters
- **user_id** (String, Required)
  - User identifier
  - Used for data isolation
  - Required for all operations
- **status** (String, Optional)
  - Filter by task completion status
  - Values: "all", "pending", "completed"
  - Default: "all"

### Output Format
```json
[
  {
    "id": integer,
    "title": string,
    "description": string or null,
    "completed": boolean,
    "created_at": ISO datetime string
  },
  ...
]
```

### Validation Rules
- user_id must be provided
- status must be "all", "pending", or "completed" if provided
- Default to "all" if status not provided

### Error Scenarios
- Missing user_id → "user_id is required"
- Invalid status value → "status must be 'all', 'pending', or 'completed'"
- Database error → "Failed to retrieve tasks"
- Empty result → Return empty array []

## MCP Tool: complete_task

### Purpose
Mark a specific task as completed

### Input Parameters
- **user_id** (String, Required)
  - User identifier
  - Used for data isolation
  - Required for all operations
- **task_id** (Integer, Required)
  - Task ID to complete
  - Must exist in database
  - Must belong to user

### Output Format
```json
{
  "task_id": integer,
  "status": "completed",
  "title": string
}
```

### Validation Rules
- user_id must be provided
- task_id must be provided and exist
- task must belong to the user
- Operation is idempotent (can complete already completed task)

### Error Scenarios
- Missing user_id → "user_id is required"
- Missing task_id → "task_id is required"
- Task not found → "Task {task_id} not found"
- Task belongs to different user → "Task not found" (don't leak user info)
- Database error → "Failed to complete task"

## MCP Tool: delete_task

### Purpose
Remove a task from database

### Input Parameters
- **user_id** (String, Required)
  - User identifier
  - Used for data isolation
  - Required for all operations
- **task_id** (Integer, Required)
  - Task ID to delete
  - Must exist in database
  - Must belong to user

### Output Format
```json
{
  "task_id": integer,
  "status": "deleted",
  "title": string
}
```

### Validation Rules
- user_id must be provided
- task_id must be provided and exist
- task must belong to the user

### Error Scenarios
- Missing user_id → "user_id is required"
- Missing task_id → "task_id is required"
- Task not found → "Task {task_id} not found"
- Task belongs to different user → "Task not found"
- Database error → "Failed to delete task"

## MCP Tool: update_task

### Purpose
Modify task title or description

### Input Parameters
- **user_id** (String, Required)
  - User identifier
  - Used for data isolation
  - Required for all operations
- **task_id** (Integer, Required)
  - Task ID to update
  - Must exist in database
  - Must belong to user
- **title** (String, Optional)
  - New title
  - Maximum 200 characters
  - Cannot be empty if provided
- **description** (String, Optional)
  - New description
  - Maximum 1000 characters

### Output Format
```json
{
  "task_id": integer,
  "status": "updated",
  "title": string
}
```

### Validation Rules
- user_id must be provided
- task_id must be provided and exist
- At least one of title or description must be provided
- If title is provided, it cannot be empty and must be ≤ 200 characters
- If description is provided, it must be ≤ 1000 characters

### Error Scenarios
- Missing user_id → "user_id is required"
- Missing task_id → "task_id is required"
- No fields to update → "At least one field (title or description) required"
- Empty title provided → "title cannot be empty"
- Task not found → "Task {task_id} not found"
- Task belongs to different user → "Task not found"
- Database error → "Failed to update task"

## Database Integration Model

### Task Entity (from existing models.py)
- **id** (Integer, Primary Key, Auto-increment)
- **user_id** (String, Required, Indexed)
- **title** (String, Required, Max 200 chars)
- **description** (String, Optional, Max 1000 chars)
- **completed** (Boolean, Default False)
- **created_at** (DateTime, Auto-populated)
- **updated_at** (DateTime, Auto-updated)

### Security Model
- All queries must filter by user_id for data isolation
- Parameterized queries to prevent SQL injection
- Sanitized error messages to prevent information leakage

### Validation Model
- Input validation before database operations
- Length validation for string fields
- Type validation for all parameters
- Range validation for enum values

## Response Format Standards

### Common Patterns
- All responses are valid JSON
- Use snake_case for field names
- Include status field in all responses where appropriate
- Timestamps in ISO 8601 format
- Null for optional fields when not provided
- Consistent error message format

### Success Responses
- Include task_id when relevant
- Include status field with operation result
- Include title for context
- Return appropriate data structure for each operation

### Error Responses
- Return clear, user-friendly messages
- Don't expose internal system details
- Maintain user privacy in error messages
- Follow consistent error message patterns