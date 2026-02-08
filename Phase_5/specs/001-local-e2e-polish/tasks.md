---

description: "Task list for Local E2E Testing & Polish - Phase V Sub-phase 5"
---

# Tasks: Local E2E Testing & Polish for Todo AI Chatbot

**Input**: Design documents from `/specs/001-local-e2e-polish/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No automated tests required - manual E2E validation per spec

**Organization**: Tasks are grouped by testing area to enable systematic validation of the deployed application.

## Format: `[ID] [P?] [Area] Description`

- **[P]**: Can run in parallel (different test areas, no dependencies)
- **[Area]**: Testing area identifier (H1, H2, F1, E1, D1, B1, D1)
- Include exact file paths and commands in descriptions

## Path Conventions

- **Application**: `backend/`, `frontend/`, `consumers/`, `charts/`
- **Documentation**: `README.md`, `docs/`
- **Dapr**: `dapr-components/`
- **Tests**: Manual execution with kubectl/curl commands

## Overview

This is a **testing and polish phase**, not a feature implementation phase. The focus is on:
1. Validating existing Phase V Step 1-4 functionality
2. Identifying and fixing bugs
3. Improving logging and error handling
4. Creating comprehensive documentation
5. Preparing demo materials

---

## Phase 1: Setup & Environment Validation

**Purpose**: Verify Minikube deployment is ready for testing

- [ ] T001 Verify Minikube is running: `minikube status`
- [ ] T002 Verify Dapr is installed: `dapr status -k`
- [ ] T003 Verify kubectl is configured: `kubectl get nodes`
- [ ] T004 Check all Phase V Step 4 deployments exist: `kubectl get deployments`
- [ ] T005 Verify frontend URL is accessible: `minikube service todo-frontend --url`

**Checkpoint**: Environment validated - ready to begin systematic testing

---

## Phase 2: Basic Health & Access Validation (Area H1)

**Purpose**: Verify all pods, services, and health endpoints are operational

**Goal**: Confirm deployment is healthy before feature testing

**Independent Test**: All pods Running, services accessible, health endpoints return 200 OK

- [ ] T006 [H1] Check all pods are Running: `kubectl get pods` (expected: 2/2 or 1/1 Ready, no CrashLoopBackOff)
- [ ] T007 [P] [H1] Verify Dapr sidecars present: `kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'`
- [ ] T008 [P] [H1] Check Dapr system status: `dapr status -k` (expected: all apps HEALTHY)
- [ ] T009 [P] [H1] Verify services exposed: `kubectl get services` (expected: LoadBalancer type)
- [ ] T010 [H1] Get frontend URL: `FRONTEND_URL=$(minikube service todo-frontend --url) && echo $FRONTEND_URL`
- [ ] T011 [H1] Test frontend health endpoint: `curl $FRONTEND_URL/health` (expected: HTTP 200)
- [ ] T012 [H1] Test backend health endpoint: `kubectl exec deployment/todo-backend -- curl localhost:8000/health`
- [ ] T013 [H1] Check for critical errors in backend logs: `kubectl logs deployment/todo-backend --tail=100 | grep -i error`
- [ ] T014 [H1] Check for critical errors in consumer logs: `kubectl logs deployment/todo-consumers --tail=100 | grep -i error`

**Checkpoint**: Basic health verified - all components accessible

---

## Phase 3: Advanced Features Testing (Area F1)

**Purpose**: Validate all Phase V advanced features work end-to-end

**Goal**: Confirm recurring tasks, due dates, priorities, tags, search, filter, sort function correctly

**Independent Test**: Create recurring task, complete it, verify next instance created

