# Database Schema - Todo Full-Stack Web Application

**Branch**: `001-foundation-setup`
**Database**: Neon Serverless PostgreSQL
**Updated**: 2026-01-06

## Overview

This document describes the database schema for the Todo Full-Stack Web Application. The schema consists of two tables:
- `users` - Managed by Better Auth (external service)
- `tasks` - Managed by our application

## Tables

### 1. users (Better Auth Managed)

**Ownership**: External - Better Auth service
**Access Pattern**: Read-only (all mutations handled by Better Auth)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| `first_name` | VARCHAR(100) | NULLABLE | User first name |
| `last_name` | VARCHAR(100) | NULLABLE | User last name |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | AUTO UPDATE | Last update timestamp |

**Important Notes**:
- This table is created and managed exclusively by Better Auth
- Our application never directly mutates this table
- All user-related operations go through Better Auth's SDK/API
- We reference the `id` field as a foreign key in our `tasks` table
- Better Auth handles password hashing, session management, and security

### 2. tasks (Application Managed)

**Ownership**: Internal - Our application

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY → `users.id`, NOT NULL, INDEXED | Owner of the task (references Better Auth `users.id`) |
| `title` | VARCHAR(200) | NOT NULL | Task title (short summary) |
| `description` | TEXT | NULLABLE | Detailed task description |
| `status` | ENUM | NOT NULL, DEFAULT 'pending', INDEXED | Task status: `pending`, `in_progress`, `completed` |
| `priority` | ENUM | NOT NULL, DEFAULT 'medium' | Task priority: `low`, `medium`, `high` |
| `due_date` | DATE | NULLABLE | Optional due date for the task |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Task creation timestamp |
| `updated_at` | TIMESTAMP | AUTO UPDATE | Last modification timestamp |

**Status Enum Values**:
- `pending` - Task not started
- `in_progress` - Task currently being worked on
- `completed` - Task finished

**Priority Enum Values**:
- `low` - Low priority task
- `medium` - Normal priority task (default)
- `high` - High priority task

## Relationships

### Users → Tasks (One-to-Many)

```
users (1) ──< (N) tasks
```

**Relationship Type**: One user can have many tasks

**Foreign Key**: `tasks.user_id → users.id`

**Cascade Behavior**: Application-managed (not database-level cascade)
- When a user is deleted via Better Auth, application logic handles task cleanup
- Database constraints ensure referential integrity

## Indexes

### users Table (Better Auth Managed)

Indexes are managed by Better Auth. We do not create or modify indexes on this table.

### tasks Table

| Index Name | Columns | Purpose |
|------------|---------|---------|
| `idx_tasks_user_id` | `user_id` | Fast lookup of all tasks for a user |
| `idx_tasks_status` | `status` | Filter tasks by status (e.g., find all completed tasks) |
| `idx_tasks_completed_user` | `(user_id, status)` | Composite index for dashboard queries (e.g., "show completed tasks for user X") |

**Index Strategy**:
- Single-column indexes on frequently filtered fields (`user_id`, `status`)
- Composite index for common query patterns (user + status filtering)
- No index on `priority` or `due_date` (expected lower cardinality usage)

## Data Constraints

### Validation Rules

**Tasks Table**:
- `user_id` must reference an existing user in the `users` table
- `title` cannot be empty (max 200 characters)
- `status` must be one of: `pending`, `in_progress`, `completed`
- `priority` must be one of: `low`, `medium`, `high`
- `due_date` must be a valid date (if provided)

**Referential Integrity**:
- Every task must be associated with a valid user
- Tasks cannot exist without a user (enforced by NOT NULL constraint on `user_id`)

## SQL Model Definitions

The corresponding SQLModel definitions will be in `backend/models.py`:

```python
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending", index=True)  # pending, in_progress, completed
    priority: str = Field(default="medium")  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Note**: The `users` table is NOT defined in our SQLModel models - it's managed exclusively by Better Auth.

## Migration Strategy

### Current Phase (Foundation)
- No database migrations run
- Schema is documented only (no actual database provisioned)
- SQLModel models are stubs for future use

### Future Phases
- Use Alembic for database migrations
- Migrations will be versioned and tracked
- Neon PostgreSQL will be provisioned with Better Auth integration
- `users` table will be created by Better Auth
- `tasks` table will be created by our application migrations

## Access Patterns

### Common Queries

1. **List all tasks for a user**:
   ```sql
   SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC;
   ```

2. **Get task details**:
   ```sql
   SELECT * FROM tasks WHERE id = $1 AND user_id = $2;
   ```

3. **Update task status**:
   ```sql
   UPDATE tasks SET status = $1, updated_at = NOW() WHERE id = $2 AND user_id = $3;
   ```

4. **Filter tasks by status**:
   ```sql
   SELECT * FROM tasks WHERE user_id = $1 AND status = $2 ORDER BY priority, due_date;
   ```

### Query Optimization

- Use `idx_tasks_user_id` for user-specific queries
- Use `idx_tasks_status` for status filtering
- Use `idx_tasks_completed_user` for dashboard queries
- Consider adding `ORDER BY` indexes if sorting patterns become clear

## Security Considerations

### Data Access Control
- Row-level security: Users can only access their own tasks
- Every task query must include `user_id = current_user_id` filter
- Better Auth handles user authentication and provides `user_id` in JWT claims

### Injection Prevention
- Use SQLModel ORM parameterized queries (not raw SQL)
- Never concatenate user input into query strings
- Validate all inputs with Pydantic models before database operations

## Future Enhancements

### Potential Additions
- **Task Comments** table - For discussion threads on tasks
- **Audit Log** table - Track all changes to tasks (who, when, what)
- **Task Tags** table - For categorizing and filtering tasks
- **Task Assignments** table - For shared/collaborative tasks (multi-user)

### Performance Optimizations
- Read replicas for query-heavy operations
- Connection pooling for high concurrency
- Caching layer (Redis) for frequently accessed tasks
- Partitioning by `user_id` for very large deployments

## Related Documents

- **Data Model Details**: `@specs/001-foundation-setup/data-model.md` - Entity definitions and relationships
- **Architecture**: `@specs/architecture.md` - System design and component responsibilities
- **Feature Spec**: `@specs/001-foundation-setup/spec.md` - Functional requirements
- **Constitution**: `.specify/memory/constitution.md` - Database management principles
