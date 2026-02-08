# Tasks: Phase V – Redpanda Cloud Integration + Real-Time Reminders

**Input**: Design documents from `/specs/009-redpanda-reminders/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/backend-api.yaml

**Tests**: Manual end-to-end testing only (no automated tests per spec)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for FastAPI application
- **Frontend**: `frontend/src/` for Next.js application
- **Infrastructure**: `dapr-components/` for Dapr YAML, `charts/` for Helm charts
- **Migrations**: `backend/migrations/` for database migration SQL

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Kubernetes secrets and Dapr component configuration

- [ ] T001 Create Kubernetes secret for Redpanda credentials using `kubectl create secret generic redpanda-credentials --from-literal=username=todo-phase5 --from-literal=password='bflLeIafHKGKvshzwRwcIZqvudhMjG' --namespace=default`
- [ ] T002 Create dapr-components directory structure at `dapr-components/`
- [ ] T003 [P] Generate Dapr Pub/Sub component YAML in `dapr-components/kafka-pubsub.yaml` with Redpanda Cloud configuration (SASL_SSL, SCRAM-SHA-256, bootstrap server)
- [ ] T004 [P] Verify Dapr component YAML syntax with `kubectl apply --dry-run=client -f dapr-components/kafka-pubsub.yaml`

**Checkpoint**: Infrastructure configuration ready for deployment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Apply Dapr Pub/Sub component to cluster with `kubectl apply -f dapr-components/kafka-pubsub.yaml`
- [ ] T006 Verify Dapr component health with `dapr components -k | grep kafka-pubsub`
- [ ] T007 [P] Create reminders database migration SQL in `backend/migrations/create_reminders_table.sql`
- [ ] T008 [P] Apply reminders table migration to database with `kubectl exec -it postgres-postgresql-0 -- psql -U postgres -d neondb -f /dev/stdin < backend/migrations/create_reminders_table.sql`
- [ ] T009 [P] Add Dapr annotations to backend deployment in `charts/backend/templates/deployment.yaml` (dapr.io/enabled, dapr.io/app-id, dapr.io/app-port)
- [ ] T010 Restart backend deployment with `kubectl rollout restart deployment/backend-service`
- [ ] T011 Wait for backend rollout with `kubectl rollout status deployment/backend-service`
- [ ] T012 [P] Verify Dapr sidecar injection with `kubectl describe pod backend-service-xxxxx | grep dapr`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Cloud-Based Reminder Notifications (Priority: P1) 🎯 MVP

**Goal**: User creates task with due time, and toast notification appears automatically when due time arrives

**Independent Test**: Create a task with due time 3 minutes in future, wait 3 minutes, verify toast appears with correct message and overdue badge shows

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create reminder CRUD operations in `backend/app/crud.py` (create_reminder, get_pending_reminders, mark_reminder_sent)
- [ ] T014 [P] [US1] Create Reminder model in `backend/app/models.py` (Reminder database entity with id, task_id, user_id, due_time, status, event_published, created_at, sent_at)
- [ ] T015 [US1] Create reminder routes in `backend/app/routes/reminders.py` (POST /api/tasks/{task_id}/reminder, GET /api/tasks/pending-reminders)
- [ ] T016 [US1] Integrate reminder creation into task creation flow in `backend/app/routes/tasks.py` (auto-create reminder when due_date has time component)
- [ ] T017 [US1] Create Dapr event publisher service in `backend/app/services/event_publisher.py` (publish_reminder_scheduled with Redpanda Cloud, fallback handling)
- [ ] T018 [US1] Add event publishing call to task creation in `backend/app/routes/tasks.py` after reminder creation
- [ ] T019 [US1] Create reminder scheduler service in `backend/app/services/reminder_scheduler.py` (background asyncio task checking pending reminders every 30 seconds)
- [ ] T020 [US1] Add scheduler startup to `backend/app/main.py` (start background scheduler on FastAPI startup)
- [ ] T021 [US1] Add SSE/notification endpoint for reminder triggers in `backend/app/routes/reminders.py` (GET /api/reminders/stream for real-time trigger delivery)
- [ ] T022 [P] [US1] Create useReminders hook in `frontend/src/hooks/useReminders.ts` (check for due reminders, show toasts, track notified tasks in session storage)
- [ ] T023 [P] [US1] Add toast notification display to tasks page in `frontend/src/app/tasks/page.tsx` (import useReminders, display toasts when reminders trigger)
- [ ] T024 [US1] Add overdue badge calculation to task list response in `backend/app/routes/tasks.py` (is_overdue field based on due_date < NOW())
- [ ] T025 [US1] Add duplicate tracking logic in `frontend/src/hooks/useReminders.ts` (session storage with 5-minute deduplication window)
- [ ] T026 [US1] Add fallback toast message for Redpanda failures in `frontend/src/app/tasks/page.tsx` (show warning when event_published=false)

**Checkpoint**: At this point, User Story 1 should be fully functional - create task with due time → wait for due time → toast appears automatically

---

## Phase 4: User Story 2 - Redpanda Cloud Event Streaming (Priority: P1)

**Goal**: Dapr Pub/Sub component publishes events to Redpanda Cloud, consumer processes events and triggers notifications

**Independent Test**: Check Dapr component health, examine backend logs for event publish, confirm Redpanda Cloud receives messages

### Implementation for User Story 2

- [ ] T027 [P] [US2] Add Dapr health check before event publish in `backend/app/services/event_publisher.py` (check component status via HTTP API)
- [ ] T028 [US2] Add Redpanda Cloud connection validation in `backend/app/services/event_publisher.py` (verify bootstrap connectivity on startup)
- [ ] T029 [US2] Add event publish logging in `backend/app/services/event_publisher.py` (log "Published reminder event {id} to task-events" with timestamp)
- [ ] T030 [US2] Add event consumption logging in `backend/app/services/reminder_scheduler.py` (log "Processing reminder event for task {id}" when consuming from Redpanda)
- [ ] T031 [US2] Add retry logic for failed publishes in `backend/app/services/event_publisher.py` (retry up to 5 times with 60-second backoff)
- [ ] T032 [US2] Add fallback status in reminder creation response in `backend/app/routes/reminders.py` (return fallback_mode: true when Redpanda fails)
- [ ] T033 [US2] Create Dapr verification script in `docs/verify-dapr.sh` (commands to check component health, test publish/consume)
- [ ] T034 [US2] Update backend logging configuration in `backend/app/main.py` (ensure INFO level for event publishing logs)

**Checkpoint**: At this point, User Story 2 should be fully functional - Dapr publishes to Redpanda, consumer processes events, logs confirm flow

---

## Phase 5: User Story 3 - Real-Time Task List Updates (Priority: P2)

**Goal**: Task page automatically refreshes every 30 seconds, showing changes without manual reload

**Independent Test**: Open task list in one tab, modify task in another tab, observe changes appear within 30 seconds

### Implementation for User Story 3

- [ ] T035 [P] [US3] Create useTaskPolling hook in `frontend/src/hooks/useTaskPolling.ts` (useEffect with 30-second interval, fetchTasks call)
- [ ] T036 [P] [US3] Add polling integration to tasks page in `frontend/src/app/tasks/page.tsx` (import useTaskPolling, trigger refetch every 30 seconds)
- [ ] T037 [US3] Add editing state tracking in `frontend/src/app/tasks/page.tsx` (isEditing state to pause polling during edits)
- [ ] T038 [US3] Add polling pause logic in `frontend/src/hooks/useTaskPolling.ts` (skip fetch when isEditing=true)
- [ ] T039 [US3] Add visual polling indicator in `frontend/src/app/tasks/page.tsx` (subtle loading state or timestamp showing last refresh)
- [ ] T040 [US3] Add network error handling in `frontend/src/hooks/useTaskPolling.ts` (retry failed requests, show error toast after 3 consecutive failures)
- [ ] T041 [US3] Optimize GET /api/tasks response in `backend/app/routes/tasks.py` (add is_overdue, has_reminder, reminder_due_soon calculated fields)

**Checkpoint**: At this point, User Story 3 should be fully functional - tasks page refreshes every 30 seconds, pauses during edits, shows changes automatically

---

## Phase 6: User Story 4 - Chat Agent Reminder Creation (Priority: P2)

**Goal**: Chat agent parses natural language times, creates tasks with reminders, publishes events

**Independent Test**: Send "Add a task Get medicine add reminder at 9:12 PM" in chat, verify task created with correct due time and reminder scheduled

### Implementation for User Story 4

- [ ] T042 [P] [US4] Enhance time parsing in `backend/app/services/due_date_service.py` (add support for "at HH:MM PM", "in X minutes", "tomorrow at HH:MM" formats)
- [ ] T043 [P] [US4] Add reminder intent detection in `backend/app/services/agent.py` (detect "add reminder", "notify me", "remind me" keywords)
- [ ] T044 [US4] Integrate reminder creation in chat flow in `backend/app/services/agent.py` (call create_reminder after task creation when due_time parsed)
- [ ] T045 [US4] Add reminder confirmation to chat response in `backend/app/services/agent.py` (include "Reminder scheduled for [time]" in response message)
- [ ] T046 [US4] Add invalid time format handling in `backend/app/services/agent.py` (ask for clarification when time parsing fails)
- [ ] T047 [US4] Add event publishing confirmation to chat logs in `backend/app/routes/chat.py` (log "Reminder event published for task {id}" after successful publish)

**Checkpoint**: At this point, User Story 4 should be fully functional - chat creates tasks with reminders, times parsed correctly, events published

---

## Phase 7: User Story 5 - Advanced Task Features (Priority: P3)

**Goal**: Tasks support recurring, priorities, tags, search/filter/sort operations

**Independent Test**: Create task with recurring/priority/tags, verify search/filter/sort returns correct results

### Implementation for User Story 5

- [ ] T048 [P] [US5] Create tag service in `backend/app/services/tag_service.py` (create_tag, get_tags_by_user, add_tag_to_task)
- [ ] T049 [P] [US5] Create priority service in `backend/app/services/priority_service.py` (validate_priority, get_priority_order)
- [ ] T050 [P] [US5] Create recurring task service in `backend/app/services/recurring_task_service.py` (process_recurring_config, create_next_occurrence)
- [ ] T051 [US5] Add tag CRUD endpoints in `backend/app/routes/tags.py` (POST /api/tags, GET /api/tags, DELETE /api/tags/{id})
- [ ] T052 [US5] Add search/filter/sort parameters to GET /api/tasks in `backend/app/routes/tasks.py` (query params: search, tag, priority, sort_by, sort_order)
- [ ] T053 [US5] Add recurring task processing to reminder scheduler in `backend/app/services/reminder_scheduler.py` (check and create next occurrences daily)
- [ ] T054 [P] [US5] Add tag selector UI component in `frontend/src/components/tasks/TagSelector.tsx` (multi-select with autocomplete)
- [ ] T055 [P] [US5] Add priority selector UI component in `frontend/src/components/tasks/PrioritySelector.tsx` (dropdown with high/medium/low options)
- [ ] T056 [P] [US5] Add recurring config UI component in `frontend/src/components/tasks/RecurringConfig.tsx` (frequency picker, end date picker)
- [ ] T057 [US5] Add filter controls to tasks page in `frontend/src/app/tasks/page.tsx` (search bar, tag filter, priority filter, sort dropdown)
- [ ] T058 [US5] Add visual priority indicators to task cards in `frontend/src/app/tasks/page.tsx` (color-coded badges or icons)
- [ ] T059 [US5] Add tag display to task cards in `frontend/src/app/tasks/page.tsx` (pill-style tags with colors)

**Checkpoint**: All user stories should now be independently functional - advanced features enable sophisticated task management

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T060 [P] Update README.md with Redpanda Cloud setup instructions in `README.md` (add quickstart reference, Dapr setup commands)
- [ ] T061 [P] Create troubleshooting guide in `docs/redpanda-troubleshooting.md` (common issues: connection failures, Dapr not injected, duplicate toasts, time zone problems)
- [ ] T062 [P] Add verification commands to quickstart in `docs/quickstart.md` (dapr components check, logs check, port forward check)
- [ ] T063 Create demo script in `docs/demo-script.md` (7-minute demo flow with exact commands and expected outputs)
- [ ] T064 [P] Add performance optimization to task list query in `backend/app/routes/tasks.py` (add database indexes on user_id, due_date, completed columns)
- [ ] T065 [P] Add error boundaries to frontend in `frontend/src/app/tasks/page.tsx` (catch and display polling errors gracefully)
- [ ] T066 Run quickstart.md validation with fresh Minikube cluster (verify all commands work from scratch)
- [ ] T067 Run full acceptance test suite (manual E2E: create task +3min, wait for toast, verify all success criteria)
- [ ] T068 [P] Code cleanup and refactoring (remove unused imports, consolidate duplicate code, add type hints)
- [ ] T069 Security hardening (verify no hardcoded secrets, all credentials in Kubernetes Secret, use Dapr secret store)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 and US2 (both P1) can proceed in parallel after Foundational
  - US3 and US4 (both P2) can proceed in parallel after Foundational
  - US5 (P3) can proceed after Foundational
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1, integrates with same components
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independent, adds polling to tasks page
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent, extends chat agent
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Independent, adds advanced features

### Within Each User Story

- CRUD operations before routes
- Services before integration
- Core implementation before UI components
- Frontend hooks can be developed in parallel with backend services

### Parallel Opportunities

- **Setup Phase**: T003, T004 can run in parallel
- **Foundational Phase**: T007, T008, T012 can run in parallel (after T005-T006)
- **US1**: T013, T014, T022, T023 can run in parallel
- **US2**: T027, T033 can run in parallel
- **US3**: T035, T036 can run in parallel
- **US4**: T042, T043 can run in parallel
- **US5**: T048, T049, T050, T054, T055, T056 can run in parallel
- **Polish**: T060, T061, T062, T065, T066, T068 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task T013: Create reminder CRUD operations in backend/app/crud.py
Task T014: Create Reminder model in backend/app/models.py
Task T022: Create useReminders hook in frontend/src/hooks/useReminders.ts
Task T023: Add toast notification display to tasks page in frontend/src/app/tasks/page.tsx

# After T013-T014 complete:
Task T015: Create reminder routes (depends on T013, T014)

# After T015, T017 complete:
Task T018: Add event publishing call to task creation
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T026) - Core reminder notifications
4. Complete Phase 4: User Story 2 (T027-T034) - Redpanda integration
5. **STOP and VALIDATE**: Full E2E test with task +3min, toast appears, Redpanda events confirmed
6. Deploy/demo if ready

**MVP Deliverable**: Users can create tasks with due times via UI/chat, toast notifications appear automatically when due, Redpanda Cloud receives events

### Incremental Delivery

1. **Foundation**: Setup + Foundational (T001-T012) → Infrastructure ready
2. **MVP**: Add US1 + US2 (T013-T034) → Core event-driven reminders working
3. **Real-time**: Add US3 (T035-T041) → 30-second polling, live updates
4. **Chat Integration**: Add US4 (T042-T047) → Natural language reminder creation
5. **Advanced Features**: Add US5 (T048-T059) → Recurring, priorities, tags, search
6. **Polish**: Add Phase 8 (T060-T069) → Documentation, optimization, hardening

Each increment adds value without breaking previous features.

### Parallel Team Strategy

With 2-3 developers after Foundational phase:

1. **Developer A**: User Story 1 (T013-T026) - Reminder notifications
2. **Developer B**: User Story 2 (T027-T034) - Redpanda integration
3. **Developer C**: User Story 3 (T035-T041) - Polling implementation

After US1-US3 complete:
- **Developer A**: User Story 4 (T042-T047) - Chat agent
- **Developer B**: User Story 5 (T048-T059) - Advanced features
- **Developer C**: Polish tasks (T060-T069) - Documentation, optimization

---

## Summary

| Phase | Tasks | Priority | Est. Time |
|-------|-------|----------|-----------|
| Phase 1: Setup | 4 | - | 15 min |
| Phase 2: Foundational | 8 | Blocking | 30 min |
| Phase 3: US1 (Notifications) | 14 | P1 | 45 min |
| Phase 4: US2 (Redpanda) | 8 | P1 | 30 min |
| Phase 5: US3 (Polling) | 7 | P2 | 30 min |
| Phase 6: US4 (Chat) | 6 | P2 | 25 min |
| Phase 7: US5 (Advanced) | 12 | P3 | 45 min |
| Phase 8: Polish | 10 | - | 30 min |
| **Total** | **69** | | **~4 hours** |

**MVP (US1+US2)**: 34 tasks, ~2 hours

**Parallel Opportunities**: 25 tasks marked [P] for potential parallel execution