- [ ] T015 [F1] Test recurring task creation: Login to frontend, create task with recurrence=daily, priority=high, tag="work", due date=tomorrow
- [ ] T016 [F1] Verify task appears in list with recurrence indicator
- [ ] T017 [F1] Complete the recurring task (mark as done)
- [ ] T018 [F1] Verify next instance auto-created for tomorrow
- [ ] T019 [F1] Check consumer logs show task.completed event: `kubectl logs deployment/todo-consumers --tail=50 | grep "task.completed"`
- [ ] T020 [P] [F1] Test due date reminder: Create task with due date 2 minutes in future, note current time
- [ ] T021 [P] [F1] Wait for due date to pass, check logs for reminder firing: `kubectl logs deployment/todo-consumers --tail=100 | grep "reminder"`
- [ ] T022 [P] [F1] Verify Dapr Jobs API scheduled reminder: Check dapr sidecar logs for job scheduling
- [ ] T023 [P] [F1] Test priority filtering: Create tasks with high/medium/low priorities, apply "High only" filter
- [ ] T024 [P] [F1] Verify only high-priority tasks displayed
- [ ] T025 [P] [F1] Test tag filtering: Create tasks with tags (work, personal, urgent), apply "work" filter
- [ ] T026 [P] [F1] Verify only tasks with "work" tag displayed
- [ ] T027 [P] [F1] Test full-text search: Search for term in task title/description
- [ ] T028 [P] [F1] Verify matching tasks highlighted/returned
- [ ] T029 [P] [F1] Test sort by due date: Apply sort, verify chronological order
- [ ] T030 [P] [F1] Test sort by priority: Apply sort, verify priority grouping (high → medium → low)
- [ ] T031 [F1] Test task edit: Edit existing task, verify all fields preserved
- [ ] T032 [F1] Test task delete: Delete task, verify removed from database

**Checkpoint**: All advanced features verified working

---

## Phase 4: Event-Driven Flow Validation (Area E1)

**Purpose**: Verify event publishing and consumer processing

**Goal**: Confirm Dapr + Kafka event flow works end-to-end

**Independent Test**: Create task, observe event published, all consumers process it

- [ ] T033 [E1] Open terminal to watch consumer logs: `kubectl logs deployment/todo-consumers -f`
- [ ] T034 [E1] Create a new task via frontend
- [ ] T035 [E1] Verify task.created event published: Check backend logs for publish confirmation
- [ ] T036 [E1] Verify recurring task consumer processed event: Look for "checked for recurrence" in logs
- [ ] T037 [E1] Verify notification consumer logged event: Look for notification log entry
- [ ] T038 [E1] Verify audit consumer recorded event: Look for audit log entry
- [ ] T039 [E1] Verify event contains complete task data: Check log payload
- [ ] T040 [E1] Verify consumer logs show processing timestamp
- [ ] T041 [E1] Test task.updated event: Edit existing task, verify event published and consumed
- [ ] T042 [E1] Test task.deleted event: Delete task, verify event published and consumed
- [ ] T043 [E1] Verify audit trail records all event types

**Checkpoint**: Event-driven flow verified working

---

## Phase 5: Dapr Integration Validation (Area D1)

**Purpose**: Verify Dapr components, sidecars, and Jobs API are functional

**Goal**: Confirm Dapr abstraction layer works correctly

**Independent Test**: All Dapr components loaded, Jobs API schedules and triggers callbacks

- [ ] T044 [D1] Check Dapr components loaded: `kubectl get components.dapr.io` (expected: STATUS=Loaded)
- [ ] T045 [P] [D1] Verify pubsub component connects to Kafka: Check component logs
- [ ] T046 [P] [D1] Verify state store component connects to PostgreSQL: Check component logs
- [ ] T047 [P] [D1] Verify secrets loaded from Kubernetes: Check sidecar logs for secret loading
- [ ] T048 [D1] Verify Jobs API can schedule: Create task with due date, check job scheduled
- [ ] T049 [D1] Verify Jobs API triggers callback: Wait for due time, verify callback fired
- [ ] T050 [D1] Check Dapr sidecar logs for errors: `kubectl logs deployment/todo-backend -c daprd --tail=100 | grep -i error`
- [ ] T051 [D1] Verify all app pods have healthy sidecars: `kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[?(@.name=="daprd")].ready}{"\n"}{end}'`

**Checkpoint**: Dapr integration verified working

---

## Phase 6: Bug Triage & Fix (Area B1)

**Purpose**: Identify, document, and fix bugs discovered during testing

**Goal**: All critical and high severity bugs fixed

**Independent Test**: Smoke test after each fix (create task, verify it works)

