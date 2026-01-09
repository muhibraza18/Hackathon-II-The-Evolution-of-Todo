# Data Model: Setup Monorepo Structure & Initial Specs

**Branch**: `001-foundation-setup`
**Date**: 2026-01-06

Because Phase 2 is blueprint-only, no live database is provisioned. This document captures the canonical schema for future implementation and ensures frontend/backend scaffolding references a consistent contract.

## Entities

### 1. Users (Better Auth Managed)
- **Ownership**: Better Auth service (external). Not stored in our database; referenced via Better Auth APIs.
- **Purpose**: Represents authenticated people who can own tasks.
- **Canonical Identifier**: `user_id` UUID provided by Better Auth.
- **Attributes** (read-only snapshot in our system):
  - `id` (UUID, primary key in Better Auth)
  - `email` (string, unique)
  - `first_name` (string)
  - `last_name` (string)
  - `created_at` (timestamp)
- **Notes**: We never persist or mutate these records directly; all operations go through Better Auth’s SDK/API.

### 2. Tasks (Local SQLModel Table)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Primary identifier for tasks |
| `user_id` | UUID | FK → Better Auth `users.id`; indexed | Owner reference |
| `title` | string | not null, max 200 chars | Short summary |
| `description` | text | nullable | Extended details |
| `status` | enum(`pending`, `in_progress`, `completed`) | default `pending`, indexed on `completed` flag | Workflow state |
| `priority` | enum(`low`, `medium`, `high`) | default `medium` | Future sorting |
| `due_date` | date | nullable | Optional deadline |
| `created_at` | timestamp | default now | Creation timestamp |
| `updated_at` | timestamp | auto-updated | Last modification |

**Indexes**
- `idx_tasks_user_id` on `user_id` for multi-tenant lookups.
- `idx_tasks_completed_user` on (`user_id`, `status`) to accelerate dashboard queries.

**Relationships**
- Many Tasks → One User (Better Auth). Delete cascades handled via application logic (task deletion when user removed, once future requirements defined).

## Derived Models
Blueprint requires schema documentation only; ORM models are stubbed in `backend/models.py` with SQLModel definitions referencing these fields. No migrations or database connections occur in Phase 2.

## Future Considerations
- Additional tables (audit logs, task comments) will be introduced via new specs.
- When Better Auth is integrated, ensure JWT claims expose `user_id` to associate tasks.
- Neon database provisioning, Alembic migrations, and data retention policies will be handled in later phases per constitution.
