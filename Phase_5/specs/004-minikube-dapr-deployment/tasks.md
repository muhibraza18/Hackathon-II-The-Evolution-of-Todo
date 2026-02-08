# Implementation Tasks: Local Minikube + Dapr Deployment for Todo AI Chatbot

**Feature**: Local Minikube + Dapr Deployment for Todo AI Chatbot
**Branch**: 004-minikube-dapr-deployment
**Created**: 2026-01-28

## Overview

This document outlines the implementation tasks for deploying the Todo AI Chatbot with Dapr integration to a local Minikube cluster. The implementation will replace direct infrastructure calls with Dapr building blocks, enabling infrastructure abstraction and vendor portability. The approach follows a phased deployment strategy that starts with cluster setup and proceeds through Dapr integration.

## Dependencies

- User Story 1 (Local Deployment Setup) must be completed before User Stories 2-5 can be fully tested
- User Story 2 (Dapr Component Integration) must be working before User Story 3 (End-to-End Validation) can be fully validated
- User Story 4 (Secure Configuration) can be developed in parallel with User Story 2 and 3
- User Story 5 (Deployment Documentation) is validated after all other stories are completed

## Parallel Execution Examples

- **Parallel Tasks**: T005-T010 (Minikube setup) can run in parallel with T015-T020 (Dapr setup)
- **Story-Level Parallelism**: User Stories 4 and 5 can be developed in parallel after User Story 1-3 are completed

## Implementation Strategy

1. **MVP Scope**: Focus on User Story 1 (Local Deployment Setup) + User Story 2 (Dapr Component Integration) as the minimal viable product
2. **Incremental Delivery**: Each user story should be independently testable and deliverable
3. **Backward Compatibility**: Ensure existing functionality continues to work throughout deployment

---

## Phase 1: Setup

- [ ] T001 Create branch 004-minikube-dapr-deployment from main
- [ ] T002 [P] Install Minikube, kubectl, helm, and dapr CLI tools
- [ ] T003 [P] Verify system requirements (Docker running, sufficient RAM for Minikube)
- [X] T004 [P] Create deployment directory structure (k8s/, charts/, dapr-components/)

## Phase 2: Foundational Tasks

- [X] T005 [P] Create Minikube start script with proper resource allocation (docker driver, 3072MiB, 4 CPUs)
- [X] T006 [P] Create Dapr initialization script for Kubernetes mode (dapr init -k)
- [X] T007 [P] Set up Kubernetes namespaces (kafka, dapr, default) for component organization
- [X] T008 [P] Create resource validation tools to verify system capacity
- [X] T009 [P] Prepare Kafka deployment files (Strimzi operator installation)
- [X] T010 [P] Prepare Dapr component configuration files (pubsub, state, secrets, jobs)
- [ ] T011 [P] Update existing Helm charts with Dapr annotation templates
- [ ] T012 [P] Create verification and smoke test scripts
- [ ] T013 [P] Prepare troubleshooting guide outline with common failure scenarios
- [ ] T014 [P] Set up deployment configuration values for Minikube environment

## Phase 3: User Story 1 - Local Deployment Setup (Priority: P1)

**Goal**: Deploy the full application stack (frontend, backend, recurring task service, notification service) to Minikube with Dapr sidecars injected into all pods via Helm chart annotations.

**Independent Test**: Can be fully tested by starting Minikube, initializing Dapr, deploying the application, and verifying that all services are running with Dapr sidecars.

**Acceptance Scenarios**:
1. **Given** Minikube is installed locally, **When** I run the deployment commands, **Then** a local cluster should start with sufficient resources (≤3072MiB) and all services should be accessible
2. **Given** Dapr CLI is available, **When** I initialize Dapr on Minikube, **Then** Dapr should be running with proper sidecar injection enabled
3. **Given** deployment scripts are executed, **When** Helm charts are installed/upgraded, **Then** all pods should be running with Dapr sidecars attached (1/1 Ready)

**Tasks**:

- [X] T015 [US1] Implement Minikube cluster start with Docker driver and resource allocation (3072MiB, 4 CPUs)
- [X] T016 [US1] Verify Minikube cluster status and node availability
- [X] T017 [US1] [P] Configure Minikube with Docker driver and appropriate resource limits
- [X] T018 [US1] [P] Test Minikube resource allocation (memory, CPU, disk space)
- [X] T019 [US1] [P] Create Minikube cluster verification script
- [X] T020 [US1] [P] Document Minikube setup requirements and troubleshooting

## Phase 4: User Story 2 - Dapr Component Integration (Priority: P1)

**Goal**: Deploy all Dapr components (pubsub-kafka, state-postgresql, jobs, secrets) to Minikube and connect to local Kafka/Redpanda.

**Independent Test**: Can be fully tested by applying Dapr component configurations and verifying they are healthy and functional.

