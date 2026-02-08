# Quick Start: E2E Testing & Polish Execution

**Feature**: 001-local-e2e-polish
**Prerequisites**: Phase V Step 4 deployment running on Minikube

## Overview

This guide provides step-by-step instructions for executing end-to-end testing, bug triage, and demo preparation for the Todo AI Chatbot hackathon submission.

---

## 1. Prerequisites Checklist

Before starting E2E testing, ensure:

- [ ] Minikube is running: `minikube status`
- [ ] Dapr is initialized: `dapr status -k`
- [ ] Phase V Step 4 deployment is complete
- [ ] All pods are running: `kubectl get pods`
- [ ] Frontend URL is accessible

---

## 2. Automated Health Checks

Run these commands first to verify basic system health:

### 2.1 Pod Status Verification
```bash
# Check all pods are running
kubectl get pods

# Expected output:
# NAME                              READY   STATUS    RESTARTS   AGE
# todo-backend-xxxxxxxxxx-xxxxx     2/2     Running   0          5m
# todo-consumers-xxxxxxxxxx-xxxxx   2/2     Running   0          5m
# todo-frontend-xxxxxxxxxx-xxxxx    2/2     Running   0          5m
# postgresql-0                      1/1     Running   0          10m
# kafka-0                           1/1     Running   0          10m
```

### 2.2 Verify Dapr Sidecars
```bash
# Check that each app pod has a dapr sidecar (2/2 Ready)
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'

# Expected: Each app pod shows two containers (app + daprd)
```

### 2.3 Dapr System Status
```bash
# Verify Dapr control plane is healthy
dapr status -k

# Expected output:
# NAME                   NAMESPACE    HEALTHY   STATUS   REPLICAS   VERSION   AGE   CREATED
# dapr-sidecar-injector  dapr-system  True      Running  1         1.13.x    10m   2026-02-02 10:00.00
# dapr-dashboard         dapr-system  True      Running  1         0.13.x    10m   2026-02-02 10:00.00
# dapr-operator          dapr-system  True      Running  1         1.13.x    10m   2026-02-02 10:00.00
# dapr-placement         dapr-system  True      Running  1          1.13.x    10m   2026-02-02 10:00.00
```

### 2.4 Service Accessibility
```bash
# Check services are exposed
kubectl get services

# Get frontend URL
FRONTEND_URL=$(minikube service todo-frontend --url)
echo "Frontend URL: $FRONTEND_URL"

# Test health endpoint
curl $FRONTEND_URL/health

# Expected: {"status": "healthy"} or HTTP 200
```

### 2.5 Check for Critical Errors
```bash
# Check backend logs for errors
kubectl logs deployment/todo-backend --tail=100 | grep -i error

# Check consumer logs for errors
kubectl logs deployment/todo-consumers --tail=100 | grep -i error

# Expected: No critical errors (CRITICAL or ERROR level with stack traces)
```

---

## 3. Manual E2E Test Scenarios

### 3.1 Test Scenario: Recurring Tasks (P1)

**Objective**: Verify recurring task creation and auto-generation of next instances.

**Steps**:
1. Login to the application via frontend URL
2. Create a new task with:
   - Title: "Daily Standup"
   - Recurrence: Daily
   - Due date: Tomorrow
   - Priority: High
   - Tag: "work"
3. Verify task appears in task list
4. Complete the task (mark as done)
5. Verify a new instance is created for tomorrow
6. Check consumer logs show event processing

**Expected Results**:
- Task created with recurrence indicator
- Completing task creates new instance with incremented date
- Consumer logs show: "task.completed" event processed
- Audit log records the completion

**Verification Commands**:
```bash
# Check consumer logs for event processing
kubectl logs deployment/todo-consumers --tail=50 | grep "task.completed"

# Expected: Log entry showing next instance creation
```

---

### 3.2 Test Scenario: Due Date Reminders (P1)

**Objective**: Verify Dapr Jobs API schedules and triggers reminders.

**Steps**:
1. Create a task with due date 2 minutes in the future
2. Note the current time
3. Wait for due date to pass
4. Check notification consumer logs for reminder firing
5. Verify reminder was logged

**Expected Results**:
- Reminder job scheduled via Dapr Jobs API
- At due time, callback fires to notification consumer
- Consumer logs show reminder notification
- No errors in job execution

**Verification Commands**:
```bash
# Watch logs for reminder firing
kubectl logs deployment/todo-consumers -f | grep "reminder"

# Expected: Log entry when due time is reached
```

