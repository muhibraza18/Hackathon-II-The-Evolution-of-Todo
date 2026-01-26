# Feature Specification: OpenAI Agents Chat API for Todo AI Chatbot

**Feature Branch**: `001-openai-agents-chat`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "FastAPI Backend with OpenAI Agents SDK integration for Todo AI Chatbot
Target audience: Backend developers implementing stateless chat API with MCP tool integration
Focus: Chat endpoint implementation, database persistence, and OpenAI Agents SDK integration
Success criteria:
- Single stateless POST endpoint handles all chat interactions
- Conversation history persists to Neon PostgreSQL between requests
- OpenAI Agents SDK successfully invokes MCP tools for task operations
- Server can restart without losing conversation context
- Response includes conversation_id, AI response, and tool_calls executed

Constraints:
- Technology: Python FastAPI, OpenAI Agents SDK, SQLModel ORM, Neon PostgreSQL
- Architecture: Completely stateless (no in-memory state between requests)
- Endpoint: POST /api/{user_id}/chat
- Database models: Must use Task, Conversation, Message models from Step 2
- MCP integration: Must use all 5 tools from Step 3 (add_task, list_tasks, complete_task, delete_task, update_task)
- Authentication: Better Auth integration (from Step 6)
- Error handling: Graceful failures with user-friendly messages

Request format:
{
  \"conversation_id\": integer (optional - creates new if absent),
  \"message\": string (required - user's natural language input)
}

Response format:
{
  \"conversation_id\": integer,
  \"response\": string (AI assistant's reply),
  \"tool_calls\": array (list of MCP tools invoked)
}

Flow requirements:
1. Receive user message via POST request
2. Fetch conversation history from database using conversation_id
3. Build message array for OpenAI agent (history + new message)
4. Store user message in database immediately
5. Execute OpenAI agent with MCP tools available
6. Agent invokes appropriate MCP tool(s) based on user intent
7. Store assistant response in database
8. Return response to client
9. Server maintains zero state (ready for next independent request)

Not building:
- WebSocket/streaming responses (REST only for this phase)
- Rate limiting or request throttling
- Multi-user conversation support (each user has separate conversations)
- Message editing or deletion functionality
- Custom authentication (using Better Auth from Step 6)
- MCP server implementation (already defined in Step 3)
- Frontend (defined in Step 7)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chat with AI Assistant and Manage Tasks (Priority: P1)

A user sends a natural language message to the AI assistant via the chat API, and the assistant responds appropriately, potentially creating, updating, or managing tasks using MCP tools. The conversation history is preserved between requests.

**Why this priority**: This is the core functionality that enables the entire chatbot experience, allowing users to interact naturally with their task management system.

**Independent Test**: Can be fully tested by sending a message to the POST /api/{user_id}/chat endpoint with a conversation_id and message. The system should return the AI response along with any tool calls executed, and the conversation should persist in the database.

**Acceptance Scenarios**:

1. **Given** a user has an existing conversation with history, **When** they send a new message to the chat endpoint, **Then** the AI assistant responds appropriately and the conversation history is maintained.
2. **Given** a user sends a message requesting to create a new task, **When** they call the chat endpoint, **Then** the assistant invokes the add_task MCP tool and returns the response.
3. **Given** a user sends a message requesting to view their tasks, **When** they call the chat endpoint, **Then** the assistant invokes the list_tasks MCP tool and returns the response.

---

### User Story 2 - Start New Conversations (Priority: P2)

A user initiates a new conversation by calling the chat API without specifying a conversation_id, and the system creates a new conversation automatically.

**Why this priority**: Essential for new user experiences and for users who want to start fresh conversations.

**Independent Test**: Can be tested by calling the POST /api/{user_id}/chat endpoint without a conversation_id. The system should create a new conversation and return the new conversation_id along with the AI response.

**Acceptance Scenarios**:

1. **Given** a user has no existing conversation, **When** they call the chat endpoint without a conversation_id, **Then** a new conversation is created and returned with a new conversation_id.

---

### User Story 3 - View Tool Invocation Details (Priority: P3)

A user receives detailed information about which MCP tools were invoked during their conversation with the AI assistant.

**Why this priority**: Helps users understand what actions the AI took on their behalf, improving transparency and trust.

**Independent Test**: Can be tested by sending a message that triggers an MCP tool, then verifying that the response includes the tool_calls array with the executed tools.

**Acceptance Scenarios**:

1. **Given** a user sends a message that requires a task operation, **When** they call the chat endpoint, **Then** the response includes the tool_calls array showing which MCP tools were invoked.

---

### Edge Cases

- What happens when the database is temporarily unavailable during a chat request?
- How does the system handle malformed JSON requests?
- What happens when an MCP tool fails during execution?
- How does the system handle very long messages that exceed reasonable limits?
- What happens when a user tries to access a conversation that doesn't belong to them?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a stateless POST endpoint at /api/{user_id}/chat that accepts user messages
- **FR-002**: System MUST persist conversation history to Neon PostgreSQL database between requests
- **FR-003**: System MUST fetch existing conversation history before processing new messages
- **FR-004**: System MUST store user messages in the database immediately upon receipt
- **FR-005**: System MUST execute OpenAI Agents SDK with MCP tools available for task operations
- **FR-006**: System MUST store assistant responses in the database after processing
- **FR-007**: System MUST return conversation_id, AI response, and tool_calls executed in the response
- **FR-008**: System MUST support all 5 MCP tools from Step 3 (add_task, list_tasks, complete_task, delete_task, update_task)
- **FR-009**: System MUST maintain zero in-memory state between requests
- **FR-010**: System MUST allow creating new conversations when conversation_id is not provided
- **FR-011**: System MUST validate request format and return appropriate error messages
- **FR-012**: System MUST ensure user data isolation (users can only access their own conversations)

### Key Entities *(include if feature involves data)*

- **Conversation**: Represents a logical grouping of messages between a user and the AI assistant, identified by conversation_id
- **Message**: Represents individual exchanges within a conversation, with role (user or assistant) and content
- **Tool Call**: Represents invocations of MCP tools made by the AI assistant during conversation processing

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can send messages to the AI assistant and receive responses within 5 seconds under normal load
- **SC-002**: Conversation history persists correctly between requests and survives server restarts
- **SC-003**: OpenAI Agents SDK successfully invokes MCP tools when appropriate based on user intent
- **SC-004**: System maintains stateless architecture with no in-memory conversation data between requests
- **SC-005**: All conversation data is properly isolated by user_id preventing cross-user access
- **SC-006**: API responses consistently include conversation_id, AI response, and tool_calls when applicable