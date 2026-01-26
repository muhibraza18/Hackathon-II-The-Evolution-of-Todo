---
id: 001
title: "Specify DB Schema"
stage: "spec"
date: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "db-schema-todo-chatbot"
branch: "001-db-schema-todo-chatbot"
user: "Wajahat traders"
command: "sp.specify"
labels: ["database", "schema", "sqlmodel", "todo-chatbot"]
links:
  spec: "specs/001-db-schema-todo-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-db-schema-todo-chatbot/spec.md"
  - "specs/001-db-schema-todo-chatbot/checklists/requirements.md"
tests:
  - "Specification completeness"
  - "Requirements validation"
---

# Database Schema Specification for Todo AI Chatbot

## Original Prompt

```
Database Schema for Todo AI Chatbot

Target audience: Claude Code implementing SQLModel database models
Focus: PostgreSQL schema design for tasks, conversations, and messages with proper relationships

Success criteria:
- All 3 required models defined (Task, Conversation, Message)
- Foreign key relationships correctly established
- Timestamps auto-populate (created_at, updated_at)
- user_id present in all models for multi-user support
- SQLModel models work with Neon Serverless PostgreSQL
- Migration scripts generate valid PostgreSQL tables
Database models to build:

1. Task Model
   Fields: user_id (string), id (int, primary key), title (string, required), description (string, optional), completed (boolean, default false), created_at (datetime, auto), updated_at (datetime, auto)
   Indexes: user_id, completed status
   Constraints: title cannot be empty, user_id required

2. Conversation Model
   Fields: user_id (string), id (int, primary key), created_at (datetime, auto), updated_at (datetime, auto)
   Indexes: user_id
   Constraints: user_id required
3. Message Model
   Fields: user_id (string), id (int, primary key), conversation_id (int, foreign key to Conversation), role (enum: "user" or "assistant"), content (text, required), created_at (datetime, auto)
   Indexes: conversation_id, created_at
   Constraints: conversation_id must exist, role must be user or assistant, content cannot be empty

Relationships:
- Message.conversation_id → Conversation.id (many-to-one)
- Cascade delete: Deleting conversation deletes all its messages
- All models filter by user_id for data isolation
Technical requirements:
- Use SQLModel (combines SQLAlchemy + Pydantic)
- Auto-increment primary keys
- UTC timestamps for all datetime fields
- Proper nullable vs required fields
- Type hints on all fields
- Support for Neon PostgreSQL connection string

Constraints:
- No sensitive data stored in plain text
- user_id format: string (supports various auth providers)
- Maximum title length: 200 characters
- Maximum description length: 1000 characters
- Message content: unlimited text length
- All IDs are integers (auto-increment)

Not building:
- User authentication table (handled by Better Auth separately)
- Task tags or categories (Basic Level scope)
- Task priorities or due dates (Basic Level scope)
- File attachments or rich media
- Soft deletes (hard deletes only)
- Task sharing between users
- Archived conversations

Deliverables:
- SQLModel model definitions in models.py
- Database initialization script (create_tables)
- Alembic migration files (or equivalent)
- database.py with Neon PostgreSQL connection setup
- Type definitions for all models
- Example queries for each CRUD operation

Migration strategy:
- Initial migration creates all 3 tables
- Foreign key constraints enforced
- Indexes created for query performance
- Works with Neon's serverless pooling

Testing validation:
- Can create task without description
- Cannot create task without title or user_id
- Messages link correctly to conversations
- Deleting conversation removes all messages
- Timestamps populate automatically
- user_id filtering works across all models
```

## Response Summary

Created a comprehensive specification for the database schema of the Todo AI Chatbot, defining all three required models (Task, Conversation, Message) with their proper fields, relationships, and constraints. The specification includes:

- Detailed functional requirements for all three models
- Proper foreign key relationships with cascade delete behavior
- User data isolation through user_id fields
- Automatic timestamp population requirements
- Indexing requirements for performance
- Field constraints and validation rules
- User scenarios covering the core functionality
- Success criteria that are measurable and technology-agnostic

## Outcome

The specification is complete and ready for the planning phase. It captures all requirements from the user input while maintaining a focus on user value and business needs without implementation details leaking into the specification. The spec includes proper acceptance scenarios, edge cases, and measurable success criteria.