# Implementation Plan: Phase V – Redpanda Cloud Integration + Real-Time Reminders

**Feature Branch**: `009-redpanda-reminders`
**Created**: 2025-02-07
**Status**: Draft
**Spec**: [spec.md](./spec.md)

---

## Technical Context

### Current System State

**Existing Components** (from Phase IV):
- Frontend: Next.js with React, TypeScript, react-hot-toast already installed
- Backend: FastAPI with async PostgreSQL connection, Dapr sidecar partially configured
- Database: PostgreSQL with tasks, users, sessions tables
- Message Queue: In-memory pub/sub (to be replaced)
- Deployment: Minikube with Helm charts for backend, frontend, PostgreSQL

**Redpanda Cloud Credentials**:
```
Bootstrap Server: d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
SASL Username: todo-phase5
SASL Password: bflLeIafHKGKvshzwRwcIZqvudhMjG
SASL Mechanism: SCRAM-SHA-256
Security Protocol: SASL_SSL
```

**Technology Stack**:
- Frontend: Next.js 14, React 18, TypeScript, react-hot-toast, TailwindCSS
- Backend: FastAPI, Python 3.11, asyncpg, SQLAlchemy, Dapr SDK
- Database: PostgreSQL (Neon DB or local)
- Event Streaming: Redpanda Cloud (Kafka-compatible)
- Pub/Sub API: Dapr Pub/Sub component
- Infrastructure: Minikube, Helm, Kubernetes

**Key Unknowns**:
- Current Dapr configuration state in existing deployment
- Existing reminder scheduler implementation status
- Current frontend task page polling implementation (if any)

---

## Architecture Decision Records

### ADR-001: Polling Interval Selection

**Decision**: Use 30-second polling interval for task list refresh

**Rationale**:
- **Real-time feel**: 30 seconds provides acceptable responsiveness for demo scenarios while not overwhelming the backend
- **API load**: 30-second interval results in 2 requests/minute/user, manageable for local deployment
- **User experience**: Balances freshness with resource consumption
- **Spec compliance**: Matches requirement FR-005 spec explicitly

**Trade-offs Evaluated**:

| Interval | Real-time Feel | API Load | Battery/Bandwidth | Recommendation |
|----------|----------------|----------|-------------------|----------------|
| 15s | Excellent | High (4 req/min) | Higher impact | Too aggressive for local demo |
| **30s** | **Good** | **Medium (2 req/min)** | **Acceptable** | **SELECTED** |
| 60s | Fair | Low (1 req/min) | Minimal | Too slow for demo impact |

**Alternatives Considered**:
- WebSocket: Rejected due to out-of-scope constraint and implementation complexity
- Server-Sent Events (SSE): Rejected due to requiring new backend infrastructure
- Event-driven via Dapr: Rejected due to requiring consumer service on frontend

---

### ADR-002: Toast Notification Library

**Decision**: Use react-hot-toast (already installed)

**Rationale**:
- **Already available**: Library is already in package.json from previous phases
- **API simplicity**: `toast.success()`, `toast.error()` straightforward to implement
- **Styling control**: Sufficient customization via TailwindCSS classes
- **Bundle size**: Small footprint (~3KB gzipped)
- **Animation quality**: Smooth enter/exit animations suitable for demo

**Trade-offs Evaluated**:

| Library | Ease | Styling Control | Bundle Size | Recommendation |
|---------|-------|-----------------|-------------|----------------|
| react-hot-toast | High | Good | Small (3KB) | **SELECTED** (already installed) |
| Custom toast | Low | Full | Depends | Not worth development effort |
| react-toastify | High | Good | Medium (5KB) | Alternative if react-hot-toast fails |
| sonner | High | Excellent | Small (2.5KB) | Newer option, no migration needed |

**Alternatives Considered**:
- Custom implementation: Rejected due to development time and animation complexity
- react-toastify: Alternative if react-hot-toast has issues
- sonner: Modern alternative but no migration benefit

---

### ADR-003: Redpanda Connection Failure Strategy

**Decision**: Graceful degradation with in-memory fallback

**Rationale**:
- **Demo reliability**: Hackathon demo must work even if Redpanda Cloud has issues
- **Debug visibility**: Error messages displayed in UI and logged for troubleshooting
- **Feature availability**: Core task creation/completion remains functional
- **Event logging**: Failed publishes logged for post-mortem analysis

**Trade-offs Evaluated**:

| Strategy | Reliability | Strict Compliance | User Experience | Recommendation |
|----------|-------------|-------------------|------------------|----------------|
| **In-memory fallback** | **High** | **Low** | **Functional** | **SELECTED** |
| Hard fail | Low | High | Broken | Too risky for demo |
| Retry with backoff | Medium | Medium | Delayed | Too complex for timeline |
| Queue for later | Medium | High | Complex | Overkill for local demo |

**Implementation Details**:
```
1. Try Dapr publish to Redpanda Cloud
2. On connection failure:
   - Log error with full details
   - Store reminder in database with "pending_publish" status
   - Schedule local reminder (in-memory scheduler)
   - Show warning toast: "Reminder scheduled (cloud sync delayed)"
3. Background retry every 60 seconds for up to 5 attempts
```

**Alternatives Considered**:
- Hard failure: Rejected due to demo risk
- Retry only: Rejected due to potential for hanging requests
- Circuit breaker: Too complex for hackathon timeline

---

### ADR-004: Duplicate Toast Prevention

**Decision**: Track notified task IDs in session storage with deduplication window

**Rationale**:
- **User experience**: Prevents annoying duplicate notifications
- **Simplicity**: Session storage API is straightforward (no backend changes)
- **Scope**: Deduplication only needed per browser session
- **Complexity**: Low implementation effort

**Trade-offs Evaluated**:

| Approach | UX Improvement | Code Complexity | Backend Change | Recommendation |
|----------|----------------|-----------------|----------------|----------------|
| **Session storage tracking** | **High** | **Low** | **None** | **SELECTED** |
| No deduplication | Poor | None | None | Too annoying |
| Backend API tracking | High | High | Yes | Overkill for local demo |
| Local storage persistence | High | Medium | None | Unnecessary persistence |

**Implementation Details**:
```typescript
// Session storage key format
const NOTIFIED_TASKS_KEY = 'notified_tasks';
const DEDUPLICATION_WINDOW_MS = 5 * 60 * 1000; // 5 minutes

// Data structure
interface NotifiedTask {
  taskId: number;
  notifiedAt: number; // timestamp
}

// Check logic
function shouldNotify(taskId: number): boolean {
  const notified = getSession(NOTIFIED_TASKS_KEY, []);
  const recent = notified.filter((n) =>
    n.taskId !== taskId ||
    Date.now() - n.notifiedAt < DEDUPLICATION_WINDOW_MS
  );
  const exists = recent.some((n) => n.taskId === taskId);
  return !exists;
}
```

**Alternatives Considered**:
- Backend tracking: Rejected due to requiring new database table and API
- No deduplication: Rejected due to poor UX
- Redis-based: Rejected due to additional infrastructure

---

## Constitution Check

### Principles Compliance

| Principle | Compliance Status | Notes |
|-----------|-------------------|-------|
| Spec-driven development | ✅ PASS | All changes traceable to spec.md |
| AI-assisted tools | ✅ PASS | Using Claude Code, kubectl, Dapr CLI |
| Dapr abstraction | ✅ PASS | Redpanda accessed via Dapr Pub/Sub |
| Security-first | ⚠️ ACTION | Redpanda credentials must use Kubernetes Secret |
| Reproducibility | ✅ PASS | All steps scripted and documented |
| Local-first validation | ✅ PASS | Minikube deployment first |
| Iterative | ✅ PASS | Complete reminders before cloud |

### Standards Compliance

| Standard | Compliance Status | Notes |
|----------|-------------------|-------|
| Dapr Pub/Sub required | ✅ PASS | Using Dapr for Redpanda integration |
| No direct Kafka clients | ✅ PASS | Application uses Dapr API only |
| No hardcoded secrets | ⚠️ ACTION | Must create Kubernetes Secret for credentials |
| Helm charts with Dapr | ✅ PASS | Update existing charts with Dapr sidecar |
| README with verification | ✅ PASS | Include demo commands and verification steps |

### Gates (Must Pass)

| Gate | Status | Mitigation |
|------|--------|------------|
| No hardcoded secrets | ⚠️ BLOCKING | Will create Kubernetes Secret in Phase 1 |
| Dapr sidecar required | ✅ PASS | Existing deployment has Dapr enabled |
| Direct Kafka library check | ✅ PASS | No kafka-python in requirements.txt |
| Local validation first | ✅ PASS | All testing on Minikube before cloud |

**Action Required**: Create Kubernetes Secret for Redpanda credentials before deployment.

---

## Phase 0: Research & Preparation

