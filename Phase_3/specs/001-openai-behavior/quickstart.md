# Quickstart Guide: OpenAI Agent Behavior for Todo AI Chatbot

## Prerequisites

- Python 3.11+
- OpenAI API key
- MCP server running with 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- PostgreSQL database with existing models

## Setup

1. Ensure you have the backend environment configured:
   ```bash
   # Navigate to backend directory
   cd backend

   # Activate your Python virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install requirements if not already installed
   pip install -r requirements.txt
   ```

2. Verify environment variables in `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_chatbot
   OPENAI_API_KEY=your_openai_api_key_here
   MCP_SERVER_URL=http://localhost:8001
   ```

## Testing the Agent Behavior

### Basic Task Operations

Add a task:
```bash
curl -X POST "http://localhost:8000/api/test_user/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

List tasks:
```bash
curl -X POST "http://localhost:8000/api/test_user/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me my pending tasks"
  }'
```

Complete a task:
```bash
curl -X POST "http://localhost:8000/api/test_user/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Mark task 1 as complete"
  }'
```

Update a task by name (triggers tool chaining - list then update):
```bash
curl -X POST "http://localhost:8000/api/test_user/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Change the groceries task to buy groceries and milk"
  }'
```

### Testing Ambiguity Handling

Test with ambiguous request:
```bash
curl -X POST "http://localhost:8000/api/test_user/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Complete the task"
  }'
```

The agent should ask for clarification.

### Testing Error Handling

Test with non-existent task:
```bash
curl -X POST "http://localhost:8000/api/test_user/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Complete task 999999"
  }'
```

The agent should respond with an appropriate error message.

## Expected Response Format

Successful task creation:
```json
{
  "conversation_id": 123,
  "response": "✓ Added 'buy groceries' to your list!",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {"user_id": "test_user", "title": "buy groceries"},
      "result": {"task_id": 456, "status": "created", "title": "buy groceries"}
    }
  ]
}
```

With clarifying question:
```json
{
  "conversation_id": 123,
  "response": "Which task would you like to mark as complete? Could you tell me the task number or title?",
  "tool_calls": []
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for agent integration | - |
| `MCP_SERVER_URL` | URL of MCP server with task tools | - |
| `LOG_LEVEL` | Logging level | INFO |

## Troubleshooting

- If the agent doesn't respond appropriately, check that the MCP server is running and accessible
- Verify that the OpenAI API key has sufficient quota
- Check logs for detailed error information when requests fail
- If the agent doesn't ask clarifying questions for ambiguous requests, review the intent recognition patterns