---

### 3.3 Test Scenario: Priority & Tag Filtering (P1)

**Objective**: Verify task filtering by priority and tags works correctly.

**Steps**:
1. Create multiple tasks with different priorities (high, medium, low)
2. Create tasks with different tags (work, personal, urgent)
3. Apply priority filter: "High only"
4. Verify only high-priority tasks shown
5. Apply tag filter: "work"
6. Verify only tasks with "work" tag shown
6. Clear filters and verify all tasks shown

**Expected Results**:
- Priority filter shows matching tasks only
- Tag filter shows matching tasks only
- Multiple filters work together (AND logic)
- Clear filters returns to full task list

---

### 3.4 Test Scenario: Search & Sort (P2)

**Objective**: Verify full-text search and sorting functionality.

**Steps**:
1. Create tasks with varied titles and descriptions
2. Search for a term that appears in some tasks
3. Verify matching tasks highlighted/returned
4. Sort tasks by due date
5. Verify chronological order
6. Sort tasks by priority
7. Verify priority grouping (high → medium → low)

**Expected Results**:
- Search returns tasks with matching text in title/description
- Due date sort shows earliest first
- Priority sort groups by priority level

---

### 3.5 Test Scenario: Event Flow Verification (P2)

**Objective**: Verify full event-driven pipeline from publish to consume.

**Steps**:
1. Open terminal to watch consumer logs
   ```bash
   kubectl logs deployment/todo-consumers -f
   ```
2. In the UI, create a new task
3. Observe logs for event processing
4. Verify all three consumers log the event:
   - Recurring task consumer
   - Notification consumer
   - Audit consumer

**Expected Results**:
- Task creation triggers event publish
- All three consumers log processing the event
- Audit log records the event
- No errors in event processing

**Expected Log Pattern**:
```json
{
  "level": "INFO",
  "event_type": "task.created",
  "task_id": "...",
  "consumer": "recurring-task-consumer",
  "action_taken": "checked for recurrence"
}
```

---

### 3.6 Test Scenario: Dapr Validation (P2)

**Objective**: Verify Dapr components are working correctly.

**Steps**:
1. Check Dapr components are loaded:
   ```bash
   kubectl get components.dapr.io
   ```
2. Verify pubsub component connects to Kafka
3. Verify state store connects to PostgreSQL
4. Verify secrets are loaded from Kubernetes

**Expected Results**:
- All components show STATUS=Loaded
- No errors in Dapr sidecar logs
- Components can communicate with backends

**Verification Commands**:
```bash
# Check components
kubectl get components.dapr.io

# Check sidecar logs for component health
kubectl logs deployment/todo-backend -c daprd --tail=50
```

---

### 3.7 Test Scenario: Pod Recovery (P3)

**Objective**: Verify system recovers from pod restarts.

**Steps**:
1. Create a test task
2. Restart backend pod:
   ```bash
   kubectl delete pod -l app=todo-backend
   ```
3. Wait for pod to restart (watch `kubectl get pods -w`)
4. Verify task still exists
5. Verify can create new tasks

**Expected Results**:
- Pod restarts successfully
- Data persisted in database
- No data loss
- System fully functional after restart

---

## 4. Bug Triage Process

### 4.1 Bug Recording Template

When a bug is discovered, record:

```markdown
## BUG-XXX: [Brief Title]

**Severity**: critical | high | medium | low
**Area**: frontend | backend | dapr | consumer
**Discovered**: [Date/time]

**Reproduction Steps**:
1. Step one
2. Step two
3. Step three

**Actual Behavior**: What happened

**Expected Behavior**: What should have happened

**Logs**: [Attach relevant log excerpts]

**Status**: open | in_progress | fixed | verified
```

### 4.2 Severity Guidelines

| Severity | Definition | Example |
|----------|------------|---------|
| Critical | System unusable or data loss | CrashLoopBackOff, database connection lost |
| High | Major feature broken | Cannot create tasks, events not publishing |
| Medium | Minor feature broken | Filter not working, sort order wrong |
| Low | Cosmetic or minor | Typos, spacing issues, unclear message |

### 4.3 Bug Fix Workflow

1. Document bug in bug report template
2. Assign severity
3. Fix via Claude Code implementation
4. Smoke test after fix (create task, verify it works)
5. Re-test the specific scenario
6. Mark as verified if fix confirmed

---

## 5. Log Analysis Guide

### 5.1 Key Log Patterns

