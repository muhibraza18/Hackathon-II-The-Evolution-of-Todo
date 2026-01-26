# Data Model: OpenAI Agent Behavior for Todo AI Chatbot

## Entity Definitions

### User Intent
Represents the user's desired action derived from natural language input.

**Attributes**:
- `intent_type`: Type of action (string, values: "add_task", "list_tasks", "complete_task", "delete_task", "update_task")
- `confidence_score`: Confidence level in intent recognition (float, 0.0-1.0)
- `parameters`: Extracted parameters from user input (dict, varies by intent type)
- `original_input`: Raw user input for context (string)

**Validation**:
- `intent_type` must be one of the supported values
- `confidence_score` must be between 0.0 and 1.0
- `parameters` must match the expected format for the intent type

### Task Reference
Represents how a task is identified (by ID or by name/title) and resolved to an actual task.

**Attributes**:
- `identifier_type`: How the task is identified (string, values: "id", "title", "partial_match")
- `identifier_value`: The actual value (int for ID, string for title)
- `resolved_task_id`: The actual task ID after resolution (int, nullable)
- `confidence_score`: Confidence in the match (float, 0.0-1.0)

**Validation**:
- `identifier_type` must be one of the supported values
- `identifier_value` must be provided
- `confidence_score` must be between 0.0 and 1.0

### Conversation Context
Represents the ongoing dialogue state and user's task-related needs.

**Attributes**:
- `conversation_id`: The current conversation (int)
- `previous_intents`: Recent user intents for context (list of Intent objects)
- `active_tasks`: Tasks currently being discussed (list of TaskReference objects)
- `user_preferences`: Personalization preferences (dict)
- `context_summary`: Brief summary of current conversation state (string)

**Validation**:
- `conversation_id` must exist in the database
- Lists must not exceed reasonable limits

### Tool Chain
Represents sequences of MCP tool calls needed to fulfill complex user requests.

**Attributes**:
- `chain_id`: Unique identifier for the chain (string)
- `steps`: Ordered list of tool calls to execute (list of ToolCall objects)
- `status`: Current status of the chain (string, values: "pending", "executing", "completed", "failed")
- `results`: Results from each step (list of dict)
- `error_info`: Error details if chain failed (dict, nullable)

**Validation**:
- `steps` must be a non-empty list
- `status` must be one of the supported values
- `chain_id` must be unique

## State Transitions

### User Intent
- Created when user input is received and parsed
- Updated when confidence is recalculated based on context
- No explicit state changes - lifecycle tied to conversation context

### Task Reference
- Created when task is referenced by user
- Updated when task is resolved from database
- Validated before being used in tool calls

### Conversation Context
- Created when new conversation starts
- Updated with each exchange
- Preserved across requests in database

### Tool Chain
- Created when multi-step operation is detected
- Updated as each step completes
- Finalized when all steps are completed or chain fails

## Constraints

- Intent recognition must validate against known patterns before execution
- Task references must be resolved to actual database records before tool calls
- Tool chains must maintain proper sequence and error handling
- Conversation context must be isolated by user_id to prevent cross-user access
- All agent responses must include proper user_id attribution