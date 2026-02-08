# Log Examples for Phase V Event-Driven Architecture

This document provides example log outputs for verification and demo purposes.

---

## Successful Event Flow Examples

### 1. Task Created Event

**Backend Log (Event Publishing)**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:30:45.123456",
  "component": "backend",
  "logger_name": "backend.app.main",
  "request_id": "req-abc123-456def-789ghi",
  "event_type": "task.created",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-123",
  "title": "Daily Standup",
  "priority": "high",
  "tags": ["work"],
  "due_date": "2026-02-03T09:00:00Z",
  "recurrence_rule": "daily",
  "message": "Task created event published to pubsub"
}
```

**Consumer Log (Recurring Task Consumer Processing)**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:30:45.234567",
  "component": "recurring-task-consumer",
  "logger_name": "consumers.recurring",
  "request_id": "req-abc123-456def-789ghi",
  "event_id": "evt-987xyz-654abc-321def",
  "event_type": "task.created",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "action_taken": "checked for recurrence",
  "recurrence_found": true,
  "recurrence_rule": "daily",
  "message": "Task has daily recurrence - will create next instance on completion"
}
```

**Consumer Log (Notification Consumer Processing)**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:30:45.345678",
  "component": "notification-consumer",
  "logger_name": "consumers.notification",
  "request_id": "req-abc123-456def-789ghi",
  "event_id": "evt-987xyz-654abc-321def",
  "event_type": "task.created",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "action_taken": "scheduled reminder",
  "due_date": "2026-02-03T09:00:00Z",
  "job_name": "reminder-550e8400-e29b-41d4-a716-446655440000",
  "message": "Reminder job scheduled via Dapr Jobs API"
}
```

**Consumer Log (Audit Consumer Processing)**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:30:45.456789",
  "component": "audit-consumer",
  "logger_name": "consumers.audit",
  "request_id": "req-abc123-456def-789ghi",
  "event_id": "evt-987xyz-654abc-321def",
  "event_type": "task.created",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "action_taken": "logged",
  "table": "audit_log",
  "message": "Task creation event recorded in audit trail"
}
```

### 2. Task Completed Event

**Backend Log (Event Publishing)**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:31:30.123456",
  "component": "backend",
  "logger_name": "backend.app.main",
  "request_id": "req-def456-789ghi-012jkl",
  "event_type": "task.completed",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-123",
  "title": "Daily Standup",
  "completed_at": "2026-02-02T10:31:30Z",
  "message": "Task completed event published to pubsub"
}
```

**Consumer Log (Next Instance Created)**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:31:30.234567",
  "component": "recurring-task-consumer",
  "logger_name": "consumers.recurring",
  "request_id": "req-def456-789ghi-012jkl",
  "event_id": "evt-111aaa-222bbb-333ccc",
  "event_type": "task.completed",
  "parent_task_id": "550e8400-e29b-41d4-a716-446655440000",
  "action_taken": "created_next_instance",
  "new_task_id": "660f9501-f30c-52e5-b827-557766551111",
  "new_title": "Daily Standup",
  "new_due_date": "2026-02-03T09:00:00Z",
  "recurrence_instance": 2,
  "message": "Next instance created for recurring task"
}
```

### 3. Reminder Fired Event

**Dapr Jobs API Callback Log**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-03T09:00:00.123456",
  "component": "dapr-jobs",
  "logger_name": "dapr.jobs",
  "job_name": "reminder-550e8400-e29b-41d4-a716-446655440001",
  "task_id": "550e8400-e29b-41d4-a716-446655440001",
  "event_type": "reminder.triggered",
  "message": "Reminder job triggered at scheduled time",
  "callback_status": "success"
}
```

**Consumer Log (Reminder Processed)**:
```json
{
  "level": "INFO",
  "timestamp": "2026-02-03T09:00:00.234567",
  "component": "notification-consumer",
  "logger_name": "consumers.notification",
  "request_id": "job-reminder-550e8400",
  "task_id": "550e8400-e29b-41d4-a716-446655440001",
  "event_type": "reminder.fired",
  "action_taken": "sent_notification",
  "notification_type": "due_date_reminder",
  "message": "Reminder notification sent for task"
}
```

---

## Dapr Sidecar Logs

### Dapr Sidecar Initialization

```
INFO[0000] Dapr sidecar is starting
INFO[0000] Dapr runtime version: 1.13.0
INFO[0000] App id: todo-backend listening on port 3500
INFO[0000] Dapr HTTP server is running on port 3500
INFO[0000] Metadata: [app-id: todo-backend]
INFO[0000] Actor runtime started
INFO[0000] Loaded components:
  - pubsub.kafka-pubsub
  - state.postgresql
  - secret.kubernetes
