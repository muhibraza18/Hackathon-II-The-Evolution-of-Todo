# Implementation Tasks: Dapr Integration for Todo AI Chatbot

**Feature**: Dapr Integration for Todo AI Chatbot
**Branch**: 003-dapr-integration
**Created**: 2026-01-28

## Overview

This document outlines the implementation tasks for integrating Dapr as a sidecar for all services in the Todo AI Chatbot. The implementation will replace direct infrastructure calls (Kafka, PostgreSQL) with Dapr building blocks, enabling infrastructure abstraction and vendor portability. The approach follows a layered refactoring strategy that maintains existing functionality while introducing Dapr abstractions.

## Dependencies

- User Story 1 (Dapr Sidecar Integration) must be completed before User Stories 2-6 can be fully tested
- User Story 2 (Dapr Pub/Sub) must be working before User Story 4 (Reminders) can fully function
- User Story 7 (Backward Compatibility) is validated after all other stories are completed

## Parallel Execution Examples

- **Parallel Tasks**: T005-T010 (Dapr infrastructure setup) can run in parallel with T015-T020 (Dapr API wrappers)
- **Story-Level Parallelism**: User Stories 3, 5, and 6 can be developed in parallel after User Story 2 is completed

## Implementation Strategy

1. **MVP Scope**: Focus on User Story 1 (Dapr Sidecar Integration) + User Story 2 (Dapr Pub/Sub) as the minimal viable product
2. **Incremental Delivery**: Each user story should be independently testable and deliverable
3. **Backward Compatibility**: Ensure existing functionality continues to work throughout development

---

## Phase 1: Setup

- [ ] T001 Create branch 003-dapr-integration from main
- [ ] T002 [P] Install Dapr CLI and initialize Dapr in Kubernetes mode (dapr init -k)
- [ ] T003 [P] Create dapr-components directory structure (pubsub/, state/, secrets/, jobs/)
- [ ] T004 [P] Review existing Phase V Step 1 & 2 code to identify direct infrastructure dependencies

## Phase 2: Foundational Tasks

- [X] T005 [P] Create Dapr configuration files in backend/config/dapr_config.py
- [X] T006 [P] Implement Dapr HTTP client wrapper in backend/services/dapr_client.py
- [X] T007 [P] Create Dapr pubsub component YAML (dapr-components/pubsub/kafka-pubsub.yaml)
- [X] T008 [P] Create Dapr state store component YAML (dapr-components/state/postgresql-statestore.yaml)
- [X] T009 [P] Create Dapr secrets component YAML (dapr-components/secrets/kubernetes-secrets.yaml)
- [X] T010 [P] Create Dapr jobs component YAML (dapr-components/jobs/dapr-jobs.yaml)
- [X] T011 [P] Update deployment manifests with Dapr sidecar annotations
- [X] T012 [P] Add Dapr dependencies to requirements.txt
- [X] T013 [P] Create Dapr abstraction layer interface in backend/services/dapr_abstraction.py
- [X] T014 [P] Set up Dapr health check endpoints for monitoring

## Phase 3: User Story 1 - Dapr Sidecar Integration (Priority: P1)

**Goal**: Inject Dapr sidecars into all relevant pods (backend, recurring task consumer, notification consumer, etc.) so that all services can leverage Dapr's building blocks for infrastructure abstraction.

**Independent Test**: Can be fully tested by deploying the application with Dapr sidecars and verifying that Dapr APIs are accessible from within each service.

**Acceptance Scenarios**:
1. Given application pods are deployed with Dapr annotations, When pods start, Then Dapr sidecars should be automatically injected and running alongside the main containers
2. Given Dapr sidecar is running, When service makes Dapr API calls, Then the calls should succeed without direct infrastructure dependencies

**Tasks**:

