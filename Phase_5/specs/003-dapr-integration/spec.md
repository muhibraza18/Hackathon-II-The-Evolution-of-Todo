# Feature Specification: Dapr Integration for Todo AI Chatbot

**Feature Branch**: `003-dapr-integration`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 3: Dapr Integration for Todo AI Chatbot

Target audience: Hackathon judges evaluating portability, microservices best practices, abstraction of infrastructure, and event-driven maturity

Focus:
- Fully integrate Dapr as sidecar for all services (backend, recurring task consumer, notification consumer, etc.)
- Use Dapr building blocks to abstract Kafka Pub/Sub, PostgreSQL state, scheduled jobs (reminders), secrets, and service invocation
- Replace direct Kafka/DB calls from Step 2 with Dapr HTTP/gRPC APIs
- Enable Dapr Jobs API for exact-time reminder triggers (no polling)
- Ensure app code remains clean and vendor-agnostic (swap Kafka → RabbitMQ via YAML only)  Success criteria:
- Dapr sidecars injected into all relevant pods via Helm annotations
- Dapr Pub/Sub component configured for Kafka/Redpanda (kafka-pubsub)
- Publish/subscribe fully working via Dapr API (no kafka-python/aiokafka in code)
- Dapr state store (state.postgresql) used for conversation/task cache
- Dapr Jobs API schedules reminders at exact due time + triggers callback
- Dapr secrets store (kubernetes-secrets) loads API keys/DB creds securely  - Service invocation used for frontend → backend calls (with retries/mTLS)
- No regressions in Step 1 (advanced features) or Step 2 (event publishing/consuming)
- Dapr components deployed via YAML (kubectl apply) or Helm
- Local Minikube verification: dapr init -k + app runs with sidecars
- All changes traceable to this spec (@specs/dapr/dapr-integration.md)  Constraints:
- Use Dapr CLI + Kubernetes mode (dapr init -k)
- Prefer Dapr HTTP API over gRPC for simplicity
- No direct infrastructure libraries in app code (kafka-python, psycopg2, etc.)
- Keep existing Phase V Step 1 & 2 code as base – refactor minimally
- Secrets must use Kubernetes Secret or Dapr secret store – no env vars
- Dapr Jobs API for reminders (not cron bindings)
- Timeline: Complete this sub-phase before moving to local/cloud deployment  Not building:
- Dapr mTLS between services (use if stretch goal)
- Advanced Dapr features (actors, workflows, output bindings)
- Custom Dapr middleware or plugins
- Production-grade observability (tracing/metrics) – defer to later
- Multi-tenancy or RBAC in Dapr
- Swap to non-Kafka Pub/Sub (e.g., Redis, RabbitMQ) – Kafka only for now
- Cloud-specific Dapr config (defer to cloud sub-phase)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dapr Sidecar Integration (Priority: P1)

As a system architect, I want Dapr sidecars to be injected into all relevant pods (backend, recurring task consumer, notification consumer, etc.), so that all services can leverage Dapr's building blocks for infrastructure abstraction.

**Why this priority**: This is the foundational requirement that enables all other Dapr features and provides the infrastructure abstraction layer.

**Independent Test**: Can be fully tested by deploying the application with Dapr sidecars and verifying that Dapr APIs are accessible from within each service.

**Acceptance Scenarios**:

1. **Given** application pods are deployed with Dapr annotations, **When** pods start, **Then** Dapr sidecars should be automatically injected and running alongside the main containers
2. **Given** Dapr sidecar is running, **When** service makes Dapr API calls, **Then** the calls should succeed without direct infrastructure dependencies

---

### User Story 2 - Dapr Pub/Sub Abstraction (Priority: P1)

As a developer, I want to replace direct Kafka/aiokafka calls with Dapr Pub/Sub API calls, so that the application code remains vendor-agnostic and can be swapped to different messaging systems via configuration only.

**Why this priority**: This achieves the key goal of infrastructure abstraction and vendor portability.

**Independent Test**: Can be fully tested by publishing and subscribing to messages using Dapr APIs and verifying that the functionality works without direct Kafka dependencies in the code.

**Acceptance Scenarios**:

1. **Given** application needs to publish events, **When** code calls Dapr Pub/Sub API, **Then** events should be published to Kafka without direct Kafka client code
2. **Given** application needs to subscribe to events, **When** Dapr Pub/Sub API receives messages, **Then** events should be processed without direct Kafka client code
3. **Given** Dapr Pub/Sub configuration, **When** Kafka is swapped with another system, **Then** application code should not require changes

---

### User Story 3 - Dapr State Store Integration (Priority: P2)

As a developer, I want to use Dapr State Store APIs to manage conversation and task cache, so that the application can leverage PostgreSQL state management through Dapr's abstraction layer.

**Why this priority**: This provides state management abstraction and improves scalability by leveraging Dapr's state management capabilities.

**Independent Test**: Can be fully tested by storing and retrieving data through Dapr State APIs and verifying that the data persists in PostgreSQL.

**Acceptance Scenarios**:

1. **Given** application needs to store conversation state, **When** code calls Dapr State API, **Then** data should be stored in PostgreSQL without direct database code
2. **Given** application needs to retrieve conversation state, **When** code calls Dapr State API, **Then** data should be retrieved from PostgreSQL without direct database code

---

### User Story 4 - Dapr Jobs for Reminders (Priority: P2)

As a system architect, I want to use Dapr Jobs API to schedule reminders at exact due times, so that the system can trigger callbacks precisely without polling mechanisms.

**Why this priority**: This provides exact-time scheduling capabilities and eliminates the need for polling-based reminder systems.

**Independent Test**: Can be fully tested by scheduling reminder jobs and verifying that they execute at the exact specified times.

