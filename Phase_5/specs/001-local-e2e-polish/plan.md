# Implementation Plan: Local E2E Testing & Polish for Todo AI Chatbot

**Feature Branch**: `001-local-e2e-polish`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 5: Local End-to-End Testing & Polish for Todo AI Chatbot

Create:
- End-to-end test scenario list (user journeys)
- Bug triage & fix checklist
- Logging & error handling improvements
- README polish section (local setup + verification)
- Demo script outline (90-second video flow)

Decisions needing documentation:
- Testing depth (manual only vs add pytest + kubectl exec)
  - Options: full manual, partial automated
  - Tradeoffs: speed vs coverage
- Log level & format (debug vs info, structured JSON vs text)
  - Tradeoffs: debuggability vs noise
- Error handling strategy (graceful messages vs crash)
  - Tradeoffs: user experience vs visibility
- Demo readiness (screenshots, logs, commands)
  - Tradeoffs: detail vs video length

Testing strategy:
- Manual E2E scenarios:
  1. Login → create recurring daily task with due date + priority/tag
  2. Complete task → verify next instance created
  3. Check logs for event publish → consumer processing
  4. Set future due date → wait → see reminder job trigger
  5. Apply filter/sort → verify results
  6. Restart pods → verify recovery
- Automated checks:
  - kubectl get pods → all Running
  - curl health endpoints
  - kubectl logs | grep error → no critical errors
- Acceptance criteria from spec fully validated (no regressions, smooth UX)
- Smoke test after every fix: minikube service --url → login + CRUD

Technical details:
- Use existing Phase V Step 1–4 deployment
- Minikube + Dapr + local Kafka/Redpanda
- Organize by validation areas:
  1. Basic app health & access
  2. Advanced features (recurring, due dates, priority/tag, search/filter/sort)
  3. Event-driven flow (publish → consume)
  4. Dapr validation (sidecars, components, jobs, secrets)
  5. Bug fixes & polish
  6. Documentation & demo prep"

## Technical Context

This plan details the comprehensive end-to-end testing and polishing phase for the Todo AI Chatbot after completing Phase V Steps 1-4 (Advanced Features, Kafka Pub/Sub, Dapr Integration, Minikube Deployment). The focus is on validating all functionality works correctly, identifying and fixing bugs, improving error handling and logging, and preparing comprehensive documentation for hackathon evaluation.

Key decisions to be documented:
- **Testing depth**: Manual-only testing vs adding automated pytest + kubectl exec scripts
- **Log level & format**: Debug vs Info level, structured JSON vs plain text logging
- **Error handling strategy**: Graceful user messages vs crash-fast approach for visibility
- **Demo readiness**: Balance between detailed verification and concise 90-second demo flow

## Constitution Check

- **Spec-Driven Development**: Following spec → plan → tasks → implement cycle
- **AI-Assisted Development**: All bug fixes and improvements via Claude Code
- **Reproducible Environments**: Testing on local Minikube deployment from Step 4
- **Security First**: No secrets hardcoded, using Dapr Secrets API
- **Minimal Viable Changes**: Only fixing bugs and polish, no new features
- **Observability**: Improving logging for debugging maturity demonstration
- **Fail-Fast**: Proper error handling while maintaining user-friendly messages
- **Documentation**: Comprehensive README for hackathon judge evaluation

## Gates

- [ ] All testing scenarios documented in checklist format
- [ ] Bug triage process defined and executed
- [ ] Log level and format decisions made
- [ ] Error handling improvements specified
- [ ] README sections planned (setup, verification, troubleshooting)
- [ ] Demo script outline created (90-second target)

## Phase 0: Research & Architecture Decisions

### research.md

#### Decision: Testing Depth Approach
**Rationale**: Using primarily manual testing with lightweight automated health checks via kubectl and curl. This provides the fastest validation path while maintaining adequate coverage for hackathon evaluation. Automated pytest integration would add complexity without proportional value given time constraints.
**Alternatives considered**:
- Manual + lightweight automated: Fastest path, adequate coverage, selected approach
- Full automated with pytest: More comprehensive but time-intensive to set up
- Manual only: Simple but slower for repeated validation

#### Decision: Log Level & Format
**Rationale**: Using INFO level with structured JSON logging for production-like observability while keeping noise manageable. DEBUG level can be enabled via environment variable for deep troubleshooting when needed. JSON format enables log aggregation and parsing tools.
**Alternatives considered**:
- INFO + JSON: Balanced approach, selected for production-like setup
- DEBUG + text: Maximum visibility but noisy and harder to parse
- INFO + text: Simpler but less tool-friendly

