# Data Model & Contracts: Local E2E Testing & Polish

**Feature**: 001-local-e2e-polish
**Created**: 2026-02-02

## Test Scenario Entities

### E2ETestScenario
Represents an end-to-end test case with steps and validation criteria.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | string | Unique scenario identifier (e.g., "E2E-001") |
| name | string | Human-readable test name |
| area | string | Testing area (health, features, events, dapr, polish, docs) |
| priority | string | P1, P2, P3 priority level |
| steps | array | Ordered list of test steps |
| expected_results | array | Expected outcomes for each step |
| validation_method | string | How to validate (manual, automated, log_check) |
| status | string | pending, passed, failed, skipped |

### TestStep
Individual step within a test scenario.

| Attribute | Type | Description |
|-----------|------|-------------|
| step_number | integer | Sequential order within scenario |
| action | string | Action to perform (command, UI action) |
| command | string | Optional kubectl/curl command |
| expected_outcome | string | Expected result |

### BugReport
Issue discovered during testing with tracking information.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | string | Unique bug identifier (e.g., "BUG-001") |
| title | string | Brief bug description |
| description | string | Full bug description |
| severity | string | critical, high, medium, low |
| area | string | Component area (frontend, backend, dapr, consumer) |
| reproduction_steps | array | Steps to reproduce the bug |
| actual_behavior | string | What actually happened |
| expected_behavior | string | What should have happened |
| status | string | open, in_progress, fixed, verified, deferred |
| fix_description | string | Description of the fix applied |

### LogEntry
Structured log entry for debugging and verification.

| Attribute | Type | Description |
|-----------|------|-------------|
| timestamp | string | ISO 8601 timestamp |
| level | string | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| component | string | Service component (backend, consumer, dapr) |
| request_id | string | Unique request correlation ID |
| message | string | Human-readable log message |
| context | object | Additional structured context data |
| error | object | Error details (stack trace, error type) if applicable |

### VerificationCommand
Automated health check command.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | string | Command identifier |
| name | string | Human-readable name |
| command | string | kubectl or curl command |
| expected_output | string | Expected result pattern |
| validation_method | string | exit_code, grep, json_path |

## Documentation Entities

### READMESection
Documentation section in README.

| Attribute | Type | Description |
|-----------|------|-------------|
| section | string | Section name (setup, verification, troubleshooting) |
| title | string | Section heading |
| content | string | Markdown content |
| code_blocks | array | Code/command examples |

### DemoStep
Individual step in demo script.

| Attribute | Type | Description |
|-----------|------|-------------|
| step_number | integer | Sequential order |
| action | string | Action description |
| ui_action | string | User interface action |
| expected_result | string | What user should see |
| command | string | Optional background command |
| log_reference | string | Log excerpt to show |
| screenshot | string | Screenshot reference |
| duration_seconds | integer | Estimated duration |
| cumulative_time | integer | Cumulative time to this step |

## Existing Data Entities (from Phase V)

### Task
Core todo entity.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | uuid | Unique task identifier |
| user_id | uuid | Owner user ID |
| title | string | Task title |
| description | string | Optional detailed description |
| priority | string | high, medium, low |
| due_date | datetime | Optional due date for reminder |
| tags | array | String tags for categorization |
| recurrence_rule | object | Recurrence pattern (daily, weekly) |
| recurrence_instance | integer | Instance number for recurring tasks |
| parent_task_id | uuid | Parent for recurring task instances |
| completed | boolean | Task completion status |
| completed_at | datetime | When task was completed |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### TaskEvent
Event published on task changes.

| Attribute | Type | Description |
|-----------|------|-------------|
| event_id | uuid | Unique event identifier |
| event_type | string | task.created, task.updated, task.deleted, task.completed |
| task_id | uuid | Related task ID |
| user_id | uuid | User who triggered the event |
| timestamp | datetime | Event timestamp |
| data | object | Full task data snapshot |

### Reminder
Scheduled reminder for task due date.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | uuid | Unique reminder identifier |
| task_id | uuid | Related task ID |
| due_date | datetime | When to remind |
| job_name | string | Dapr Jobs API job name |
| status | string | scheduled, fired, cancelled |
| fired_at | datetime | When reminder was triggered |

### AuditLog
Audit trail entry for event processing.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | uuid | Unique log entry identifier |
| event_id | uuid | Related event ID |
| consumer | string | Which consumer processed it |
| processed_at | datetime | Processing timestamp |
| action_taken | string | What action was performed |
| result | string | success, failure |

## Test Area Organization

```
E2E Testing Areas:
├── Area 1: Basic Health & Access
│   ├── Pod status verification
│   ├── Service accessibility
│   └── Health endpoint checks
│
├── Area 2: Advanced Features
│   ├── Recurring tasks (create, complete, next instance)
│   ├── Due dates & reminders
│   ├── Priorities & tags
│   └── Search, filter, sort
│
├── Area 3: Event-Driven Flow
│   ├── Event publishing verification
│   ├── Consumer processing logs
│   └── End-to-end event tracing
│
├── Area 4: Dapr Validation
│   ├── Sidecar health checks
│   ├── Component verification
│   ├── Jobs API testing
│   └── Secrets loading validation
│
├── Area 5: Bug Fixes & Polish
│   ├── Error handling improvements
│   ├── Logging enhancements
│   └── UX refinements
│
└── Area 6: Documentation & Demo Prep
    ├── README updates
    ├── Verification commands
    └── Demo script creation
```

## State Transitions

### BugReport State Machine
```
open → in_progress → fixed → verified
  ↓                          ↓
deferred ←──────────────────┘
```

### E2ETestScenario State Machine
```
pending → passed
   ↓
failed → passed (after fix)
   ↓
skipped
```

## Key Relationships

```
Task (1) ←→ (N) TaskEvent
Task (1) ←→ (1) Reminder
TaskEvent (1) ←→ (N) AuditLog
User (1) ←→ (N) Task
Task (1) ←→ (N) Task (recurring instances)
```

## Validation Patterns

### Log Pattern Matching
- Event published: `"event_type": "task.created"`
- Consumer processed: `"action_taken": "created_next_instance"`
- Error occurred: `"level": "ERROR"`
- Dapr sidecar healthy: `"dapr_sidecar": "running"`

### kubectl Output Patterns
- All pods running: `STATUS=Running`
- Sidecar present: Container count includes `daprd`
- Service exposed: `TYPE=LoadBalancer`
- Component loaded: `STATUS=Loaded` in `kubectl get components.dapr.io`

## Quick Reference: Verification Commands

| Purpose | Command | Expected Pattern |
|---------|---------|------------------|
| Pod health | `kubectl get pods` | All Running, 1/1 Ready |
| Sidecars present | `kubectl get pods -o jsonpath='{...}'` | daprd in containers list |
| Dapr status | `dapr status -k` | All apps HEALTHY |
| Components | `kubectl get components.dapr.io` | STATUS=Loaded |
| Service URL | `minikube service todo-frontend --url` | http://192.168.x.x:x |
| Health check | `curl $URL/health` | HTTP 200 |
| Event log | `kubectl logs deployment/todo-consumers` | "event_type": "task.created" |
| Errors only | `kubectl logs deployment/todo-backend \| grep -i error` | No critical errors |