**Acceptance Scenarios**:

1. **Given** a task with a due date, **When** Dapr Jobs API schedules a reminder, **Then** the callback should execute at the exact due time
2. **Given** a scheduled reminder job, **When** due time arrives, **Then** the appropriate callback should be triggered

---

### User Story 5 - Dapr Secrets Management (Priority: P2)

As a security engineer, I want to use Dapr Secrets API to load API keys and database credentials securely, so that sensitive information is managed through Dapr's secure secrets store.

**Why this priority**: This ensures secure management of sensitive information and follows security best practices.

**Independent Test**: Can be fully tested by configuring Dapr to load secrets from Kubernetes secrets and verifying that the application can access them securely.

**Acceptance Scenarios**:

1. **Given** application needs database credentials, **When** code calls Dapr Secrets API, **Then** credentials should be retrieved securely without environment variables
2. **Given** application needs API keys, **When** code calls Dapr Secrets API, **Then** keys should be retrieved securely without environment variables

---

### User Story 6 - Dapr Service Invocation (Priority: P3)

As a developer, I want to use Dapr Service Invocation for frontend-backend communication, so that services can communicate with built-in retries, circuit breakers, and optional mTLS.

**Why this priority**: This provides reliable service-to-service communication with resilience features.

**Independent Test**: Can be fully tested by making service invocations through Dapr and verifying that retries and other resilience features work.

**Acceptance Scenarios**:

1. **Given** frontend needs to call backend service, **When** code uses Dapr Service Invocation, **Then** the call should succeed with built-in resilience features
2. **Given** backend service is temporarily unavailable, **When** Dapr Service Invocation is used, **Then** automatic retries should occur

---

### User Story 7 - Maintain Backward Compatibility (Priority: P3)

As a user, I want existing functionality from Phase V Steps 1 and 2 (advanced features, event publishing/consuming) to continue working unchanged, so that there are no regressions during the Dapr integration.

**Why this priority**: Maintaining existing functionality is critical to ensure no disruption to users during the Dapr migration.

**Independent Test**: Can be fully tested by running all existing functionality tests and verifying they still pass after Dapr integration.

**Acceptance Scenarios**:

1. **Given** existing users with recurring tasks, due dates, priorities, and tags, **When** Dapr integration is deployed, **Then** all existing functionality should continue to work as before
2. **Given** existing event publishing and consuming functionality, **When** Dapr integration is deployed, **Then** events should continue to flow correctly

---

### Edge Cases

- What happens when Dapr sidecar is temporarily unavailable - should the application handle the outage gracefully?
- How does the system handle Dapr API rate limiting or throttling?
- What if a Dapr Job fails to execute - should it be retried or dead-lettered?
- How does the system handle migration of existing data to Dapr state store?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST inject Dapr sidecars into all relevant pods via Helm annotations
- **FR-002**: System MUST use Dapr Pub/Sub API for all publish/subscribe operations instead of direct Kafka clients
- **FR-003**: System MUST use Dapr State Store API for conversation/task caching instead of direct database calls
- **FR-004**: System MUST use Dapr Jobs API to schedule reminders at exact due times
- **FR-005**: System MUST use Dapr Secrets API to load API keys and database credentials securely
- **FR-006**: System MUST use Dapr Service Invocation for frontend-backend communication
- **FR-007**: System MUST maintain all existing functionality from Phase V Steps 1 & 2
- **FR-008**: System MUST allow Kafka replacement with other Pub/Sub systems via configuration only
- **FR-009**: System MUST deploy Dapr components via YAML manifests or Helm charts
- **FR-010**: System MUST support local Minikube verification with dapr init -k
- **FR-011**: System MUST provide resilience features (retries, circuit breakers) through Dapr
- **FR-012**: System MUST secure all sensitive data through Dapr Secrets API
- **FR-013**: System MUST prefer Dapr HTTP API over gRPC for simplicity
- **FR-014**: System MUST remove all direct infrastructure libraries (kafka-python, psycopg2, etc.) from application code
- **FR-015**: System MUST schedule exact-time reminders using Dapr Jobs API without polling

### Key Entities *(include if feature involves data)*

- **Dapr Sidecar**: Lightweight proxy that provides infrastructure services to the application
- **Dapr Pub/Sub Component**: Abstraction layer for messaging systems (configured for Kafka/Redpanda)
- **Dapr State Store**: Abstraction layer for state management (configured for PostgreSQL)
- **Dapr Jobs**: Scheduling component for time-based operations (reminders)
- **Dapr Secrets**: Secure storage and retrieval system for sensitive information
- **Dapr Service Invocation**: Component for service-to-service communication with resilience features

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dapr sidecars successfully injected into all relevant pods with proper Helm annotations
- **SC-002**: All publish/subscribe operations work via Dapr API without direct Kafka client code in application
- **SC-003**: State management operations work via Dapr State API without direct database calls in application
- **SC-004**: Reminder jobs scheduled via Dapr Jobs API execute at exact due times with callback triggers
- **SC-005**: Secrets loaded securely via Dapr Secrets API without environment variables
- **SC-006**: Service invocation works between frontend and backend with Dapr's resilience features
- **SC-007**: No regressions in existing functionality from Phase V Steps 1 & 2
- **SC-008**: Dapr components deployed successfully via YAML manifests or Helm charts
- **SC-009**: Local Minikube verification successful with dapr init -k and app running with sidecars
- **SC-010**: Application code remains vendor-agnostic and Kafka can be swapped via configuration only
- **SC-011**: All infrastructure dependencies abstracted through Dapr building blocks
- **SC-012**: Security requirements met with proper secret management via Dapr