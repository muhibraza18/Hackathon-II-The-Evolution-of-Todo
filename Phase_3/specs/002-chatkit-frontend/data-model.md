# Data Model: OpenAI ChatKit Frontend for Todo AI Chatbot

## Entity Definitions

### Authentication Token
Cryptographically secure identifier that verifies user identity for API requests.

**Attributes**:
- `token_value`: The actual token string (string, 32+ characters)
- `user_id`: Associated user identifier (string)
- `expires_at`: Expiration timestamp (datetime)
- `created_at`: Issue timestamp (datetime)

**Validation**:
- `token_value` must be present and properly formatted
- `user_id` must be present and valid
- `expires_at` must be in the future
- Token must be securely stored in browser storage

### Chat Message
User or assistant communication displayed in conversation format with timestamps.

**Attributes**:
- `id`: Unique message identifier (string, auto-generated)
- `sender`: Message originator ('user' or 'assistant') (string)
- `content`: Message text content (string, required)
- `timestamp`: When message was sent/received (datetime)
- `status`: Message status ('sent', 'delivered', 'error') (string)
- `conversation_id`: Associated conversation identifier (string, optional)

**Validation**:
- `content` must be non-empty
- `sender` must be either 'user' or 'assistant'
- `timestamp` must be present
- `status` must be one of the allowed values

### Conversation Context
Maintained state of ongoing chat session including message history.

**Attributes**:
- `id`: Conversation identifier (string, auto-generated)
- `messages`: Array of chat messages (array of Message objects)
- `created_at`: When conversation started (datetime)
- `updated_at`: When conversation last updated (datetime)
- `user_id`: Associated user identifier (string)

**Validation**:
- `messages` array must be valid
- `id` must be unique per user
- `user_id` must reference a valid user
- `updated_at` must be greater than or equal to `created_at`

### User Session
Browser-based storage of authentication state and user preferences.

**Attributes**:
- `auth_token`: Stored authentication token (string)
- `user_id`: Associated user identifier (string)
- `expires_at`: Session expiration time (datetime)
- `preferences`: User-specific preferences (object, optional)

**Validation**:
- `auth_token` must be present and valid
- `user_id` must be present
- `expires_at` must be in the future when session is valid
- Session data must be cleared appropriately on logout

## State Transitions

### Authentication Token
- Created when user successfully authenticates
- Validated on each API request
- Expires automatically after 7 days
- Invalidated when user logs out

### Chat Message
- Created when user sends message
- Status updated to 'sent' when delivered to backend
- Status updated to 'delivered' when confirmed by backend
- Status updated to 'error' if delivery fails

### Conversation Context
- Created when new chat session starts
- Updated with each new message
- Maintained across page refreshes if token is valid
- Cleared when session expires or user logs out

### User Session
- Created when user successfully logs in
- Validated on each page load
- Maintained across browser sessions until logout or expiration
- Cleared when user logs out or token expires

## Constraints
- Authentication tokens must be stored securely in browser storage
- Message content must be sanitized before display to prevent XSS
- Conversation contexts must be isolated by user_id to prevent cross-user access
- Session data must be cleared appropriately to prevent unauthorized access
- All API requests must include proper authentication tokens
- Expiration times must be respected for security