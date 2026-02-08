# Feature Specification: Local Minikube + Dapr Deployment for Todo AI Chatbot

**Feature Branch**: `004-minikube-dapr-deployment`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 4: Local Minikube + Dapr Deployment for Todo AI Chatbot

Target audience: Hackathon judges evaluating local-first validation, Kubernetes + Dapr orchestration maturity, and reproducible local setup

Focus:
- Deploy the full application stack (frontend, backend, recurring task service, notification service) to Minikube
- Inject Dapr sidecars into all pods via Helm chart annotations
- Deploy all Dapr components (pubsub-kafka, state-postgresql, jobs, secrets) to Minikube
- Deploy local Kafka/Redpanda (Strimzi operator or Redpanda Docker) and connect via Dapr Pub/Sub
- Ensure end-to-end local functionality: advanced features + event-driven flow + Dapr abstractions
- Validate everything works without cloud dependencies Success criteria:
- Minikube cluster starts successfully (docker driver, sufficient resources)
- Dapr initialized on Minikube (dapr init -k) with sidecars running in all pods
- All Dapr components applied (kubectl apply -f dapr-components/) and healthy
- Kafka/Redpanda running in cluster + connected via Dapr pubsub-kafka component
- Helm upgrade/install succeeds for updated charts (with Dapr sidecar annotations)
- All pods Running 1/1 (including sidecars)
- End-to-end test passes locally:  - Create recurring task with due date → reminder job scheduled → callback fires → notification event published
  - Task CRUD → task-events published → recurring/audit consumers process
  - Frontend accessible via minikube service --url
  - No regressions from previous sub-phases (advanced features, event publishing)
- Secrets loaded securely (Dapr secret store or Kubernetes Secret)
- All deployment steps scripted/documented in README (minikube start → dapr init → helm upgrade → verification)
- All changes traceable to this spec (@specs/deployment/minikube-dapr-deployment.md)  Constraints:
- Use existing Phase V Step 1–3 code/charts as base
- Minikube only (docker driver, memory ≤3072MiB, no external cloud services)
- No cloud-specific config (AKS/GKE/OKE) yet – defer to Step 5
- Dapr must be fully initialized before app deployment
- Kafka/Redpanda must be local (Strimzi preferred for K8s-native)
- Helm charts must include readiness/liveness probes + Dapr annotations
- No persistent volumes for Kafka/state (ephemeral OK for local testing)
- Timeline: Complete this sub-phase before moving to cloud deployment  Not building:
- Production-grade ingress/TLS (use minikube service or port-forward)
- Horizontal scaling / HPA
- Full observability stack (Prometheus/Grafana) – defer to stretch goal
- Multi-node Minikube cluster
- Cloud-managed Kafka (Redpanda Cloud / Confluent) – local only
- Advanced Dapr security (mTLS, RBAC) – basic sidecar injection only
- Automated testing pipeline – manual verification sufficient"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Local Deployment Setup (Priority: P1)

As a developer, I want to deploy the full Todo AI Chatbot stack to a local Minikube cluster with Dapr sidecars, so that I can validate the event-driven architecture works in a Kubernetes environment before moving to cloud deployment.

**Why this priority**: This is the foundational requirement that enables local validation of the Dapr integration and validates the complete system works in the target Kubernetes environment.

**Independent Test**: Can be fully tested by starting Minikube, initializing Dapr, deploying the application, and verifying that all services are running with Dapr sidecars.

**Acceptance Scenarios**:

1. **Given** Minikube is installed locally, **When** I run the deployment commands, **Then** a local cluster should start with sufficient resources (≤3072MiB) and all services should be accessible
2. **Given** Dapr CLI is available, **When** I initialize Dapr on Minikube, **Then** Dapr should be running with proper sidecar injection enabled
3. **Given** deployment scripts are executed, **When** Helm charts are installed/upgraded, **Then** all pods should be running with Dapr sidecars attached (1/1 Ready)

---

### User Story 2 - Dapr Component Integration (Priority: P1)

As a system architect, I want all Dapr components (pubsub-kafka, state-postgresql, jobs, secrets) to be deployed and functioning in the Minikube cluster, so that the application can leverage Dapr's infrastructure abstractions without direct dependencies.

**Why this priority**: This ensures that the Dapr integration from previous phases works properly in the Kubernetes environment with actual Dapr components.

**Independent Test**: Can be fully tested by applying Dapr component configurations and verifying they are healthy and functional.

**Acceptance Scenarios**:

1. **Given** Dapr components are defined in YAML files, **When** I apply them to Minikube, **Then** all components should be in healthy status
2. **Given** Kafka/Redpanda is running in cluster, **When** Dapr pubsub-kafka component is configured, **Then** the component should connect successfully and be ready for event publishing/subscribing
3. **Given** PostgreSQL is available, **When** Dapr state-postgresql component is configured, **Then** the component should connect and be ready for state operations

---

### User Story 3 - End-to-End Functionality Validation (Priority: P2)

As a user, I want the complete Todo AI Chatbot functionality to work in the local Minikube environment, so that I can verify the advanced features, event-driven flow, and Dapr abstractions all work together properly.

**Why this priority**: This validates that the integration of all previous phases works correctly in the target environment with no regressions.

**Independent Test**: Can be fully tested by creating recurring tasks with due dates and verifying the complete event-driven flow works end-to-end.

**Acceptance Scenarios**:

