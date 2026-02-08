---
id: 59
title: Fix manual task reminder notifications
stage: green
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-local-e2e-polish
user: Wajahat traders
command: /sp.analyze
labels: ["bug-fix","reminder","notifications","frontend","backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/app/routes/tasks.py
 - frontend/src/hooks/useReminders.ts
tests:
 - Manual test: Create a task with due time 2 minutes in future, verify notification appears
 - Manual test: Create task with due time 1 minute in future, verify toast notification shows
 - Manual test: Refresh page after notification, verify notification doesn't reappear
---

## Prompt

I made a task manually but when the time came the time when I had to get reminder notification so the notification not triggered why check the logs and remove this problem

## Response snapshot

## Root Cause Analysis

**User Report**: "I made a task manually but when the time came the time when I had to get reminder notification so the notification not triggered"

**Backend logs showed**: No reminder scheduling activity when tasks were created manually through the REST API.

**Problems Found**:

1. **Backend (`backend/app/routes/tasks.py`)**:
   - `create_task()` function never called `ReminderScheduler.schedule_reminder_for_task()`
   - `update_task()` function never called `ReminderScheduler.reschedule_reminder()`
   - `complete_task()` and `delete_task()` never called `ReminderScheduler.cancel_scheduled_reminder()`
   - The reminder scheduler was only designed for Kafka-based event publishing, not REST API task creation

2. **Frontend (`frontend/src/hooks/useReminders.ts`)**:
   - `seenReminderIds` stored only in component state - lost on page refresh
   - Empty dependency array `[]` in useEffect caused stale closure issues
   - Only checked for overdue tasks (`dueDate <= now`), not upcoming tasks
   - 30-second polling interval could miss the exact moment a task becomes due
   - No persistence of seen reminders across sessions

### Fixes Applied

**Backend (`backend/app/routes/tasks.py`)**:
- Added `ReminderScheduler` import to `create_task()`, `update_task()`, `complete_task()`, and `delete_task()` routes
- Added `await ReminderScheduler.schedule_reminder_for_task(task, db)` after task creation (if task has due_date)
- Added reminder cancellation when task is completed
- Added reminder rescheduling when task is updated with new due_date
- Added reminder cancellation when task is deleted

**Frontend (`frontend/src/hooks/useReminders.ts`)**:
- Implemented localStorage persistence for `seenReminderIds`
- Added cleanup of old reminder IDs (> 24 hours) to prevent unlimited growth
- Changed from component state to `useRef` to avoid stale closure issues
- Reduced polling interval from 30 seconds to 10 seconds
- Added `REMINDER_WINDOW_MS = 5 minutes` - now shows reminders for tasks due within 5 minutes, not just overdue
- Used `Date.now()` instead of `new Date()` for more accurate time comparisons

## Outcome

- ✅ Impact: Fixed reminder notifications for manually created tasks with due dates
- 🧪 Tests: Manual testing recommended - create task with due time 2 minutes in future
- 📁 Files: backend/app/routes/tasks.py, frontend/src/hooks/useReminders.ts
- 🔁 Next prompts: Test with "Add a task Take medicine in 2 minutes"
- 🧠 Reflection: Reminders need both backend scheduling and frontend polling with persistence

## Evaluation notes (flywheel)

- Failure modes observed: (1) Backend never scheduled reminders for REST API tasks; (2) Frontend lost seen reminders on refresh; (3) 30-second poll could miss due time
- Graders run and results (PASS/FAIL): Pending user testing
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Consider WebSocket for real-time reminders instead of polling