**Acceptance Scenarios**:
1. **Given** Dapr components are defined in YAML files, **When** I apply them to Minikube, **Then** all components should be in healthy status
2. **Given** Kafka/Redpanda is running in cluster, **When** Dapr pubsub-kafka component is configured, **Then** the component should connect successfully and be ready for event publishing/subscribing
3. **Given** PostgreSQL is available, **When** Dapr state-postgresql component is configured, **Then** the component should connect and be ready for state operations

**Tasks**:

- [X] T021 [US2] Initialize Dapr on Minikube using CLI (dapr init -k --enable-ha=false)
- [X] T022 [US2] Verify Dapr control plane services are running (sidecar-injector, operator, placement)
- [X] T023 [US2] [P] Create Dapr pubsub component configuration for Kafka integration
- [X] T024 [US2] [P] Create Dapr state store component configuration for PostgreSQL
- [X] T025 [US2] [P] Create Dapr secrets store component configuration for Kubernetes secrets
- [X] T026 [US2] [P] Create Dapr jobs component configuration for reminder scheduling
- [X] T027 [US2] [P] Apply Dapr component configurations to Minikube cluster
- [X] T028 [US2] [P] Verify all Dapr components are healthy and ready
- [X] T029 [US2] [P] Test Dapr component connectivity (pubsub, state, secrets)
- [X] T030 [US2] [P] Create Dapr component health check scripts

## Phase 5: User Story 3 - Kafka Deployment and Integration (Priority: P2)

**Goal**: Deploy local Kafka/Redpanda (Strimzi operator) in the cluster and connect via Dapr Pub/Sub component.

**Independent Test**: Can be fully tested by deploying Kafka, configuring the Dapr pubsub component, and verifying event publishing/subscribing works.

**Acceptance Scenarios**:
1. **Given** Strimzi operator is installed, **When** Kafka cluster CRD is applied, **Then** Kafka should start successfully with ephemeral storage
2. **Given** Kafka is running in cluster, **When** Dapr pubsub component connects to it, **Then** event publishing and subscribing should work correctly
3. **Given** Kafka cluster is deployed, **When** I test connectivity from application pods, **Then** they should be able to reach Kafka brokers

**Tasks**:

- [X] T031 [US3] Install Strimzi operator in Kafka namespace on Minikube
- [X] T032 [US3] Deploy Kafka cluster with ephemeral storage using Strimzi CRDs
- [X] T033 [US3] [P] Verify Kafka cluster is running and healthy (brokers, zookeeper)
- [X] T034 [US3] [P] Create Kafka topics for task events, reminders, and updates
- [X] T035 [US3] [P] Test Kafka connectivity from within Minikube cluster
- [X] T036 [US3] [P] Configure Dapr pubsub component to connect to Kafka cluster
- [X] T037 [US3] [P] Verify Dapr pubsub component can publish and subscribe to Kafka topics
- [X] T038 [US3] [P] Test event publishing and consuming via Dapr pubsub
- [X] T039 [US3] [P] Create Kafka connectivity verification scripts
- [X] T040 [US3] [P] Document Kafka troubleshooting for common connection issues

## Phase 6: User Story 4 - End-to-End Functionality Validation (Priority: P2)

**Goal**: Ensure complete event-driven functionality works in the local Minikube environment with advanced features, event-driven flow, and Dapr abstractions.

**Independent Test**: Can be fully tested by creating recurring tasks with due dates and verifying the complete event-driven flow works end-to-end.

**Acceptance Scenarios**:
1. **Given** I create a recurring task with a due date, **When** the due date arrives, **Then** a reminder job should execute, trigger a callback, and publish a notification event via Dapr
2. **Given** I perform task CRUD operations, **When** events are published via Dapr pub/sub, **Then** recurring and audit consumers should process the events correctly
3. **Given** the system is running in Minikube, **When** I access the frontend, **Then** it should be accessible via minikube service URL and all features should work without cloud dependencies

**Tasks**:

- [X] T041 [US4] Update Helm charts with Dapr sidecar annotations for all services
- [X] T042 [US4] Deploy full application stack (backend, frontend, consumers) to Minikube
- [X] T043 [US4] [P] Verify all pods are running with Dapr sidecars (2/2 containers ready)
- [X] T044 [US4] [P] Test recurring task creation and next occurrence generation via Dapr pubsub
- [X] T045 [US4] [P] Test due date reminder scheduling and callback execution via Dapr jobs
- [X] T046 [US4] [P] Test task CRUD operations with event publishing via Dapr pubsub
- [X] T047 [US4] [P] Verify frontend accessibility via minikube service URL
- [X] T048 [US4] [P] Test complete event-driven flow: create → publish → consume → process
- [X] T049 [US4] [P] Run regression tests to ensure no functionality regressions
- [X] T050 [US4] [P] Create end-to-end smoke test automation

## Phase 7: User Story 5 - Secure Configuration Management (Priority: P2)

