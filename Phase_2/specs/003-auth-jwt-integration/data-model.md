# Data Model: Authentication with Better Auth + JWT Integration

## 1. Entity Relationships

### 1.1 User Entity (Managed by Better Auth)
```
users (automatically managed by Better Auth)
├── id: UUID (primary key)
├── email: String (unique, indexed)
├── email_verified: Boolean
├── password: String (hashed)
├── created_at: DateTime
└── updated_at: DateTime
```

### 1.2 Task Entity (Updated for User Association)
```
tasks (managed by application)
├── id: UUID (primary key)
├── user_id: UUID (foreign key → users.id, indexed)
├── title: String (max_length=200)
├── description: String (nullable)
├── status: String (default: "pending", indexed)
├── priority: String (default: "medium")
├── completed: Boolean (default: false)
├── created_at: DateTime
└── updated_at: DateTime
```

## 2. Database Schema Changes

### 2.1 Better Auth Schema (Automatically Created)
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### 2.2 Updated Task Schema with User Association
```sql
-- Existing tasks table needs user_id foreign key added
ALTER TABLE tasks ADD COLUMN user_id TEXT REFERENCES users(id) NOT NULL;
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

## 3. JWT Token Structure

### 3.1 JWT Payload Claims
```json
{
  "sub": "user-id-here",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### 3.2 Claim Definitions
- `sub`: Subject (user ID) - used for identifying the authenticated user
- `email`: User email - for reference and validation
- `exp`: Expiration timestamp - when the token expires
- `iat`: Issued at timestamp - when the token was issued

## 4. SQLModel Updates

### 4.1 Updated Task Model
```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Added for user association
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## 5. Migration Strategy

### 5.1 Existing Tasks Migration
1. Create a default user account for existing tasks
2. Update all existing tasks to assign to the default user
3. Ensure foreign key constraint is properly applied

### 5.2 Migration Steps
```sql
-- Step 1: Create default user for existing tasks
INSERT INTO users (id, email, email_verified, password, created_at, updated_at)
VALUES ('test-user-1', 'test@example.com', TRUE, 'dummy-password-hash', NOW(), NOW());

-- Step 2: Update existing tasks to reference the default user
UPDATE tasks SET user_id = 'test-user-1' WHERE user_id IS NULL;

-- Step 3: Apply NOT NULL constraint to user_id
ALTER TABLE tasks ALTER COLUMN user_id SET NOT NULL;
```

## 6. Indexing Strategy

### 6.1 Required Indexes
- `idx_users_email`: For efficient user lookup by email
- `idx_tasks_user_id`: For efficient filtering by user
- `idx_tasks_status`: For filtering tasks by status

### 6.2 Performance Considerations
- Foreign key columns should be indexed for JOIN operations
- Frequently queried columns should have appropriate indexes
- Balance between query performance and write performance

## 7. Data Validation Rules

### 7.1 User Data Validation
- Email format validation
- Password strength requirements (minimum 8 characters)
- Unique email constraint enforced

### 7.2 Task Data Validation
- Title must be 1-200 characters
- Description limited to 1000 characters
- Status must be one of allowed values
- User_id must reference existing user

## 8. Security Constraints

### 8.1 Data Access Constraints
- All task queries must be filtered by user_id
- Cross-user data access prevented at application level
- Foreign key constraints prevent orphaned tasks

### 8.2 Data Integrity
- Referential integrity maintained through foreign keys
- Cascading operations handled appropriately
- Data consistency validated at both database and application levels