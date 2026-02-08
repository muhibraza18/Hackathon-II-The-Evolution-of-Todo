# Implementation Plan: Event-Driven Foundation (Kafka / PubSub)

**Feature Branch**: `002-kafka-pubsub-foundation`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 2: Event-Driven Foundation (Kafka / PubSub) for Todo AI Chatbot

Create:
- High-level event-driven architecture sketch (text or mermaid diagram)
- Kafka/Redpanda topic structure and event schema definitions (JSON examples)
- Producer wrapper architecture (abstraction layer for future Dapr swap)
- Consumer service skeleton structure (recurring, notification, audit)
- Deployment & bootstrap strategy for local Kafka (Strimzi or Redpanda Docker)
- Quality validation checklist (publish/consume tests, log verification)  Decisions needing documentation:
- Kafka implementation choice (Strimzi operator vs Redpanda Docker vs Redpanda Cloud)
  - Options: Strimzi (K8s-native), Redpanda Docker (single binary), Redpanda Cloud (managed)
  - Tradeoffs: learning value vs setup speed vs future cloud migration
- Event schema format (plain JSON vs Avro with schema registry)
  - Tradeoffs: simplicity vs type safety & evolution
- Producer library (aiokafka direct vs Dapr-ready HTTP wrapper) - Tradeoffs: performance vs portability to Dapr in next sub-phase
- Consumer deployment model (separate Deployment per consumer vs single multi-consumer pod)
  - Tradeoffs: isolation vs resource efficiency
- Topic partitioning & replication (single partition vs multiple)
  - Tradeoffs: scalability vs simplicity in local Minikube
- Error handling & retry policy (dead-letter queue vs simple retry)
  - Tradeoffs: reliability vs complexity  Testing strategy:
- Unit tests for producer wrapper (mock publish success/failure)
- Integration tests for consumer logic (mock consume → assert next task created)
- Manual verification:
  - Create task → see task-created event in logs
  - Complete recurring task → see next instance created by consumer
  - Set due date → see reminder event published
  - Check Kafka consumer group status (offset committed)
- Acceptance criteria from spec fully validated (topics exist, events published/consumed, no direct Kafka in app code)
- Smoke test: restart Kafka pod → consumers reconnect & resume  Technical details:
- Use existing Phase V Step 1 backend as base
- Prefer Strimzi operator for Kafka on Minikube (kubectl apply install)
- Topics: task-events (CRUD), reminders (due date triggers), task-updates (optional real-time)
- Event schema: JSON with event_type, task_id, user_id, timestamp, payload object
- Producer: async wrapper function publish_event(topic, payload)
- Consumers: separate FastAPI services (or background tasks) consuming via aiokafka
- Organize implementation by layers:
  1. Kafka/Redpanda deployment & topic creation
  2. Event schema design & documentation
  3. Producer wrapper in backend
  4. Consumer services (recurring, notification, audit)
  5. Integration & testing
  6. Documentation & README updates"

## Technical Context

This plan details the implementation of an event-driven foundation using Kafka/Redpanda for the Todo AI Chatbot. The implementation will establish a decoupled architecture where task operations trigger events published to Kafka topics, which are then consumed by separate services for processing. The architecture will include an abstraction layer to facilitate future migration to Dapr Pub/Sub.

Key decisions to be documented:
- **Kafka implementation choice**: Strimzi operator vs Redpanda Docker vs Redpanda Cloud
- **Event schema format**: Plain JSON vs Avro with schema registry
- **Producer library**: aiokafka direct vs Dapr-ready HTTP wrapper
- **Consumer deployment model**: Separate deployments vs single multi-consumer pod
- **Topic partitioning**: Single partition vs multiple partitions
- **Error handling**: Dead-letter queue vs simple retry mechanism

## Constitution Check

- **Spec-Driven Development**: Following spec → plan → tasks → implement cycle as outlined in constitution
- **AI-Assisted Development**: Using Claude Code for implementation
- **Reproducible Environments**: Maintaining consistency across dev/test/prod
- **Security First**: Ensuring proper validation and sanitization of event payloads
- **Minimal Viable Changes**: Implementing features incrementally
- **Container-First Architecture**: Maintaining existing containerized architecture
- **Immutable Infrastructure**: Following existing deployment patterns
- **Observability**: Maintaining existing logging/monitoring with enhanced event tracing
- **Fail-Fast**: Proper error handling for event publishing and consumption
- **Environment Parity**: Ensuring changes work across all environments
- **Backward Compatibility**: Preserving existing functionality

