# Data Model: Phase V – Redpanda Cloud Integration + Real-Time Reminders

**Feature**: 009-redpanda-reminders
**Date**: 2025-02-07

---

## Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    Users    │         │    Tasks    │         │  Reminders  │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id (PK)     │────1:N─→│ id (PK)     │←───1:1──│ id (PK)     │
│ email       │         │ user_id FK  │         │ task_id FK  │
│ password    │         │ title       │         │ user_id FK  │
│ created_at  │         │ description │         │ due_time    │
└─────────────┘         │ due_date    │         │ status      │
                        │ priority    │         │ event_pub   │
                        │ completed   │         │ sent_at     │
                        │ recurring   │         │ error_msg   │
                        └─────────────┘         └─────────────┘
                               │
                               │ 1:N
                               ▼
                        ┌─────────────┐
                        │  TaskTags   │
                        ├─────────────┤
                        │ task_id FK  │
                        │ tag_id FK   │
                        └─────────────┘
                               │
                               │ N:1
                               ▼
                        ┌─────────────┐
                        │     Tags    │
                        ├─────────────┤
                        │ id (PK)     │
                        │ name        │
                        │ color       │
                        └─────────────┘
```

---

## Tables

### reminders (NEW)

**Purpose**: Store scheduled reminders for tasks with due times

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | NO | - | Primary key (auto-increment) |
| task_id | INTEGER | NO | - | Foreign key to tasks.id (CASCADE) |
| user_id | INTEGER | NO | - | Foreign key to users.id |
| due_time | TIMESTAMPTZ | NO | - | When reminder should trigger (UTC) |
| status | VARCHAR(20) | NO | 'pending' | pending, sent, failed |
| event_published | BOOLEAN | NO | false | Whether event was published to Redpanda |
| created_at | TIMESTAMPTZ | NO | NOW() | When reminder was created |
| sent_at | TIMESTAMPTZ | YES | - | When reminder was sent |
| error_message | TEXT | YES | - | Error if publish failed |
| retry_count | INTEGER | NO | 0 | Number of retry attempts |

**Constraints**:
- `UNIQUE(task_id)` - One reminder per task
- `FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE`
- `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`

**Indexes**:
- `idx_reminders_due_time` on `(due_time)` WHERE `status = 'pending'`
- `idx_reminders_user_status` on `(user_id, status)`

**State Transitions**:
```
pending → sent
    ↓
  failed
    ↓