**Successful Event Flow**:
```json
{"level": "INFO", "event_type": "task.created", "task_id": "...", "timestamp": "..."}
{"level": "INFO", "consumer": "audit", "action": "logged", "event_id": "..."}
```

**Error Pattern**:
```json
{"level": "ERROR", "message": "...", "error": {"type": "...", "message": "..."}}
```

**Dapr Sidecar Healthy**:
```
INFO[0000] dapr (version 1.13.x) initialized
INFO[0000] app id: todo-backend listening on port 3500
```

### 5.2 Useful Log Commands

```bash
# Tail all application logs
kubectl logs deployment/todo-backend -f
kubectl logs deployment/todo-consumers -f

# Tail only Dapr sidecar logs
kubectl logs deployment/todo-backend -c daprd -f

# Search for specific event types
kubectl logs deployment/todo-consumers | grep "task.created"

# Find errors in last 100 lines
kubectl logs deployment/todo-backend --tail=100 | grep -i error

# Watch logs in real-time
kubectl logs -f -l app=todo-backend
```

---

## 6. Demo Preparation

### 6.1 Demo Script (90 seconds)

**0:00-0:15: Introduction & Login**
- Show frontend URL
- Login with demo credentials

**0:15-0:35: Create Recurring Task**
- Click "New Task"
- Enter: "Daily Standup", Recurrence: Daily, Priority: High
- Save and show task in list

**0:35-0:55: Show Event Flow**
- Switch to terminal with consumer logs running
- Point out event published and processed
- Show audit log entry

**0:55-0:75: Schedule Reminder**
- Create task with due date 2 min out
- Show Dapr Jobs scheduling
- Wait and show reminder firing

**0:75-0:90: Summary**
- Show all tasks working
- Mention features: recurring, reminders, events, Dapr
- End demo

### 6.2 Pre-Demo Checklist

- [ ] Minikube running with all pods healthy
- [ ] Frontend URL accessible and loaded
- [ ] Demo user credentials ready
- [ ] Terminal open with log tailing command ready
- [ ] Screenshots captured as backup
- [ ] Log excerpts prepared for event flow section

### 6.3 Screenshot Checklist

Capture screenshots at these moments:
1. Login screen
2. Task list with varied tasks
3. Create task form (filled out)
4. Task list with new task
5. Consumer logs showing event processing
6. Dapr components list
7. Pod status showing all Running

---

## 7. Troubleshooting Common Issues

### Issue: Pods in CrashLoopBackOff

**Diagnosis**:
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Common Causes**:
- Database connection failure
- Missing environment variables
- Dapr sidecar not starting

**Resolution**:
- Check database is accessible
- Verify secrets are mounted
- Restart Dapr: `dapr uninstall -k && dapr init -k`

---

### Issue: Events Not Publishing

**Diagnosis**:
```bash
kubectl logs deployment/todo-backend | grep "publish"
kubectl logs deployment/todo-consumers | grep "subscribe"
```

**Resolution**:
- Verify Kafka is running: `kubectl get pods -l app=kafka`
- Check Dapr pubsub component: `kubectl get components.dapr.io`
- Restart backend pod

---

### Issue: Frontend Not Accessible

**Diagnosis**:
```bash
minikube service todo-frontend --url
kubectl get services
```

**Resolution**:
- Check minikube tunnel is running (if using LoadBalancer)
- Verify frontend pod is Running
- Restart minikube if needed

---

### Issue: Dapr Sidecar Not Starting

**Diagnosis**:
```bash
kubectl logs <pod-name> -c daprd
dapr status -k
```

**Resolution**:
- Reinstall Dapr: `dapr uninstall -k && dapr init -k`
- Check sidecar-injector is running
- Verify pod annotations include `dapr.io/enabled: "true"`

---

## 8. Success Criteria Checklist

After completing all tests, verify:

- [ ] All pods Running (1/1 or 2/2 Ready)
- [ ] No CrashLoopBackOff pods
- [ ] Frontend accessible via minikube service URL
- [ ] Can create, edit, delete, complete tasks
- [ ] Recurring tasks auto-create next instances
- [ ] Due date reminders fire at scheduled time
- [ ] Priority and tag filtering works
- [ ] Search returns matching results
- [ ] Sort orders tasks correctly
- [ ] Event publishing verified in logs
- [ ] All consumers processing events
- [ ] Dapr sidecars healthy
- [ ] Dapr components loaded
- [ ] No critical errors in logs
- [ ] Error messages are user-friendly
- [ ] README sections complete
- [ ] Demo script runs in <90 seconds