## Gates

- [ ] All architectural decisions documented in ADR format
- [ ] Implementation plan reviewed and approved by team
- [ ] All decisions that meet significance criteria have ADRs created
- [ ] Security implications assessed for event payloads
- [ ] Performance impact evaluated for event-driven operations
- [ ] Database migration strategy validated
- [ ] Backward compatibility verified with existing clients

## Phase 0: Research & Architecture Decisions

### research.md

#### Decision: Kafka Implementation Choice
**Rationale**: Using Strimzi operator for local Kafka setup on Minikube to provide the most educational value and production-like setup for Kubernetes environment. This approach provides learning opportunities for Kafka administration while maintaining compatibility with cloud deployments.
**Alternatives considered**:
- Strimzi operator: Kubernetes-native, educational value, complex setup
- Redpanda Docker: Simple setup, single binary, less learning value
- Redpanda Cloud: Managed service, no local learning, defers to later phase

#### Decision: Event Schema Format
**Rationale**: Using plain JSON format for event schemas to maintain simplicity and compatibility with both Kafka and future Dapr Pub/Sub implementations. This reduces complexity while maintaining flexibility.
**Alternatives considered**:
- Plain JSON: Simple, flexible, less type safety
- Avro with schema registry: Strong typing, schema evolution, increased complexity

#### Decision: Producer Library
**Rationale**: Using aiokafka directly for the producer wrapper to maintain performance while creating an abstraction layer that can be swapped for Dapr in the future. This provides the right balance of performance and portability.
**Alternatives considered**:
- aiokafka direct: High performance, direct Kafka dependency
- Dapr-ready HTTP wrapper: Portable, lower performance initially

#### Decision: Consumer Deployment Model
**Rationale**: Using separate deployments per consumer service to provide better isolation, independent scaling, and fault tolerance. Each consumer can be scaled independently based on load.
**Alternatives considered**:
- Separate deployments: Better isolation, more resources
- Single multi-consumer pod: Resource efficient, less isolation

#### Decision: Topic Partitioning
**Rationale**: Using single partition for local Minikube setup to maintain simplicity while planning for multiple partitions in production environments.
**Alternatives considered**:
- Single partition: Simple, limited scalability
- Multiple partitions: Scalable, more complex

#### Decision: Error Handling
**Rationale**: Implementing simple retry mechanism with configurable attempts for local development, with plans to enhance with dead-letter queues in production.
**Alternatives considered**:
- Simple retry: Simple, basic reliability
- Dead-letter queue: Advanced, higher reliability, more complexity

## Phase 1: Design & Contracts

### data-model.md

#### Event Schema Definitions
- **Base Event Structure**:
  - event_type (str): Type of event (task.created, task.updated, etc.)
  - task_id (str): Unique identifier for the task
  - user_id (str): Identifier for the user who triggered the event
  - timestamp (datetime): When the event was created
  - payload (dict): Additional data specific to the event type

- **Task Created Event**:
  - event_type: "task.created"
  - task_id: Unique task identifier
  - user_id: Creator's user ID
  - timestamp: Creation time
  - payload: { title, description, due_date, priority, tags, recurring_config, status }

- **Task Updated Event**:
  - event_type: "task.updated"
  - task_id: Updated task identifier
  - user_id: Updater's user ID
  - timestamp: Update time
  - payload: { title, description, due_date, priority, tags, recurring_config, status }

- **Task Completed Event**:
  - event_type: "task.completed"
  - task_id: Completed task identifier
  - user_id: Completer's user ID
  - timestamp: Completion time
  - payload: { title, due_date, priority, tags, next_occurrence_id }

- **Reminder Event**:
  - event_type: "task.reminder"
  - task_id: Task identifier for reminder
  - user_id: Associated user ID
  - timestamp: Reminder trigger time
  - payload: { title, due_date, priority, notification_method }

#### Kafka Topics Structure
- **task-events**: Contains all task lifecycle events (created, updated, completed, deleted)
- **reminders**: Contains reminder events for upcoming due dates
- **task-updates**: Contains real-time task updates (optional, for future use)

### Architecture Diagram

