# Feature Specification: Local E2E Testing & Polish

**Feature Branch**: `001-local-e2e-polish`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 5: Local End-to-End Testing & Polish for Todo AI Chatbot"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify Advanced Todo Features Work End-to-End (Priority: P1)

As a hackathon judge, I want to see all advanced todo features working correctly in the local environment so that I can verify the application meets its functional requirements.

**Why this priority**: This is the core value proposition - demonstrating that all Phase V features (recurring tasks, due dates, reminders, priorities, tags, search, filter, sort) actually work as specified.

**Independent Test**: Can be fully tested by creating a recurring task, setting a due date, and verifying event-driven behavior without needing any other features to work.

**Acceptance Scenarios**:

1. **Given** a user is logged in, **When** they create a task with recurrence (daily), **Then** the task is created and marked as recurring
2. **Given** a recurring task exists, **When** the user completes it, **Then** a new instance is automatically created for the next occurrence
3. **Given** a task with a due date exists, **When** the due date is set, **Then** a reminder event is published and scheduled via Dapr Jobs
4. **Given** tasks exist with various priorities, **When** the user filters by priority, **Then** only matching tasks are displayed
5. **Given** tasks exist with tags, **When** the user searches by tag, **Then** only matching tasks are displayed
6. **Given** multiple tasks exist, **When** the user sorts by due date, **Then** tasks are displayed in chronological order

---

### User Story 2 - Verify Event-Driven Architecture Works Correctly (Priority: P2)

As a hackathon judge, I want to see event-driven flow working so that I can verify the Dapr and Kafka/Redpanda integration is functional.

**Why this priority**: Demonstrates the technical sophistication of the solution and validates that the microservices architecture is operational.

**Independent Test**: Can be tested by creating any task and observing the event logs in consumer services.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** a task is created, **Then** a "task.created" event is published to the pub/sub
2. **Given** an event is published, **When** the recurring task consumer receives it, **Then** it processes the event and logs the action
3. **Given** an event is published, **When** the notification consumer receives it, **Then** it logs a reminder notification
4. **Given** an event is published, **When** the audit consumer receives it, **Then** it logs the event to the audit trail
5. **Given** all pods are running, **When** checking pod status, **Then** all Dapr sidecars show as healthy/ready

---

### User Story 3 - Verify Stability and Error Handling (Priority: P3)

As a hackathon judge, I want to see the application runs without crashes or errors so that I can verify production readiness.

**Why this priority**: Demonstrates stability and debugging maturity - critical for judging.

**Independent Test**: Can be verified by monitoring pod status and logs during normal operation.

**Acceptance Scenarios**:

1. **Given** the application is deployed, **When** checking pod status, **Then** no pods are in CrashLoopBackOff state
2. **Given** the application is running, **When** using the frontend, **Then** no connection refused errors occur
3. **Given** a user performs an invalid action, **When** the error occurs, **Then** a user-friendly error message is displayed
4. **Given** the application is under load, **When** requests are made, **Then** logs show proper error handling and status codes

---

### User Story 4 - Access Comprehensive Documentation (Priority: P4)

As a hackathon judge, I want to find clear documentation on how to verify the application so that I can understand what I'm evaluating.

**Why this priority**: Enables judges to quickly understand and verify the application without asking questions.

**Independent Test**: Can be verified by reading the README and following the verification commands.

**Acceptance Scenarios**:

1. **Given** a judge accesses the repository, **When** they read the README, **Then** they find clear local setup instructions
2. **Given** the README is open, **When** following verification commands, **Then** all commands execute successfully
3. **Given** an issue occurs, **When** checking the troubleshooting section, **Then** common issues have documented solutions
4. **Given** a demo is being prepared, **When** reading the demo steps, **Then** a clear end-to-end flow is documented

---

### Edge Cases

