# Phase V Verification Checklist

## Overview
This checklist verifies all Phase V requirements are implemented and working locally.

## Pre-deployment Verification

### 1. Code Changes Verification
- [x] **Chat History Persistence** - `frontend/src/services/daprState.ts`, `frontend/src/hooks/useChat.ts`
  - Dapr state service created with localStorage fallback
  - Chat history automatically saved on message changes (debounced 500ms)
  - Chat history loaded on component mount
  - Clear chat removes from persistent storage

- [x] **Navbar Component** - `frontend/src/components/Navbar.tsx`
  - Added to login page (`frontend/src/app/login/page.tsx`)
  - Added to register page (`frontend/src/app/register/page.tsx`)
  - Links to Chat and Tasks pages
  - User info display with logout button

- [x] **Task Management UI** - Full task management interface
  - Tasks page: `frontend/src/app/tasks/page.tsx`
  - Task form: `frontend/src/components/tasks/TaskForm.tsx`
  - Task list: `frontend/src/components/tasks/TaskList.tsx`
  - Task filters: `frontend/src/components/tasks/TaskFilters.tsx`
  - Priority badge: `frontend/src/components/tasks/PriorityBadge.tsx`
  - Tasks service: `frontend/src/services/tasks.ts`
  - Tasks hook: `frontend/src/hooks/useTasks.ts`

- [x] **API Service Updates** - `frontend/src/services/api.ts`
  - Added generic GET, POST, PUT, PATCH, DELETE methods
  - Proper error handling for 401 responses
  - All task endpoints supported

- [x] **Auth Session Persistence**
  - JWT expiry set to 7 days in `backend/app/config.py`
  - Session properly restored from localStorage
  - User info persists across page reloads

## Deployment Steps

### 1. Rebuild and Load Images
```bash
# Backend (includes all Python dependencies and code changes)
cd backend
docker build --no-cache -t todo-backend:latest .
minikube image load todo-backend:latest

# Frontend (includes all new components and TypeScript files)
cd frontend
docker build --no-cache -t todo-frontend:latest .
minikube image load todo-frontend:latest

# Consumers (if not yet deployed)
cd consumers
docker build --no-cache -t todo-consumers:latest .
minikube image load todo-consumers:latest
```

### 2. Update Helm Values
Update `charts/backend/values.yaml` to ensure MCP_SERVER_URL points to the correct service:
```yaml
env:
  MCP_SERVER_URL: "http://mcp-service:8002"  # Service alias for mcp-server-service
```

### 3. Deploy/Upgrade Releases
```bash
# Upgrade backend (includes Dapr sidecar)
helm upgrade --install backend charts/backend -n default --force

# Upgrade frontend
helm upgrade --install frontend charts/frontend -n default --force

# Deploy consumers (if not deployed)
helm upgrade --install consumers charts/consumers -n default --force
```

### 4. Apply Dapr Components
```bash
# Apply Dapr components
kubectl apply -f dapr-components/
```

### 5. Restart Services
```bash
# Restart deployments
kubectl rollout restart deployment/backend-service -n default
kubectl rollout restart deployment/frontend-service -n default
kubectl rollout restart deployment/consumers-release -n default
```

### 6. Port Forward (if testing locally)
```bash
# Backend
kubectl port-forward svc/backend-service 8000:8000 -n default

# Frontend (check actual service name)
kubectl port-forward svc/frontend-service 3000:3000 -n default
```

## Post-deployment Verification

### 1. Pod Status
```bash
kubectl get pods -n default
```
Expected: All pods Running with 1/1 READY

### 2. Service Connectivity
```bash
# From frontend pod, test backend connection
kubectl exec -it frontend-service-xxxx -n default -- curl http://backend-service:8000/health

# Check Dapr sidecar is injected
kubectl get pods -n default -l app=backend -o jsonpath='{.items[*].spec.containers[*].name}'
```

### 3. Database Tables
```bash
# Verify all Phase V tables exist
kubectl exec -it backend-service-xxxx -n default -- python -c "
from backend.app.database.models import engine
from sqlalchemy import inspect
inspector = inspect(engine)
print(inspector.get_table_names())
"
```
Expected: task, conversation, message, session, user, dapr_metadata, dapr_state_store

### 4. API Endpoints Test
```bash
# Health check
curl http://localhost:8000/health

# Tasks API (requires auth token)
curl http://localhost:8000/api/tasks -H "Authorization: Bearer <token>"
```

## Functional Verification (E2E Tests)

### 1. Authentication Flow
1. Navigate to frontend URL
2. Click "Get Started" to register
3. Fill in email, password (8+ chars, upper/lower/digit/special)
4. Submit and verify redirect to /chat
5. Refresh page - verify user stays logged in
6. Logout and verify redirect to /login

### 2. Chat with History Persistence
1. Log in
2. Send message: "Add a task to buy groceries"
3. Verify assistant responds
4. Refresh page
5. Verify chat history is restored (both messages visible)

### 3. Task Management UI
1. Click "Tasks" in navbar
2. Click "Add Task" button
3. Fill in:
   - Title: "Complete project documentation"
   - Description: "Write all necessary docs"
   - Due Date: Tomorrow's date
   - Priority: High
   - Tags: "docs", "urgent"