#### Decision: Error Handling Strategy
**Rationale**: Using graceful degradation with user-friendly error messages displayed in UI while logging full error details for debugging. Frontend shows actionable messages ("Task creation failed, please try again") while backend logs stack traces and context. This balances user experience with debugging visibility.
**Alternatives considered**:
- Graceful + detailed logs: Best balance, selected approach
- Crash-fast: Maximum visibility but poor user experience
- Silent failures: Best UX but impossible to debug

#### Decision: Demo Readiness Approach
**Rationale**: Preparing a 90-second demo script showing the key features: login → create recurring task → event flow verification → reminder scheduling. Commands and logs will be pre-captured and documented for inclusion in video/README. This provides maximum impact within hackathon time constraints.
**Alternatives considered**:
- 90-second scripted demo: Focused and impactful, selected approach
- Live unscripted demo: Authentic but risky
- Comprehensive feature walkthrough: Too long for attention span

## Phase 1: Design & Contracts

### data-model.md

#### Test Scenario Entities
- **E2ETestScenario**: Named test case with steps, expected outcomes, validation method
- **BugReport**: Issue description, severity, reproduction steps, fix status
- **LogEntry**: Structured log with timestamp, level, component, message, context
- **VerificationCommand**: kubectl/curl command for automated health checks

#### Documentation Entities
- **READMESection**: Setup instructions, verification commands, troubleshooting guide
- **DemoStep**: Action, expected result, command/log reference, timestamp

### Test Organization Structure

```
E2E Testing Areas:
├── Area 1: Basic Health & Access
│   ├── Pod status verification
│   ├── Service accessibility
│   └── Health endpoint checks
├── Area 2: Advanced Features
│   ├── Recurring tasks (create, complete, next instance)
│   ├── Due dates & reminders
│   ├── Priorities & tags
│   └── Search, filter, sort
├── Area 3: Event-Driven Flow
│   ├── Event publishing verification
│   ├── Consumer processing logs
│   └── End-to-end event tracing
├── Area 4: Dapr Validation
│   ├── Sidecar health checks
│   ├── Component verification
│   ├── Jobs API testing
│   └── Secrets loading validation
├── Area 5: Bug Fixes & Polish
│   ├── Error handling improvements
│   ├── Logging enhancements
│   └── UX refinements
└── Area 6: Documentation & Demo Prep
    ├── README updates
    ├── Verification commands
    └── Demo script creation
```

### quickstart.md

#### Quick Start: E2E Testing & Polish Execution

1. **Prerequisites**:
   - Phase V Step 4 deployment running on Minikube
   - kubectl configured to communicate with cluster
   - Frontend URL from `minikube service todo-frontend --url`

2. **Automated Health Checks**:
   ```bash
   # Check all pods running
   kubectl get pods
   # Expected: All pods in Running state, 1/1 Ready

   # Check Dapr sidecars
   kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
   # Expected: Each app pod shows dapr sidecar container

   # Check services
   kubectl get services
   # Expected: LoadBalancer services for frontend and backend

   # Health endpoint check
   FRONTEND_URL=$(minikube service todo-frontend --url)
   curl $FRONTEND_URL/health
   # Expected: 200 OK response
   ```

3. **Manual E2E Test Scenarios**:
   - See detailed test scenarios in tasks/checklists
   - Execute each scenario sequentially
   - Document results and capture logs for failures

4. **Bug Triage Process**:
   - Record each bug found with severity
   - Categorize by area (feature, infrastructure, UX)
   - Fix via Claude Code implementation
   - Re-test after fix

5. **Log Verification**:
   ```bash
   # Check for errors in backend logs
   kubectl logs deployment/todo-backend --tail=100 | grep -i error

   # Check Dapr sidecar logs
   kubectl logs deployment/todo-backend -c daprd --tail=50

   # Check consumer logs for event processing
   kubectl logs deployment/todo-consumers --tail=100
   ```

6. **Demo Preparation**:
   - Execute demo script steps
   - Capture screenshots at key points
   - Record log excerpts showing event flow
   - Time walkthrough to ensure <90 seconds

## Phase 2: Implementation Strategy

### Layer 1: Basic Health & Access Validation
1. Create pod health verification checklist
2. Verify all services accessible via minikube service URLs
3. Test health endpoints return 200 OK
4. Document expected state and commands

### Layer 2: Advanced Features Testing
1. Test recurring task creation and completion flow
2. Verify due date reminders are scheduled and triggered
3. Validate priority and tag filtering
4. Test search and sort functionality
5. Document each test case with expected results

### Layer 3: Event-Driven Flow Validation
1. Create test task and verify event publishing
2. Check consumer logs for event processing
3. Verify audit trail records all events
4. Test event flow end-to-end with tracing
5. Document event flow with log examples

### Layer 4: Dapr Integration Verification
1. Verify all sidecars are healthy and communicating
2. Validate Dapr components are loaded and functional
3. Test Jobs API with scheduled reminder
4. Verify secrets loading via Dapr Secrets API
5. Document Dapr-specific verification commands

