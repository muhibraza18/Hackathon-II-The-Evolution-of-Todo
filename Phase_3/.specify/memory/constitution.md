<!--
SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
- I. Stateless Architecture: Added scalability and zero hardcoded state details
- II. MCP-First Design: Enhanced with additional requirements
- III. Conversation Persistence: Added additional detail about PostgreSQL
- IV. Natural Language Interface: Added detail about understanding variations
- V. Agentic Development: Expanded with specific constraint details
- VI. Type Safety and Validation: Added additional validation requirements
Added sections:
- VII. Agent Behavior Requirements
- VIII. Architecture Constraints
- Success Criteria
- Deployment Requirements
- Documentation Deliverables
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ updated
- .specify/templates/spec-template.md: ✅ updated
- .specify/templates/tasks-template.md: ✅ updated
- .specify/templates/phr-template.prompt.md: ✅ updated
Follow-up TODOs: None
-->
# Todo AI Chatbot Constitution

## Core Principles

### I. Stateless Architecture
Server holds NO state between requests. Each request is independent and self-contained. All state (tasks, conversations, messages) persists to PostgreSQL database only. Scalability: Horizontal scaling ready (any server handles any request). Zero hardcoded state in server memory.

### II. MCP-First Design
All task operations MUST go through MCP tools. Direct database access from agent is prohibited. Agent chains multiple MCP tools when needed for complex operations. All task operations MUST go through MCP tools. All implementation via Claude Code.

### III. Conversation Persistence
All chat history stored in database. Conversation context maintained across server restarts. Database-first approach for all state management. All state (tasks, conversations, messages) persists to PostgreSQL database only.

### IV. Natural Language Interface
Users interact ONLY through chat (no buttons/forms). Agent interprets natural language commands and converts them to appropriate MCP tool calls. Natural language interface: Users interact ONLY through chat (no buttons/forms). Agent understands natural language variations.

### V. Agentic Development
NO manual coding allowed. All implementation via Claude Code. MCP tools serve as the primary interface for all functionality. NO manual coding allowed (Agentic Dev Stack only). NO in-memory state storage (database persistence only). NO custom UI components (ChatKit standard interface). NO direct database access from agent (MCP tools only). NO HTML forms in React (event handlers only).

### VI. Type Safety and Validation
Type hints on all Python functions. Input validation on all API endpoints. Error handling on all database operations. Type hints on all Python functions. Docstrings for all public functions. Error handling on all database operations. Input validation on all API endpoints. Logging for debugging (not print statements).

### VII. Agent Behavior Requirements
Friendly and conversational tone. Always confirm actions taken. Understand natural language variations. Chain tools when needed (e.g., find task by name, then delete). Handle ambiguity by asking clarifying questions.

### VIII. Architecture Constraints
Stateless server: Each request is independent and self-contained. Database-first: All state (tasks, conversations, messages) persists to PostgreSQL. Tool composition: Agent can chain multiple MCP tools in single turn. Error handling: Graceful failures with user-friendly messages. Scalability: Horizontal scaling ready (any server handles any request).

## Additional Constraints

### Technology Stack
- Backend framework: Python FastAPI exclusively
- AI framework: OpenAI Agents SDK for all AI logic
- MCP implementation: Official MCP SDK (Python) for tool definitions
- Database ORM: SQLModel for all database operations
- Database: Neon Serverless PostgreSQL only
- Authentication: Better Auth integration required
- Frontend: OpenAI ChatKit (no custom UI components)
- API design: Single endpoint pattern (POST /api/{user_id}/chat)
- Technology versions: Python 3.11+, Latest stable FastAPI, Latest OpenAI Agents SDK, Official Python MCP SDK, Latest stable SQLModel, Neon Serverless PostgreSQL compatible

### Database Models
Three required tables:
1. Task - user_id, id, title, description, completed, created_at, updated_at
2. Conversation - user_id, id, created_at, updated_at
3. Message - user_id, id, conversation_id, role, content, created_at

### MCP Tools (Five Mandatory Tools)
1. add_task - Create new tasks
2. list_tasks - Retrieve tasks (all/pending/completed)
3. complete_task - Mark tasks as done
4. delete_task - Remove tasks
5. update_task - Modify task details

### Error Handling
Graceful failures with user-friendly messages. Comprehensive error handling on all database operations and API endpoints.

## Development Workflow

### Implementation Process
1. Write specification using Spec-Kit Plus
2. Generate implementation plan
3. Break into atomic tasks
4. Execute via Claude Code
5. Iterate based on testing

### Testing Approach
- Test each MCP tool independently
- Test conversation flow end-to-end
- Test stateless behavior (restart server mid-conversation)
- Test error scenarios (invalid task IDs, etc.)
- Test natural language variations

### Code Quality Standards
- Type hints on all Python functions
- Docstrings for all public functions
- Error handling on all database operations
- Input validation on all API endpoints
- Logging for debugging (not print statements)

## Success Criteria

- All CRUD operations work through natural language
- Conversation context maintained across server restarts
- Zero hardcoded state in server memory
- All 5 MCP tools functional and tested
- ChatKit UI successfully connects to backend
- Database persists all conversations and tasks
- Agent correctly interprets natural language commands
- Errors handled gracefully with helpful messages

## Deployment Requirements

- Backend: Python server deployed (Render/Railway/similar)
- Frontend: Vercel/GitHub Pages with domain allowlist configured
- Database: Neon PostgreSQL cloud instance
- Environment variables: Secure storage for API keys
- OpenAI domain allowlist: Frontend URL registered

## Documentation Deliverables

- README with setup instructions
- Database migration scripts
- Environment variables template
- API endpoint documentation
- MCP tools specification
- Agent behavior specification

## Governance

Constitution governs all development decisions for the Todo AI Chatbot project. All implementations must comply with stateless architecture, MCP-first design, and database persistence requirements. Any deviation from these principles requires constitutional amendment with proper justification.

**Version**: 1.1.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-13