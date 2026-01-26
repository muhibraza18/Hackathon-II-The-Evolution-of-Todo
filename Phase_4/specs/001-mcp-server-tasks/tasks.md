# Tasks: MCP Server for Todo AI Chatbot

**Feature**: MCP Server for Todo AI Chatbot
**Feature Branch**: 001-mcp-server-tasks
**Created**: 2026-01-13
**Status**: Complete
**Author**: Claude Code

## Implementation Strategy

Build the MCP server incrementally with a focus on delivering value early. The MVP will include the add_task tool to satisfy User Story 1 (P1). Subsequent phases will add the remaining tools to fulfill User Stories 2, 3, and 4.

## Dependencies

- User Story 1 (P1) completion is not required for other user stories since tools are independent
- Foundational tasks must be completed before any user story-specific tasks
- Server infrastructure must be set up before any tool implementation

## Parallel Execution Examples

- [P] T005-T008 can be executed in parallel (different tool implementations)
- [P] T015-T017 can be executed in parallel (different validation functions)
- [P] T025-T027 can be executed in parallel (different test files)

## Phase 1: Setup

Initialize project structure and install dependencies required for the MCP server implementation.

- [x] T001 Create backend directory structure for MCP server
- [x] T002 Install required dependencies: mcp, sqlmodel, asyncpg, python-dotenv, pydantic
- [x] T003 Create requirements.txt with all dependencies
- [x] T004 Create .env.example with environment variables template

## Phase 2: Foundational

Implement foundational components that are required by all user stories.

- [x] T005 Create mcp_server.py with basic server structure and imports
- [x] T006 Implement MCP server initialization with proper configuration
- [x] T007 Create health check endpoint at /health
- [x] T008 Set up logging infrastructure with configurable levels
- [ ] T009 Create utils.py for validation and helper functions
- [x] T010 Verify database connection with existing models.py and database.py

## Phase 3: User Story 1 - Add New Tasks via Natural Language (Priority: P1)

As a user of the Todo AI Chatbot, I want to create new tasks through natural language so that the AI agent can add them to my task list by calling the add_task MCP tool.

**Goal**: Implement the add_task tool with all validation and database integration to enable task creation.

**Independent Test**: Can be fully tested by having the AI agent call the add_task tool with user_id, title, and description parameters. The system should create a new task record and return the success response.

- [x] T011 [P] [US1] Implement add_task tool in mcp_server.py with @server.tool() decorator
- [x] T012 [US1] Add input validation for user_id, title, and description parameters
- [x] T013 [US1] Implement database operation to create new Task record
- [x] T014 [US1] Add proper error handling for database operations
- [x] T015 [P] [US1] Create validation function for title length (max 200 chars)
- [x] T016 [P] [US1] Create validation function for description length (max 1000 chars)
- [x] T017 [US1] Ensure user_id filtering and data isolation
- [x] T018 [US1] Test add_task tool with valid parameters
- [x] T019 [US1] Test error scenarios for add_task tool

## Phase 4: User Story 2 - View Current Tasks (Priority: P2)

As a user of the Todo AI Chatbot, I want to see my current tasks so that I can track what I need to do by having the AI agent call the list_tasks MCP tool.

**Goal**: Implement the list_tasks tool with status filtering to enable task retrieval.

**Independent Test**: Can be fully tested by having the AI agent call the list_tasks tool with user_id and status parameters. The system should return the appropriate list of tasks.

- [x] T020 [P] [US2] Implement list_tasks tool in mcp_server.py with @server.tool() decorator
- [x] T021 [US2] Add input validation for user_id and status parameters
- [x] T022 [US2] Implement database query with status filtering (all, pending, completed)
- [x] T023 [US2] Format response as array of task objects with required fields
- [x] T024 [US2] Add proper error handling for database operations
- [x] T025 [P] [US2] Create validation function for status parameter
- [x] T026 [US2] Ensure user_id filtering and data isolation
- [x] T027 [US2] Test list_tasks tool with different status filters
- [x] T028 [US2] Test error scenarios for list_tasks tool

## Phase 5: User Story 3 - Complete Tasks (Priority: P3)

As a user of the Todo AI Chatbot, I want to mark tasks as completed so that I can track my progress by having the AI agent call the complete_task MCP tool.

**Goal**: Implement the complete_task tool with idempotent behavior to enable task completion.

**Independent Test**: Can be fully tested by having the AI agent call the complete_task tool with user_id and task_id parameters. The system should update the task status and return success.

- [x] T029 [P] [US3] Implement complete_task tool in mcp_server.py with @server.tool() decorator
- [x] T030 [US3] Add input validation for user_id and task_id parameters
- [x] T031 [US3] Implement database operation to update task completion status
- [x] T032 [US3] Ensure idempotent behavior (can complete already completed task)
- [x] T033 [US3] Add proper error handling for database operations
- [x] T034 [US3] Ensure user_id filtering and data isolation
- [x] T035 [US3] Test complete_task tool with valid task_id
- [x] T036 [US3] Test idempotent behavior of complete_task
- [x] T037 [US3] Test error scenarios for complete_task tool

## Phase 6: User Story 4 - Manage Tasks (Priority: P4)

As a user of the Todo AI Chatbot, I want to update or delete tasks so that I can keep my task list current by having the AI agent call the update_task or delete_task MCP tools.

**Goal**: Implement the update_task and delete_task tools to enable task management.

**Independent Test**: Can be fully tested by having the AI agent call update_task or delete_task tools with appropriate parameters. The system should modify the task and return success.

- [x] T038 [P] [US4] Implement delete_task tool in mcp_server.py with @server.tool() decorator
- [x] T039 [US4] Implement update_task tool in mcp_server.py with @server.tool() decorator
- [x] T040 [US4] Add input validation for delete_task parameters
- [x] T041 [US4] Add input validation for update_task parameters (at least one field required)
- [x] T042 [US4] Implement database operation to delete task record
- [x] T043 [US4] Implement database operation to update task fields (title, description)
- [x] T044 [US4] Add proper error handling for both tools
- [x] T045 [US4] Ensure user_id filtering and data isolation for both tools
- [x] T046 [US4] Test delete_task tool with valid task_id
- [x] T047 [US4] Test update_task tool with partial updates
- [x] T048 [US4] Test error scenarios for both tools

## Phase 7: Validation & Testing

Implement comprehensive testing to validate all functionality.

- [ ] T049 Create test configuration for MCP server testing
- [ ] T050 Write tests for add_task tool functionality and error scenarios
- [ ] T051 Write tests for list_tasks tool functionality and error scenarios
- [ ] T052 Write tests for complete_task tool functionality and error scenarios
- [ ] T053 Write tests for delete_task tool functionality and error scenarios
- [ ] T054 Write tests for update_task tool functionality and error scenarios
- [ ] T055 Write tests for user_id isolation between different users
- [ ] T056 Write integration tests for all MCP tools
- [ ] T057 Validate all success criteria are met (SC-001 through SC-006)

## Phase 8: Polish & Cross-Cutting Concerns

Final implementation details and documentation.

- [x] T058 Add comprehensive docstrings to all tools and functions
- [x] T059 Add type hints to all functions and parameters
- [x] T060 Create server startup script with proper configuration loading
- [x] T061 Add comprehensive error handling and logging to all tools
- [x] T062 Update .env.example with all required environment variables
- [x] T063 Write README with MCP server setup instructions
- [ ] T064 Run all tests and ensure 100% pass rate
- [ ] T065 Verify MCP server can be discovered by OpenAI Agent