# Implementation Plan: Dapr Integration for Todo AI Chatbot

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

## Technical Context

This plan details the implementation of Dapr integration for the Todo AI Chatbot. The implementation will replace direct infrastructure calls (Kafka, PostgreSQL) with Dapr building blocks, enabling infrastructure abstraction and vendor portability. The approach follows a layered refactoring strategy that maintains existing functionality while introducing Dapr abstractions.

Key decisions to be documented:
- **HTTP vs gRPC for Dapr API calls**: HTTP (simpler) vs gRPC (faster but more complex)
- **Pub/Sub component type**: Kafka (consistent with Step 2) vs Redis (easier local testing)
- **State store choice**: PostgreSQL (persistent) vs Redis (fast cache)
- **Jobs API vs Cron bindings**: Jobs API (exact time) vs Cron bindings (polling)
- **Secret store**: Kubernetes secrets (native) vs Vault (advanced features)
- **Sidecar resource limits**: Balance between stability on Minikube and performance

## Constitution Check

- **Spec-Driven Development**: Following spec → plan → tasks → implement cycle as outlined in constitution
- **AI-Assisted Development**: Using Claude Code for implementation
- **Reproducible Environments**: Maintaining consistency across dev/test/prod with Dapr sidecars
- **Security First**: Ensuring proper secret management through Dapr Secrets API
- **Minimal Viable Changes**: Implementing Dapr integration incrementally
- **Container-First Architecture**: Maintaining existing containerized architecture with Dapr sidecars
- **Immutable Infrastructure**: Following existing deployment patterns with Dapr additions
- **Observability**: Maintaining existing logging/monitoring with Dapr insights
- **Fail-Fast**: Proper error handling for Dapr API calls
- **Environment Parity**: Ensuring Dapr-enabled changes work across all environments
- **Backward Compatibility**: Preserving existing functionality during Dapr migration

## Gates

- [ ] All architectural decisions documented in ADR format
- [ ] Implementation plan reviewed and approved by team
- [ ] All decisions that meet significance criteria have ADRs created
- [ ] Security implications assessed for Dapr configuration
- [ ] Performance impact evaluated for Dapr sidecar overhead
- [ ] Dapr component configuration validated
- [ ] Backward compatibility verified with existing functionality

## Phase 0: Research & Architecture Decisions

### research.md

#### Decision: HTTP vs gRPC for Dapr API Calls
**Rationale**: Using HTTP for Dapr API calls to maintain simplicity and broad compatibility. HTTP is easier to debug and works well with existing Python HTTP libraries like httpx/requests.
**Alternatives considered**:
- HTTP: Simpler, easier to debug, broader compatibility
- gRPC: Higher performance, more complex client setup

#### Decision: Pub/Sub Component Type
**Rationale**: Using Kafka as the Dapr Pub/Sub component to maintain consistency with Phase V Step 2 implementation. This allows for seamless migration without changing the underlying messaging system.
**Alternatives considered**:
- Kafka: Consistent with existing implementation, enterprise-grade
- Redis: Simpler local setup, less robust for production

#### Decision: State Store Choice
**Rationale**: Using PostgreSQL as the Dapr state store to maintain data persistence and consistency with existing database. This provides ACID properties and reliable storage for conversation state.
**Alternatives considered**:
- PostgreSQL: Persistent, consistent, fits existing architecture
- Redis: Faster, in-memory, potential data loss on restart

#### Decision: Jobs API vs Cron Bindings
**Rationale**: Using Dapr Jobs API for reminders to achieve exact-time scheduling without polling. This provides precise timing for due date reminders.
**Alternatives considered**:
- Jobs API: Exact timing, no polling, newer feature
- Cron bindings: Proven approach, polling-based

#### Decision: Secret Store
**Rationale**: Using Kubernetes secrets as the Dapr secret store for native integration with the Kubernetes environment and simplicity.
**Alternatives considered**:
- Kubernetes secrets: Native integration, simple setup
- HashiCorp Vault: Advanced features, more complex setup

#### Decision: Sidecar Resource Limits
**Rationale**: Setting conservative resource limits (CPU/memory) to ensure stable operation on Minikube while maintaining adequate performance.
**Tradeoffs**: Stability vs performance on resource-constrained environments

## Phase 1: Design & Contracts

### data-model.md

#### Dapr-Integrated Task Entity
- **Original fields** (maintained): id, user_id, title, description, completed, created_at, updated_at
- **New Dapr-specific associations**:
  - pubsub_topic: "task-events" for event publishing
  - state_key: "task-{id}" for state operations
  - job_id: "reminder-{task_id}" for reminder scheduling
- **Validation**: Maintains all existing validation rules

#### Dapr Component Entities
- **DaprPubSubComponent**: Configuration for Kafka pubsub (broker, auth, etc.)
- **DaprStateStoreComponent**: Configuration for PostgreSQL state store (connection, etc.)
- **DaprSecretStoreComponent**: Configuration for Kubernetes secrets store
- **DaprJobComponent**: Configuration for reminder scheduling

### contracts/

#### Dapr API Contract: Task Event Publishing
```
POST http://localhost:3500/v1.0/publish/task-events
Content-Type: application/json
{
  "event_type": "task.created",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "datetime",
  "payload": { ... }
}
```

#### Dapr API Contract: State Operations
```
GET http://localhost:3500/v1.0/state/task-state-store/task-{id}
POST http://localhost:3500/v1.0/state/task-state-store
[
  {
    "key": "task-{id}",
    "value": { ... }
  }
]
```

#### Dapr API Contract: Secret Retrieval
```
GET http://localhost:3500/v1.0/secrets/kubernetes-secret-store/{secret-name}
```

