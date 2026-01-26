# Feature Specification: Database Schema for Todo AI Chatbot

**Feature Branch**: `001-db-schema-todo-chatbot`
**Created**: 2026-01-13
**Status**: Draft
**Input**: User description: "Database Schema for Todo AI Chatbot

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
- user_id filtering works across all models"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Store and Retrieve User Tasks (Priority: P1)

As a user of the Todo AI Chatbot, I want to create, view, update, and delete my tasks so that I can manage my to-do list effectively through natural language interactions.

**Why this priority**: This is the core functionality of a todo chatbot - users need to be able to manage their tasks for the system to provide value.

**Independent Test**: Can be fully tested by creating tasks for a user, retrieving them, updating their status, and deleting them. Delivers core task management functionality.

**Acceptance Scenarios**:

1. **Given** a user has no tasks, **When** they ask to add a new task, **Then** the system creates a new task record with the specified title and stores it with their user_id
2. **Given** a user has completed tasks, **When** they ask to see pending tasks, **Then** the system returns only tasks with completed status set to false for that user_id

---

### User Story 2 - Maintain Conversation Context (Priority: P2)

As a user of the Todo AI Chatbot, I want to have conversations with the AI assistant that maintain context so that I can have natural, multi-turn interactions about my tasks.

**Why this priority**: Conversational context is essential for a chatbot to feel intelligent and responsive to user needs.

**Independent Test**: Can be fully tested by creating conversations and exchanging messages within them. Delivers conversational continuity.

**Acceptance Scenarios**:

1. **Given** a user starts a new conversation, **When** they send multiple messages in sequence, **Then** all messages are associated with the same conversation and stored chronologically
2. **Given** a user has multiple conversations, **When** they ask to see conversation history, **Then** the system returns only conversations belonging to that user_id

---

### User Story 3 - Track Message History (Priority: P3)

As a user of the Todo AI Chatbot, I want my messages and the AI's responses to be stored so that I can reference past interactions and maintain context across sessions.

**Why this priority**: Message history enables users to revisit conversations and provides audit trails for the AI's recommendations and actions.

**Independent Test**: Can be fully tested by sending messages between user and assistant and verifying they're stored correctly with proper roles and timestamps.

**Acceptance Scenarios**:

1. **Given** a conversation exists, **When** a user sends a message, **Then** the system stores the message with role='user', proper content, and timestamp
2. **Given** a conversation exists, **When** the assistant responds, **Then** the system stores the message with role='assistant', proper content, and timestamp

---

### Edge Cases

- What happens when a conversation is deleted - all related messages should be removed due to cascade delete?
- How does the system handle very long message content that exceeds typical length constraints?
- What occurs when a user tries to create a task with an extremely long title (over 200 characters)?
- How does the system handle rapid-fire message creation that could cause timestamp collisions?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST define a Task model with user_id (string), id (int primary key), title (string, required), description (string, optional), completed (boolean, default false), created_at (datetime, auto-populate), updated_at (datetime, auto-populate)
- **FR-002**: System MUST define a Conversation model with user_id (string), id (int primary key), created_at (datetime, auto-populate), updated_at (datetime, auto-populate)
- **FR-003**: System MUST define a Message model with user_id (string), id (int primary key), conversation_id (int foreign key to Conversation), role (enum: "user" or "assistant"), content (text, required), created_at (datetime, auto-populate)
- **FR-004**: System MUST enforce foreign key relationship: Message.conversation_id → Conversation.id with cascade delete behavior
- **FR-005**: System MUST ensure all models include user_id field for data isolation between users
- **FR-006**: System MUST automatically populate created_at and updated_at timestamps for all records
- **FR-007**: System MUST create indexes on user_id field for all three models to support efficient user-based queries
- **FR-008**: System MUST create index on Task.completed field to support efficient filtering of completed/incomplete tasks
- **FR-009**: System MUST create indexes on Message.conversation_id and created_at fields for efficient conversation retrieval and chronological ordering
- **FR-010**: System MUST enforce that Task.title cannot be empty (not null and length > 0)
- **FR-011**: System MUST enforce that Task.user_id cannot be empty (not null)
- **FR-012**: System MUST enforce that Message.conversation_id must reference an existing Conversation
- **FR-013**: System MUST enforce that Message.role must be either "user" or "assistant"
- **FR-014**: System MUST enforce that Message.content cannot be empty (not null and length > 0)
- **FR-015**: System MUST implement proper length constraints: Task.title ≤ 200 characters, Task.description ≤ 1000 characters
- **FR-016**: System MUST use SQLModel combining SQLAlchemy and Pydantic for model definitions
- **FR-017**: System MUST support auto-increment integer primary keys for all models
- **FR-018**: System MUST use UTC timestamps for all datetime fields

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's todo item with title, description, completion status, and timestamps. Associated with a specific user via user_id.
- **Conversation**: Represents a logical grouping of messages between a user and the AI assistant. Associated with a specific user via user_id.
- **Message**: Represents individual exchanges within a conversation, with role indicating sender (user or assistant) and content of the message. Belongs to a specific conversation and user.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: All 3 required database models (Task, Conversation, Message) are successfully defined and accessible to the application
- **SC-002**: Foreign key relationships are correctly established with proper referential integrity enforced at the database level
- **SC-003**: Timestamps auto-populate correctly for created_at and updated_at fields without application-level intervention
- **SC-004**: User data isolation is maintained through user_id field present in all models with appropriate indexing
- **SC-005**: SQLModel models are compatible with Neon Serverless PostgreSQL and can be properly instantiated and queried
- **SC-006**: Migration scripts successfully create all 3 tables with proper constraints, relationships, and indexes in PostgreSQL