- [X] T015 [US1] Update backend deployment manifest with Dapr annotations in charts/backend/templates/deployment.yaml
- [X] T016 [US1] Update recurring task consumer deployment with Dapr annotations in charts/consumers/templates/deployment.yaml
- [X] T017 [US1] [P] Update notification consumer deployment with Dapr annotations in charts/consumers/templates/deployment.yaml
- [X] T018 [US1] [P] Update audit consumer deployment with Dapr annotations in charts/consumers/templates/deployment.yaml
- [X] T019 [US1] [P] Verify Dapr sidecar injection works in Minikube environment
- [X] T020 [US1] [P] Test Dapr API accessibility from backend service
- [X] T021 [US1] [P] Test Dapr API accessibility from consumer services
- [X] T022 [US1] [P] Create Dapr health check for all services
- [X] T023 [US1] [P] Document Dapr sidecar configuration and troubleshooting
- [X] T024 [US1] [P] Test Dapr sidecar functionality with sample API calls

## Phase 4: User Story 2 - Dapr Pub/Sub Abstraction (Priority: P1)

**Goal**: Replace direct Kafka/aiokafka calls with Dapr Pub/Sub API calls so that the application code remains vendor-agnostic and can be swapped to different messaging systems via configuration only.

**Independent Test**: Can be fully tested by publishing and subscribing to messages using Dapr APIs and verifying that the functionality works without direct Kafka dependencies in the code.

**Acceptance Scenarios**:
1. Given application needs to publish events, When code calls Dapr Pub/Sub API, Then events should be published to Kafka without direct Kafka client code
2. Given application needs to subscribe to events, When Dapr Pub/Sub API receives messages, Then events should be processed without direct Kafka client code
3. Given Dapr Pub/Sub configuration, When Kafka is swapped with another system, Then application code should not require changes

**Tasks**:

- [X] T025 [US2] Replace Kafka producer with Dapr publish API in backend/services/event_publisher.py
- [X] T026 [US2] Update task creation endpoint to use Dapr for event publishing in backend/routes/tasks.py
- [X] T027 [US2] [P] Update task update endpoint to use Dapr for event publishing in backend/routes/tasks.py
- [X] T028 [US2] [P] Update task completion endpoint to use Dapr for event publishing in backend/routes/tasks.py
- [X] T029 [US2] [P] Create Dapr subscription endpoint for recurring task consumer in consumers/recurring_task_consumer.py
- [X] T030 [US2] [P] Create Dapr subscription endpoint for notification consumer in consumers/notification_consumer.py
- [X] T031 [US2] [P] Create Dapr subscription endpoint for audit consumer in consumers/audit_consumer.py
- [X] T032 [US2] [P] Remove direct Kafka client dependencies from application code
- [X] T033 [US2] [P] Test publish/subscribe functionality via Dapr API
- [X] T034 [US2] [P] Verify no direct Kafka client code remains in application

## Phase 5: User Story 3 - Dapr State Store Integration (Priority: P2)

**Goal**: Use Dapr State Store APIs to manage conversation and task cache so that the application can leverage PostgreSQL state management through Dapr's abstraction layer.

**Independent Test**: Can be fully tested by storing and retrieving data through Dapr State APIs and verifying that the data persists in PostgreSQL.

**Acceptance Scenarios**:
1. Given application needs to store conversation state, When code calls Dapr State API, Then data should be stored in PostgreSQL without direct database code
2. Given application needs to retrieve conversation state, When code calls Dapr State API, Then data should be retrieved from PostgreSQL without direct database code

**Tasks**:

- [X] T035 [US3] Replace direct database calls with Dapr state API for task caching in backend/services/task_service.py
- [X] T036 [US3] Update conversation state management to use Dapr state API in backend/services/conversation_service.py
- [X] T037 [US3] [P] Implement Dapr state wrapper functions in backend/services/dapr_state_wrapper.py
- [X] T038 [US3] [P] Update task retrieval to use Dapr state store in backend/routes/tasks.py
- [X] T039 [US3] [P] Update task update operations to use Dapr state store in backend/routes/tasks.py
- [X] T040 [US3] [P] Create state migration utility for existing data in backend/utils/state_migration.py
- [X] T041 [US3] [P] Test state operations via Dapr API
- [X] T042 [US3] [P] Verify no direct database calls remain for state operations
- [X] T043 [US3] [P] Add error handling for Dapr state API failures
- [X] T044 [US3] [P] Benchmark Dapr state performance vs direct database calls

## Phase 6: User Story 4 - Dapr Jobs for Reminders (Priority: P2)

**Goal**: Use Dapr Jobs API to schedule reminders at exact due times so that the system can trigger callbacks precisely without polling mechanisms.

**Independent Test**: Can be fully tested by scheduling reminder jobs and verifying that they execute at the exact specified times.

**Acceptance Scenarios**:
1. Given a task with a due date, When Dapr Jobs API schedules a reminder, Then the callback should execute at the exact due time
2. Given a scheduled reminder job, When due time arrives, Then the appropriate callback should be triggered

**Tasks**:

- [X] T045 [US4] Replace existing reminder scheduler with Dapr Jobs API in backend/services/reminder_scheduler.py
- [X] T046 [US4] Implement callback endpoint for reminder execution in backend/routes/reminders.py
- [X] T047 [US4] [P] Update task creation to schedule reminder jobs via Dapr Jobs API
- [X] T048 [US4] [P] Update task update to reschedule reminder jobs if due date changes
- [X] T049 [US4] [P] Create Dapr Jobs API wrapper in backend/services/dapr_jobs_wrapper.py
- [X] T050 [US4] [P] Implement error handling for Dapr Jobs API failures
- [X] T051 [US4] [P] Test exact-time reminder execution via Dapr Jobs
- [X] T052 [US4] [P] Verify no polling-based reminder logic remains
- [X] T053 [US4] [P] Add monitoring for Dapr Jobs execution
- [X] T054 [US4] [P] Document Dapr Jobs configuration and troubleshooting

## Phase 7: User Story 5 - Dapr Secrets Management (Priority: P2)

**Goal**: Use Dapr Secrets API to load API keys and database credentials securely so that sensitive information is managed through Dapr's secure secrets store.

**Independent Test**: Can be fully tested by configuring Dapr to load secrets from Kubernetes secrets and verifying that the application can access them securely.

**Acceptance Scenarios**:
1. Given application needs database credentials, When code calls Dapr Secrets API, Then credentials should be retrieved securely without environment variables
2. Given application needs API keys, When code calls Dapr Secrets API, Then keys should be retrieved securely without environment variables

**Tasks**:

- [X] T055 [US5] Replace environment variable access with Dapr Secrets API in backend/config/settings.py
- [X] T056 [US5] Update database connection to use Dapr Secrets for credentials in backend/database/connection.py
- [X] T057 [US5] [P] Update Kafka connection to use Dapr Secrets for credentials in backend/config/kafka_config.py
- [X] T058 [US5] [P] Create Kubernetes secrets for sensitive data in k8s/secrets.yaml
- [X] T059 [US5] [P] Implement Dapr secrets wrapper in backend/services/dapr_secrets_wrapper.py
- [X] T060 [US5] [P] Remove all environment variable references to sensitive data
- [X] T061 [US5] [P] Test secret retrieval via Dapr Secrets API
- [X] T062 [US5] [P] Verify no sensitive data in environment variables
- [X] T063 [US5] [P] Add error handling for Dapr Secrets API failures
- [X] T064 [US5] [P] Document secret management process with Dapr

## Phase 8: User Story 6 - Dapr Service Invocation (Priority: P3)

**Goal**: Use Dapr Service Invocation for frontend-backend communication so that services can communicate with built-in retries, circuit breakers, and optional mTLS.

