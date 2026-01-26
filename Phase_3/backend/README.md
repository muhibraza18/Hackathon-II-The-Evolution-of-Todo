# OpenAI Agents Chat API for Todo AI Chatbot

This is a FastAPI backend service that integrates with OpenAI Agents SDK to process natural language chat messages and invoke MCP tools for task management operations. The system maintains conversation history in Neon PostgreSQL database while adhering to stateless architecture principles.

## Features

- **Natural Language Processing**: Users can interact with the AI assistant using natural language to manage tasks
- **MCP Integration**: Seamlessly integrates with MCP tools for task operations (add, list, complete, delete, update)
- **Conversation Persistence**: Maintains conversation history in PostgreSQL database
- **Stateless Architecture**: Each request is independent and self-contained
- **User Isolation**: Proper data isolation between different users

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon Serverless recommended)
- OpenAI API key
- MCP server running with 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   cd backend
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_chatbot
   OPENAI_API_KEY=your_openai_api_key_here
   MCP_SERVER_URL=http://localhost:8001
   ```

## Running the Server

Start the backend server:

```bash
python start_server.py
```

Or alternatively:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Usage

### Chat Endpoint

Send a message to the AI assistant:

```
POST /api/{user_id}/chat
```

**Request Body**:
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {"user_id": "test_user", "title": "buy groceries"},
      "result": {"task_id": 456, "status": "created", "title": "buy groceries"}
    }
  ]
}
```

**Parameters**:
- `user_id` (path): Unique identifier for the user
- `conversation_id` (optional): ID of existing conversation (creates new if absent)
- `message` (required): User's natural language message

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `OPENAI_API_KEY` | OpenAI API key for agent integration | - |
| `MCP_SERVER_URL` | URL of MCP server with task tools | http://localhost:8001 |
| `BETTER_AUTH_SECRET` | Better Auth secret | - |
| `LOG_LEVEL` | Logging level | INFO |
| `SERVER_HOST` | Server host | 0.0.0.0 |
| `SERVER_PORT` | Server port | 8000 |

## Architecture

The application follows a service-oriented architecture:

- `app/main.py`: FastAPI application entry point
- `app/routes/chat.py`: Chat endpoint definition
- `app/services/agent.py`: OpenAI agent processing logic
- `app/services/mcp_client.py`: MCP server communication
- `app/services/conversation.py`: Conversation management
- `app/services/message.py`: Message operations
- `app/database/connection.py`: Database connection management
- `app/config.py`: Configuration management

## MCP Tool Integration

The system integrates with the following MCP tools:
- `add_task`: Create new tasks
- `list_tasks`: Retrieve tasks (all/pending/completed)
- `complete_task`: Mark tasks as done
- `delete_task`: Remove tasks
- `update_task`: Modify task details

## Error Handling

The API implements comprehensive error handling:
- Validation errors return 400 Bad Request
- Unauthorized access attempts return 401 Unauthorized
- Server errors return 500 Internal Server Error
- User-friendly error messages for common issues

## Testing

To run the application tests (when implemented):
```bash
pytest tests/
```

## Troubleshooting

- If you get database connection errors, ensure PostgreSQL is running and credentials are correct
- If MCP tools aren't working, verify the MCP server is running on the configured URL
- Check logs for detailed error information when requests fail
- Ensure your OpenAI API key is valid and has sufficient quota