4. Submit
5. Verify task appears in Pending list
6. Click checkbox to complete
7. Verify task moves to Completed list

### 4. Advanced Task Features
1. Create recurring task:
   - Title: "Weekly team meeting"
   - Recurring: Weekly, 1 time
   - Due date: Next Monday
2. Verify recurring indicator shows in task card
3. Complete the task
4. Check backend logs for event publishing
5. Check consumer logs for next instance creation

### 5. Search and Filter
1. Create multiple tasks with different priorities/tags
2. Use search bar to find specific task
3. Filter by priority (e.g., "High")
4. Filter by status (Pending/Completed)
5. Sort by Due Date
6. Verify all filters work correctly

### 6. Event Flow Verification
```bash
# Check backend logs for event publishing
kubectl logs backend-service-xxxx -n default --tail=50 | grep "publishing event"

# Check consumer logs for event processing
kubectl logs consumers-release-recurring-task-consumer-xxxx -n default --tail=50

# Check Dapr pub/sub is working
kubectl logs -c daprd backend-service-xxxx -n default --tail=50 | grep "topic"
```

### 7. Reminder System
1. Create task with due date < 24 hours away
2. Check backend logs for reminder scheduling
3. Check for "reminder scheduled" log entry
4. Wait for reminder time (or simulate)
5. Verify reminder callback/execution

## Troubleshooting Commands

### Check Logs
```bash
# Backend
kubectl logs backend-service-xxxx -n default --tail=100 --follow

# Frontend
kubectl logs frontend-service-xxxx -n default --tail=100 --follow

# MCP Server
kubectl logs mcp-server-xxxx -n default --tail=100 --follow

# Consumers
kubectl logs consumers-release-recurring-task-consumer-xxxx -n default --tail=50
kubectl logs consumers-release-notification-consumer-xxxx -n default --tail=50
kubectl logs consumers-release-audit-consumer-xxxx -n default --tail=50

# Dapr sidecar
kubectl logs backend-service-xxxx -c daprd -n default --tail=50
```

### Database Access
```bash
# Port-forward PostgreSQL
kubectl port-forward svc/postgres-mcp 5432:5432 -n default

# Connect to database
psql -h localhost -U postgres -d todo_chatbot

# Check tables
\dt
SELECT * FROM "task" LIMIT 5;
SELECT * FROM "user" LIMIT 5;
```

### Common Issues

**Issue**: Chat history not persisting
- Check: Browser console for Dapr errors
- Fix: Ensure Dapr sidecar is running (kubectl logs -c daprd)
- Fallback: Will use localStorage if Dapr unavailable

**Issue**: Tasks not loading
- Check: Network tab in browser for API errors
- Fix: Verify backend-service is accessible from frontend pod
- Command: `kubectl exec frontend-service-xxxx -- curl http://backend-service:8000/api/health`

**Issue**: Events not being published
- Check: Backend logs for "publishing event" messages
- Fix: Verify Kafka pub/sub component is applied
- Command: `kubectl get pubsub -n default`

**Issue**: Consumers not processing events
- Check: Consumer logs for subscription errors
- Fix: Verify Dapr subscription endpoint returns correct config
- Command: `kubectl port-forward svc/consumers-release 8001:8001 && curl http://localhost:8001/dapr/subscribe`

## Phase V Requirements Checklist

### Core Features
- [x] **Chat History Persistence** - Messages survive reload
- [x] **7-Day Session Expiry** - Users stay logged in for 7 days
- [x] **Landing Page** - Root redirects appropriately
- [x] **Navbar** - On all pages including login/register

### Task Management UI
- [x] **Task Creation** - Form with all fields
- [x] **Task Display** - List view with all details
- [x] **Task Editing** - Edit form with all fields
- [x] **Task Deletion** - With confirmation
- [x] **Task Completion** - Checkbox that handles recurring
- [x] **Priority Badges** - Visual priority indicators
- [x] **Tag Display** - Tag chips on tasks
- [x] **Due Dates** - Displayed with color coding
- [x] **Recurring Indicators** - Shows frequency
- [x] **Search** - Real-time search across tasks
- [x] **Filters** - By status, priority, tags
- [x] **Sort** - By created date, due date, priority

### Event-Driven Architecture
- [x] **Event Publishing** - Backend publishes on task CRUD
- [x] **Dapr Pub/Sub** - Kafka integration configured
- [x] **Recurring Task Consumer** - Handles task completion
- [x] **Notification Consumer** - Logs notifications
- [x] **Audit Consumer** - Logs all events

### Dapr Integration
- [x] **State Store** - PostgreSQL configured
- [x] **Pub/Sub** - Kafka configured
- [x] **Secrets** - Kubernetes secrets
- [x] **Jobs** - Cron bindings for reminders
- [x] **Sidecars** - Dapr injected into backend/frontend

### Verification
- [ ] **Full E2E Test** - Complete the tests above
- [ ] **Performance Check** - No significant delays
- [ ] **Error Handling** - Graceful degradation
- [ ] **Security** - Auth tokens not exposed
- [ ] **Cross-Browser** - Works in Chrome/Firefox/Safari
