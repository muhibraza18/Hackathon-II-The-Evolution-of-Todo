# Feature Specification: Phase V – Redpanda Cloud Integration + Real-Time Reminders

**Feature Branch**: `009-redpanda-reminders`
**Created**: 2025-02-07
**Status**: Draft
**Input**: User description: "Phase V – Local Completion: Redpanda Cloud Integration + Real-Time Reminders (No Cloud Deployment)"

## Overview

**Purpose**: Replace in-memory pub/sub with cloud-based event streaming using Redpanda Cloud, and add real-time reminder notifications for hackathon judges to evaluate full event-driven architecture maturity.

**Target Audience**: Hackathon judges evaluating event-driven maturity, Dapr usage, real-time UI updates, and local deployment readiness before cloud deployment.

**Scope Summary**:
- **In Scope**: Redpanda Cloud integration (Kafka-compatible), real-time reminder toast notifications, automatic overdue badge updates via polling, task list auto-refresh every 30 seconds, reminder scheduler service, verification of all Phase V local requirements
- **Out of Scope**: Cloud deployment (AKS/GKE/OKE), advanced monitoring/logging stack (Prometheus/Grafana), CI/CD pipeline, multi-region or high-availability setup

## User Scenarios & Testing

### User Story 1 - Cloud-Based Reminder Notifications (Priority: P1)

A user creates a task with a due time (e.g., "3 minutes from now") via chat or the tasks page. When the due time arrives, the user sees a visible toast notification appearing automatically with the message "Reminder: [task title] is due now!" and the task list automatically refreshes to show the overdue badge without requiring manual page reload.

**Why this priority**: This is the core demonstration of event-driven architecture using Redpanda Cloud for hackathon judges. It shows the complete flow: task creation → event publish → reminder trigger → notification → UI update.

**Independent Test**: Can be fully tested by creating a task with a due time 3 minutes in the future, waiting 3 minutes, and verifying the toast notification appears with correct message and overdue badge shows automatically.

**Acceptance Scenarios**:

1. **Given** a logged-in user on the tasks page, **When** they create a task with a due time set to 3 minutes in the future, **Then** after 3 minutes a toast notification appears saying "Reminder: [task title] is due now!"
2. **Given** a user with a task due in 3 minutes, **When** the due time arrives, **Then** the overdue badge appears automatically on the task without page refresh
3. **Given** a user viewing the task list, **When** a task becomes overdue, **Then** the task list refreshes automatically to reflect the updated status
4. **Given** multiple tasks with different due times, **When** each task's due time arrives, **Then** separate toast notifications appear for each task

---

### User Story 2 - Redpanda Cloud Event Streaming (Priority: P1)

A system administrator configures the Dapr Pub/Sub component to use Redpanda Cloud instead of in-memory pub/sub. The system publishes reminder events to Redpanda Cloud, and a consumer service processes these events to trigger notifications at the exact due time.

**Why this priority**: This demonstrates production-ready event streaming architecture using cloud-managed Kafka-compatible service, a key requirement for hackathon evaluation of event-driven maturity.

**Independent Test**: Can be verified by checking Dapr component health status, examining backend logs for successful event publish, and confirming Redpanda Cloud receives and processes messages.

**Acceptance Scenarios**:

1. **Given** a configured Redpanda Cloud account, **When** the Dapr Pub/Sub component is applied with Redpanda credentials, **Then** the component shows as healthy
2. **Given** a task with a due time is created, **When** the task is saved to database, **Then** a reminder event is published to Redpanda Cloud
3. **Given** a published reminder event, **When** the consumer service processes the event, **Then** the reminder is scheduled and backend logs confirm event receipt
4. **Given** Redpanda Cloud connection, **When** the due time arrives, **Then** the reminder notification is triggered

---

### User Story 3 - Real-Time Task List Updates (Priority: P2)

A user viewing the tasks page sees the task list automatically refresh every 30 seconds, reflecting changes like newly overdue tasks, completed tasks, or updated priorities without requiring manual refresh.

**Why this priority**: This provides the real-time experience for hackathon judges without implementing WebSocket infrastructure, using simple polling as specified in constraints.

**Independent Test**: Can be tested by opening the task list in one browser tab and modifying a task in another tab, then observing the changes appear within 30 seconds automatically.

**Acceptance Scenarios**:

1. **Given** a user viewing the task list, **When** 30 seconds pass, **Then** the task list automatically refreshes to show any changes
2. **Given** a task with approaching due time, **When** the due time is reached, **Then** the overdue badge appears within 30 seconds
3. **Given** multiple users viewing the same task list, **When** one user completes a task, **Then** other users see the updated status within 30 seconds
4. **Given** a user actively editing a task, **When** the 30-second refresh occurs, **Then** the user's current edits are not disrupted (refresh pauses during editing)

---

### User Story 4 - Chat Agent Reminder Creation (Priority: P2)

A user types a natural language request in chat like "Add a task Get medicine add reminder at 9:12 PM to be notified" and the system correctly parses the due time, creates the task with reminder, and schedules the notification.

**Why this priority**: This demonstrates the AI agent's ability to handle time parsing and reminder scheduling, showcasing the complete integration of chat, backend processing, and event publishing.

**Independent Test**: Can be tested by sending the specific chat message and verifying the task is created with correct due time and reminder is scheduled.

**Acceptance Scenarios**:

1. **Given** a logged-in user on the chat page, **When** they type "Add a task Get medicine add reminder at 9:12 PM to be notified", **Then** a task titled "Get medicine" is created with a due date set to today at 9:12 PM
2. **Given** a task created via chat with a reminder time, **When** the task is saved, **Then** a reminder event is published to Redpanda Cloud
3. **Given** multiple reminder formats in chat (e.g., "in 5 minutes", "at 3pm", "tomorrow at 10am"), **When** tasks are created, **Then** all times are correctly parsed and reminders scheduled
4. **Given** a chat request with invalid time format, **When** the agent processes the request, **Then** it asks for clarification rather than creating an invalid task

---

### User Story 5 - Advanced Task Features (Priority: P3)

A user creates tasks with advanced features including recurring tasks, priorities, tags, due dates with specific times, and can search, filter, and sort tasks across these dimensions.

**Why this priority**: These features showcase the full capability of the task management system for hackathon judges, demonstrating data model completeness and UI sophistication.

**Independent Test**: Can be tested by creating tasks with various combinations of features and verifying search/filter/sort operations return correct results.

**Acceptance Scenarios**:

1. **Given** a user creating a task, **When** they set it to recur daily, **Then** new tasks are automatically created for each subsequent day
2. **Given** tasks with different priorities (high, medium, low), **When** the user sorts by priority, **Then** tasks appear in correct priority order
3. **Given** tasks with various tags (work, personal, urgent), **When** the user filters by tag "work", **Then** only work-tagged tasks appear
4. **Given** many tasks in the list, **When** the user searches for a keyword, **Then** matching tasks appear instantly

---

### Edge Cases

- What happens when Redpanda Cloud connection is lost during event publishing?
- How does the system handle tasks with due times in the past (overdue on creation)?
- What happens when a user completes a task that has an overdue reminder scheduled?
- How does the system handle duplicate reminder notifications for the same task?
- What happens when the reminder scheduler service restarts while reminders are pending?
- How does the system handle time zone changes for existing reminders?
- What happens when a user is logged out when a reminder is due?
- How does the system handle tasks with invalid or unparseable due times?
- What happens when multiple tasks become overdue simultaneously?
- How does the polling mechanism handle network interruptions during refresh?

## Requirements

### Functional Requirements

- **FR-001**: System MUST publish reminder events to Redpanda Cloud when tasks with due times are created
- **FR-002**: System MUST consume reminder events from Redpanda Cloud and schedule notifications for exact due times
- **FR-003**: System MUST display toast notifications when reminder due time arrives with message format "Reminder: [task title] is due now!"
- **FR-004**: System MUST automatically update overdue badges on tasks without requiring manual page refresh
- **FR-005**: System MUST refresh the task list every 30 seconds to reflect changes
- **FR-006**: Dapr Pub/Sub component MUST use Redpanda Cloud with SASL_SSL authentication and SCRAM-SHA-256 mechanism
- **FR-007**: System MUST support creating tasks with reminders via chat agent using natural language time parsing
- **FR-008**: System MUST support recurring tasks with configurable frequency
- **FR-009**: System MUST support task priorities (high, medium, low) with visual indicators
- **FR-010**: System MUST support task tags for categorization and filtering
- **FR-011**: System MUST support search, filter, and sort operations on task list
- **FR-012**: System MUST log all event publishing and reminder triggers for verification
- **FR-013**: Backend MUST confirm Dapr Pub/Sub component health before publishing events
- **FR-014**: Frontend MUST use existing toast notification library for reminders
- **FR-015**: Frontend MUST pause auto-refresh during user editing to prevent disruption