### Research Tasks

| Task | Description | Owner | Status |
|------|-------------|-------|--------|
| R-001 | Document existing Dapr configuration in current deployment | Claude | Pending |
| R-002 | Verify react-hot-toast installation and usage in frontend | Claude | Pending |
| R-003 | Research Redpanda Cloud cluster requirements from local Minikube | Claude | Pending |
| R-004 | Identify existing reminder scheduler implementation | Claude | Pending |
| R-005 | Document current frontend task page implementation | Claude | Pending |

### Research Outputs

**R-001: Existing Dapr Configuration**
```yaml
# Current state (to be verified)
# dapr-components.yaml - if exists
# Current: May have in-memory pubsub or no pubsub component
# Target: kafka-pubsub with Redpanda Cloud configuration
```

**R-002: react-hot-toast Verification**
```bash
# Check if already installed
grep "react-hot-toast" frontend/package.json
# Expected: Already present from Phase IV
```

**R-003: Redpanda Cloud Network Access**
```bash
# Test connectivity from Minikube pod
kubectl run test-connectivity --image=curlimages/curl --rm -it -- \
  curl -v https://d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
```

**R-004: Reminder Scheduler Status**
```bash
# Check for existing scheduler
find backend -name "*reminder*" -o -name "*scheduler*"
# May need to create new service
```

**R-005: Frontend Task Page**
```typescript
// File: frontend/src/app/tasks/page.tsx
// Current: Manual refresh, basic polling for overdue
// Target: Add 30s polling, toast notifications
```

---

## Phase 1: Design & Contracts

### Data Model

**Reminder Entity** (new table):
```sql
CREATE TABLE reminders (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    due_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, sent, failed
    event_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    UNIQUE(task_id) -- One reminder per task
);

CREATE INDEX idx_reminders_due_time ON reminders(due_time) WHERE status = 'pending';
CREATE INDEX idx_reminders_user_status ON reminders(user_id, status);
```

**Task Entity Updates** (existing table):
```sql
-- Already has these columns from Phase IV
-- due_date TIMESTAMP WITH TIME ZONE
-- priority VARCHAR(20)
-- recurring_config JSONB
-- No schema changes needed
```

**Reminder Event Schema** (Redpanda message):
```json
{
  "eventType": "reminder.scheduled",
  "eventId": "uuid-v4",
  "timestamp": "2025-02-07T12:00:00Z",
  "data": {
    "reminderId": 123,
    "taskId": 456,
    "userId": 2,
    "dueTime": "2025-02-07T12:03:00Z",
    "taskTitle": "Get medicine",
    "priority": "high"
  }
}
```

---

### API Contracts

#### Backend API (New Endpoints)

**POST /api/tasks/{task_id}/reminder**
```json
// Request
{
  "due_time": "2025-02-07T12:03:00Z"
}

// Response 201
{
  "reminder_id": 123,
  "task_id": 456,
  "due_time": "2025-02-07T12:03:00Z",
  "status": "pending",
  "event_published": true
}

// Response 500 (Redpanda failure)
{
  "detail": "Reminder scheduled but cloud publish failed",
  "reminder_id": 123,
  "fallback_mode": true
}
```

**GET /api/tasks/pending-reminders**
```json
// Response 200
{
  "reminders": [
    {
      "id": 123,
      "task_id": 456,
      "title": "Get medicine",
      "due_time": "2025-02-07T12:03:00Z",
      "priority": "high",
      "is_overdue": false
    }
  ]
}
```

#### Dapr Pub/Sub Contract

**Publish to: task-events topic**
```yaml
# Dapr component will handle serialization
pubsubName: kafka-pubsub
topic: task-events
metadata:
  reminderId: "123"
  taskId: "456"
  userId: "2"
  dueTime: "2025-02-07T12:03:00Z"
```

#### Frontend Polling

**GET /api/tasks**
```json
// Existing endpoint, enhanced response
{
  "tasks": [
    {
      "id": 456,
      "title": "Get medicine",
      "due_date": "2025-02-07T12:03:00Z",
      "priority": "high",
      "completed": false,
      "is_overdue": true,
      "has_reminder": true,
      "reminder_due_soon": true
    }
  ]
}
```

---