- [ ] T052 [B1] Review all test results and compile bug list with severities
- [ ] T053 [B1] Create bug report template in `specs/001-local-e2e-polish/bug-reports.md`
- [ ] T054 [B1] Document each discovered bug with: title, severity, area, reproduction steps, actual vs expected behavior
- [ ] T055 [B1] Prioritize bugs: critical > high > medium > low
- [ ] T056 [B1] Fix critical bugs via Claude Code implementation
- [ ] T057 [B1] Smoke test after critical fixes: Login + create task + verify works
- [ ] T058 [B1] Fix high severity bugs via Claude Code implementation
- [ ] T059 [B1] Re-test affected scenarios after high severity fixes
- [ ] T060 [B1] Fix medium severity bugs (time permitting)
- [ ] T061 [B1] Document all fixes in `specs/001-local-e2e-polish/changelog.md`
- [ ] T062 [B1] Verify no regressions: Re-run Phase 3-5 test scenarios after fixes

**Checkpoint**: Bugs documented and fixed

---

## Phase 7: Logging & Error Handling Improvements (Area L1)

**Purpose**: Improve logging quality and error messages

**Goal**: INFO level with JSON logging, user-friendly error messages

**Independent Test**: Trigger error scenarios, verify friendly messages in UI and details in logs

- [ ] T063 [L1] Review current logging in `backend/app/main.py` and identify gaps
- [ ] T064 [L1] Review current logging in `consumers/main.py` and identify gaps
- [ ] T065 [P] [L1] Add structlog dependency to `backend/requirements.txt` if not present
- [ ] T066 [P] [L1] Configure structured JSON logging in `backend/app/utils/logging.py`
- [ ] T067 [L1] Set default log level to INFO, enable DEBUG via LOG_LEVEL env var
- [ ] T068 [L1] Add request ID tracing middleware in `backend/app/middleware/request_id.py`
- [ ] T069 [L1] Update all log calls to include request_id context
- [ ] T070 [L1] Review error messages in frontend for technical jargon
- [ ] T071 [L1] Update frontend error handling to show user-friendly messages
- [ ] T072 [L1] Add loading states for async operations in frontend
- [ ] T073 [L1] Test error scenarios: Invalid input, network errors, connection failures
- [ ] T074 [L1] Verify logs show full error details (stack trace, context) for debugging
- [ ] T075 [L1] Verify UI shows actionable error messages for users

**Checkpoint**: Logging and error handling improved

---

## Phase 8: Documentation & Demo Prep (Area D1)

**Purpose**: Create comprehensive documentation and demo materials

**Goal**: README with setup/verification/troubleshooting, 90-second demo script

**Independent Test**: Follow README instructions, verify all commands work

- [ ] T076 [D1] Create "Local Setup" section in `README.md` with Minikube start, Dapr init, deployment commands
- [ ] T077 [D1] Create "Verification Commands" section in `README.md` with all health check commands
- [ ] T078 [D1] Create "Troubleshooting Guide" section in `README.md` with common issues and solutions
- [ ] T079 [P] [D1] Add "Testing Checklist" to `README.md` with all test scenarios
- [ ] T080 [P] [D1] Create demo script outline in `docs/demo-script.md` with 90-second timing
- [ ] T081 [D1] Add demo steps: 0:00-0:15 Introduction & Login
- [ ] T082 [D1] Add demo steps: 0:15-0:35 Create Recurring Task
- [ ] T083 [D1] Add demo steps: 0:35-0:55 Show Event Flow
- [ ] T084 [D1] Add demo steps: 0:55-0:75 Schedule Reminder
- [ ] T085 [D1] Add demo steps: 0:75-0:90 Summary
- [ ] T086 [D1] Prepare log excerpts for event flow section in `docs/log-examples.md`
- [ ] T087 [D1] Create screenshot checklist in `docs/screenshots.md` (7 key moments)
- [ ] T088 [D1] Capture screenshots: Login screen, task list, create form, new task, consumer logs, Dapr components, pod status
- [ ] T089 [D1] Time demo walkthrough to verify <90 seconds
- [ ] T090 [D1] Update README with "Demo Preparation" section referencing demo script

**Checkpoint**: Documentation complete, demo materials ready

---

## Phase 9: Final Validation & Polish

**Purpose**: End-to-end validation and final touches

**Goal**: All acceptance criteria met, demo-ready

**Independent Test**: Execute full demo script, verify all features work smoothly