**Goal**: Load secrets securely via Dapr secret store or Kubernetes secrets without using environment variables.

**Independent Test**: Can be fully tested by configuring the application to load secrets via Dapr APIs and verifying they are accessible to the application.

**Acceptance Scenarios**:
1. **Given** sensitive data is stored in Kubernetes secrets, **When** Dapr secret store component is configured, **Then** applications should be able to retrieve secrets via Dapr APIs
2. **Given** application needs database credentials, **When** it accesses secrets via Dapr, **Then** credentials should be retrieved securely without environment variables

**Tasks**:

- [X] T051 [US5] Create Kubernetes secrets for database connection strings and API keys
- [X] T052 [US5] Update application configuration to use Dapr secrets API instead of environment variables
- [X] T053 [US5] [P] Implement secret retrieval functions using Dapr secrets API
- [X] T054 [US5] [P] Test secret retrieval from application pods via Dapr
- [X] T055 [US5] [P] Verify no sensitive data is stored in environment variables
- [X] T056 [US5] [P] Create secret rotation and management procedures
- [X] T057 [US5] [P] Test secret access security and authorization
- [X] T058 [US5] [P] Document secure secret management with Dapr

## Phase 8: User Story 6 - Deployment Documentation and Reproducibility (Priority: P3)

**Goal**: Document all deployment steps in README with clear command sequences so anyone can reproduce the local Minikube + Dapr setup.

**Independent Test**: Can be fully tested by following the documented steps from a clean environment and successfully deploying the complete system.

**Acceptance Scenarios**:
1. **Given** clean local environment, **When** I follow the documented deployment steps, **Then** the complete system should be deployed successfully
2. **Given** deployment documentation exists, **When** I run the verification commands, **Then** all services should be confirmed as running and accessible

**Tasks**:

- [X] T059 [US6] Update README.md with Minikube + Dapr deployment instructions
- [X] T060 [US6] Create deployment scripts for automated setup (start-minikube.sh, deploy-all.sh)
- [X] T061 [US6] [P] Document troubleshooting procedures for common deployment issues
- [X] T062 [US6] [P] Create verification checklist for deployment validation
- [X] T063 [US6] [P] Document service access URLs and port mappings
- [X] T064 [US6] [P] Create cleanup and reset procedures for development
- [X] T065 [US6] [P] Add monitoring and health check commands to documentation
- [X] T066 [US6] [P] Document resource requirements and system prerequisites
- [X] T067 [US6] [P] Create rollback and recovery procedures

## Phase 9: Service Invocation and Advanced Features

- [X] T068 [P] Update service-to-service communication to use Dapr service invocation
- [X] T069 [P] Implement retry policies and circuit breakers via Dapr configuration
- [X] T070 [P] Test service invocation between frontend and backend via Dapr
- [X] T071 [P] Add mTLS configuration for secure service communication (if stretch goal)
- [X] T072 [P] Implement health checks for service invocation endpoints
- [X] T073 [P] Test service invocation resilience features (retries, timeouts)

## Phase 10: Testing & Validation

- [X] T074 [P] Create automated tests for Minikube deployment process
- [X] T075 [P] Implement Dapr component health checks
- [X] T076 [P] Create Kafka connectivity tests
- [X] T077 [P] Implement end-to-end integration tests for event flow
- [X] T078 [P] Test application recovery after Minikube restart
- [X] T079 [P] Performance benchmarking with Dapr sidecars
- [X] T080 [P] Security validation of Dapr configuration
- [X] T081 [P] Chaos testing: Dapr sidecar unavailability scenarios
- [X] T082 [P] Manual verification of all functionality with Dapr integration
- [X] T083 [P] Load testing with Dapr-enabled services
- [X] T084 [P] Final validation of all acceptance criteria from specification

## Phase 11: Polish & Cross-Cutting Concerns

- [X] T085 [P] Update API documentation for Dapr-enabled endpoints
- [X] T086 [P] Add monitoring and logging for Dapr components
- [X] T087 [P] Create deployment metrics and observability setup
- [X] T088 [P] Add performance monitoring for Dapr sidecar overhead
- [X] T089 [P] Conduct security review of Dapr configurations
- [X] T090 [P] Perform integration testing of all new features together
- [X] T091 [P] Update user guides with Dapr architecture concepts
- [X] T092 [P] Create troubleshooting guides for Dapr-related issues
- [X] T093 [P] Optimize resource usage for Dapr-enabled services
- [X] T094 [P] Run complete test suite to verify no regressions
- [X] T095 [P] Update deployment configurations for production readiness
- [X] T096 [P] Prepare migration guide from direct infrastructure to Dapr
- [X] T097 [P] Final validation of all acceptance criteria from specification
- [X] T098 [P] Create monitoring dashboards for Dapr components
- [X] T099 [P] Document Dapr component configurations and scaling guidelines
- [X] T100 [P] Complete final deployment and verification in Minikube environment