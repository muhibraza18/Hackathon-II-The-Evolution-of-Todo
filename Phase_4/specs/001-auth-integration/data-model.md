# Data Model: Better Auth Integration for Todo AI Chatbot

## Entity Definitions

### User
Represents a registered user with credentials and profile information.

**Attributes**:
- `id`: Primary key identifier (int, auto-increment)
- `email`: Unique email address (string, required, indexed)
- `password_hash`: Securely hashed password (string, required)
- `name`: Optional user name (string, nullable)
- `created_at`: Timestamp of account creation (datetime)
- `updated_at`: Timestamp of last update (datetime)

**Validation**:
- `email` must be a valid email format
- `email` must be unique across all users
- `password_hash` must exist and be properly formatted
- `id` must be positive integer

### Session
Represents an active user session with token validation and expiration.

**Attributes**:
- `id`: Primary key identifier (string, UUID format)
- `user_id`: Foreign key reference to User (int, required)
- `token`: Unique session token (string, required, indexed)
- `expires_at`: Expiration timestamp (datetime)
- `created_at`: Creation timestamp (datetime)

**Validation**:
- `id` must be a valid UUID format
- `user_id` must reference an existing User
- `token` must be unique across all sessions
- `expires_at` must be in the future
- `created_at` must be before `expires_at`

### Authentication Token
Cryptographically secure identifier that verifies user identity without exposing credentials.

**Attributes**:
- `token_value`: The actual token string (string, 32+ bytes)
- `token_type`: Type of token (string, values: "session", "refresh")
- `user_id`: Associated user (int, required)
- `created_at`: Issue timestamp (datetime)
- `expires_at`: Expiration timestamp (datetime)

**Validation**:
- `token_value` must be cryptographically random
- `token_value` must be unique and not guessable
- `token_type` must be one of the allowed values
- `expires_at` must be in the future relative to `created_at`

## State Transitions

### User
- Created when user registers successfully
- Updated when user profile information changes
- No deletion in Phase III (marked inactive in future phases)

### Session
- Created when user logs in successfully
- Validated on each protected request
- Invalidated when user logs out
- Expires automatically after set duration

### Authentication Token
- Generated when session is created
- Validated on each protected request
- Invalidated when associated session ends
- Expires based on configured duration

## Constraints
- User email must be unique and properly formatted
- Passwords must be securely hashed before storage
- Sessions must reference valid users
- Session tokens must be unique and cryptographically random
- Expired sessions must be rejected by validation logic
- Session data must be cleaned up periodically to prevent database bloat