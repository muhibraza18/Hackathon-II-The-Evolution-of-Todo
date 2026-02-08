# Quickstart Guide: Better Auth Integration for Todo AI Chatbot

## Prerequisites

- Python 3.11+
- Better Auth Python SDK
- PostgreSQL database with existing models
- MCP server running with task tools
- Environment properly configured with secrets

## Setup

1. Ensure you have the backend environment configured:
   ```bash
   # Navigate to backend directory
   cd backend

   # Activate your Python virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install requirements including Better Auth
   pip install -r requirements.txt
   pip install better-auth bcrypt
   ```

2. Verify environment variables in `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_chatbot
   BETTER_AUTH_SECRET=your_secure_secret_key_minimum_32_chars
   ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
   SESSION_EXPIRY_DAYS=7
   ```

## Testing the Authentication Flow

### Register a New User

Register endpoint:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'
```

Expected response (success):
```json
{
  "user_id": "user_abc123",
  "email": "test@example.com",
  "token": "session_token_here"
}
```

### Login with Credentials

Login endpoint:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

Expected response (success):
```json
{
  "user_id": "user_abc123",
  "token": "session_token_here",
  "expires_at": "2026-01-15T10:30:00Z"
}
```

### Access Protected Endpoint

Using the token for protected access:
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer session_token_here"
```

Expected response:
```json
{
  "user_id": "user_abc123",
  "email": "test@example.com",
  "name": "Test User"
}
```

### Test Protected Chat Endpoint

Access chat endpoint with authentication:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Authorization: Bearer session_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "message": "Add buy groceries"
  }'
```

### Logout

End session:
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer session_token_here"
```

Expected response:
```json
{
  "message": "Logged out successfully"
}
```

### Test Invalid Token

Attempt to access with invalid token:
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer invalid_token_here"
```

Expected response:
```json
{
  "detail": "Unauthorized"
}
```

## Error Handling Tests

### Register with Duplicate Email
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "AnotherPass456!",
    "name": "Another User"
  }'
```
Response: 409 Conflict with error message

### Login with Wrong Credentials
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "wrongpassword"
  }'
```
Response: 401 Unauthorized

### Access with Expired Token
Response: 401 Unauthorized

## Expected Response Format

Successful registration:
```json
{
  "user_id": "user_abc123",
  "email": "test@example.com",
  "token": "session_token_here"
}
```

Authentication error:
```json
{
  "detail": "Unauthorized"
}
```

Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BETTER_AUTH_SECRET` | Secret key for token signing (min 32 chars) | - |
| `DATABASE_URL` | Database connection string | - |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed origins | - |
| `SESSION_EXPIRY_DAYS` | Number of days before session expires | 7 |
| `PASSWORD_HASH_ROUNDS` | Number of bcrypt rounds for password hashing | 12 |

## Troubleshooting

- If authentication fails, verify that the BETTER_AUTH_SECRET is properly set
- Check that the database connection is working and User/Session tables exist
- Verify that CORS settings allow the frontend domain
- Check that session tokens are being sent in the Authorization header correctly
- If rate limiting seems to be triggering unexpectedly, check the rate limiting configuration