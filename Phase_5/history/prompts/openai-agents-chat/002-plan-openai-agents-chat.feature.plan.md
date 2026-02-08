---
id: 002
title: "Plan OpenAI Agents Chat"
stage: "plan"
date: "2026-01-14"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "openai-agents-chat"
branch: "001-openai-agents-chat"
user: "MuhibRaza"
command: "sp.plan"
labels: ["openai", "agents", "chat", "api", "todo-chatbot"]
links:
  spec: "specs/001-openai-agents-chat/spec.md"
  plan: "specs/001-openai-agents-chat/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-openai-agents-chat/plan.md"
  - "specs/001-openai-agents-chat/research.md"
  - "specs/001-openai-agents-chat/data-model.md"
  - "specs/001-openai-agents-chat/quickstart.md"
  - "specs/001-openai-agents-chat/contracts/chat-api.yaml"
tests:
  - "Architecture design validation"
  - "Technology stack validation"
  - "Database model validation"
---

## Prompt

Create:
- API architecture diagram showing FastAPI → OpenAI Agents SDK → MCP Server → Database flow
- Module structure (routes, services, database, agent configuration)
- Database interaction patterns for stateless operation
- Error handling and logging approach
- Development and testing workflow

Decisions needing documentation:
1. **Conversation History Management**
   - Option A: Load full conversation history every request (simple, potentially slow)
   - Option B: Load last N messages + summarization (complex, faster)
   - Option C: Load last N messages only (simple, loses context)
   - Tradeoff: Simplicity vs. performance vs. context retention
   - Recommendation needed: Balance for Phase III scope

2. **OpenAI Agents SDK Integration Pattern**
   - Option A: Initialize agent on every request (stateless, slower)
   - Option B: Singleton agent instance (stateful, faster but breaks architecture)
   - Option C: Agent pool with connection reuse (complex, optimal)
   - Tradeoff: Architecture purity vs. performance vs. complexity
   - Recommendation needed: Best fit for stateless requirement

3. **MCP Tool Error Handling**
   - Option A: Return errors directly to user (transparent, technical)
   - Option B: Agent interprets errors and responds naturally (user-friendly, complex)
   - Option C: Hybrid - show error codes + friendly message (balanced)
   - Tradeoff: User experience vs. debugging ease vs. implementation effort
   - Recommendation needed: Error UX strategy

4. **Database Transaction Scope**
   - Option A: Single transaction for entire request (atomic, risk of rollback)
   - Option B: Separate transactions for user message storage and assistant response (flexible, partial saves)
   - Option C: No explicit transactions (simple, potential inconsistency)
   - Tradeoff: Data consistency vs. error recovery vs. simplicity
   - Recommendation needed: Transaction boundary strategy

5. **Tool Call Result Storage**
   - Option A: Store tool_calls array in message content as JSON (simple, searchable)
   - Option B: Separate ToolCall table with relationships (normalized, complex)
   - Option C: Don't store, only return in response (stateless, no audit trail)
   - Tradeoff: Data normalization vs. query complexity vs. auditability
   - Recommendation needed: Tool call persistence approach

Testing strategy:
- **Unit tests**: Database models, MCP tool invocation, message storage/retrieval
- **Integration tests**: Full chat flow with mock OpenAI responses, conversation persistence across requests
- **Statelessness validation**: Server restart mid-conversation, multiple concurrent requests
- **Error scenario tests**: MCP tool failures, database unavailability, malformed requests
- **Acceptance criteria validation**:
  ✓ Single endpoint handles all interactions
  ✓ Conversation resumes after server restart
  ✓ No in-memory state between requests
  ✓ Response includes conversation_id, response text, and tool_calls
  ✓ Database correctly stores user and assistant messages

Technical details:
- **Development approach**: Iterative implementation
  1. Basic FastAPI skeleton with health check
  2. Database connection and SQLModel setup
  3. Message storage endpoints (without AI)
  4. OpenAI Agents SDK integration (without MCP)
  5. MCP tool integration
  6. Full stateless chat flow
  7. Error handling and validation

- **File structure**:
backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── routes/
│   │   └── chat.py          # POST /api/{user_id}/chat
│   ├── services/
│   │   ├── agent.py         # OpenAI Agents SDK wrapper
│   │   ├── conversation.py  # Conversation history management
│   │   └── mcp_client.py    # MCP server client
│   ├── database/
│   │   ├── models.py        # SQLModel definitions (from Step 2)
│   │   └── connection.py    # Neon DB connection
│   └── config.py            # Environment variables
├── tests/
├── requirements.txt
└── README.md

- **Dependencies to specify**:
  - fastapi
  - uvicorn
  - sqlmodel
  - psycopg2-binary (Neon PostgreSQL)
  - openai (OpenAI Agents SDK)
  - mcp (Official MCP SDK client)
  - pydantic-settings (environment config)
  - better-auth-python (from Step 6)

- **Environment variables needed**:
  - DATABASE_URL (Neon PostgreSQL connection string)
  - OPENAI_API_KEY
  - MCP_SERVER_URL (local MCP server endpoint)
  - BETTER_AUTH_SECRET (from Step 6)

- **Stateless implementation checklist**:
  □ No global variables holding conversation state
  □ No in-memory caching of messages
  □ Agent initialized per-request or from stateless pool
  □ All state loaded from database on every request
  □ Response contains everything frontend needs (no session reliance)

## Response snapshot

Completed comprehensive planning for the OpenAI Agents Chat API implementation:

1. **Created implementation plan** (plan.md) with:
   - Technical context and constitution check
   - Project structure following backend API service pattern
   - Compliance with stateless architecture requirements

2. **Resolved all key decisions** (research.md):
   - Conversation history: Load full history every request (Option A)
   - Agent integration: Initialize on every request (Option A)
   - Error handling: Agent interprets errors naturally (Option B)
   - Transactions: Single transaction for entire request (Option A)
   - Tool calls: Store as JSON in message content (Option A)

3. **Defined data model** (data-model.md) with:
   - Conversation entity for grouping messages
   - Message entity for user/assistant exchanges
   - Tool call representation within messages
   - Proper relationships and validation

4. **Created quickstart guide** (quickstart.md) with:
   - Setup and installation instructions
   - Environment configuration
   - API testing examples
   - Troubleshooting tips

5. **Created API contract** (contracts/chat-api.yaml) with:
   - OpenAPI specification for the chat endpoint
   - Request/response schemas
   - Error handling definitions

All deliverables created following the constitution requirements for stateless architecture, MCP-first design, and database persistence. The plan aligns with the feature specification and sets up the proper architecture for the iterative development approach.

## Outcome

- ✅ Impact: Complete planning for OpenAI Agents Chat API with resolved technical decisions
- 🧪 Tests: Architecture and data model validated against requirements
- 📁 Files: Created all planning artifacts in proper directory structure
- 🔁 Next prompts: Ready for task breakdown phase (`/sp.tasks`)
- 🧠 Reflection: Planning addresses all key decisions while maintaining stateless architecture

## Evaluation notes (flywheel)

- Failure modes observed: None - all decisions justified with alternatives considered
- Graders run and results (PASS/FAIL): PASS - all planning requirements met
- Prompt variant (if applicable): Standard planning following template guidelines
- Next experiment (smallest change to try): Proceed to task breakdown to implement the design