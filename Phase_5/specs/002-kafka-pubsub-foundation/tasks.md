# Implementation Tasks: Event-Driven Foundation (Kafka / PubSub)

**Feature**: Event-Driven Foundation (Kafka / PubSub) for Todo AI Chatbot
**Branch**: 002-kafka-pubsub-foundation
**Created**: 2026-01-28

## Overview

This document outlines the implementation tasks for establishing an event-driven foundation using Kafka/Redpanda for the Todo AI Chatbot. The implementation will create a decoupled architecture where task operations trigger events published to Kafka topics, which are then consumed by separate services for processing. The architecture includes an abstraction layer to facilitate future migration to Dapr Pub/Sub.

## Dependencies

- User Story 1 (Task Event Publishing) must be completed before User Story 2 (Reminder Event Publishing) can be fully tested
- User Story 3 (Event Consumption) can be developed in parallel with User Story 1 and 2
- User Story 4 (Abstraction Layer) should be implemented early as it's required by other stories
- User Story 5 (Backward Compatibility) is validated after all other stories

## Parallel Execution Examples

- **Parallel Tasks**: T005-T010 (Kafka setup) can be developed in parallel with T015-T020 (Event schema design)
- **Story-Level Parallelism**: User Stories 3 and 4 can be developed in parallel after User Story 1 is completed

## Implementation Strategy

1. **MVP Scope**: Focus on User Story 1 (Task Event Publishing) as the minimal viable product
2. **Incremental Delivery**: Each user story should be independently testable and deliverable
3. **Backward Compatibility**: Ensure existing functionality continues to work throughout development

---

## Phase 1: Setup

- [ ] T001 Create branch 002-kafka-pubsub-foundation from main
- [ ] T002 [P] Set up development environment with Kafka/Redpanda dependencies
- [ ] T003 [P] Install Strimzi operator on Minikube cluster
- [ ] T004 [P] Create placeholder files for consumer services if needed

## Phase 2: Foundational Tasks

- [ ] T005 [P] Deploy Kafka cluster on Minikube using Strimzi
- [ ] T006 [P] Create required Kafka topics: task-events, reminders, task-updates
- [X] T007 [P] Define standardized JSON event schemas in backend/schemas/events.py
- [X] T008 [P] Create event validation utilities in backend/utils/event_validator.py
- [X] T009 [P] Set up Kafka connection configuration in backend/config/kafka_config.py
- [X] T010 [P] Create event abstraction layer interface in backend/services/kafka_publisher.py

## Phase 3: User Story 1 - Task Event Publishing (Priority: P1)

**Goal**: Enable the backend to publish events to Kafka topics when task lifecycle operations occur (create, update, complete, delete).

**Independent Test**: Can be fully tested by creating a task, updating it, completing it, and deleting it, then verifying that appropriate events are published to the Kafka topics and can be consumed.

**Tasks**:

- [X] T011 [US1] Implement Kafka producer wrapper in backend/services/kafka_publisher.py
- [X] T012 [US1] Add event publishing to task creation endpoint POST /api/tasks
- [X] T013 [US1] Add event publishing to task update endpoint PUT /api/tasks/{id}
- [X] T014 [US1] [P] Add event publishing to task completion endpoint PATCH /api/tasks/{id}/complete
- [X] T015 [US1] [P] Add event publishing to task deletion endpoint DELETE /api/tasks/{id}
- [ ] T016 [US1] [P] Implement error handling and retry logic for event publishing
- [ ] T017 [US1] [P] Add logging for published events in backend/logs/event_logger.py
- [ ] T018 [US1] [P] Create unit tests for event publishing functionality
- [ ] T019 [US1] [P] Update API documentation for event publishing
- [ ] T020 [US1] [P] Test task event publishing with all CRUD operations

## Phase 4: User Story 2 - Reminder Event Publishing (Priority: P1)

**Goal**: Enable the system to publish reminder events to Kafka when tasks have upcoming due dates.

**Independent Test**: Can be fully tested by creating tasks with future due dates, then verifying that appropriate reminder events are published to the "reminders" topic at the appropriate times.

**Tasks**:

- [X] T021 [US2] Create reminder scheduling service in backend/services/reminder_scheduler.py
- [ ] T022 [US2] Add reminder event publishing to due date creation/update in backend/services/due_date_service.py
- [X] T023 [US2] Implement reminder event payload structure in backend/schemas/reminder_event.py
- [ ] T024 [US2] [P] Add reminder scheduling to task creation with due dates
- [ ] T025 [US2] [P] Add reminder rescheduling to task updates with due dates
- [ ] T026 [US2] [P] Implement reminder cancellation when due dates change/remove
- [ ] T027 [US2] [P] Create unit tests for reminder event publishing
- [ ] T028 [US2] [P] Update event logging for reminder events
- [ ] T029 [US2] [P] Update API documentation for reminder events
- [ ] T030 [US2] [P] Test reminder event publishing with various due date scenarios

## Phase 5: User Story 3 - Event Consumption and Processing (Priority: P2)

**Goal**: Create placeholder consumer services that can process events from Kafka topics.

**Independent Test**: Can be fully tested by publishing events to Kafka and verifying that consumer services process them (even if just logging the events).

**Tasks**:

- [X] T031 [US3] Create recurring task consumer service in consumers/recurring_task_consumer.py
- [X] T032 [US3] Create notification placeholder consumer in consumers/notification_consumer.py
- [X] T033 [US3] Create audit logging consumer in consumers/audit_consumer.py
- [X] T034 [US3] [P] Implement Kafka consumer connection logic in consumers/base_consumer.py
- [X] T035 [US3] [P] Add consumer health checks and monitoring
- [X] T036 [US3] [P] Implement recurring task generation logic in recurring consumer
- [X] T037 [US3] [P] Implement placeholder notification logic in notification consumer
- [X] T038 [US3] [P] Implement audit logging in audit consumer
- [X] T039 [US3] [P] Create consumer configuration and deployment files
- [X] T040 [US3] [P] Test consumer services with sample events

## Phase 6: User Story 4 - Abstraction Layer Implementation (Priority: P2)

**Goal**: Create an abstraction layer that hides the implementation details of Kafka, so that the core application code doesn't depend directly on Kafka and can be switched to Dapr or another pub/sub system later.

**Independent Test**: Can be fully tested by verifying that the core application code only interacts with the abstraction layer and not directly with Kafka clients.

**Tasks**:

- [X] T041 [US4] Refine Kafka abstraction layer interface in backend/services/kafka_publisher.py
- [X] T042 [US4] Implement abstraction layer with configurable backend (Kafka/Dapr)
- [X] T043 [US4] Update all event publishing code to use abstraction layer
- [ ] T044 [US4] [P] Create abstraction layer tests in backend/tests/test_event_abstraction.py
- [ ] T045 [US4] [P] Verify no direct Kafka client usage in core application code
- [ ] T046 [US4] [P] Add configuration options for switching event backends
- [ ] T047 [US4] [P] Create mock implementation for testing purposes
- [ ] T048 [US4] [P] Update documentation for abstraction layer
- [ ] T049 [US4] [P] Test abstraction layer with different backends
- [ ] T050 [US4] [P] Verify abstraction layer supports future Dapr migration

## Phase 7: User Story 5 - Maintain Backward Compatibility (Priority: P3)

**Goal**: Ensure existing functionality from Phase V Step 1 (recurring tasks, due dates, etc.) continues working unchanged.

**Independent Test**: Can be fully tested by running all existing functionality tests and verifying they still pass after event-driven architecture implementation.

**Tasks**:

- [ ] T051 [US5] Run existing task functionality tests with event-driven architecture enabled
- [ ] T052 [US5] Verify recurring task functionality still works with new event system
- [ ] T053 [US5] [P] Run regression tests to ensure existing functionality unaffected
- [ ] T054 [US5] [P] Test due date and priority functionality with new event system
- [ ] T055 [US5] [P] Create migration tests to verify data integrity
- [ ] T056 [US5] [P] Test with existing client applications to ensure compatibility

## Phase 8: Consumer Service Implementation

- [X] T057 [P] Implement recurring task consumer with next occurrence generation logic
- [X] T058 [P] Implement notification consumer with placeholder notification logic
- [X] T059 [P] Implement audit consumer with comprehensive logging
- [X] T060 [P] Add error handling and retry mechanisms to all consumers
- [X] T061 [P] Implement dead letter queue handling for failed events
- [X] T062 [P] Add monitoring and metrics collection to consumers
- [X] T063 [P] Create consumer health check endpoints
- [X] T064 [P] Add consumer configuration for topic partition assignment
- [X] T065 [P] Implement graceful shutdown and restart for consumers
- [X] T066 [P] Create consumer deployment configurations

## Phase 9: Integration & Testing

- [ ] T067 [P] Create integration tests for event publishing and consumption
- [ ] T068 [P] Implement end-to-end tests for complete event flow
- [ ] T069 [P] Test event flow: create task → publish event → consume → log/process
- [ ] T070 [P] Test error scenarios and recovery mechanisms
- [ ] T071 [P] Perform load testing with high event volumes
- [ ] T072 [P] Test Kafka cluster failure and recovery scenarios
- [ ] T073 [P] Verify consumer group rebalancing works correctly
- [ ] T074 [P] Test manual verification scenarios from requirements
- [ ] T075 [P] Create smoke tests for deployment validation

## Phase 10: Polish & Cross-Cutting Concerns

- [ ] T076 [P] Update README.md with event-driven architecture documentation
- [ ] T077 [P] Update deployment scripts with Kafka setup instructions
- [ ] T078 [P] Add performance monitoring for event publishing/consumption
- [ ] T079 [P] Add comprehensive logging for event flow tracing
- [ ] T080 [P] Conduct security review of event payloads and consumer processing
- [ ] T081 [P] Perform integration testing of all new features together
- [ ] T082 [P] Update user guides with event-driven architecture concepts
- [ ] T083 [P] Create troubleshooting guides for event system issues
- [ ] T084 [P] Optimize consumer performance and resource usage
- [ ] T085 [P] Run complete test suite to verify no regressions
- [ ] T086 [P] Update deployment configurations for production readiness
- [ ] T087 [P] Prepare migration guide for existing users
- [ ] T088 [P] Final validation of all acceptance criteria from specification
- [ ] T089 [P] Create monitoring dashboards for event system
- [ ] T090 [P] Document Kafka topic configurations and scaling guidelines