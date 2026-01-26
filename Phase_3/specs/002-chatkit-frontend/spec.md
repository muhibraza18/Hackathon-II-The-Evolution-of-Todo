# Feature Specification: OpenAI ChatKit Frontend for Todo AI Chatbot

**Feature Branch**: `002-chatkit-frontend`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "OpenAI ChatKit frontend for Todo AI Chatbot with authentication
Target audience: Frontend developers implementing ChatKit UI with Better Auth integration
Focus: Chat interface, API integration, authentication flow, and deployment configuration
Success criteria:
- Users can register and login through UI
- Authenticated users can chat with AI assistant
- Chat messages display in real-time conversation format
- Task operations visible through assistant responses
- Sessions persist across page refreshes
- Token stored securely and sent with API requests
- Deployment-ready with environment configuration

Constraints:
- Framework: OpenAI ChatKit (https://platform.openai.com/docs/chatkit)
- Backend API: FastAPI from Step 4 (modified in Step 6 for auth)
- Authentication: Better Auth tokens from Step 6
- Deployment: Vercel, Netlify, or GitHub Pages
- Domain allowlist: Required for hosted ChatKit
- No custom UI framework (use ChatKit components only)
- No state management library (ChatKit handles chat state)

Technology requirements:
- OpenAI ChatKit library
- Environment variables for API configuration
- Token storage (localStorage or secure cookies)
- HTTP client for API calls (fetch or axios)
- OpenAI domain allowlist configuration

ChatKit configuration:

**Domain allowlist setup:**
1. Deploy frontend to get production URL
2. Add domain to OpenAI allowlist: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Receive domain key from OpenAI
4. Configure ChatKit with domain key

**Environment variables:**
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend URL
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here  # From OpenAI allowlist

User interface requirements:

**Authentication screens:**

Login screen:
- Email input field
- Password input field (type="password")
- "Login" button
- "Don't have an account? Register" link
- Error message display area
- Form validation (email format, required fields)

Registration screen:
- Name input field (optional)
- Email input field
- Password input field (min 8 characters)
- "Register" button
- "Already have an account? Login" link
- Error message display area
- Password strength indicator (optional for Phase III)

**Chat interface (post-authentication):**
- ChatKit conversation area (messages display)
- Message input box
- Send button
- Logout button (top-right corner)
- User email display (top-right, optional)
- Loading indicator during API calls
- Error message display for failed requests

ChatKit integration:

**Basic ChatKit setup:**
```javascript
import { ChatKit } from '@openai/chatkit';

const chatConfig = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL,
  authToken: localStorage.getItem('auth_token'),
  onSendMessage: async (message) => {
    // Send to backend /api/chat
  },
  onReceiveMessage: (response) => {
    // Display assistant response
  }
};

<ChatKit config={chatConfig} />
```

API integration specification:

**Authentication flow:**

Registration:
```javascript
async function register(email, password, name) {
  const response = await fetch(`${API_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('auth_token', data.token);
    localStorage.setItem('user_id', data.user_id);
    // Redirect to chat
  } else {
    // Show error
  }
}
```

Login:
```javascript
async function login(email, password) {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('auth_token', data.token);
    localStorage.setItem('user_id', data.user_id);
    // Redirect to chat
  } else {
    // Show error message
  }
}
```

Logout:
```javascript
async function logout() {
  const token = localStorage.getItem('auth_token');

  await fetch(`${API_URL}/api/auth/logout`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_id');
    // Redirect to login
}
```

**Chat API integration:**

Send message:
```javascript
async function sendMessage(message, conversationId = null) {
  const token = localStorage.getItem('auth_token');

  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      message: message,
      conversation_id: conversationId
    })
  });

  if (response.ok) {
    const data = await response.json();
    // Store conversation_id for subsequent messages
    // Display assistant response
    return data;
  } else if (response.status === 401) {
    // Token expired, redirect to login
  } else {
    // Show error message
  }
}
```

Application flow:

**Initial load:**
1. Check if auth_token exists in localStorage
2. If yes → Load chat interface
3. If no → Show login screen

**After login/registration:**
1. Store token in localStorage
2. Redirect to chat interface
3. Initialize ChatKit with token
4. Ready to send messages

**During chat session:**
1. User types message in ChatKit input
2. Frontend sends message to /api/chat with auth token
3. Display user message immediately in ChatKit
4. Show loading indicator
5. Backend processes and returns response
6. Display assistant response in ChatKit
7. Store conversation_id for next message
8. Remove loading indicator

**On page refresh:**
1. Check localStorage for token
2. If valid token exists → Resume chat interface
3. If no token → Redirect to login
4. Previous conversation persists (conversation_id in URL or localStorage)

**On logout:**
1. Call /api/auth/logout
2. Clear localStorage
3. Redirect to login screen
4. ChatKit conversation cleared

Error handling:

**Authentication errors:**
- 400 Bad Request → "Invalid email or password format"
- 401 Unauthorized → "Invalid credentials"
- 409 Conflict → "Email already registered"
- Network error → "Connection failed. Please try again"

**Chat errors:**
- 401 Unauthorized → Clear token, redirect to login
- 500 Internal Server Error → "Something went wrong. Please try again"
- Network timeout → "Request timed out. Please try again"
- Empty response → "No response from server"

State management:

**localStorage keys:**
- `auth_token` - Session token from backend
- `user_id` - User identifier
- `conversation_id` - Current conversation (optional, can use URL param)

**Session persistence:**
- Token remains valid for 7 days (from Step 6)
- User stays logged in across browser sessions
- Logout clears all stored data

Deployment configuration:

**Vercel deployment:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "NEXT_PUBLIC_API_URL": "https://your-backend.com",
    "NEXT_PUBLIC_OPENAI_DOMAIN_KEY": "@openai-domain-key"
  }
}
```

