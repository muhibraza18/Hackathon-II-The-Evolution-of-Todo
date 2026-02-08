# Feature Specification: MCP Server for Todo AI Chatbot

**Feature Branch**: `001-mcp-server-tasks`
**Created**: 2026-01-13
**Status**: Draft
**Input**: User description: "MCP Server for Todo AI Chatbot

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
- Verify stateless behavior (restart server, tools still work)"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Add New Tasks via Natural Language (Priority: P1)

As a user of the Todo AI Chatbot, I want to create new tasks through natural language so that the AI agent can add them to my task list by calling the add_task MCP tool.

**Why this priority**: This is the core functionality - users need to be able to add tasks for the system to provide value.

**Independent Test**: Can be fully tested by having the AI agent call the add_task tool with user_id, title, and description parameters. The system should create a new task record and return the success response.

**Acceptance Scenarios**:

1. **Given** a user speaks a task to add, **When** the AI agent calls add_task with valid parameters, **Then** the system creates a new task and returns the created task ID with success status
2. **Given** a user speaks a task with missing title, **When** the AI agent calls add_task, **Then** the system returns an error message "title is required"

---

### User Story 2 - View Current Tasks (Priority: P2)

As a user of the Todo AI Chatbot, I want to see my current tasks so that I can track what I need to do by having the AI agent call the list_tasks MCP tool.

**Why this priority**: Essential for task management - users need to see their tasks to manage them effectively.

**Independent Test**: Can be fully tested by having the AI agent call the list_tasks tool with user_id and status parameters. The system should return the appropriate list of tasks.

**Acceptance Scenarios**:

1. **Given** a user asks to see their tasks, **When** the AI agent calls list_tasks with user_id and status "all", **Then** the system returns all tasks for that user
2. **Given** a user asks to see pending tasks, **When** the AI agent calls list_tasks with status "pending", **Then** the system returns only incomplete tasks for that user

---

### User Story 3 - Complete Tasks (Priority: P3)

As a user of the Todo AI Chatbot, I want to mark tasks as completed so that I can track my progress by having the AI agent call the complete_task MCP tool.

**Why this priority**: Task completion is a core part of task management functionality.

**Independent Test**: Can be fully tested by having the AI agent call the complete_task tool with user_id and task_id parameters. The system should update the task status and return success.

**Acceptance Scenarios**:

1. **Given** a user indicates a task is done, **When** the AI agent calls complete_task with valid task_id, **Then** the system marks the task as completed and returns success status
2. **Given** a user tries to complete a task that doesn't exist, **When** the AI agent calls complete_task with invalid task_id, **Then** the system returns "Task {task_id} not found"

---

### User Story 4 - Manage Tasks (Priority: P4)

As a user of the Todo AI Chatbot, I want to update or delete tasks so that I can keep my task list current by having the AI agent call the update_task or delete_task MCP tools.

**Why this priority**: Task management requires the ability to modify or remove tasks that are no longer relevant.

**Independent Test**: Can be fully tested by having the AI agent call update_task or delete_task tools with appropriate parameters. The system should modify the task and return success.

**Acceptance Scenarios**:

1. **Given** a user wants to update a task description, **When** the AI agent calls update_task with new description, **Then** the system updates the task and returns success status
2. **Given** a user wants to remove a task, **When** the AI agent calls delete_task with valid task_id, **Then** the system removes the task and returns success status

---

### Edge Cases

- What happens when a database connection fails - tools should return appropriate error messages?
- How does the system handle simultaneous requests from the same user?
- What occurs when a user attempts to access another user's tasks - proper isolation enforced?
- How does the system handle very long task titles or descriptions that exceed character limits?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST provide an add_task MCP tool that accepts user_id, title, and optional description parameters
- **FR-002**: System MUST provide a list_tasks MCP tool that accepts user_id and optional status filter parameters
- **FR-003**: System MUST provide a complete_task MCP tool that accepts user_id and task_id parameters
- **FR-004**: System MUST provide a delete_task MCP tool that accepts user_id and task_id parameters
- **FR-005**: System MUST provide an update_task MCP tool that accepts user_id, task_id, and optional title/description parameters
- **FR-006**: System MUST connect to Neon PostgreSQL database using SQLModel for all operations
- **FR-007**: System MUST implement stateless design with no in-memory caching of tasks
- **FR-008**: System MUST filter all database queries by user_id to ensure data isolation between users
- **FR-009**: System MUST return structured JSON responses from all MCP tools
- **FR-010**: System MUST handle database connection errors gracefully and return user-friendly messages
- **FR-011**: System MUST validate all input parameters before database operations
- **FR-012**: System MUST sanitize error messages to prevent information leakage
- **FR-013**: System MUST implement proper timeout handling (max 30 seconds per tool execution)
- **FR-014**: System MUST return appropriate error messages for all error scenarios specified in the tool definitions
- **FR-015**: System MUST support idempotent operations where applicable (e.g., completing an already completed task)

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's todo item with title, description, completion status, and timestamps. Associated with a specific user via user_id.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: All 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) are successfully implemented and registered with the MCP server
- **SC-002**: Each tool connects successfully to the Neon PostgreSQL database and performs operations using SQLModel
- **SC-003**: All tools maintain stateless design with no in-memory storage between requests
- **SC-004**: Error handling returns appropriate user-friendly messages for all specified error scenarios
- **SC-005**: All tools return structured JSON responses in the specified formats
- **SC-006**: MCP server can be discovered and called by the OpenAI Agent successfully