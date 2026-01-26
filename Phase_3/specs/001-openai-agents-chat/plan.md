# Implementation Plan: OpenAI Agents Chat API for Todo AI Chatbot

**Branch**: `001-openai-agents-chat` | **Date**: 2026-01-14 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless FastAPI endpoint that integrates with OpenAI Agents SDK to process natural language chat messages and invoke MCP tools for task management operations. The system maintains conversation history in Neon PostgreSQL database while adhering to stateless architecture principles.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, SQLModel, Neon PostgreSQL, Official MCP SDK
**Storage**: Neon PostgreSQL database with existing Task, Conversation, Message models
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (deployment-ready)
**Project Type**: Backend API service
**Performance Goals**: Responses within 5 seconds under normal load
**Constraints**: <200ms p95 for database operations, stateless operation, horizontal scaling ready
**Scale/Scope**: Support for multiple concurrent users with user data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Stateless Architecture: All state persists to PostgreSQL, no in-memory conversation data
- ✅ MCP-First Design: All task operations will go through MCP tools (add_task, list_tasks, etc.)
- ✅ Conversation Persistence: All chat history stored in database with Conversation/Message models
- ✅ Natural Language Interface: OpenAI Agents will interpret natural language and call MCP tools
- ✅ Agentic Development: Implementation via Claude Code only, no manual coding
- ✅ Type Safety and Validation: Type hints on all functions, input validation on endpoints

## Project Structure

### Documentation (this feature)

```text
specs/001-openai-agents-chat/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
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
```

**Structure Decision**: Backend API service following the provided architecture with clear separation of concerns between routes, services, and database layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None identified] | [N/A] | [N/A] |