**Environment setup:**
- Development: `.env.local` with localhost backend
- Production: Environment variables in hosting platform
- API_URL points to deployed FastAPI backend
- OPENAI_DOMAIN_KEY from domain allowlist

**CORS requirements:**
- Backend must include frontend domain in ALLOWED_ORIGINS (Step 6)
- Example: `https://your-app.vercel.app`
- Credentials must be allowed for auth tokens

Security considerations:
- Store token in localStorage (simple) or httpOnly cookies (more secure)
- Always send token in Authorization header
- Validate token on every API request (backend handles this)
- Clear sensitive data on logout
- Use HTTPS in production
- No sensitive data in URL parameters
- Token expiration handled by backend (7 days)

User experience requirements:
- Chat messages appear instantly (optimistic UI)
- Loading states during API calls
- Error messages are user-friendly
- Smooth transitions between auth and chat screens
- Mobile-responsive layout (ChatKit provides this)
- Clear logout option always visible
- Conversation history persists during session

File structure:
frontend/
├── src/
│   ├── components/
│   │   ├── LoginForm.jsx
│   │   ├── RegisterForm.jsx
│   │   ├── ChatInterface.jsx
│   │   └── Layout.jsx
│   ├── services/
│   │   ├── api.js          # API calls
│   │   └── auth.js         # Auth helpers
│   ├── App.jsx             # Main app with routing
│   └── main.jsx
├── .env.local              # Local environment
├── .env.production         # Production environment
├── package.json
└── README.md

Validation requirements:
- ✓ Users can register with email/password
- ✓ Users can login with credentials
- ✓ Invalid credentials show error message
- ✓ Token stored after successful auth
- ✓ Chat interface loads after authentication
- ✓ Messages sent to backend with auth token
- ✓ Assistant responses displayed in chat
- ✓ Logout clears session and redirects to login
- ✓ Page refresh maintains session (if token valid)
- ✓ Expired token redirects to login
- ✓ 401 errors trigger re-authentication
- ✓ Production deployment works with domain allowlist

Not building:
- Custom chat UI components (using ChatKit)
- Password reset functionality (future)
- Email verification (future)
- Remember me / persistent login option (future)
- Multi-device session management (future)
- Push notifications (future)
- Offline mode (future)
- Message editing/deletion (future)
- File uploads in chat (future)
- Dark mode toggle (use ChatKit default)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication Flow (Priority: P1)

A user wants to create an account or login to access the Todo AI Chatbot. The system provides registration and login screens with proper validation and secure token management, allowing users to authenticate and access the chat interface.

**Why this priority**: This is the foundational functionality that enables all other features of the Todo AI Chatbot, allowing users to have personalized experiences with their tasks.

**Independent Test**: Can be fully tested by navigating to the application, registering with valid credentials, and verifying that the user is redirected to the chat interface with a stored authentication token.

**Acceptance Scenarios**:

