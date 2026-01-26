---
id: 002
title: "Plan DB Schema"
stage: "plan"
date: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "db-schema-todo-chatbot"
branch: "001-db-schema-todo-chatbot"
user: "Wajahat traders"
command: "sp.plan"
labels: ["database", "schema", "sqlmodel", "todo-chatbot", "planning"]
links:
  spec: "specs/001-db-schema-todo-chatbot/spec.md"
  plan: "specs/001-db-schema-todo-chatbot/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-db-schema-todo-chatbot/plan.md"
  - "specs/001-db-schema-todo-chatbot/research.md"
  - "specs/001-db-schema-todo-chatbot/data-model.md"
  - "specs/001-db-schema-todo-chatbot/quickstart.md"
  - "specs/001-db-schema-todo-chatbot/contracts/openapi.yaml"
tests:
  - "Research completion"
  - "Data model validation"
  - "API contract validation"
---

# Database Schema Implementation Plan for Todo AI Chatbot

## Original Prompt

```
Database Schema Implementation

Create:
- Database architecture diagram showing 3 tables with relationships
- SQLModel file structure (models.py, database.py, migrations/)
- Connection setup for Neon PostgreSQL with async support
- CRUD helper functions for each model
- Testing queries to validate schema works

Implementation approach:
1. Setup phase:
   - Install SQLModel, psycopg2-binary, alembic
   - Configure Neon PostgreSQL connection string
   - Create database.py with engine and session setup
   - Test connection to Neon database

2. Models phase:
   - Define Task model with all fields and constraints
   - Define Conversation model with timestamps
   - Define Message model with foreign key to Conversation
   - Add __repr__ methods for debugging
   - Add JSON serialization methods

3. Relationships phase:
   - Configure Message → Conversation foreign key
   - Setup cascade delete for conversations
   - Add relationship attributes (conversation.messages)
   - Test relationship queries

4. Migration phase:
   - Initialize Alembic (or use SQLModel.metadata.create_all)
   - Generate initial migration
   - Apply migration to Neon database
   - Verify tables created correctly

5. Validation phase:
   - Test creating records in each table
   - Test foreign key constraints work
   - Test cascade deletes
   - Test user_id filtering
   - Test timestamp auto-population

Decisions needing documentation:

1. Migration tool choice:
   Options: (a) Alembic (industry standard), (b) SQLModel.metadata.create_all (simpler)
   Tradeoffs: Alembic = version control but more setup; create_all = fast but no migration history
   Recommendation: Start with create_all, add Alembic if needed

2. Async vs Sync database operations:
   Options: (a) Async (asyncio/asyncpg), (b) Sync (psycopg2)
   Tradeoffs: Async = better performance but more complex; Sync = simpler, easier debugging
   Recommendation: Async for FastAPI compatibility

3. Session management pattern:
   Options: (a) Dependency injection, (b) Context manager, (c) Global session
   Tradeoffs: DI = cleanest but verbose; Context = simple; Global = anti-pattern
   Recommendation: Dependency injection for FastAPI best practices

4. user_id data type:
   Options: (a) String (flexible for various auth), (b) UUID, (c) Integer
   Tradeoffs: String = works with any auth provider; UUID = unique but complex; Integer = simple but limiting
   Recommendation: String to support Better Auth flexibility

5. Timestamp timezone handling:
   Options: (a) UTC everywhere, (b) User timezone, (c) Database default
   Tradeoffs: UTC = consistent, simple; User TZ = complex conversions; DB default = inconsistent
   Recommendation: UTC timestamps, convert in frontend if needed

Testing strategy:

Validation checks based on acceptance criteria:

1. Model creation tests:
   - ✓ Task created with required fields (user_id, title)
   - ✓ Task created without optional description
   - ✗ Task creation fails without user_id
   - ✗ Task creation fails without title
   - ✓ Conversation created successfully
   - ✓ Message created with valid conversation_id
   - ✗ Message creation fails with invalid conversation_id

2. Relationship tests:
   - ✓ Message.conversation returns correct Conversation object
   - ✓ Conversation.messages returns all associated messages
   - ✓ Deleting conversation deletes all messages (cascade)
   - ✓ Deleting task doesn't affect conversations

3. Timestamp tests:
   - ✓ created_at auto-populates on creation
   - ✓ updated_at auto-updates on modification
   - ✓ Timestamps are UTC
   - ✓ Timestamps are datetime objects

4. Query performance tests:
   - ✓ user_id filtering works on all models
   - ✓ Conversation lookup by ID is fast
   - ✓ Message ordering by created_at works
   - ✓ Task filtering by completed status works

5. Data integrity tests:
   - ✓ Cannot create duplicate task IDs
   - ✓ user_id isolation (user A can't see user B's data)
   - ✓ Role enum only accepts "user" or "assistant"
   - ✓ Foreign keys enforced properly
Technical details:

File structure:
backend/
├── models.py           # SQLModel table definitions
├── database.py         # Connection, engine, session setup
├── crud.py            # CRUD helper functions
├── schemas.py         # Pydantic response schemas
└── migrations/        # Alembic migrations (if using)
└── versions/

Database connection pattern:
- Use async engine for FastAPI compatibility
- Connection pooling via Neon's pooler
- Environment variable for DATABASE_URL
- Graceful connection error handling

SQLModel patterns to follow:
- Use table=True for database models
- Use Optional[] for nullable fields
- Use Field() for constraints and defaults
- Inherit from SQLModel base class
- Separate read/write schemas if needed

Dependencies to install:
- sqlmodel
- psycopg2-binary (or asyncpg for async)
- alembic (optional)
- python-dotenv (for env vars)

Quality validation:
- All models have type hints
- All fields documented with comments
- CRUD operations don't raise unhandled exceptions
- Database connection handles network errors
- Models serialize to JSON correctly
- Foreign keys prevent orphaned records

Risk mitigation:
- Test Neon connection before building models
- Validate schema with sample data before MCP integration
- Keep models simple (no premature optimization)
- Document any Neon-specific configurations
```

## Response Summary

Created a comprehensive implementation plan for the Todo AI Chatbot database schema, including:

- **Research phase**: Completed research on key decisions including migration tool (SQLModel.metadata.create_all), async operations (using asyncpg), session management (dependency injection), and Neon PostgreSQL configuration
- **Data model**: Defined complete specifications for Task, Conversation, and Message entities with proper fields, relationships, and constraints
- **API contracts**: Created OpenAPI specification for database operations
- **Quickstart guide**: Provided detailed setup and usage instructions
- **Constitution compliance**: Verified all requirements from the project constitution are met

## Outcome

The implementation plan is complete with all research, design, and architecture decisions documented. The plan includes:
- Complete data model specification with relationships and constraints
- API contracts defined in OpenAPI format
- Technical decisions made on migration strategy, async operations, and session management
- Constitutional compliance verified
- Ready for the implementation phase