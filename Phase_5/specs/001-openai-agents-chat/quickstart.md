# Quickstart Guide: OpenAI Agents Chat API for Todo AI Chatbot

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
   ```

2. Navigate to backend directory:
   ```bash
   cd backend
   ```

3. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_chatbot
   OPENAI_API_KEY=your_openai_api_key_here
   MCP_SERVER_URL=http://localhost:8001
   ```

## Database Initialization

Run the database initialization script to create tables:

```bash
python init_db.py
```

## Running the Server

Start the backend server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The chat API will be available at `http://localhost:8000/api/{user_id}/chat`.

## Testing the API

Send a test request to the chat endpoint:

```bash
curl -X POST "http://localhost:8000/api/test_user/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

Expected response:
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

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `OPENAI_API_KEY` | OpenAI API key for agent integration | - |
| `MCP_SERVER_URL` | URL of MCP server with task tools | - |
| `BETTER_AUTH_SECRET` | Better Auth secret (from Step 6) | - |
| `LOG_LEVEL` | Logging level | INFO |

## Troubleshooting

- If you get database connection errors, ensure PostgreSQL is running and credentials are correct
- If MCP tools aren't working, verify the MCP server is running on the configured URL
- Check logs for detailed error information when requests fail