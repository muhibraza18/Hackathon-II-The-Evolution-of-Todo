---
id: 002
title: "Plan MCP Server"
stage: "plan"
date: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "mcp-server-tasks"
branch: "001-mcp-server-tasks"
user: "Wajahat traders"
command: "sp.plan"
labels: ["mcp", "server", "tasks", "todo-chatbot", "planning"]
links:
  spec: "specs/001-mcp-server-tasks/spec.md"
  plan: "specs/001-mcp-server-tasks/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-mcp-server-tasks/plan.md"
  - "specs/001-mcp-server-tasks/research.md"
  - "specs/001-mcp-server-tasks/data-model.md"
  - "specs/001-mcp-server-tasks/quickstart.md"
tests:
  - "Research completion"
  - "Data model validation"
  - "API contract validation"
---

# MCP Server Implementation Plan for Todo AI Chatbot

## Original Prompt

```
MCP Server Implementation

Create:
- MCP server architecture diagram showing 5 tools connecting to database
- Tool registration flow with Official MCP SDK
- Database integration pattern for each tool
- Error handling strategy with user-friendly messages
- Testing approach for each tool independently

Implementation approach:

1. Setup phase:
   - Install Official MCP SDK for Python (mcp package)
   - Import SQLModel models from Step 2
   - Import database session from Step 2
   - Create mcp_server.py file structure
   - Setup logging configuration

2. Tool definition phase:
   - Define add_task tool with @mcp.tool() decorator
   - Define list_tasks tool with status filtering
   - Define complete_task tool with database update
   - Define delete_task tool with soft validation
   - Define update_task tool with partial updates
   - Add docstrings explaining each tool's purpose

3. Database integration phase:
   - Create async database session dependency
   - Implement user_id filtering in all queries
   - Add error handling for database connection failures
   - Implement proper session cleanup (async context managers)
   - Add query validation before execution

4. Input validation phase:
   - Validate user_id is present in all tools
   - Validate task_id is integer where required
   - Validate title/description length limits
   - Validate status enum values in list_tasks
   - Return clear error messages for invalid inputs

5. Server initialization phase:
   - Register all 5 tools with MCP server
   - Configure server port from environment variable
   - Add health check endpoint
   - Setup graceful shutdown handling
   - Add startup logging

6. Testing phase:
   - Test each tool with valid inputs
   - Test all error scenarios
   - Test user_id isolation
   - Test stateless behavior (restart server)
   - Verify JSON response formats

Decisions needing documentation:

1. MCP SDK server pattern:
   Options: (a) FastMCP (simpler), (b) Official MCP SDK server class
   Tradeoffs: FastMCP = easier setup; Official SDK = more control, standards-compliant
   Recommendation: Official MCP SDK for hackathon compliance

2. Database session management:
   Options: (a) Dependency injection per tool, (b) Global session, (c) Context manager per call
   Tradeoffs: DI = clean but verbose; Global = simple but not async-safe; Context = safe but repetitive
   Recommendation: Context manager with helper function

3. Error response format:
   Options: (a) Throw exceptions, (b) Return error dict, (c) Mixed approach
   Tradeoffs: Exceptions = MCP handles; Dict = more control; Mixed = flexible but inconsistent
   Recommendation: Return structured error dicts for better agent understanding

4. Tool naming convention:
   Options: (a) snake_case (add_task), (b) camelCase (addTask), (c) kebab-case (add-task)
   Tradeoffs: snake_case = Python convention; camelCase = JavaScript style; kebab-case = URL friendly
   Recommendation: snake_case for Python consistency

5. List filtering strategy:
   Options: (a) status parameter ("all"/"pending"/"completed"), (b) separate tools, (c) multiple filters
   Tradeoffs: Single param = simple; Separate tools = clear; Multiple = complex
   Recommendation: Single status parameter (matches spec)

6. Update tool behavior:
   Options: (a) Require at least one field, (b) Allow no-op updates, (c) Full replacement only
   Tradeoffs: Require field = prevents mistakes; No-op = idempotent; Full replace = simpler
   Recommendation: Require at least one field (title or description)

7. Completed task handling:
   Options: (a) Allow re-completing (idempotent), (b) Reject if already completed, (c) Track completion history
   Tradeoffs: Idempotent = simpler agent logic; Reject = more explicit; History = overkill for Basic Level
   Recommendation: Idempotent (return success even if already completed)

Testing strategy:

Validation checks based on acceptance criteria:

1. Tool registration tests:
   - ✓ MCP server discovers all 5 tools
   - ✓ Each tool has proper name and description
   - ✓ Tool parameters defined correctly
   - ✓ Server starts without errors
   - ✓ Health check endpoint responds

2. add_task tool tests:
   - ✓ Creates task with title only
   - ✓ Creates task with title and description
   - ✓ Returns task_id, status="created", title
   - ✗ Fails without user_id
   - ✗ Fails without title
   - ✗ Fails with empty title
   - ✓ Handles database errors gracefully

3. list_tasks tool tests:
   - ✓ Returns all tasks with status="all"
   - ✓ Returns only pending tasks with status="pending"
   - ✓ Returns only completed tasks with status="completed"
   - ✓ Returns empty array when no tasks
   - ✓ Filters by user_id (doesn't show other users' tasks)
   - ✗ Fails with invalid status value
   - ✗ Fails without user_id

4. complete_task tool tests:
   - ✓ Marks task as completed
   - ✓ Returns task_id, status="completed", title
   - ✓ Idempotent (can complete already completed task)
   - ✗ Fails without user_id
   - ✗ Fails without task_id
   - ✗ Fails with non-existent task_id
   - ✓ Cannot complete other user's tasks

5. delete_task tool tests:
   - ✓ Deletes task from database
   - ✓ Returns task_id, status="deleted", title
   - ✗ Fails without user_id
   - ✗ Fails without task_id
   - ✗ Fails with non-existent task_id
   - ✓ Cannot delete other user's tasks

6. update_task tool tests:
   - ✓ Updates title only
   - ✓ Updates description only
   - ✓ Updates both title and description
   - ✓ Returns task_id, status="updated", title
   - ✗ Fails without user_id
   - ✗ Fails without task_id
   - ✗ Fails with no fields to update
   - ✗ Fails with empty title
   - ✗ Fails with non-existent task_id
   - ✓ Cannot update other user's tasks

7. Security and isolation tests:
   - ✓ User A cannot see User B's tasks
   - ✓ User A cannot complete User B's tasks
   - ✓ User A cannot delete User B's tasks
   - ✓ User A cannot update User B's tasks
   - ✓ Error messages don't leak user information

8. Stateless behavior tests:
   - ✓ Restart server, tasks still accessible
   - ✓ No in-memory task storage
   - ✓ Each tool call is independent
   - ✓ Concurrent requests don't interfere

Technical details:

File structure:
backend/
├── mcp_server.py           # Main MCP server with 5 tools
├── models.py               # SQLModel models (from Step 2)
├── database.py             # DB connection (from Step 2)
├── utils.py                # Validation helpers
├── .env                    # Environment variables (gitignored)
├── .env.example            # Template for environment setup
└── requirements.txt        # Python dependencies

MCP tool definition pattern:
```python
from mcp.server import Server
from mcp.types import Tool