1. **Given** I create a recurring task with a due date, **When** the due date arrives, **Then** a reminder job should execute, trigger a callback, and publish a notification event via Dapr
2. **Given** I perform task CRUD operations, **When** events are published via Dapr pub/sub, **Then** recurring and audit consumers should process the events correctly
3. **Given** the system is running in Minikube, **When** I access the frontend, **Then** it should be accessible via minikube service URL and all features should work without cloud dependencies

---

### User Story 4 - Secure Configuration Management (Priority: P2)

As a security engineer, I want secrets to be loaded securely via Dapr secret store or Kubernetes secrets, so that sensitive configuration is not exposed in environment variables or source code.

**Why this priority**: This ensures proper security practices are followed in the deployment environment.

**Independent Test**: Can be fully tested by configuring the application to load secrets via Dapr APIs and verifying they are accessible to the application.

**Acceptance Scenarios**:

1. **Given** sensitive data is stored in Kubernetes secrets, **When** Dapr secret store component is configured, **Then** applications should be able to retrieve secrets via Dapr APIs
2. **Given** application needs database credentials, **When** it accesses secrets via Dapr, **Then** credentials should be retrieved securely without environment variables

---

### User Story 5 - Deployment Documentation & Reproducibility (Priority: P3)

As a DevOps engineer, I want all deployment steps to be scripted and documented in the README, so that anyone can reproduce the local Minikube + Dapr setup following a clear sequence of commands.

**Why this priority**: This ensures the deployment process is repeatable and accessible to other team members.

**Independent Test**: Can be fully tested by following the documented steps from a clean environment and successfully deploying the complete system.

**Acceptance Scenarios**:

1. **Given** clean local environment, **When** I follow the documented deployment steps, **Then** the complete system should be deployed successfully
2. **Given** deployment documentation exists, **When** I run the verification commands, **Then** all services should be confirmed as running and accessible

---

### Edge Cases

- What happens when Minikube doesn't have sufficient resources to run all services with Dapr sidecars?
- How does the system handle Dapr component initialization failures during deployment?
- What if Kafka/Redpanda fails to start properly in the Minikube environment?
- How does the system behave when network connectivity is limited during the deployment process?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST deploy all application services (frontend, backend, recurring task consumer, notification consumer) to Minikube
- **FR-002**: System MUST inject Dapr sidecars into all application pods via Helm chart annotations
- **FR-003**: System MUST deploy and configure all Dapr components (pubsub-kafka, state-postgresql, jobs, secrets) to Minikube
- **FR-004**: System MUST deploy local Kafka/Redpanda (preferably via Strimzi operator) in the cluster
- **FR-005**: System MUST connect Dapr pubsub-kafka component to the local Kafka/Redpanda instance
- **FR-006**: System MUST ensure all pods run with 1/1 readiness (including Dapr sidecars)
- **FR-007**: System MUST execute end-to-end tests to validate complete event-driven functionality locally
- **FR-008**: System MUST load secrets securely via Dapr secret APIs or Kubernetes secrets (no environment variables)
- **FR-009**: System MUST provide frontend accessibility via minikube service URL
- **FR-010**: System MUST maintain all functionality from previous sub-phases without regressions
- **FR-011**: System MUST document all deployment steps in README with clear command sequences
- **FR-012**: System MUST provide verification commands to confirm successful deployment
- **FR-013**: System MUST use Helm charts with readiness/liveness probes and Dapr annotations
- **FR-014**: System MUST initialize Dapr completely before deploying application services
- **FR-015**: System MUST use ephemeral storage for Kafka/state during local testing (no persistent volumes required)

### Key Entities *(include if feature involves data)*

- **Minikube Cluster**: Local Kubernetes environment with docker driver and resource constraints (≤3072MiB)
- **Dapr Sidecar**: Lightweight proxy injected into application pods to provide infrastructure services
- **Dapr Components**: Configuration resources for pubsub, state, jobs, and secrets building blocks
- **Application Services**: Frontend, backend, recurring task consumer, and notification consumer services
- **Local Kafka/Redpanda**: In-cluster messaging system for event streaming
- **Deployment Scripts**: Helm charts and kubectl commands for reproducible deployment
- **Verification Commands**: Test procedures to confirm successful deployment and functionality

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Minikube cluster starts successfully with docker driver and ≤3072MiB memory allocation
- **SC-002**: Dapr is initialized on Minikube (dapr init -k) with sidecars running in all application pods
- **SC-003**: All Dapr components (pubsub-kafka, state-postgresql, jobs, secrets) are applied and healthy
- **SC-004**: Kafka/Redpanda runs in cluster and connects successfully via Dapr pubsub-kafka component
- **SC-005**: Helm upgrade/install succeeds for updated charts with Dapr sidecar annotations
- **SC-006**: All pods show Running 1/1 status (including Dapr sidecars)
- **SC-007**: End-to-end test passes: create recurring task → reminder job scheduled → callback fires → notification event published
- **SC-008**: Task CRUD operations trigger event publishing → Dapr pub/sub → consumers process events correctly
- **SC-009**: Frontend is accessible via minikube service URL without cloud dependencies
- **SC-010**: No regressions in functionality from previous sub-phases (advanced features, event publishing)
- **SC-011**: Secrets are loaded securely via Dapr secret store or Kubernetes Secret (no environment variables)
- **SC-012**: Complete deployment steps are scripted and documented in README with verification procedures
- **SC-013**: All changes are traceable to this specification document
- **SC-014**: System operates entirely without external cloud services during local validation
- **SC-015**: Deployment process can be reproduced from clean environment following documented steps