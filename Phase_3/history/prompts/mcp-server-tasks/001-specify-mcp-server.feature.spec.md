---
id: 001
title: "Specify MCP Server"
stage: "spec"
date: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "mcp-server-tasks"
branch: "001-mcp-server-tasks"
user: "Wajahat traders"
command: "sp.specify"
labels: ["mcp", "server", "tasks", "todo-chatbot"]
links:
  spec: "specs/001-mcp-server-tasks/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-mcp-server-tasks/spec.md"
  - "specs/001-mcp-server-tasks/checklists/requirements.md"
tests:
  - "Specification completeness"
  - "Requirements validation"
---

# MCP Server Specification for Todo AI Chatbot

## Original Prompt

```
MCP Server for Todo AI Chatbot

Target audience: Claude Code implementing MCP tools using Official MCP SDK (Python)
Focus: Create 5 MCP tools that expose task operations to the OpenAI Agent

Success criteria:
- All 5 MCP tools implemented (add_task, list_tasks, complete_task, delete_task, update_task)
- Each tool connects to Neon PostgreSQL database via SQLModel
- Tools are stateless (no in-memory storage)
- Proper error handling with user-friendly messages
- Tools return structured JSON responses
- MCP server can be discovered and called by OpenAI Agent

MCP Tools to build:

1. add_task
   Purpose: Create a new task in the database
   Input parameters:
   - user_id (string, required): User identifier
   - title (string, required): Task title (max 200 chars)
   - description (string, optional): Task details (max 1000 chars)

   Output format:
   {
     "task_id": integer,
     "status": "created",
     "title": string
   }

   Error scenarios:
   - Missing user_id → "user_id is required"
   - Missing title → "title is required"
   - Empty title → "title cannot be empty"
   - Database error → "Failed to create task"

2. list_tasks
   Purpose: Retrieve tasks from database based on filter
   Input parameters:
   - user_id (string, required): User identifier
   - status (string, optional): Filter by "all", "pending", or "completed" (default: "all")

   Output format:
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

   Error scenarios:
   - Missing user_id → "user_id is required"
   - Invalid status value → "status must be 'all', 'pending', or 'completed'"
   - Database error → "Failed to retrieve tasks"
   - Empty result → Return empty array []

3. complete_task
   Purpose: Mark a specific task as completed
   Input parameters:
   - user_id (string, required): User identifier
   - task_id (integer, required): Task ID to complete

   Output format:
   {
     "task_id": integer,
     "status": "completed",
     "title": string
   }

   Error scenarios:
   - Missing user_id → "user_id is required"
   - Missing task_id → "task_id is required"
   - Task not found → "Task {task_id} not found"
   - Task belongs to different user → "Task not found" (don't leak user info)
   - Already completed → Return success (idempotent)
   - Database error → "Failed to complete task"

4. delete_task
   Purpose: Remove a task from database
   Input parameters:
   - user_id (string, required): User identifier
   - task_id (integer, required): Task ID to delete

   Output format:
   {
     "task_id": integer,
     "status": "deleted",
     "title": string
   }

   Error scenarios:
   - Missing user_id → "user_id is required"
   - Missing task_id → "task_id is required"
   - Task not found → "Task {task_id} not found"
   - Task belongs to different user → "Task not found"
   - Database error → "Failed to delete task"

5. update_task
   Purpose: Modify task title or description
   Input parameters:
   - user_id (string, required): User identifier
   - task_id (integer, required): Task ID to update
   - title (string, optional): New title (max 200 chars)
   - description (string, optional): New description (max 1000 chars)

   Output format:
   {
     "task_id": integer,
     "status": "updated",
     "title": string
   }

   Error scenarios:
   - Missing user_id → "user_id is required"
   - Missing task_id → "task_id is required"
   - No fields to update → "At least one field (title or description) required"
   - Empty title provided → "title cannot be empty"
   - Task not found → "Task {task_id} not found"
   - Task belongs to different user → "Task not found"
   - Database error → "Failed to update task"

Technical requirements:

MCP SDK implementation:
- Use Official MCP SDK for Python
- Define tools using @mcp.tool() decorator
- Register all 5 tools with MCP server
- Server runs on dedicated port (e.g., 8001)
- Health check endpoint for monitoring

Database integration:
- Import SQLModel models from models.py
- Use async database sessions
- All queries filter by user_id for security
- Close database connections properly
- Handle database connection errors gracefully

Stateless design:
- NO in-memory caching of tasks
- NO session state storage
- Each tool call is independent
- All data persisted to PostgreSQL immediately
- Tools can be called in any order

Security considerations:
- Always filter by user_id (prevent cross-user access)
- Validate all inputs before database operations
- Sanitize error messages (don't leak sensitive info)
- Use parameterized queries (prevent SQL injection)
- Log tool calls for debugging (without PII)

Response format standards:
- All responses are valid JSON
- Use snake_case for field names
- Include status field in all responses
- Timestamps in ISO 8601 format
- Null for optional fields when not provided

Constraints:
- Tool execution timeout: 30 seconds max
- No file system operations
- No external API calls (database only)
- No HTML/JavaScript in responses (JSON only)
- Maximum 100 tasks returned by list_tasks (pagination not required for Basic Level)

Not building:
- Task sharing between users
- Task categories or tags
- Due dates or reminders
- Task priorities
- Batch operations (update multiple tasks)
- Task search by keyword
- Task export/import
- Undo functionality
- Task history/audit log

Deliverables:
- mcp_server.py with all 5 tool definitions
- Tool registration and server initialization
- Error handling for each tool
- Input validation functions
- Database query helpers
- Server startup script
- Environment configuration (.env support)
- Logging setup for debugging

File structure:
backend/
├── mcp_server.py      # MCP server with tool definitions
├── models.py          # SQLModel database models (from Step 2)
├── database.py        # Database connection (from Step 2)
├── utils.py           # Validation and helper functions
└── .env.example       # Environment variables template

Environment variables needed:
- DATABASE_URL: Neon PostgreSQL connection string
- MCP_SERVER_PORT: Port for MCP server (default: 8001)
- LOG_LEVEL: Logging verbosity (default: INFO)

Testing requirements:
- Test each tool independently with valid inputs
- Test each error scenario returns proper message
- Test user_id isolation (user A can't access user B's tasks)
- Test database connection failures handled gracefully
- Test tool discovery by MCP client
- Verify all responses are valid JSON
- Verify stateless behavior (restart server, tools still work)
```

## Response Summary

Created a comprehensive specification for the MCP server for the Todo AI Chatbot, defining all five required MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) with their proper parameters and response formats. The specification includes:

- Detailed functional requirements for all five tools
- User scenarios covering the core functionality
- Proper error handling and security considerations
- Success criteria that are measurable and technology-agnostic
- Edge cases consideration

## Outcome

The specification is complete and ready for the planning phase (`/sp.plan`). It captures all requirements from the user input while maintaining a focus on user value and business needs without implementation details leaking into the specification. The spec includes proper acceptance scenarios, edge cases, and measurable success criteria.