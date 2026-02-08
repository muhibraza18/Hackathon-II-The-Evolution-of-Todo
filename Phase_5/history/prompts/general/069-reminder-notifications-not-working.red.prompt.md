---
id: 069
title: Reminder Notifications Not Working
stage: red
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: none
branch: 010-doks-deployment
user: Wajahat traders
command: /sp.analyze I make a tasks at /tasks page with a reminder Today at 15:47 Pakistani time so I don't get any notification
labels: [bug-report,reminders,notifications,consumers,not-deployed]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - consumers/notification_consumer.py
  - charts/consumers/values-doks.yaml
tests:
  - Database query to verify tasks with due dates
  - Check for notification consumer pods
  - Check for consumer Helm releases
---

## Prompt

I make a tasks at /tasks page with a reminder Today at 15:47 Pakistani time so I don't get any notification

## Response snapshot

## Issue Analysis

User created a task with a reminder at 15:47 Pakistani time but received no notification.

## Investigation Findings

### 1. Task with Due Date Exists
Database query confirmed task "washing clothes" with due date `2026-02-08 15:47:00` exists in the database.

### 2. Notification Consumer Not Deployed
```bash
helm list -A | grep consumer
# No consumer Helm release found
```

The `notification-consumer` service exists in code (`consumers/notification_consumer.py`) but is **not deployed** to the Kubernetes cluster.

### 3. Consumer Helm Chart Exists
The Helm chart exists at `charts/consumers/` with:
- `notificationConsumer.enabled: true`
- Configuration for Dapr sidecar
- Database and Kafka connections

However, the values file has placeholder `<docker-hub-username>` that needs to be updated.

### 4. How Reminders Should Work

**Notification Consumer Service** (`consumers/notification_consumer.py`):
- Background task runs every 30 seconds
- Queries database for tasks where `due_date <= now_utc` and `completed = false`
- Logs and publishes reminder events via Dapr pub/sub
- Tracks reminded tasks to avoid duplicates

**Frontend Notifications** (`frontend/src/app/tasks/page.tsx`):
- Client-side polling every 15 seconds while on tasks page
- Shows toast notifications for due/overdue tasks
- Only works when browser is open on tasks page

### 5. Why User Didn't Get Notifications

1. **No backend notification service running**: The notification consumer is not deployed
2. **Frontend-only notifications**: Only work while actively viewing the tasks page
3. **Time zone handling**: The user specified "Pakistani time" (PKT, UTC+5) but due dates are stored in UTC

## Root Cause

**The reminder notification system is not deployed**. The code exists but:
- Consumers Docker image not built/pushed
- Consumers Helm chart not installed
- Values file has placeholder `<docker-hub-username>`

## Required Fixes

### 1. Build Consumers Docker Image
```bash
# Build consumers image
docker build -t muhibraza/todo-consumers:doks-v1 -f consumers/Dockerfile consumers/
docker push muhibraza/todo-consumers:doks-v1
```

### 2. Update values-doks.yaml
Replace `<docker-hub-username>` with `muhibraza`

### 3. Deploy Consumers Helm Chart
```bash
helm install consumers charts/consumers -f charts/consumers/values-doks.yaml
```

### 4. Verify Deployment
```bash
kubectl get pods -l app=notification-consumer
kubectl logs -l app=notification-consumer --tail=50
```

## Alternative: Simpler Client-Side Solution

If deploying the full consumer system is too complex:
1. The frontend already has client-side reminder checking
2. Users need to keep the tasks page open in their browser
3. Notifications appear as toast messages on the page

## Database Query Used for Investigation
```sql
SELECT id, title, due_date, completed FROM task
WHERE due_date IS NOT NULL
ORDER BY created_at DESC LIMIT 10;
```

## Outcome

- ✅ Impact: Identified root cause - notification consumer service not deployed
- 🧪 Tests: Database query confirmed tasks with due dates exist
- 📁 Files: consumers/notification_consumer.py, charts/consumers/values-doks.yaml
- 🔁 Next prompts: Deploy notification consumer service
- 🧠 Reflection: The reminder system is a microservice that requires separate deployment. It's not enough to have the code - the service must be running.

## Recommendation

Deploy the notification consumer service to enable reminder notifications. This requires:
1. Building and pushing the consumers Docker image
2. Updating values file with correct Docker Hub username
3. Installing the consumers Helm chart

## Evaluation notes (flywheel)

- Failure modes observed: Reminder notifications not working because consumer service not deployed
- Graders run and results (PASS/FAIL): FAIL - Service not deployed
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Build and deploy notification consumer service