```
┌─────────────────┐    Publish Events    ┌──────────────────┐
│   Todo Backend  │ ────────────────────▶│   Kafka/Redpanda │
│                 │                      │                  │
│ • Task CRUD     │                      │ • task-events    │
│ • Event Producer│                      │ • reminders      │
│ • Event Wrapper │                      │ • task-updates   │
└─────────────────┘                      └──────────────────┘
                                                    │
                                                    ▼ Subscribe Events
┌─────────────────┐    Process Events     ┌──────────────────┐
│ Recurring Task  │◀──────────────────────┤   Event Consumers│
│ Consumer        │                       │                  │
│                 │                       ├──────────────────┤
│ • Generate next │                       │ • Recurring Task │
│   occurrence    │                       │ • Notifications  │
│ • Update DB     │                       │ • Audit Logging  │
└─────────────────┘                       └──────────────────┘
```

### quickstart.md

#### Quick Start: Event-Driven Foundation Implementation

1. **Deploy Kafka/Redpanda**:
   - Install Strimzi operator on Minikube
   - Create Kafka cluster and topics (task-events, reminders, task-updates)

2. **Define Event Schemas**:
   - Create standardized JSON schemas for all event types
   - Document event payload structures

3. **Implement Producer Wrapper**:
   - Create abstraction layer for Kafka publishing
   - Implement publish_event(topic, payload) function
   - Add error handling and retry logic

4. **Develop Consumer Services**:
   - Create recurring task consumer service
   - Create notification placeholder consumer
   - Create audit logging consumer

5. **Integrate with Existing Backend**:
   - Add event publishing to task CRUD operations
   - Connect reminder events to due date logic
   - Verify no direct Kafka dependencies in core code

6. **Testing & Validation**:
   - Unit tests for producer wrapper
   - Integration tests for consumer logic
   - Manual verification of event flow

## Phase 2: Implementation Strategy

### Layer 1: Kafka/Redpanda Deployment & Topic Creation
1. Install Strimzi operator on Minikube cluster
2. Deploy Kafka cluster configuration
3. Create required topics: task-events, reminders, task-updates
4. Configure topic settings (partitions, replication)

### Layer 2: Event Schema Design & Documentation
1. Define standardized JSON event schemas
2. Create documentation for each event type
3. Implement schema validation utilities

### Layer 3: Producer Wrapper in Backend
1. Create Kafka abstraction layer
2. Implement async publish_event function
3. Add error handling and retry mechanisms
4. Integrate with existing task operations

### Layer 4: Consumer Services (recurring, notification, audit)
1. Develop recurring task consumer service
2. Create notification placeholder consumer
3. Implement audit logging consumer
4. Add health checks and monitoring

### Layer 5: Integration & Testing
1. Connect producers and consumers
2. Run integration tests
3. Perform manual verification
4. Test failure scenarios and recovery

### Layer 6: Documentation & README Updates
1. Update README with event-driven architecture
2. Document deployment procedures
3. Add troubleshooting guides
4. Update API documentation

## Architecture Decision Records (ADRs)

The following architectural decisions require formal ADR documentation:

1. **ADR-001**: Kafka implementation choice (Strimzi vs Redpanda)
2. **ADR-002**: Event schema format and validation approach
3. **ADR-003**: Producer abstraction layer design
4. **ADR-004**: Consumer service deployment architecture

## Risk Analysis

- **Kafka Availability Risk**: System must handle Kafka downtime gracefully - implement local queuing or circuit breaker patterns
- **Performance Risk**: Event publishing shouldn't block main operations - use async publishing with buffering
- **Complexity Risk**: Event-driven architecture adds operational complexity - ensure proper monitoring and logging
- **Migration Risk**: Future Dapr migration requires careful abstraction design - validate interface compatibility early

## Success Metrics

- [ ] Kafka/Redpanda cluster successfully deployed on Minikube
- [ ] Three required topics created and accessible (task-events, reminders, task-updates)
- [ ] Event schemas defined and documented with examples
- [ ] Producer wrapper implements abstraction layer without direct Kafka dependencies in core app
- [ ] Consumer services successfully process events from all topics
- [ ] Events are published on all required task operations (create, update, complete, delete)
- [ ] Reminder events are published for upcoming due dates
- [ ] No regressions in existing Phase V Step 1 functionality
- [ ] All events are traceable with clear publish/consume logs
- [ ] Unit and integration tests pass for event-driven components