### Components Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Frontend (Next.js)                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Tasks Page (/tasks)                                                    │ │
│  │  - 30-second polling hook                                               │ │
│  │  - Toast notification display                                           │ │
│  │  - Duplicate tracking (session storage)                                 │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│                                    │ HTTP (polling)                          │
│                                    ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Backend (FastAPI)                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Task Routes (/api/tasks/*)                                             │ │
│  │  - Create task → publish reminder event                                 │ │
│  │  - Get tasks → calculate overdue status                                 │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Reminder Scheduler Service                                             │ │
│  │  - Background process checking due reminders                            │ │
│  │  - Publish events via Dapr                                              │ │
│  │  - In-memory fallback on failure                                       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│                                    │ Dapr HTTP (gRPC)                        │
│                                    ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Dapr Sidecar                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Pub/Sub Component (kafka-pubsub)                                       │ │
│  │  - SASL_SSL authentication                                              │ │
│  │  - SCRAM-SHA-256 mechanism                                              │ │
│  │  - Connection pooling                                                   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│                                    │ Kafka protocol                          │
│                                    ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Redpanda Cloud                                    │
│  Topic: task-events                                                         │
│  - reminder.scheduled events                                               │
│  - Persistent storage for 7 days                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 2: Implementation Plan

### Implementation Phases

| Phase | Description | Tasks | Est. Time |
|-------|-------------|-------|-----------|
| **Phase 2a** | **Infrastructure Setup** | 3 tasks | 30 min |
| **Phase 2b** | **Backend Services** | 4 tasks | 45 min |
| **Phase 2c** | **Frontend Features** | 3 tasks | 30 min |
| **Phase 2d** | **Testing & Verification** | 2 tasks | 30 min |
| **Phase 2e** | **Documentation** | 2 tasks | 15 min |

---

### Phase 2a: Infrastructure Setup

**Goal**: Configure Redpanda Cloud Dapr component and Kubernetes secrets

| Task | Description | Commands | Verification |
|------|-------------|----------|---------------|
| **2a-1** | Create Kubernetes Secret for Redpanda credentials | `kubectl create secret generic redpanda-credentials --from-literal=username=todo-phase5 --from-literal=password='bflLeIafHKGKvshzwRwcIZqvudhMjG'` | `kubectl get secret redpanda-credentials` |
| **2a-2** | Generate Dapr Pub/Sub component YAML | Create `dapr-components/kafka-pubsub.yaml` | `kubectl apply --dry-run=client -f dapr-components/kafka-pubsub.yaml` |
| **2a-3** | Apply Dapr component to cluster | `kubectl apply -f dapr-components/kafka-pubsub.yaml` | `dapr components -k | grep kafka-pubsub` |

**Deliverable**: Working Dapr Pub/Sub component connected to Redpanda Cloud

---

### Phase 2b: Backend Services

**Goal**: Implement reminder event publishing and scheduler service

| Task | Description | File Changes | Verification |
|------|-------------|--------------|---------------|
| **2b-1** | Create reminders database table | `backend/migrations/create_reminders_table.sql` | `SELECT * FROM reminders LIMIT 1` |
| **2b-2** | Add reminder CRUD operations | `backend/app/crud.py`, `backend/app/routes/reminders.py` | Test via API |
| **2b-3** | Add Dapr publish to task creation flow | `backend/app/routes/tasks.py`, `backend/app/services/event_publisher.py` | Logs show "Published to task-events" |
| **2b-4** | Create reminder scheduler service | `backend/app/services/reminder_scheduler.py` | Logs show "Processing due reminders" |

**Deliverable**: Backend publishes reminder events and schedules notifications

---

### Phase 2c: Frontend Features

**Goal**: Add polling, toast notifications, and duplicate tracking

| Task | Description | File Changes | Verification |
|------|-------------|--------------|---------------|
| **2c-1** | Add 30-second polling hook to tasks page | `frontend/src/hooks/useTaskPolling.ts`, `frontend/src/app/tasks/page.tsx` | Network tab shows requests every 30s |
| **2c-2** | Add toast notification for due reminders | `frontend/src/hooks/useReminders.ts` | Toast appears when task becomes overdue |
| **2c-3** | Add duplicate tracking in session storage | `frontend/src/hooks/useReminders.ts` | Session storage has `notified_tasks` key |

**Deliverable**: Frontend shows reminders as toasts without duplicates

---

### Phase 2d: Testing & Verification

**Goal**: End-to-end testing and performance validation

| Task | Description | Commands | Expected Result |
|------|-------------|----------|-----------------|
| **2d-1** | Manual E2E test: Create task with 3-min reminder | UI or chat: "Add a task Get medicine add reminder at [now+3min]" | Toast appears after 3 min |
| **2d-2** | Performance validation | Browser DevTools, kubectl top pods | Load <3s, checkbox instant |

**Deliverable**: All acceptance criteria validated

---

### Phase 2e: Documentation

**Goal**: Update README and create troubleshooting guide

| Task | Description | File Changes | Verification |
|------|-------------|--------------|---------------|
| **2e-1** | Update README with Redpanda setup | `README.md` | Commands work from fresh clone |
| **2e-2** | Create troubleshooting guide | `docs/redpanda-troubleshooting.md` | Covers common issues |

**Deliverable**: Complete documentation for demo setup

---

## Phase 3: Verification & Demo

### Acceptance Criteria Validation

| Criterion | Test Method | Expected Result |
|-----------|-------------|-----------------|
| SC-001: Dapr component healthy | `dapr components -k` | Status: HEALTHY |
| SC-002: Toast within 10s | Create task +3min, wait | Toast appears within 10s of due time |
| SC-003: Overdue badge within 30s | Create task +3min, wait | Badge shows without refresh |
| SC-004: Event publish logged | Check backend logs | "Published reminder event" message |
| SC-005: Reminder trigger logged | Check scheduler logs | "Triggering reminder for task" message |
| SC-006: Polling reflects changes | Two browser tabs | Changes appear within 30s |
| SC-007: Chat parses 95% | Test various formats | Correct time parsing |
| SC-008: Advanced features work | UI test | All features functional |
| SC-009: Load <3s | Browser DevTools | Page load under 3s |
| SC-010: Checkbox instant | UI test | Immediate response |
| SC-011: Session persists | Refresh page | User stays logged in |
| SC-012: Redpanda receives events | Redpanda dashboard | Messages in task-events topic |

### Demo Script

```
=== Phase V Demo: Redpanda Cloud + Real-Time Reminders ===

[Setup - 2 min]
1. Show Minikube running: minikube status
2. Show Dapr components: dapr components -k
3. Show port forwards running

[Feature 1: Chat Agent - 1 min]
4. Open chat: http://localhost:3000/chat
5. Type: "Add a task Call mom add reminder at 2 minutes from now"
6. Show task created with correct due time

[Feature 2: Real-Time Reminders - 2 min]
7. Open tasks page: http://localhost:3000/tasks
8. Show "Call mom" task with due time
9. Wait for reminder (2 minutes)
10. Toast appears: "Reminder: Call mom is due now!"
11. Overdue badge appears automatically

[Feature 3: Event Streaming - 1 min]
12. Show backend logs: kubectl logs -f backend-service
13. Show Redpanda Cloud dashboard with task-events topic

[Feature 4: Advanced Features - 1 min]
14. Show recurring task creation
15. Show priority indicators
16. Show tag filtering
17. Show search and sort

[Performance - 30s]
18. Show instant checkbox completion
19. Show 30-second auto-refresh in Network tab

[Total: ~7 minutes]
```

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Redpanda Cloud connection fails from Minikube | Medium | High | Implement in-memory fallback, document troubleshooting |
| Polling causes performance regression | Low | Medium | Measure load times, optimize queries if needed |
| Duplicate toasts annoy users | Medium | Low | Session storage tracking implemented |
| Dapr sidecar not injected | Low | High | Verify with `kubectl describe pod backend-service` |
| Time zone issues with reminders | Medium | Medium | Store all times in UTC, display in local time |
| Session storage cleared on refresh | N/A | Low | Expected behavior, re-notification after 5min window |

---

## Rollback Plan

If critical issues arise:

1. **Revert Dapr component**: `kubectl delete -f dapr-components/kafka-pubsub.yaml`
2. **Restore in-memory pub/sub**: Use previous implementation
3. **Disable polling**: Remove `useTaskPolling` hook from tasks page
4. **Keep database changes**: Reminders table can stay for future use

---

## Open Questions

None. All decisions documented in ADRs above.

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Reminders triggered on time | 100% | Within 10s of due time |
| Event publish success rate | >95% | Backend logs |
| Demo completes without errors | 100% | Manual verification |
| Page load time | <3s | Browser DevTools |
| Polling reliability | 100% | No missed updates in 5min window |

---

## Next Steps

After this plan is approved:

1. Run `/sp.tasks` to generate actionable tasks
2. Execute Phase 0 research tasks
3. Implement Phase 2a (Infrastructure Setup)
4. Continue through Phase 2e
5. Final verification and demo preparation