#### Dapr API Contract: Service Invocation
```
POST http://localhost:3500/v1.0/invoke/backend/method/api/tasks
Content-Type: application/json
{
  "title": "Task Title",
  ...
}
```

### quickstart.md

#### Quick Start: Dapr Integration Implementation

1. **Install Dapr on Minikube**:
   ```bash
   dapr init -k
   ```

2. **Deploy Dapr Components**:
   ```bash
   kubectl apply -f dapr-components/pubsub/kafka-pubsub.yaml
   kubectl apply -f dapr-components/state/postgresql-statestore.yaml
   kubectl apply -f dapr-components/secrets/kubernetes-secrets.yaml
   ```

3. **Update Application Code**:
   - Replace Kafka producer calls with Dapr publish API
   - Replace Kafka consumer logic with Dapr subscription endpoints
   - Replace database calls with Dapr state API
   - Replace reminder scheduling with Dapr Jobs API
   - Replace secret access with Dapr Secrets API

4. **Update Deployment Manifests**:
   - Add Dapr annotations to pod templates
   - Configure sidecar resource limits
   - Set up service invocation endpoints

5. **Testing & Validation**:
   - Unit tests for Dapr wrapper functions
   - Integration tests for publish/subscribe via Dapr
   - Manual verification of sidecar injection
   - End-to-end validation of all functionality

## Phase 2: Implementation Strategy

### Layer 1: Dapr Infrastructure Setup
1. Install Dapr on Minikube cluster
2. Create Dapr component YAMLs for pubsub, state, secrets
3. Configure Kafka pubsub component with existing Kafka cluster
4. Configure PostgreSQL state store component
5. Configure Kubernetes secrets store component
6. Set up Dapr sidecar injection in deployment manifests

### Layer 2: Dapr API Wrappers
1. Create Dapr HTTP client wrapper in backend/services/dapr_client.py
2. Implement publish_event() function using Dapr pubsub API
3. Implement get_state() and save_state() functions using Dapr state API
4. Implement get_secret() function using Dapr secrets API
5. Implement service_invoke() function using Dapr service invocation API

### Layer 3: Refactor Producers (Backend)
1. Replace aiokafka producer with Dapr publish API calls
2. Update task creation endpoint to use Dapr for event publishing
3. Update task update/completion endpoints to use Dapr for event publishing
4. Add error handling for Dapr API failures with fallback strategies

### Layer 4: Refactor Consumers (Recurring, Notification, Audit)
1. Replace direct Kafka consumers with Dapr subscription endpoints
2. Update recurring task consumer to use Dapr pubsub subscription
3. Update notification consumer to use Dapr pubsub subscription
4. Update audit consumer to use Dapr pubsub subscription

### Layer 5: Dapr Jobs for Reminders
1. Replace existing reminder scheduling with Dapr Jobs API
2. Implement callback endpoints for reminder execution
3. Schedule jobs using Dapr Jobs API for exact-time execution

### Layer 6: Dapr State Store Integration
1. Replace direct database calls with Dapr state store API
2. Update conversation and task caching to use Dapr state store
3. Implement state management functions using Dapr state API

### Layer 7: Dapr Secrets Management
1. Replace environment variable access with Dapr secrets API
2. Update configuration loading to use Dapr for secrets
3. Configure Kubernetes secrets for sensitive data

### Layer 8: Dapr Service Invocation
1. Update frontend-backend communication to use Dapr service invocation
2. Implement resilient service calls with built-in retries/circuit breakers

### Layer 9: Testing & Validation
1. Unit tests for Dapr wrapper functions
2. Integration tests for Dapr-enabled functionality
3. End-to-end tests for complete workflows
4. Regression tests to ensure no functionality lost

### Layer 10: Documentation & Deployment
1. Update README with Dapr setup instructions
2. Document Dapr component configurations
3. Update deployment manifests with Dapr annotations
4. Create troubleshooting guide for Dapr-related issues

## Architecture Decision Records (ADRs)

The following architectural decisions require formal ADR documentation:

1. **ADR-001**: Dapr component configuration approach (pubsub, state, secrets)
2. **ADR-002**: Dapr API integration pattern (wrapper vs direct calls)
3. **ADR-003**: Migration strategy from direct Kafka/DB to Dapr APIs
4. **ADR-004**: Error handling and fallback strategies for Dapr API failures

## Risk Analysis

- **Dapr Dependency Risk**: Application becomes dependent on Dapr infrastructure - implement graceful degradation if Dapr unavailable
- **Performance Risk**: Dapr sidecar overhead might impact performance - monitor and tune resource allocation
- **Complexity Risk**: Adding Dapr increases operational complexity - ensure proper monitoring and documentation
- **Migration Risk**: Refactoring existing code could introduce regressions - maintain thorough testing
- **Compatibility Risk**: Dapr version changes might affect functionality - pin versions in deployment

## Success Metrics

- [ ] Dapr sidecars successfully injected into all relevant pods with proper annotations
- [ ] All publish/subscribe operations work via Dapr API without direct Kafka code
- [ ] State management operations work via Dapr State API without direct DB calls
- [ ] Reminder jobs scheduled via Dapr Jobs API execute at exact due times
- [ ] Secrets loaded securely via Dapr Secrets API without environment variables
- [ ] Service invocation works between services with Dapr resilience features
- [ ] No regressions in existing Phase V Step 1 & 2 functionality
- [ ] Dapr components deployed successfully via YAML manifests
- [ ] Local Minikube verification successful with app running with sidecars
- [ ] Application code remains vendor-agnostic (Kafka swappable via config)
- [ ] All infrastructure dependencies abstracted through Dapr building blocks
- [ ] Security requirements met with proper secret management via Dapr