- [ ] T091 Run complete test suite from Phases 2-5 after all fixes
- [ ] T092 Verify all success criteria from spec are met
- [ ] T093 Execute 90-second demo script end-to-end
- [ ] T094 Verify no console errors in browser DevTools
- [ ] T095 Verify no critical errors in any pod logs: `kubectl logs --all-containers=true --tail=100 -l 'app in (todo-backend,todo-consumers,todo-frontend)' | grep -i "ERROR\|CRITICAL"`
- [ ] T096 Verify frontend responsive and usable
- [ ] T097 Verify all README commands execute successfully
- [ ] T098 Verify troubleshooting guide solutions work
- [ ] T099 Create test results summary in `specs/001-local-e2e-polish/test-results.md`
- [ ] T100 Create known issues document if any bugs remain unfixed
- [ ] T101 Final smoke test: Login → Create recurring task → Complete → Verify next instance → Check logs
- [ ] T102 Mark feature as ready for hackathon submission

**Checkpoint**: Feature complete and demo-ready

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Basic Health)**: Depends on Phase 1 - BLOCKS all feature testing
- **Phases 3-5 (Feature/Event/Dapr Testing)**: Can run in parallel after Phase 2, but recommended sequential for systematic validation
- **Phase 6 (Bug Fix)**: Depends on Phases 3-5 completion - needs bug list from testing
- **Phase 7 (Logging)**: Can run in parallel with Phase 6 after initial testing
- **Phase 8 (Documentation)**: Can run in parallel with Phase 6-7, but final polish should wait until fixes are done
- **Phase 9 (Final Validation)**: Depends on all previous phases - MUST be last

### Within Each Phase

- Tasks marked [P] can run in parallel (different commands, different files)
- Verification steps depend on test execution completing first
- Bug fixing (Phase 6) follows iterative cycle: find → fix → verify → next bug

### Parallel Opportunities

- **Phase 2**: T007, T008, T009 can run in parallel (different health checks)
- **Phase 3**: T020, T023, T027, T029 can run in parallel (different feature tests)
- **Phase 5**: T045, T046, T047 can run in parallel (different component checks)
- **Phase 7**: T065, T066 can run in parallel (different logging components)
- **Phase 8**: T079, T080 can start in parallel (different documentation sections)

---

## Parallel Example: Feature Testing (Phase 3)

```bash
# Terminal 1: Test recurring tasks
Task: "Test recurring task creation via frontend"

# Terminal 2: Test due date reminders (wait 2 min)
Task: "Test due date reminder: Create task with due date 2 minutes in future"

# Terminal 3: Test priority/tag filtering
Task: "Test priority filtering: Create tasks with high/medium/low priorities"
```

---

## Implementation Strategy

### Systematic Validation Approach

1. Complete Phase 1: Setup → Environment ready
2. Complete Phase 2: Basic Health → Confirm deployment healthy
3. Complete Phases 3-5 sequentially: Feature → Events → Dapr validation
4. Complete Phase 6: Bug Fix → Address discovered issues
5. Complete Phase 7: Logging → Improve observability
6. Complete Phase 8: Documentation → Create demo materials
7. Complete Phase 9: Final Validation → Confirm all criteria met

### Iterative Bug Fix Approach

1. Run Phases 3-5 to discover bugs
2. Document all bugs with severity
3. Fix critical bugs first (blocking issues)
4. Smoke test after each fix
5. Fix high/medium bugs
6. Re-run affected test scenarios
7. Verify no regressions

### Demo Preparation Approach

1. Begin documentation (Phase 8) early - can work in parallel
2. Capture log excerpts and screenshots during testing phases
3. Practice demo script multiple times to ensure <90 seconds
4. Have backup screenshots ready in case of live demo issues

---

## Notes

- This is a testing/polish phase - no new features being implemented
- All changes should be minimal and targeted (fix bugs, don't refactor)
- Use Claude Code for all bug fixes and improvements
- Manual testing focus - automated health checks via kubectl/curl only
- Keep detailed notes of bugs discovered and fixes applied
- All changes traceable to this spec: `specs/001-local-e2e-polish/spec.md`
- After each fix, run smoke test: Login → Create task → Verify works
- Demo success critical for hackathon evaluation