### Key Entities

- **Task**: Represents a todo item with attributes including title, description, due date (with optional time), priority (high/medium/low), completion status, recurring configuration, and tags
- **Reminder**: Represents a scheduled notification for a task, linked to a specific task ID with trigger time and status (pending/sent/failed)
- **Reminder Event**: Represents a published event message containing task ID, user ID, due time, and notification metadata for Redpanda Cloud
- **Tag**: Represents a category label that can be associated with multiple tasks for filtering and organization
- **Recurring Configuration**: Defines how a task repeats with attributes for frequency (daily/weekly/monthly) and end conditions

## Success Criteria

### Measurable Outcomes

- **SC-001**: Dapr Pub/Sub component shows status "healthy" when queried with verification command
- **SC-002**: Task with due time 3 minutes in the future triggers toast notification within 10 seconds of due time
- **SC-003**: Overdue badge appears on task within 30 seconds of due time without manual refresh
- **SC-004**: Backend logs show event publish confirmation when task with reminder is created
- **SC-005**: Backend logs show reminder trigger confirmation when due time is reached
- **SC-006**: Task list reflects changes from other users within 30 seconds (polling interval)
- **SC-007**: Chat agent correctly parses and creates tasks with reminders in 95% of natural language time formats
- **SC-008**: All advanced features (recurring, priorities, tags, search, filter, sort) are visible and functional in UI
- **SC-009**: Page load time remains under 2 seconds (no regression from polling overhead)
- **SC-010**: Task completion checkbox responds instantly (no regression from background processes)
- **SC-011**: User session persists correctly across page refreshes (no regression)
- **SC-012**: Redpanda Cloud receives and acknowledges all published reminder events

### Technical Validation

- Verification command `dapr components -k` shows kafka-pubsub component with status "healthy"
- Redpanda Cloud bootstrap connection successful to `d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092`
- SASL authentication succeeds with username `todo-phase5` using SCRAM-SHA-256
- Toast notification appears with exact format "Reminder: [title] is due now!"
- No errors in backend logs related to Redpanda Cloud connection or event publishing
- Polling interval configured to 30 seconds with pause during active editing

## Assumptions

1. Redpanda Cloud credentials provided are valid and have necessary permissions for the cluster
2. The system has network connectivity to Redpanda Cloud endpoints from the local Minikube environment
3. react-hot-toast library is already installed in the frontend project
4. Dapr sidecar is already installed and configured for the backend service
5. Users are comfortable with polling-based updates (no WebSocket implementation required)
6. All date/times are handled in the server's local timezone unless otherwise specified
7. Reminder scheduler runs as a background service/process within the backend pod
8. Tasks page is the primary interface where users will see reminder notifications

## Dependencies

1. **Redpanda Cloud Cluster**: Active Redpanda Cloud instance with provided credentials
2. **Dapr Runtime**: Dapr sidecar injected into backend deployment
3. **Existing Task Database**: PostgreSQL database with tasks table already populated
4. **Chat Agent Service**: AI agent service for natural language processing and task creation
5. **Frontend Toast Library**: react-hot-toast for notification display
6. **Kubernetes Cluster**: Minikube cluster running for local deployment
7. **Helm Charts**: Existing Helm charts for backend and frontend deployments

## Out of Scope Items

The following items are explicitly NOT part of this phase:

1. **Cloud Deployment**: Deployment to AKS, GKE, OKE, or other cloud Kubernetes platforms
2. **Monitoring Stack**: Prometheus, Grafana, or other advanced monitoring/logging tools
3. **CI/CD Pipeline**: GitHub Actions, GitLab CI, or other automated deployment pipelines
4. **WebSocket Implementation**: Real-time updates via WebSocket connections (using polling instead)
5. **Multi-Region Deployment**: High-availability across multiple geographic regions
6. **Email/SMS Notifications**: External notification delivery beyond in-app toasts
7. **Mobile Applications**: iOS or Android mobile apps
8. **Advanced Analytics**: Usage analytics, dashboards, or reporting beyond basic logs

## Open Questions

None at this time. All requirements are clear based on the provided feature description and Redpanda Cloud credentials.
