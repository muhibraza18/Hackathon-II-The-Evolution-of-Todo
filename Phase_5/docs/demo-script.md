# Demo Script: Todo AI Chatbot - Phase V Features

**Target Duration**: 90 seconds
**Audience**: Hackathon judges
**Focus**: Advanced features (recurring tasks, reminders, events, Dapr)

---

## Pre-Demo Checklist

- [ ] Minikube running with all pods healthy
- [ ] Frontend URL accessible: `minikube service todo-frontend --url`
- [ ] Demo user credentials ready
- [ ] Terminal open with log tailing: `kubectl logs deployment/todo-consumers -f`
- [ ] Screenshots ready as backup
- [ ] Log excerpts prepared

---

## Demo Script

### Segment 1: Introduction & Login (0:00 - 0:15) | 15 seconds

**Action**: Show application and login

**Narration**: "Hi, I'm demonstrating the Todo AI Chatbot with advanced Phase V features including recurring tasks, automated reminders, and event-driven architecture powered by Dapr."

**Steps**:
1. Show frontend URL: `echo $FRONTEND_URL` or `minikube service todo-frontend --url`
2. Open browser to frontend URL
3. Show login screen
4. Enter demo credentials
5. Click Login

**What to Point Out**:
- Clean, modern UI
- Fast page load

---

### Segment 2: Create Recurring Task (0:15 - 0:35) | 20 seconds

**Action**: Create a recurring task with advanced attributes

**Narration**: "Let me create a recurring daily standup task. I'll set it to high priority, tag it as work, and add a due date for tomorrow."

**Steps**:
1. Click "New Task" button
2. Enter title: "Daily Standup"
3. Select Recurrence: "Daily"
4. Select Priority: "High"
5. Enter Tag: "work"
6. Set Due Date: Tomorrow
7. Click Save/Create

**What to Point Out**:
- Rich task creation form
- Recurrence indicator on task card
- Priority badge (high = red)
- Tag visible on task card

---

### Segment 3: Show Event Flow (0:35 - 0:55) | 20 seconds

**Action**: Demonstrate event-driven architecture

**Narration**: "When I created that task, it triggered an event flow. Let me show you the logs. You can see the event was published to Kafka, and the consumer services processed it for recurrence and audit."

**Steps**:
1. Switch to terminal with consumer logs running
2. Point out: `"event_type": "task.created"`
3. Point out: `"consumer": "recurring-task-consumer"`
4. Point out: `"consumer": "audit-consumer"`

**What to Point Out**:
- JSON structured logging
- Event-driven architecture
- Multiple consumers processing events
- Audit trail for compliance

---

### Segment 4: Schedule Reminder (0:55 - 0:75) | 20 seconds

**Action**: Create a task with due date reminder

**Narration**: "Now I'll create a task with a due date reminder. The Dapr Jobs API automatically schedules a callback to fire a reminder at the scheduled time."

**Steps**:
1. Click "New Task"
2. Enter title: "Call with client"
3. Set Due Date: 2 minutes from now
4. Click Save
5. Show (or mention): Job scheduled in Dapr
6. Wait for due time (or fast-forward)
7. Show logs: Reminder fired at scheduled time

**What to Point Out**:
- Automatic reminder scheduling
- Dapr Jobs API integration
- Callback firing at exact time
- Notification in consumer logs

---

### Segment 5: Summary (0:75 - 0:90) | 15 seconds

**Action**: Wrap up and highlight key features

**Narration**: "So we've seen recurring tasks that auto-generate, due date reminders via Dapr Jobs, and a complete event-driven architecture. All running locally on Minikube with Dapr sidecars. Thank you!"

**What to Point Out**:
- All features working end-to-end
- Local deployment on Minikube
- Dapr integration for cloud-native architecture
- Production-ready event-driven design

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---------|----------|------------|
| Introduction & Login | 15s | 0:15 |
| Create Recurring Task | 20s | 0:35 |
| Show Event Flow | 20s | 0:55 |
| Schedule Reminder | 20s | 1:15 |
| Summary | 15s | 1:30 |

**Total**: 90 seconds

---

## Backup Screenshots

If live demo fails, use these screenshots in order:

1. `screenshots/01-login.png` - Login screen
2. `screenshots/02-task-list.png` - Task list with various tasks
3. `screenshots/03-create-form.png` - Create task form filled out
4. `screenshots/04-new-task.png` - Task list with new task
5. `screenshots/05-consumer-logs.png` - Consumer logs showing events
6. `screenshots/06-dapr-components.png` - Dapr components list
7. `screenshots/07-pod-status.png` - Pod status showing all Running

---

## Log Excerpts to Reference

### Event Publishing Log

```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:30:45.123Z",
  "component": "backend",
  "event_type": "task.created",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-123",
  "message": "Task created event published"
}
```

### Consumer Processing Log

```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:30:45.234Z",
  "component": "recurring-task-consumer",
  "event_type": "task.created",
  "action_taken": "checked for recurrence",
  "recurrence_rule": "daily",
  "message": "Task has recurrence rule - set up next instance"
}
```

### Reminder Fired Log

```json
{
  "level": "INFO",
  "timestamp": "2026-02-02T10:32:45.567Z",
  "component": "notification-consumer",
  "event_type": "reminder.fired",
  "task_id": "550e8400-e29b-41d4-a716-446655440001",
  "due_date": "2026-02-02T10:32:00Z",
  "message": "Reminder callback executed for task"
}
```

---

## Troubleshooting Demo Issues

### Issue: Frontend Not Accessible

**Fix**:
```bash
# Get correct URL
minikube service todo-frontend --url

# If using NodePort
minikube service list
```

### Issue: Events Not Showing in Logs

**Fix**:
```bash
# Tail consumer logs
kubectl logs deployment/todo-consumers -f

# Or use tail with specific line count
kubectl logs deployment/todo-consumers --tail=100
```

### Issue: Pods Not Healthy

**Fix**:
```bash
# Check pod status
kubectl get pods

# Restart problematic deployment
kubectl rollout restart deployment/todo-backend
```

---

## Tips for Smooth Demo

1. **Practice at least 3 times** before the actual demo
2. **Have screenshots ready** as backup in case of network issues
3. **Pre-load log files** - tail them in advance and scroll through during demo
4. **Use browser bookmarks** for quick access to frontend URL
5. **Prepare terminal aliases** for frequently used commands
6. **Time yourself** - ensure each segment stays within its time budget
7. **Have a "Plan B"** - know what to skip if running short on time
8. **Stay calm** - if something fails, move to the next segment smoothly

---

## Post-Demo Questions (Anticipated)

**Q: How does the recurring task work?**
A: When you complete a recurring task, the consumer service detects the recurrence rule and automatically creates a new instance for the next occurrence.

**Q: What's Dapr doing here?**
A: Dapr provides the sidecar infrastructure for event publishing, job scheduling, and service-to-service communication. It abstracts away the complexity of Kafka and service discovery.

**Q: Can this run in the cloud?**
A: Absolutely! The same deployment works on any Kubernetes cluster with minimal changes - just update the service type from NodePort to LoadBalancer.

**Q: How do you handle database state?**
A: We're using PostgreSQL with the database stored externally (Neon or local), so state persists across pod restarts and deployments.

---

## Contact for Questions

For questions about the implementation, architecture, or features, refer to:
- `specs/001-local-e2e-polish/spec.md` - Feature specification
- `specs/001-local-e2e-polish/plan.md` - Implementation plan
- `specs/001-local-e2e-polish/quickstart.md` - Quick start guide