- What happens when Dapr sidecar fails to start?
- How does the system handle Kafka connection failures?
- What happens when a scheduled reminder job fails to execute?
- How does the system handle database connection timeouts?
- What happens when a user creates a recurring task with invalid dates?
- How does the system handle concurrent task modifications?
- What happens when pod resource limits are exceeded?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support creating recurring tasks that auto-generate next instances upon completion
- **FR-002**: System MUST support setting due dates on tasks with reminder scheduling
- **FR-003**: System MUST publish events for all task CRUD operations (create, read, update, delete)
- **FR-004**: System MUST consume events via at least three consumers: recurring task service, notification service, and audit service
- **FR-005**: System MUST support task filtering by priority (high, medium, low)
- **FR-006**: System MUST support task tagging with ability to filter by tag
- **FR-007**: System MUST support full-text search across task titles and descriptions
- **FR-008**: System MUST support task sorting by due date, priority, and creation date
- **FR-009**: System MUST deploy with Dapr sidecars in all service pods
- **FR-010**: System MUST use Kafka/Redpanda for pub/sub messaging
- **FR-011**: System MUST use Dapr Jobs API for scheduling reminder callbacks
- **FR-012**: System MUST load secrets securely via Dapr Secrets API
- **FR-013**: System MUST run without pod crashes or CrashLoopBackOff errors
- **FR-014**: Frontend MUST be accessible via minikube service URL
- **FR-015**: System MUST provide clear error messages for all failure scenarios
- **FR-016**: System MUST log all events and errors for debugging
- **FR-017**: README MUST include local setup instructions
- **FR-018**: README MUST include verification commands to test all features
- **FR-019**: README MUST include troubleshooting section for common issues
- **FR-020**: README MUST include demo script showing end-to-end flow

### Key Entities

- **Task**: Core entity with title, description, priority (high/medium/low), due date, tags, recurrence rules, completion status
- **TaskEvent**: Event published on task changes (created, updated, deleted, completed)
- **Reminder**: Scheduled job for task due date reminders
- **AuditLog**: Record of all events processed by audit consumer
- **User**: Entity for authentication and task ownership

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All advanced features (recurring tasks, due dates, reminders, priorities, tags, search, filter, sort) work end-to-end without errors
- **SC-002**: Dapr sidecars are healthy in all pods (100% of pods show Dapr sidecar as ready)
- **SC-003**: Event flow works: publish → consume → action taken (100% of test events flow correctly)
- **SC-004**: Dapr Jobs API triggers callbacks at scheduled time (reminders fire within 1 minute of due time)
- **SC-005**: No pod crashes, CrashLoopBackOff, or connection refused errors during 30-minute test period
- **SC-006**: Frontend is accessible and usable via minikube service --url
- **SC-007**: All user journeys (login, CRUD, chatbot, advanced features) complete without errors
- **SC-008**: README includes complete local setup, verification commands, and troubleshooting sections
- **SC-009**: Demo can be performed following documented steps in under 10 minutes
- **SC-010**: All bugs and issues discovered during testing are fixed and verified

## Scope & Constraints

### In Scope

- Comprehensive end-to-end testing of all Phase V features locally on Minikube
- Bug fixes and polish for existing features only
- Documentation improvements (README, demo guide, troubleshooting)
- UI/UX improvements for error handling and user feedback
- Logging improvements for debugging

### Out of Scope

- Cloud deployment (deferred to final phase)
- Production-grade monitoring (Prometheus, Grafana, Loki)
- Automated E2E testing pipeline (manual verification acceptable)
- Real email/push notifications (mock/log only)
- Advanced security features (RBAC, mTLS beyond basic auth)
- Performance/load testing (functional correctness only)
- New major features

### Constraints

- Local Minikube deployment only
- Use existing Phase V Step 1-4 code, charts, and Dapr components
- Testing manual + automated with kubectl, curl, logs
- Keep changes minimal and targeted (fix bugs, don't refactor)
- Complete quickly before cloud deferral

## Assumptions

- Minikube is installed and running on the evaluator's machine
- kubectl is configured to communicate with the Minikube cluster
- Phase V Steps 1-4 have been successfully deployed and are functional
- Database schema includes all required tables for advanced features
- Kafka/Redpanda and Dapr are installed in the Minikube cluster
- Default resource limits are sufficient for testing workloads

## Dependencies

- Existing Phase V Step 1-4 implementation
- Dapr runtime installed in Minikube
- Kafka/Redpanda running in Minikube
- PostgreSQL database running with proper schema
- Frontend application deployed and accessible