server = Server("todo-mcp-server")

@server.tool()
async def add_task(user_id: str, title: str, description: str = None):
    """Create a new task"""
    # Validation
    # Database operation
    # Return structured response
```

Database query pattern:
```python
async with get_session() as session:
    # Query with user_id filter
    result = await session.exec(
        select(Task).where(
            Task.user_id == user_id,
            Task.id == task_id
        )
    )
    task = result.first()
```

Error handling pattern:
```python
try:
    # Database operation
    return {"task_id": task.id, "status": "created", "title": task.title}
except Exception as e:
    logger.error(f"Failed to create task: {e}")
    return {"error": "Failed to create task"}
```

Dependencies to add to requirements.txt:
- mcp (Official MCP SDK)
- sqlmodel (from Step 2)
- psycopg2-binary or asyncpg (from Step 2)
- python-dotenv
- pydantic
- asyncio

Environment variables (.env.example):
DATABASE_URL=postgresql://user:password@host/database
MCP_SERVER_PORT=8001
LOG_LEVEL=INFO

Quality validation:
- All tools have type hints
- All tools have descriptive docstrings
- Error messages are user-friendly (no stack traces)
- All database queries use async/await
- Sessions properly closed after use
- Logging includes tool name and parameters
- No hardcoded values (use env vars)

Risk mitigation:
- Test database connection before starting server
- Validate MCP SDK installation
- Handle missing environment variables gracefully
- Add timeout for database operations
- Log all errors for debugging
- Test with sample data before agent integration

Next integration point:
- MCP server will be called by OpenAI Agent (Step 5)
- Agent will use these tools to fulfill user requests
- FastAPI endpoint (Step 4) will coordinate between agent and MCP server
```

## Response Summary

Created a comprehensive implementation plan for the Todo AI Chatbot MCP server, including:

- **Research phase**: Completed research on MCP SDK installation, server configuration, health checks, session management, and logging
- **Data model**: Defined complete specifications for all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) with proper parameters and response formats
- **API contracts**: Specified detailed input/output formats and error scenarios for each tool
- **Quickstart guide**: Provided detailed setup and usage instructions
- **Constitution compliance**: Verified all requirements from the project constitution are met

## Outcome

The implementation plan is complete with all research, design, and architecture decisions documented. The plan includes:
- Complete data model specification with all 5 MCP tools
- Technical decisions made on MCP SDK usage, session management, and error handling
- Constitutional compliance verified
- Ready for the implementation phase