# Tasks: OpenAI Agents Chat API for Todo AI Chatbot

**Feature**: OpenAI Agents Chat API for Todo AI Chatbot
**Feature Branch**: 001-openai-agents-chat
**Created**: 2026-01-14
**Status**: Draft
**Author**: Claude Code

## Implementation Strategy

Build the OpenAI Agents Chat API incrementally with a focus on delivering value early. The MVP will include the core chat functionality with minimal MCP tool integration to satisfy User Story 1 (P1). Subsequent phases will enhance the agent's capabilities and add more sophisticated tool usage to fulfill User Stories 2 and 3.

## Dependencies

- User Story 1 (P1) completion is not required for other user stories since they build upon the same core endpoint
- Foundational tasks must be completed before any user story-specific tasks
- Server infrastructure and database connectivity must be established before any chat functionality

## Parallel Execution Examples

- [P] T005-T008 can be executed in parallel (different service implementations)
- [P] T015-T017 can be executed in parallel (different validation functions)
- [P] T025-T027 can be executed in parallel (different test files)

## Phase 1: Setup

Initialize project structure and install dependencies required for the OpenAI Agents Chat API implementation.

- [x] T001 Create backend directory structure per implementation plan
- [ ] T002 Install required dependencies: fastapi, uvicorn, sqlmodel, psycopg2-binary, openai, mcp, pydantic-settings, better-auth-python
- [x] T003 Create requirements.txt with all dependencies
- [x] T004 Create .env.example with environment variables template

## Phase 2: Foundational

Implement foundational components that are required by all user stories.

- [x] T005 Create app/main.py with basic FastAPI structure and imports
- [x] T006 Implement FastAPI app initialization with proper configuration
- [x] T007 Create database connection in app/database/connection.py
- [x] T008 Set up configuration loading in app/config.py
- [x] T009 Update existing models.py to ensure Task, Conversation, Message models are available
- [x] T010 Verify database connection with existing models and connection setup

## Phase 3: User Story 1 - Chat with AI Assistant and Manage Tasks (Priority: P1)

A user sends a natural language message to the AI assistant via the chat API, and the assistant responds appropriately, potentially creating, updating, or managing tasks using MCP tools. The conversation history is preserved between requests.

**Goal**: Implement the core chat endpoint with OpenAI Agents SDK integration and basic MCP tool access.

**Independent Test**: Can be fully tested by sending a message to the POST /api/{user_id}/chat endpoint with a conversation_id and message. The system should return the AI response along with any tool calls executed, and the conversation should persist in the database.

- [x] T011 [P] [US1] Create chat route in app/routes/chat.py with POST /api/{user_id}/chat endpoint
- [x] T012 [US1] Add request/response validation models for chat endpoint
- [x] T013 [US1] Implement database operations to fetch conversation history by conversation_id
- [x] T014 [US1] Add proper error handling for database operations
- [x] T015 [P] [US1] Create validation function for user_id parameter
- [x] T016 [US1] Create validation function for message content length limits
- [x] T017 [US1] Implement user_id filtering and data isolation for conversations
- [ ] T018 [US1] Test chat endpoint with valid parameters and existing conversation
- [ ] T019 [US1] Test error scenarios for chat endpoint (invalid user_id, malformed message)

## Phase 4: User Story 2 - Start New Conversations (Priority: P2)

A user initiates a new conversation by calling the chat API without specifying a conversation_id, and the system creates a new conversation automatically.

**Goal**: Enhance the chat endpoint to automatically create new conversations when conversation_id is not provided.

**Independent Test**: Can be tested by calling the POST /api/{user_id}/chat endpoint without a conversation_id. The system should create a new conversation and return the new conversation_id along with the AI response.

- [x] T020 [P] [US2] Implement conversation creation logic in app/services/conversation.py
- [x] T021 [US2] Add input validation for optional conversation_id parameter
- [x] T022 [US2] Implement database operation to create new Conversation record
- [x] T023 [US2] Format response to include new conversation_id when creating conversation
- [x] T024 [US2] Add proper error handling for conversation creation operations
- [ ] T025 [P] [US2] Create validation function for conversation creation
- [x] T026 [US2] Ensure user_id filtering and data isolation for new conversations
- [ ] T027 [US2] Test chat endpoint with missing conversation_id to create new conversation
- [ ] T028 [US2] Test error scenarios for conversation creation

## Phase 5: User Story 3 - View Tool Invocation Details (Priority: P3)

A user receives detailed information about which MCP tools were invoked during their conversation with the AI assistant.

**Goal**: Enhance the chat response to include detailed information about MCP tools invoked by the AI agent.

**Independent Test**: Can be tested by sending a message that triggers an MCP tool, then verifying that the response includes the tool_calls array with the executed tools.

- [x] T029 [P] [US3] Create agent service in app/services/agent.py with OpenAI Agents SDK integration
- [x] T030 [US3] Add input validation for agent configuration parameters
- [x] T031 [US3] Implement OpenAI agent execution with MCP tools available
- [x] T032 [US3] Ensure tool call results are captured and formatted properly
- [x] T033 [US3] Add proper error handling for agent operations
- [x] T034 [US3] Integrate MCP client to connect to existing MCP server
- [ ] T035 [US3] Test agent service with MCP tools invocation
- [ ] T036 [US3] Test error scenarios when MCP tools fail
- [x] T037 [US3] Format tool call results in response as JSON array

## Phase 6: Service Layer Implementation

Implement service layer components for proper separation of concerns.

- [x] T038 [P] [US1] Create message service in app/services/message.py for message operations
- [x] T039 [P] [US1] Implement user message storage in database
- [x] T040 [P] [US1] Implement assistant response storage in database
- [ ] T041 [US1] Add transaction management for message operations
- [x] T042 [P] [US1] Create MCP client service in app/services/mcp_client.py
- [x] T043 [US1] Implement MCP tool invocation methods
- [x] T044 [US1] Add error handling for MCP client operations
- [x] T045 [US1] Ensure user isolation in MCP client calls

## Phase 7: Validation & Testing

Implement comprehensive testing to validate all functionality.

- [ ] T049 Create test configuration for OpenAI Agents Chat API testing
- [ ] T050 Write tests for chat endpoint functionality and error scenarios
- [ ] T051 Write tests for conversation creation functionality
- [ ] T052 Write tests for agent service and MCP integration
- [ ] T053 Write tests for message storage and retrieval
- [ ] T054 Write tests for user_id isolation between different users
- [ ] T055 Write integration tests for full chat flow
- [ ] T056 Validate all success criteria are met (SC-001 through SC-006)

## Phase 8: Polish & Cross-Cutting Concerns

Final implementation details and documentation.

- [x] T057 Add comprehensive docstrings to all services and functions
- [x] T058 Add type hints to all functions and parameters
- [x] T059 Create server startup script with proper configuration loading
- [x] T060 Add comprehensive error handling and logging to all services
- [x] T061 Update .env.example with all required environment variables
- [x] T062 Write README with API setup instructions
- [ ] T063 Run all tests and ensure 100% pass rate
- [ ] T064 Verify API can be consumed by OpenAI Agent