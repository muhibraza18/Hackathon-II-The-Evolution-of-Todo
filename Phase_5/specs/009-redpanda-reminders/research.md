# Research Findings: Phase V – Redpanda Cloud Integration + Real-Time Reminders

**Feature**: 009-redpanda-reminders
**Date**: 2025-02-07
**Status**: Complete

---

## R-001: Existing Dapr Configuration

**Finding**: Current deployment has Dapr partially configured

**Evidence**:
```bash
# Check current Dapr components
kubectl get components -n default
# Result: No components found (in-memory or none)

# Check Dapr sidecar injection
kubectl describe pod backend-service-xxxxx | grep dapr
# Result: No Dapr annotations found on backend deployment
```

**Decision**: Need to enable Dapr sidecar injection on backend deployment

**Action**: Add Dapr annotations to backend Helm chart:
```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "todo-backend"
  dapr.io/app-port: "8000"
```

---

## R-002: react-hot-toast Installation

**Finding**: react-hot-toast is already installed in frontend

**Evidence**:
```json
// frontend/package.json
{
  "dependencies": {
    "react-hot-toast": "^2.4.1"
  }
}
```

**Usage Found**:
```typescript
// frontend/src/app/tasks/page.tsx (existing)
import toast from 'react-hot-toast';
toast.success('Task completed');
```

**Decision**: No additional installation needed. Extend existing usage for reminders.

---

## R-003: Redpanda Cloud Network Access from Minikube

**Finding**: Redpanda Cloud accessible from Minikube pods

**Test Procedure**:
```bash
# From within a Minikube pod
kubectl run test-redpanda --image=curlimages/curl --rm -it --restart=Never -- \
  curl -v https://d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092

# Result: Connection established (SASL auth required for Kafka operations)
```

**Decision**: Network connectivity confirmed. No firewall issues expected.

**Note**: Using port 9092 (Kafka protocol) not 443 (HTTPS). SASL_SSL required.

---

## R-004: Reminder Scheduler Implementation Status

**Finding**: No existing reminder scheduler service found

**Evidence**:
```bash
# Search for reminder-related files
find backend -name "*reminder*" -o -name "*scheduler*"
# Result: No matches found

# Check for background processes
grep -r "APScheduler\|celery\|background" backend/
# Result: No background job libraries found
```

**Decision**: Create new reminder scheduler service as background FastAPI process

**Implementation Choice**: Use `asyncio.create_task()` for background scheduler

**Rationale**:
- No additional dependencies (APScheduler, Celery)
- Integrates with existing async FastAPI app
- Simple for hackathon timeline
- Can run in same pod as backend

---

## R-005: Frontend Task Page Implementation

**Finding**: Basic task page exists with manual refresh

**Current State**:
```typescript
// frontend/src/app/tasks/page.tsx
// - Manual task fetching on mount
// - Checkbox for task completion
// - Basic task display
// - No polling for updates
// - No automatic notifications
```

**Needed Changes**:
1. Add `useTaskPolling` hook for 30-second refresh
2. Add `useReminders` hook for toast notifications
3. Calculate `isOverdue` status for each task
4. Track notified tasks in session storage

**Decision**: Extend existing page rather than rewrite

---

## Summary of Decisions

| Research Item | Decision | Action Required |
|---------------|----------|-----------------|
| R-001: Dapr Config | Sidecar not injected | Add Dapr annotations to Helm chart |
| R-002: Toast Library | Already installed | Extend existing usage |
| R-003: Network Access | Connectivity confirmed | Proceed with Redpanda Cloud |
| R-004: Scheduler | Not implemented | Create new service |
| R-005: Frontend Page | Basic implementation | Add polling and notifications |

---

## Additional Technical Notes

### Redpanda Cloud Configuration

**Brokers**: `d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092`

**SASL Configuration**:
- Mechanism: `SCRAM-SHA-256`
- Username: `todo-phase5`
- Password: `bflLeIafHKGKvshzwRwcIZqvudhMjG`

**Topics to Create**:
- `task-events` - For reminder scheduling events

### Dapr Component Schema

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092"
    - name: authRequired
      value: "true"
    - name: saslUsername
      secretKeyRef:
        name: redpanda-credentials
        key: username
    - name: saslPassword
      secretKeyRef:
        name: redpanda-credentials
        key: password
    - name: saslMechanism
      value: "SCRAM-SHA-256"
    - name: securityProtocol
      value: "SASL_SSL"
```

### Time Zone Handling

**Storage**: All times stored in UTC in PostgreSQL
**Display**: Converted to user's local timezone in frontend
**Scheduling**: Reminder scheduler compares UTC times

---

## All Clarifications Resolved

No remaining NEEDS CLARIFICATION items. All unknowns from Technical Context have been researched and documented.

Ready to proceed with Phase 1 (Design & Contracts) and Phase 2 (Implementation).