pending (after retry)
```

---

### tasks (EXISTING - No Schema Changes)

**Purpose**: Store todo items

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users |
| title | VARCHAR(255) | Task title |
| description | TEXT | Optional description |
| due_date | TIMESTAMPTZ | Optional due date/time (UTC) |
| priority | VARCHAR(20) | Priority: high, medium, low |
| completed | BOOLEAN | Completion status |
| recurring_config | JSONB | Recurrence settings |
| created_at | TIMESTAMPTZ | Creation timestamp |
| updated_at | TIMESTAMPTZ | Last update timestamp |

**Note**: No schema changes needed. Columns already support Phase V requirements.

---

### task_tags (EXISTING - Junction Table)

**Purpose**: Many-to-many relationship between tasks and tags

| Column | Type | Description |
|--------|------|-------------|
| task_id | INTEGER | Foreign key to tasks |
| tag_id | INTEGER | Foreign key to tags |

---

### tags (EXISTING)

**Purpose**: Tag/categories for tasks

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(50) | Tag name |
| color | VARCHAR(7) | Hex color for UI |

---

## Event Schemas

### Reminder Scheduled Event (Published to Redpanda)

**Topic**: `task-events`
**Event Type**: `reminder.scheduled`

```json
{
  "eventType": "reminder.scheduled",
  "eventId": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-02-07T12:00:00Z",
  "data": {
    "reminderId": 123,
    "taskId": 456,
    "userId": 2,
    "dueTime": "2025-02-07T12:03:00Z",
    "taskTitle": "Get medicine",
    "priority": "high",
    "createdAt": "2025-02-07T12:00:00Z"
  }
}
```

### Reminder Triggered Event (Published by Scheduler)

**Topic**: `task-events`
**Event Type**: `reminder.triggered`

```json
{
  "eventType": "reminder.triggered",
  "eventId": "660e8400-e29b-41d4-a716-446655440001",
  "timestamp": "2025-02-07T12:03:00Z",
  "data": {
    "reminderId": 123,
    "taskId": 456,
    "userId": 2,
    "triggeredAt": "2025-02-07T12:03:00Z",
    "taskTitle": "Get medicine",
    "wasOverdue": false
  }
}
```

---

## Validation Rules

### Reminder Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| task_id | Must exist and belong to user_id | "Task not found" |
| due_time | Must be in the future (warning only) | "Warning: Due time is in the past" |
| due_time | Must have time component (not just date) | "Due time must include a specific time" |
| status | Must be one of: pending, sent, failed | "Invalid status" |
| retry_count | Must be < 5 | "Maximum retry attempts exceeded" |

### Task Due Date Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| due_date | If set, must be valid ISO 8601 | "Invalid due date format" |
| priority | Must be: high, medium, low | "Invalid priority" |
| recurring_config | If set, must have valid JSON schema | "Invalid recurring configuration" |

---

## Query Patterns

### Common Queries

**Get pending reminders for user**:
```sql
SELECT r.*, t.title, t.priority
FROM reminders r
JOIN tasks t ON r.task_id = t.id
WHERE r.user_id = $1
  AND r.status = 'pending'
  AND r.due_time <= NOW() + INTERVAL '5 minutes'
ORDER BY r.due_time ASC;
```

**Check if task is overdue**:
```sql
SELECT
  t.id,
  t.due_date < NOW() AS is_overdue,
  r.id IS NOT NULL AS has_reminder,
  r.due_time <= NOW() AS reminder_due
FROM tasks t
LEFT JOIN reminders r ON r.id = t.id
WHERE t.id = $1;
```

**Get tasks with reminder status for frontend**:
```sql
SELECT
  t.*,
  r.id AS reminder_id,
  r.due_time AS reminder_due_time,
  r.status AS reminder_status,
  t.due_date < NOW() AS is_overdue,
  EXTRACT(EPOCH FROM (t.due_date - NOW())) AS seconds_until_due
FROM tasks t
LEFT JOIN reminders r ON t.id = r.task_id
WHERE t.user_id = $1
  AND t.completed = false
ORDER BY t.due_date ASC NULLS LAST, t.priority DESC;
```

---

## Migration SQL

```sql
-- Create reminders table
CREATE TABLE IF NOT EXISTS reminders (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    due_time TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed')),
    event_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    sent_at TIMESTAMPTZ,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0 CHECK (retry_count >= 0),
    UNIQUE(task_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_reminders_due_time
  ON reminders(due_time)
  WHERE status = 'pending';

CREATE INDEX IF NOT EXISTS idx_reminders_user_status
  ON reminders(user_id, status);

-- Add comments
COMMENT ON TABLE reminders IS 'Scheduled reminders for tasks with due times';
COMMENT ON COLUMN reminders.due_time IS 'UTC timestamp when reminder should trigger';
COMMENT ON COLUMN reminders.event_published IS 'Whether event was published to Redpanda Cloud';
```

---

## Data Retention

| Entity | Retention Policy | Purge Method |
|--------|------------------|--------------|
| Reminders (sent) | 30 days after sent_at | Scheduled job |
| Reminders (failed) | 7 days after last retry | Scheduled job |
| Redpanda events | 7 days (Redpanda default) | Automatic |

---

## Session Storage (Frontend)

**Key**: `notified_tasks`

**Schema**:
```typescript
interface NotifiedTask {
  taskId: number;
  notifiedAt: number; // Unix timestamp (ms)
}
```

**Purpose**: Track which reminders have shown toasts to prevent duplicates within 5-minute window.

**Cleanup**: Remove entries older than 5 minutes on each page load.