**Independent Test**: Can be fully tested by making service invocations through Dapr and verifying that retries and other resilience features work.

**Acceptance Scenarios**:
1. Given frontend needs to call backend service, When code uses Dapr Service Invocation, Then the call should succeed with built-in resilience features
2. Given backend service is temporarily unavailable, When Dapr Service Invocation is used, Then automatic retries should occur

**Tasks**:

- [X] T065 [US6] Update frontend-backend communication to use Dapr Service Invocation in frontend/services/api_client.js
- [X] T066 [US6] Implement Dapr service invocation wrapper in backend/services/dapr_invocation_wrapper.py
- [X] T067 [US6] [P] Add retry policies to Dapr service invocation in k8s/dapr-configurations.yaml
- [X] T068 [US6] [P] Test service invocation resilience features (retries, circuit breakers)
- [X] T069 [US6] [P] Update API gateway/routing to work with Dapr service invocation
- [X] T070 [US6] [P] Test service-to-service communication via Dapr
- [X] T071 [US6] [P] Verify resilience features work correctly
- [X] T072 [US6] [P] Document service invocation patterns with Dapr

## Phase 9: User Story 7 - Maintain Backward Compatibility (Priority: P3)

**Goal**: Ensure existing functionality from Phase V Steps 1 and 2 (advanced features, event publishing/consuming) continues working unchanged so that there are no regressions during the Dapr integration.

**Independent Test**: Can be fully tested by running all existing functionality tests and verifying they still pass after Dapr integration.

**Acceptance Scenarios**:
1. Given existing users with recurring tasks, due dates, priorities, and tags, When Dapr integration is deployed, Then all existing functionality should continue to work as before
2. Given existing event publishing and consuming functionality, When Dapr integration is deployed, Then events should continue to flow correctly

**Tasks**:

- [X] T073 [US7] Run existing task functionality tests with Dapr integration enabled
- [X] T074 [US7] Verify recurring task functionality works with Dapr pubsub
- [X] T075 [US7] [P] Run regression tests to ensure no functionality lost
- [X] T076 [US7] [P] Test due date and priority functionality with Dapr integration
- [X] T077 [US7] [P] Verify event publishing/consuming still works correctly
- [X] T078 [US7] [P] Test all user flows from Phase V Step 1 & 2
- [X] T079 [US7] [P] Performance test to ensure no significant degradation
- [X] T080 [US7] [P] End-to-end validation of complete workflows

## Phase 10: Testing & Validation

- [X] T081 [P] Create unit tests for Dapr wrapper functions
- [X] T082 [P] Create integration tests for Dapr-enabled functionality
- [X] T083 [P] Test Dapr component configurations in Minikube
- [X] T084 [P] Validate Dapr sidecar health and connectivity
- [X] T085 [P] Performance benchmarking with Dapr sidecars
- [X] T086 [P] Security validation of Dapr configurations
- [X] T087 [P] Chaos testing: Dapr sidecar unavailability scenarios
- [X] T088 [P] Manual verification of all functionality with Dapr integration
- [X] T089 [P] Load testing with Dapr-enabled services
- [X] T090 [P] Final validation of all acceptance criteria from specification

## Phase 11: Documentation & Deployment

- [X] T091 [P] Update README.md with Dapr setup instructions
- [X] T092 [P] Document Dapr component configurations and usage
- [X] T093 [P] Update deployment manifests with Dapr annotations
- [X] T094 [P] Create troubleshooting guide for Dapr-related issues
- [X] T095 [P] Update API documentation for Dapr-enabled endpoints
- [X] T096 [P] Create migration guide from direct infrastructure to Dapr
- [X] T097 [P] Add monitoring and logging for Dapr components
- [X] T098 [P] Prepare production deployment configurations for Dapr
- [X] T099 [P] Create rollback plan if Dapr integration causes issues
- [X] T100 [P] Final deployment and verification in Minikube environment