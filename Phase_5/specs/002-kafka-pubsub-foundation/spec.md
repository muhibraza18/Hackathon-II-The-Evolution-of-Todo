# Feature Specification: Event-Driven Foundation (Kafka / PubSub)

**Feature Branch**: `002-kafka-pubsub-foundation`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 2: Event-Driven Foundation (Kafka / PubSub) for Todo AI Chatbot

Target audience: Hackathon judges evaluating event-driven architecture maturity, decoupling, and preparation for scalable microservices

Focus:
- Define all required Kafka/Redpanda topics (task-events, reminders, task-updates)
- Establish consistent event schemas (JSON payloads) for task lifecycle and reminders
- Implement basic producer logic in backend (publish events on task CRUD + reminder triggers)
- Implement basic consumer logic in new services (recurring task generator, notification placeholder, audit log)
- Prepare abstraction layer so Kafka can be swapped with Dapr Pub/Sub later without code changes  Success criteria:
- Three topics created and documented: task-events, reminders, task-updates
- All events have well-defined JSON schemas (event_type, task_id, user_id, timestamp, payload)
- Backend publishes events on create/update/complete/delete + reminder scheduling
- Placeholder consumers exist (log events, simulate next recurring task, mock notification)
- No direct Kafka client code in core app – use wrapper or Dapr-ready interface
- Events are traceable (logs show publish + consume)
- Deployment scripts (Helm or kubectl) include Kafka/Redpanda setup (Strimzi or Docker)
- No regressions in Phase V Step 1 features (recurring, due dates, etc.)
- All changes traceable to this spec (@specs/event-driven/kafka-pubsub-foundation.md) Constraints:
- Use existing Phase V Step 1 backend (FastAPI + SQLModel) as base
- Prefer self-hosted Kafka via Strimzi operator on Minikube (or Redpanda Docker)
- No Redpanda Cloud or Confluent Cloud yet (defer to later cloud sub-phase)
- Consumers are minimal (log + basic logic) – full processing in later steps
- No real-time client sync yet (only backend-to-backend events)
- Keep producer/consumer code simple and testable (unit tests for publish/consume)
- Timeline: Complete this sub-phase before moving to Dapr integration  Not building:
- Full Dapr Pub/Sub abstraction (defer to Step 3)
- Real notification delivery (email/push) – only event publish + mock consumer
- Advanced Kafka config (partitions, replication, schema registry)
- Monitoring Kafka lag / throughput (defer to observability stretch goal)
- Multi-consumer groups or complex routing
- WebSocket broadcasting (defer to later real-time sync)
- Cloud-managed Kafka (Redpanda Cloud / Confluent) – local only for now"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Event Publishing (Priority: P1)

As a system architect, I want the backend to publish events to Kafka topics when task lifecycle operations occur (create, update, complete, delete), so that other services can react to these changes asynchronously without tight coupling.

**Why this priority**: This is the core functionality that enables event-driven architecture and decouples services in the system.

**Independent Test**: Can be fully tested by creating a task, updating it, completing it, and deleting it, then verifying that appropriate events are published to the Kafka topics and can be consumed.

**Acceptance Scenarios**:

1. **Given** user creates a new task, **When** task is saved to database, **Then** a "task.created" event should be published to the "task-events" topic
2. **Given** user updates an existing task, **When** update is processed, **Then** a "task.updated" event should be published to the "task-events" topic
3. **Given** user completes a task, **When** completion is processed, **Then** a "task.completed" event should be published to the "task-events" topic
4. **Given** user deletes a task, **When** deletion is processed, **Then** a "task.deleted" event should be published to the "task-events" topic

---

### User Story 2 - Reminder Event Publishing (Priority: P1)

As a system architect, I want the system to publish reminder events to Kafka when tasks have upcoming due dates, so that a separate notification service can process these reminders without blocking the main task operations.

**Why this priority**: This enables the separation of concerns between task management and notification delivery, supporting scalable microservices architecture.

**Independent Test**: Can be fully tested by creating tasks with future due dates, then verifying that appropriate reminder events are published to the "reminders" topic at the appropriate times.

**Acceptance Scenarios**:

1. **Given** user creates a task with a due date, **When** due date approaches, **Then** a "task.reminder" event should be published to the "reminders" topic
2. **Given** user modifies a task's due date, **When** change is processed, **Then** appropriate reminder events should be published or cancelled as needed

---

### User Story 3 - Event Consumption and Processing (Priority: P2)

As a system architect, I want placeholder consumer services to exist that can process events from Kafka topics, so that the event-driven architecture is complete and ready for future expansion.

**Why this priority**: Having both producers and consumers validates the end-to-end event flow and demonstrates the architecture's readiness.

**Independent Test**: Can be fully tested by publishing events to Kafka and verifying that consumer services process them (even if just logging the events).

**Acceptance Scenarios**:

1. **Given** "task.created" event is published to "task-events" topic, **When** consumer processes the event, **Then** it should log the event and potentially trigger placeholder logic
2. **Given** "task.reminder" event is published to "reminders" topic, **When** reminder consumer processes the event, **Then** it should log the event and potentially trigger placeholder notification logic
3. **Given** recurring task is completed, **When** "task.completed" event indicates recurring pattern, **Then** consumer should generate next occurrence

---

### User Story 4 - Abstraction Layer Implementation (Priority: P2)

As a developer, I want an abstraction layer that hides the implementation details of Kafka, so that the core application code doesn't depend directly on Kafka and can be switched to Dapr or another pub/sub system later.

**Why this priority**: This ensures architectural flexibility and prevents vendor lock-in, making future technology migrations easier.

**Independent Test**: Can be fully tested by verifying that the core application code only interacts with the abstraction layer and not directly with Kafka clients.

**Acceptance Scenarios**:

1. **Given** task CRUD operations occur, **When** events need to be published, **Then** core code should only call abstraction layer methods, not Kafka client directly
2. **Given** need to switch from Kafka to another pub/sub system, **When** abstraction layer implementation is changed, **Then** core application code should not require modifications

---

### User Story 5 - Maintain Backward Compatibility (Priority: P3)

As a user, I want existing functionality from Phase V Step 1 (recurring tasks, due dates, etc.) to continue working unchanged, so that there are no regressions during the event-driven architecture implementation.

**Why this priority**: Maintaining existing functionality is critical to ensure no disruption to users during the architectural enhancement.

**Independent Test**: Can be fully tested by running all existing functionality tests and verifying they still pass after event-driven architecture implementation.

**Acceptance Scenarios**:

1. **Given** existing users with recurring tasks, due dates, priorities, and tags, **When** new event-driven architecture is deployed, **Then** all existing functionality should continue to work as before

---

### Edge Cases

- What happens when Kafka is temporarily unavailable - should events be queued or dropped?
- How does the system handle malformed events in the queue?
- What if a consumer service fails to process an event - should it be retried or dead-lettered?
- How does the system handle high-volume periods when many events are published simultaneously?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST publish events to Kafka topics when task lifecycle operations occur (create, update, complete, delete)
- **FR-002**: System MUST define and use consistent event schemas with event_type, task_id, user_id, timestamp, and payload fields
- **FR-003**: System MUST create and document three Kafka topics: task-events, reminders, task-updates
- **FR-004**: System MUST implement a Kafka abstraction layer that hides direct Kafka client usage from core application code
- **FR-005**: System MUST implement placeholder consumer services that can process events from Kafka topics
- **FR-006**: System MUST publish reminder events to the reminders topic when tasks have upcoming due dates
- **FR-007**: System MUST log all published and consumed events for traceability
- **FR-008**: System MUST handle Kafka connectivity issues gracefully without disrupting core functionality
- **FR-009**: Consumer services MUST be able to process recurring task completion events and generate next occurrences
- **FR-010**: Consumer services MUST be able to process reminder events with placeholder notification logic
- **FR-011**: System MUST support switching to Dapr Pub/Sub with minimal code changes
- **FR-012**: System MUST maintain backward compatibility with all existing Phase V Step 1 features
- **FR-013**: System MUST include deployment scripts that set up Kafka/Redpanda alongside the application
- **FR-014**: System MUST provide unit tests for event publishing and consumption logic
- **FR-015**: System MUST validate event schemas before publishing to ensure data consistency

### Key Entities *(include if feature involves data)*

- **Event**: Structured message published to Kafka with event_type, task_id, user_id, timestamp, and payload fields
- **Kafka Topic**: Named channel for event distribution (task-events, reminders, task-updates)
- **Producer**: Component responsible for publishing events to Kafka topics
- **Consumer**: Service that subscribes to Kafka topics and processes events
- **Abstraction Layer**: Interface that separates core application logic from specific Kafka implementation
- **Event Schema**: JSON structure defining the format of events published to Kafka

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Events are successfully published to Kafka topics when task CRUD operations occur without disrupting core functionality
- **SC-002**: Three Kafka topics (task-events, reminders, task-updates) are created and documented with clear usage patterns
- **SC-003**: All events follow a consistent JSON schema with required fields (event_type, task_id, user_id, timestamp, payload)
- **SC-004**: Backend publishes events on create/update/complete/delete operations and reminder scheduling
- **SC-005**: Placeholder consumer services exist and can process events from all three Kafka topics
- **SC-006**: No direct Kafka client code exists in core application - all interaction goes through abstraction layer
- **SC-007**: Events are traceable with clear logs showing both publish and consume operations
- **SC-008**: Deployment scripts successfully set up Kafka/Redpanda alongside the application
- **SC-009**: All existing functionality from Phase V Step 1 continues to work without regressions
- **SC-010**: The system is prepared for switching to Dapr Pub/Sub with minimal code changes
- **SC-011**: Unit tests exist and pass for event publishing and consumption logic