1. **Given** a user visits the Todo AI Chatbot for the first time, **When** they navigate to the registration screen and submit valid credentials (email, password, optional name), **Then** the system creates their account, stores the authentication token, and redirects them to the chat interface.
2. **Given** a user has already registered, **When** they visit the login screen and submit correct credentials, **Then** the system validates their credentials, stores the authentication token, and redirects them to the chat interface.
3. **Given** a user submits invalid credentials, **When** they attempt to login or register, **Then** the system displays appropriate error messages without storing any tokens.

---

### User Story 2 - Real-Time Chat Interaction (Priority: P1)

An authenticated user wants to interact with the AI assistant to manage their tasks. The system provides a real-time chat interface where messages appear instantly, and the assistant responds with appropriate task-related actions and confirmations.

**Why this priority**: This is the core functionality that delivers the value proposition of the Todo AI Chatbot, enabling users to manage their tasks through natural language conversations.

**Independent Test**: Can be tested by authenticating as a user, sending messages to the AI assistant, and verifying that messages appear in real-time with appropriate assistant responses showing task operations.

**Acceptance Scenarios**:

1. **Given** an authenticated user is on the chat interface, **When** they send a message to add a task, **Then** the system sends the message to the backend, displays it immediately, shows a loading indicator, and displays the assistant's confirmation response.
2. **Given** an authenticated user is chatting with the assistant, **When** they send a message to list their tasks, **Then** the system processes the request and displays the assistant's response with their current tasks.
3. **Given** the backend returns an error, **When** the user sends a message, **Then** the system displays an appropriate error message to the user.

---

### User Story 3 - Session Management and Persistence (Priority: P2)

An authenticated user wants to maintain their session across page refreshes and browser sessions. The system securely manages authentication tokens and maintains the user's chat context during their session.

**Why this priority**: Essential for a good user experience, allowing users to continue their conversations without having to re-authenticate frequently.

**Independent Test**: Can be tested by logging in, refreshing the page, and verifying that the user remains authenticated and their chat interface is preserved.

**Acceptance Scenarios**:

1. **Given** a user has authenticated successfully, **When** they refresh the page, **Then** the system detects the stored authentication token and resumes the chat interface.
2. **Given** a user has an active session, **When** they click the logout button, **Then** the system clears all stored tokens and redirects to the login screen.
3. **Given** a user's token has expired, **When** they make a request, **Then** the system detects the 401 response and redirects to the login screen.

---

### Edge Cases

- What happens when the network connection is lost during a chat session?
- How does the system handle token expiration mid-conversation?
- What occurs when the backend API is temporarily unavailable?
- How does the system respond to rapid-fire message submissions?
- What happens when the user closes the browser tab during an active session?
- How does the system handle concurrent sessions from multiple devices?
- What occurs when the domain allowlist is not properly configured with OpenAI?
- How does the system handle invalid domain keys or API misconfigurations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide registration screen with email, password, and optional name fields
- **FR-002**: System MUST provide login screen with email and password fields
- **FR-003**: System MUST validate email format and password strength before submission
- **FR-004**: System MUST store authentication tokens securely in browser storage
- **FR-005**: System MUST send authentication tokens with all API requests in Authorization header
- **FR-006**: System MUST provide real-time chat interface using OpenAI ChatKit components
- **FR-007**: System MUST display user and assistant messages in conversation format
- **FR-008**: System MUST handle API errors gracefully with user-friendly messages
- **FR-009**: System MUST redirect unauthenticated users to login screen
- **FR-010**: System MUST clear authentication tokens on logout
- **FR-011**: System MUST maintain chat context across page refreshes when token is valid
- **FR-012**: System MUST detect and handle token expiration automatically
- **FR-013**: System MUST integrate with OpenAI domain allowlist configuration
- **FR-014**: System MUST support deployment to Vercel, Netlify, or GitHub Pages
- **FR-015**: System MUST implement proper CORS handling with backend API

### Key Entities

- **Authentication Token**: Cryptographically secure identifier that verifies user identity for API requests
- **Chat Message**: User or assistant communication displayed in conversation format with timestamps
- **Conversation Context**: Maintained state of ongoing chat session including message history
- **User Session**: Browser-based storage of authentication state and user preferences

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can register with email/password successfully with 95% success rate under normal conditions
- **SC-002**: User login succeeds with correct credentials within 2 seconds 98% of the time
- **SC-003**: Chat messages appear in real-time with minimal delay (under 500ms) 95% of the time
- **SC-004**: Sessions persist across page refreshes and remain valid for the full 7-day duration
- **SC-005**: Authentication tokens are properly sent with all API requests 100% of the time
- **SC-006**: Error scenarios are handled gracefully with user-friendly messages 100% of the time