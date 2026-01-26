---
id: 001
title: "Amend Constitution"
stage: "constitution"
date: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "Wajahat traders"
command: "sp.constitution"
labels: ["constitution", "todo-ai-chatbot", "spec-driven-development"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests:
  - "Constitution validation"
  - "Template consistency check"
---

# Amendment to Todo AI Chatbot Constitution

## Original Prompt

```
Project: Todo AI Chatbot - AI-powered task management through natural language

Core principles:
- Stateless architecture: Server holds NO state between requests
- MCP-first design: All task operations MUST go through MCP tools
- Conversation persistence: All chat history stored in database
- Natural language interface: Users interact ONLY through chat (no buttons/forms)
- Agentic development: NO manual coding - all implementation via Claude Code

Key standards:
- Backend framework: Python FastAPI exclusively
- AI framework: OpenAI Agents SDK for all AI logic
- MCP implementation: Official MCP SDK (Python) for tool definitions
- Database ORM: SQLModel for all database operations
- Database: Neon Serverless PostgreSQL only
- Authentication: Better Auth integration required
- Frontend: OpenAI ChatKit (no custom UI components)
- API design: Single endpoint pattern (POST /api/{user_id}/chat)

Architecture constraints:
- Stateless server: Each request is independent and self-contained
- Database-first: All state (tasks, conversations, messages) persists to PostgreSQL
- Tool composition: Agent can chain multiple MCP tools in single turn
- Error handling: Graceful failures with user-friendly messages
- Scalability: Horizontal scaling ready (any server handles any request)

MCP Tools (mandatory 5 tools):
1. add_task - Create new tasks
2. list_tasks - Retrieve tasks (all/pending/completed)
3. complete_task - Mark tasks as done
4. delete_task - Remove tasks
5. update_task - Modify task details

Database models (required 3 tables):
1. Task - user_id, id, title, description, completed, created_at, updated_at
2. Conversation - user_id, id, created_at, updated_at
3. Message - user_id, id, conversation_id, role, content, created_at

Agent behavior requirements:
- Friendly and conversational tone
- Always confirm actions taken
- Understand natural language variations
- Chain tools when needed (e.g., find task by name, then delete)
- Handle ambiguity by asking clarifying questions

Development workflow:
1. Write specification using Spec-Kit Plus
2. Generate implementation plan
3. Break into atomic tasks
4. Execute via Claude Code
5. Iterate based on testing

Success criteria:
- All CRUD operations work through natural language
- Conversation context maintained across server restarts
- Zero hardcoded state in server memory
- All 5 MCP tools functional and tested
- ChatKit UI successfully connects to backend
- Database persists all conversations and tasks
- Agent correctly interprets natural language commands
- Errors handled gracefully with helpful messages

Constraints:
- NO manual coding allowed (Agentic Dev Stack only)
- NO in-memory state storage (database persistence only)
- NO custom UI components (ChatKit standard interface)
- NO direct database access from agent (MCP tools only)
- NO HTML forms in React (event handlers only)

Technology versions:
- Python: 3.11+
- FastAPI: Latest stable
- OpenAI Agents SDK: Latest
- MCP SDK: Official Python implementation
- SQLModel: Latest stable
- PostgreSQL: Neon Serverless compatible

Deployment requirements:
- Backend: Python server deployed (Render/Railway/similar)
- Frontend: Vercel/GitHub Pages with domain allowlist configured
- Database: Neon PostgreSQL cloud instance
- Environment variables: Secure storage for API keys
- OpenAI domain allowlist: Frontend URL registered

Code quality standards:
- Type hints on all Python functions
- Docstrings for all public functions
- Error handling on all database operations
- Input validation on all API endpoints
- Logging for debugging (not print statements)

Testing approach:
- Test each MCP tool independently
- Test conversation flow end-to-end
- Test stateless behavior (restart server mid-conversation)
- Test error scenarios (invalid task IDs, etc.)
- Test natural language variations

Documentation deliverables:
- README with setup instructions
- Database migration scripts
- Environment variables template
- API endpoint documentation
- MCP tools specification
- Agent behavior specification
```

## Response Summary

Updated the Todo AI Chatbot Constitution to version 1.1.0 with comprehensive coverage of all requirements from the user input. The updated constitution now includes:

- Enhanced core principles with additional details
- New sections for Agent Behavior Requirements and Architecture Constraints
- Success Criteria, Deployment Requirements, and Documentation Deliverables sections
- Sync Impact Report documenting all changes
- Proper versioning and governance information

## Outcome

The constitution now fully captures all specified requirements and serves as a complete governing document for the Todo AI Chatbot project development.