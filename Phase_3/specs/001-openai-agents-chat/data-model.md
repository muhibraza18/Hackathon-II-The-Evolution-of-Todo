# Data Model: OpenAI Agents Chat API for Todo AI Chatbot

## Entity Definitions

### Conversation
Represents a logical grouping of messages between a user and the AI assistant, identified by conversation_id.

**Fields**:
- `id`: Primary key (integer, auto-incrementing)
- `user_id`: Foreign key linking to user (string, indexed)
- `created_at`: Timestamp when conversation was created (datetime, default: now)
- `updated_at`: Timestamp when conversation was last updated (datetime, default: now)

**Relationships**:
- One-to-many with Message (conversation has many messages)

**Validation**:
- `user_id` must not be empty
- `created_at` and `updated_at` automatically managed by system

### Message
Represents individual exchanges within a conversation, with role (user or assistant) and content.

**Fields**:
- `id`: Primary key (integer, auto-incrementing)
- `user_id`: Foreign key linking to user (string, indexed)
- `conversation_id`: Foreign key linking to Conversation (integer, indexed)
- `role`: Role of message sender (string, values: "user", "assistant", "tool")
- `content`: Content of the message (string, min length: 1)
- `created_at`: Timestamp when message was created (datetime, indexed, default: now)

**Relationships**:
- Many-to-one with Conversation (message belongs to one conversation)

**Validation**:
- `user_id` must not be empty
- `conversation_id` must exist in Conversation table
- `role` must be one of "user", "assistant", or "tool"
- `content` must not be empty

### Tool Call
Represents invocations of MCP tools made by the AI assistant during conversation processing, stored as JSON in message content.

**Fields**:
- Stored as JSON within Message content when role is "tool"
- Contains: `name` (tool name), `arguments` (tool arguments as JSON), `result` (tool execution result)

**Relationships**:
- Embedded within Message entity when role is "tool"

## State Transitions

### Conversation
- Created when user initiates first message without conversation_id
- Updated when new messages are added to the conversation
- No explicit state changes - lifecycle tied to message activity

### Message
- Created when user sends message to chat endpoint
- Created when assistant generates response
- Created when MCP tools are invoked (as tool role messages)

## Database Indexes

- `Conversation.user_id`: For efficient user-based queries
- `Message.conversation_id`: For efficient conversation history retrieval
- `Message.user_id`: For efficient user-based queries
- `Message.created_at`: For chronological ordering of messages
- Composite: `(user_id, conversation_id)` for efficient user conversation access

## Constraints

- Foreign key constraint: `Message.conversation_id` references `Conversation.id`
- User isolation: All queries must filter by `user_id` to prevent cross-user access
- Data integrity: Messages cannot exist without valid Conversation
- Consistency: `updated_at` automatically updated when Conversation is modified