```

### Dapr Component Health

**PubSub Component (Kafka)**:
```
INFO[0001] Component kafka-pubsub is healthy
INFO[0001] Connected to Kafka broker: kafka.kafka.svc.cluster.local:9092
INFO[0001] Topic check: todo-events topic exists
```

**State Store Component (PostgreSQL)**:
```
INFO[0002] Component postgresql is healthy
INFO[0002] Connected to PostgreSQL: postgres-mcp-service.default.svc.cluster.local:5432
INFO[0002] State store initialized: todo-state
```

**Secret Store Component (Kubernetes)**:
```
INFO[0003] Component kubernetes is healthy
INFO[0003] Loaded secrets from Kubernetes secrets
INFO[0003] Secret access configured for namespace: default
```

---

## Health Check Examples

### Backend Health Check

**Request**:
```bash
curl http://localhost:8000/health
```

**Success Response**:
```json
{
  "status": "healthy",
  "service": "backend",
  "version": "1.0.0",
  "timestamp": "2026-02-02T10:30:00Z",
  "dapr_status": "connected"
}
```

### Frontend Health Check

**Request**:
```bash
curl http://localhost:3000/health
```

**Success Response**:
```json
{
  "status": "healthy",
  "service": "frontend",
  "version": "1.0.0",
  "timestamp": "2026-02-02T10:30:00Z",
  "api_connection": "ready"
}
```

---

## Error Examples (For Troubleshooting)

### Database Connection Error

```json
{
  "level": "ERROR",
  "timestamp": "2026-02-02T10:30:45.123456",
  "component": "backend",
  "logger_name": "backend.app.database",
  "request_id": "req-error-123",
  "error": {
    "type": "ConnectionError",
    "message": "Could not connect to database",
    "details": "Connection refused to postgres-mcp-service.default.svc.cluster.local:5432"
  },
  "message": "Database connection failed"
}
```

### Kafka Connection Error

```json
{
  "level": "ERROR",
  "timestamp": "2026-02-02T10:30:45.123456",
  "component": "backend",
  "logger_name": "backend.app.kafka",
  "request_id": "req-error-456",
  "error": {
    "type": "KafkaError",
    "message": "Failed to publish event to Kafka",
    "details": "Connection refused to kafka-0.kafka.kafka.svc.cluster.local:9092"
  },
  "message": "Event publishing failed"
}
```

### Dapr Sidecar Error

```
ERRO[0000] Error connecting to placement service
ERRO[0000] Failed to initialize sidecar
ERRO[0000] Retrying in 5 seconds...
```

---

## kubectl Commands for Log Retrieval

### View Recent Logs

```bash
# Backend logs (last 50 lines)
kubectl logs deployment/todo-backend --tail=50

# Consumer logs (last 100 lines)
kubectl logs deployment/todo-consumers --tail=100

# Frontend logs (last 30 lines)
kubectl logs deployment/todo-frontend --tail=30
```

### Follow Logs in Real-Time

```bash
# Follow backend logs
kubectl logs deployment/todo-backend -f

# Follow consumer logs
kubectl logs deployment/todo-consumers -f

# Follow Dapr sidecar logs only
kubectl logs deployment/todo-backend -c daprd -f
```

### Search Logs for Patterns

```bash
# Search for errors
kubectl logs deployment/todo-backend | grep -i "error"

# Search for specific event types
kubectl logs deployment/todo-consumers | grep "task.created"

# Search for Dapr activity
kubectl logs deployment/todo-backend -c daprd | grep "Component"

# Count occurrences
kubectl logs deployment/todo-consumers | grep -c "INFO"
```

### Logs from Multiple Containers

```bash
# All logs from backend (app + sidecar)
kubectl logs deployment/todo-backend --all-containers=true --tail=50

# Only Dapr sidecar logs
kubectl logs deployment/todo-backend -c daprd --tail=50

# Only application container logs
kubectl logs deployment/todo-backend -c todo-backend --tail=50
```

---

## Log Analysis Quick Reference

### Successful Flow Indicators

| Component | Success Indicator |
|-----------|-------------------|
| Backend | `"event_type": "task.created"` |
| Recurring Consumer | `"action_taken": "created_next_instance"` |
| Notification Consumer | `"action_taken": "scheduled reminder"` |
| Audit Consumer | `"action_taken": "logged"` |
| Dapr Sidecar | `"Connected to Kafka broker"` |
| Jobs API | `"callback_status": "success"` |

### Problem Indicators

| Issue | Log Pattern |
|-------|-------------|
| Database down | `"Could not connect to database"` |
| Kafka down | `"Connection refused to kafka"` |
| Dapr unhealthy | `"ERRO[0000] Error connecting"` |
| Event publish failed | `"Event publishing failed"` |
| Consumer error | `"error": { ... }` |
| Connection refused | `"Connection refused"` |

---

## Log Levels and Their Meanings

| Level | Usage | Example |
|-------|---------|---------|
| **DEBUG** | Detailed diagnostic information | Function entry/exit, variable values |
| **INFO** | Normal operational events | Task created, event published, job scheduled |
| **WARNING** | Unexpected but non-critical issues | Retry attempt, fallback behavior |
| **ERROR** | Error that affects functionality | Connection failed, event publish failed |
| **CRITICAL** | Severe error requiring immediate attention | Database connection lost, service unavailable |

---

## Using Logs for Demo

### Prepare Log Files Before Demo

```bash
# Export recent logs to files for easy access
kubectl logs deployment/todo-consumers --tail=200 > demo/consumer-logs.txt
kubectl logs deployment/todo-backend --tail=200 > demo/backend-logs.txt

# Search for specific patterns
kubectl logs deployment/todo-consumers | grep "task.created" > demo/created-events.txt
kubectl logs deployment/todo-consumers | grep "reminder" > demo/reminders.txt
```

### Real-Time Log Monitoring During Demo

```bash
# Open terminal window 1: Watch consumer logs
kubectl logs deployment/todo-consumers -f | grep "event"

# Open terminal window 2: Watch for errors
kubectl logs deployment/todo-backend -f | grep -i "error"

# Open terminal window 3: Watch Dapr status
watch kubectl get pods
```

---

## Notes

- All timestamps in ISO 8601 format
- JSON structured logging for easy parsing
- Request IDs for correlation across services
- Component names identify the source service
- Event types follow pattern: `entity.action` (e.g., `task.created`)
