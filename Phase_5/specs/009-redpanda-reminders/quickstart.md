# Quickstart: Phase V – Redpanda Cloud + Real-Time Reminders

**Feature**: 009-redpanda-reminders
**Branch**: `009-redpanda-reminders`

---

## Prerequisites

1. **Minikube Running**:
   ```bash
   minikube start
   minikube status
   ```

2. **Dapr Installed**:
   ```bash
   dapr version
   # If not installed: winget install Dapr.CLI
   ```

3. **kubectl Configured**:
   ```bash
   kubectl get nodes
   ```

4. **Redpanda Cloud Credentials** (already provisioned):
   - Bootstrap: `d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092`
   - Username: `todo-phase5`

---

## Setup Steps (15 minutes)

### Step 1: Create Kubernetes Secret for Redpanda

```bash
kubectl create secret generic redpanda-credentials \
  --from-literal=username=todo-phase5 \
  --from-literal=password='bflLeIafHKGKvshzwRwcIZqvudhMjG' \
  --namespace=default

# Verify
kubectl get secret redpanda-credentials
```

### Step 2: Apply Dapr Pub/Sub Component

```bash
# From dapr-components directory
kubectl apply -f dapr-components/kafka-pubsub.yaml

# Verify component is healthy
dapr components -k

# Expected output:
# NAME                    TYPE            VERSION  AGE
# kafka-pubsub            pubsub.kafka    v1       10s
```

### Step 3: Enable Dapr on Backend Deployment

```bash
# Add Dapr annotations to backend Helm chart
# Edit charts/backend/templates/deployment.yaml
# Add annotations section to pod template

kubectl patch deployment backend-service \
  --namespace=default \
  --type=json \
  -p='[
    {"op": "add", "path": "/spec/template/metadata annotations", "value": {
      "dapr.io/enabled": "true",
      "dapr.io/app-id": "todo-backend",
      "dapr.io/app-port": "8000"
    }}
  ]'

# Restart backend
kubectl rollout restart deployment/backend-service

# Wait for rollout
kubectl rollout status deployment/backend-service
```

### Step 4: Create Reminders Table

```bash
# Apply migration
kubectl exec -it postgres-postgresql-0 -- psql -U postgres -d neondb \
  -f /dev/stdin < backend/migrations/create_reminders_table.sql

# Verify table exists
kubectl exec -it postgres-postgresql-0 -- psql -U postgres -d neondb \
  -c "\dt reminders"
```

### Step 5: Start Port Forwards

```bash
# Frontend
kubectl port-forward -n default service/frontend-service 3000:3000 &

# Backend
kubectl port-forward -n default service/backend-service 8000:8000 &

# Verify
curl http://localhost:8000/health
```

---

## Testing (5 minutes)

### Test 1: Create Task via Chat with Reminder

1. Open http://localhost:3000/chat
2. Type: `Add a task Get medicine add reminder at 2 minutes from now`
3. Verify:
   - Task appears in response
   - Backend logs show "Published reminder event"

### Test 2: Wait for Toast Notification

1. Open http://localhost:3000/tasks
2. Wait 2 minutes
3. Verify:
   - Toast appears: "Reminder: Get medicine is due now!"
   - Overdue badge shows on task
   - No page refresh needed

### Test 3: Verify Redpanda Event

```bash
# Check backend logs for event publish
kubectl logs -f backend-service-xxxxx | grep "Published"

# Or check Redpanda Cloud dashboard
# Navigate to Topics → task-events → Messages
```

---

## Verification Commands

```bash
# Dapr component health
dapr components -k | grep kafka-pubsub

# Backend pods with Dapr sidecar
kubectl get pods -l app=backend-service -o wide

# Check Dapr is injected
kubectl describe pod backend-service-xxxxx | grep -A5 dapr

# Reminders table exists
kubectl exec postgres-postgresql-0 -- psql -U postgres -d neondb \
  -c "SELECT COUNT(*) FROM reminders"

# Recent reminder events (backend logs)
kubectl logs backend-service-xxxxx --tail=50 | grep -i reminder

# Polling frequency (browser Network tab should show requests every 30s)
```

---

## Troubleshooting

| Issue | Symptom | Fix |
|-------|---------|-----|
| Dapr not injected | Pod has 1/2 containers | Check annotations, restart deployment |
| Redpanda connection failed | "connection refused" in logs | Verify secret, check bootstrap URL |
| Reminder not triggered | No toast appears | Check scheduler logs, verify due_time |
| Polling not working | Tasks not updating | Check browser console for errors |
| Duplicate toasts | Same notification multiple times | Clear browser session storage |

For detailed troubleshooting, see: [docs/redpanda-troubleshooting.md](../docs/redpanda-troubleshooting.md)

---

## Demo Script (7 minutes)

```
[Setup - 2 min]
1. Show Minikube: minikube status
2. Show Dapr: dapr components -k
3. Show port forwards running

[Chat Agent - 1 min]
4. "Add a task Call mom at 2 minutes from now"
5. Show task created with due time

[Real-Time Reminder - 2 min]
6. Open tasks page
7. Wait for reminder (2 minutes)
8. Toast appears automatically
9. Overdue badge shows

[Event Streaming - 1 min]
10. Show backend logs: kubectl logs -f backend-service
11. Show Redpanda dashboard with events

[Advanced Features - 1 min]
12. Show recurring, priority, tags
13. Show filter and sort

[Total: ~7 minutes]
```

---

## Next Steps

After successful local testing:

1. Run full acceptance test suite (see [plan.md](./plan.md) Phase 2d)
2. Update README with Redpanda setup
3. Prepare demo video (≤90s)
4. Document any issues for future cloud deployment