### Layer 5: Bug Triage & Fix
1. Execute all test scenarios and document issues
2. Categorize bugs by severity and area
3. Fix bugs via Claude Code implementation
4. Re-test after each fix to verify resolution
5. Document all fixes in changelog

### Layer 6: Logging & Error Handling Improvements
1. Review current logging and identify gaps
2. Add structured logging at INFO level
3. Improve error messages with actionable guidance
4. Add request ID tracing for debugging
5. Test error scenarios for graceful handling

### Layer 7: Documentation & Demo Prep
1. Write README section: Local Setup Instructions
2. Write README section: Verification Commands
3. Write README section: Troubleshooting Guide
4. Create 90-second demo script with timestamps
5. Prepare log excerpts and screenshot checklist

## Architecture Decision Records (ADRs)

The following architectural decisions require formal ADR documentation:

1. **ADR-005**: Testing depth approach (manual + lightweight automated vs full automated)
2. **ADR-006**: Logging strategy (INFO level + JSON format)
3. **ADR-007**: Error handling pattern (graceful UI + detailed logs)
4. **ADR-008**: Demo presentation approach (90-second scripted flow)

## Risk Analysis

- **Time Overrun Risk**: Comprehensive testing may uncover many issues - prioritize by severity and focus on P1/P2 features first
- **Demo Failure Risk**: Live demos can fail - mitigate by pre-recording flows and having backup screenshots
- **Incomplete Documentation Risk**: README updates may be rushed - allocate dedicated time for documentation
- **Regression Risk**: Bug fixes may break other features - smoke test after every fix
- **Environment Drift Risk**: Minikube state may change between tests - document clean state requirements

## Success Metrics

- [ ] All pods running and healthy (1/1 Ready, no CrashLoopBackOff)
- [ ] Frontend accessible via minikube service URL
- [ ] All P1 advanced features working (recurring tasks, due dates, reminders)
- [ ] Event flow verified: publish → consume → action logged
- [ ] Dapr sidecars healthy in all app pods
- [ ] Dapr components loaded and functional
- [ ] Jobs API schedules and triggers reminders correctly
- [ ] Secrets loaded securely via Dapr Secrets API
- [ ] All critical bugs fixed (severity: high, critical)
- [ ] Log level set to INFO with JSON format
- [ ] Error handling provides user-friendly messages
- [ ] README includes local setup, verification, and troubleshooting sections
- [ ] Demo script documented and executable in <90 seconds
- [ ] No regressions from previous Phase V steps
- [ ] All test scenarios documented with pass/fail results

## Test Scenario Checklist

### Area 1: Basic Health & Access
- [ ] All pods Running and 1/1 Ready
- [ ] No pods in CrashLoopBackOff or Error state
- [ ] All services show LoadBalancer type
- [ ] Frontend accessible via `minikube service todo-frontend --url`
- [ ] Backend health endpoint returns 200 OK
- [ ] No connection refused errors in logs

### Area 2: Advanced Features
- [ ] Can create recurring daily task
- [ ] Completing recurring task creates next instance
- [ ] Due date reminder scheduled via Dapr Jobs API
- [ ] Reminder fires at scheduled time
- [ ] Priority filtering works (high/medium/low)
- [ ] Tag filtering works
- [ ] Full-text search returns matching tasks
- [ ] Sort by due date works correctly
- [ ] Sort by priority works correctly
- [ ] Edit task preserves all fields
- [ ] Delete task removes from database

### Area 3: Event-Driven Flow
- [ ] Task creation publishes event to pub/sub
- [ ] Recurring task consumer processes event
- [ ] Notification consumer logs reminder
- [ ] Audit consumer records event
- [ ] Event contains complete task data
- [ ] Consumer logs show processing timestamp

### Area 4: Dapr Validation
- [ ] All app pods have Dapr sidecar container
- [ ] `dapr status -k` shows all apps healthy
- [ ] `kubectl get components.dapr.io` shows loaded components
- [ ] Pubsub component connects to Kafka
- [ ] State store component connects to PostgreSQL
- [ ] Secrets loaded from Kubernetes secrets
- [ ] Jobs API can schedule and trigger callbacks

### Area 5: Bug Fixes & Polish
- [ ] Error messages are user-friendly and actionable
- [ ] Logs include request context and timestamps
- [ ] No console errors in browser
- [ ] Network errors handled gracefully
- [ ] Loading states displayed for async operations
- [ ] Form validation gives clear feedback

### Area 6: Documentation & Demo
- [ ] README has local setup section
- [ ] README has verification commands section
- [ ] README has troubleshooting guide
- [ ] Demo script has <10 steps
- [ ] Demo script estimated at <90 seconds
- [ ] Screenshots prepared for key demo moments
- [ ] Log excerpts prepared for event flow
