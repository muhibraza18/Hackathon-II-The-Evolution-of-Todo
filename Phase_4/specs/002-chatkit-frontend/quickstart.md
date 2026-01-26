# Quickstart Guide: OpenAI ChatKit Frontend for Todo AI Chatbot

## Prerequisites

- Node.js 18+ installed
- OpenAI ChatKit library access
- Backend API running (from Step 4/6) with authentication endpoints
- Domain added to OpenAI domain allowlist
- OpenAI domain key configured

## Setup

1. Ensure you have the frontend environment configured:
   ```bash
   # Navigate to frontend directory
   cd frontend

   # Install dependencies
   npm install

   # Copy environment file
   cp .env.example .env.local
   ```

2. Configure environment variables in `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_openai_domain_key_here
   ```

## Running the Application

### Development Mode

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Production Build

Build the application for production:
```bash
npm run build
```

Serve the production build:
```bash
npm run serve
```

## Testing the Frontend Functionality

### Registration Flow

Navigate to registration screen:
1. Go to `http://localhost:3000/register`
2. Enter valid email, password (min 8 chars), and optional name
3. Click "Register" button
4. Verify successful registration and redirect to chat

Expected behavior: Account created, token stored, redirected to chat interface.

### Login Flow

Navigate to login screen:
1. Go to `http://localhost:3000/login` (or `http://localhost:3000/` if not authenticated)
2. Enter registered email and password
3. Click "Login" button
4. Verify successful authentication and redirect to chat

Expected behavior: Credentials validated, token stored, redirected to chat interface.

### Chat Functionality

Interact with the AI assistant:
1. Ensure you're logged in and on the chat interface
2. Type a message in the input box (e.g., "Add buy groceries")
3. Press Enter or click "Send"
4. Verify message appears in chat and assistant responds

Expected behavior: Message sent to backend, appears in chat, assistant response received and displayed.

### Logout Functionality

End the session:
1. Click the "Logout" button (top-right corner)
2. Verify token is cleared and redirected to login

Expected behavior: Token cleared from storage, redirected to login screen.

## API Integration Tests

### Authentication API Calls

Test registration endpoint:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'
```

Test login endpoint:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

Test chat endpoint:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token_here" \
  -d '{
    "message": "Add buy groceries"
  }'
```

## Expected User Flows

### Happy Path Flow
1. User navigates to application
2. User registers with valid credentials
3. User is redirected to chat interface
4. User sends messages and receives responses
5. User logs out when finished
6. User is redirected to login screen

### Error Handling Flow
1. User enters invalid credentials
2. System displays appropriate error message
3. User corrects input and tries again
4. System validates corrected input
5. User proceeds with successful authentication

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | http://localhost:8000 |
| `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` | OpenAI domain key for ChatKit | - |
| `NODE_ENV` | Environment mode | development |

## Troubleshooting

- If ChatKit fails to initialize, verify domain is in OpenAI allowlist
- If authentication fails, check that backend API is running and accessible
- If messages don't appear in chat, verify that the backend `/api/chat` endpoint is working
- If session doesn't persist, check that localStorage is enabled in the browser
- If API requests return 401 errors, verify authentication token is being sent correctly
- If the application fails to build, ensure all dependencies are installed and environment variables are configured