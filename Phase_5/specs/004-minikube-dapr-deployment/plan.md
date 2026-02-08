# Implementation Plan: Local Minikube + Dapr Deployment for Todo AI Chatbot

**Feature Branch**: `004-minikube-dapr-deployment`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 4: Local Minikube + Dapr Deployment for Todo AI Chatbot

Create:
- Minikube cluster setup & resource allocation strategy
- Dapr initialization & sidecar injection architecture (Helm annotations)
- Full deployment flow diagram (Minikube → Dapr → Kafka → App pods)
- Updated Helm chart structure (Dapr sidecars, components mounting)
- Verification & smoke test checklist
- Troubleshooting guide outline (common failures: sidecar crash, component not found)  Decisions needing documentation:
- Minikube driver & resource config (docker vs hyperv, memory 2048–3072MiB, CPUs)
  - Options: docker (default), hyperv (Windows native), virtualbox
  - Tradeoffs: compatibility vs performance in WSL/Windows
- Dapr installation method (dapr init -k vs Helm chart)
  - Options: CLI init (simpler), Helm (more customizable)
  - Tradeoffs: speed vs control over namespace/components
- Kafka deployment choice (Strimzi operator vs Redpanda Docker container)
  - Options: Strimzi (K8s-native), Redpanda Docker (single pod)  - Tradeoffs: Kubernetes integration vs setup simplicity
- Helm chart updates (single chart vs separate for frontend/backend/consumers)
  - Tradeoffs: maintainability vs deployment simplicity
- Service exposure strategy (NodePort vs LoadBalancer vs port-forward)
  - Tradeoffs: ease of access vs realism
- Ephemeral vs persistent storage for Kafka/state (local only)
  - Tradeoffs: simplicity vs data loss on restart  Testing strategy:
- Cluster health checks (minikube status, kubectl get nodes)
- Dapr readiness (dapr status -k, sidecar logs)
- Component validation (kubectl get components.dapr.io, dapr components)
- End-to-end smoke tests:
  - Create task → event published → consumer logs event
  - Schedule reminder → job fires → callback logs
  - Frontend accessible (minikube service --url) → login + CRUD works
  - Restart Minikube → app recovers (state in Neon DB)
- Manual verification commands (kubectl logs, curl health endpoints)
- Acceptance criteria from spec fully validated (pods/sidecars running, events flow, no cloud deps) Technical details:
- Use existing Phase V Step 1–3 code/charts as base
- Minikube start: --driver=docker --memory=3072 --cpus=4 (adjust if low RAM)
- Dapr init: dapr init -k --enable-ha=false (single node)
- Kafka: Strimzi operator install + Kafka CRD (ephemeral storage)
- Helm annotations for sidecars: dapr.io/enabled: "true", dapr.io/app-id, dapr.io/app-port
- Components: mount via ConfigMap or direct YAML apply
- Organize implementation by phases:
  1. Minikube cluster preparation & start
  2. Dapr installation & verification
  3. Kafka/Redpanda deployment & connection test
  4. Dapr components apply & health check
  5. Helm chart updates (sidecars, env vars, probes)
  6. Deploy full app stack (helm upgrade)
  7. End-to-end testing & validation
  8. Documentation & README updates"

## Technical Context

This plan details the implementation of deploying the Todo AI Chatbot with full Dapr integration to a local Minikube cluster. The implementation will replace direct infrastructure calls (Kafka, PostgreSQL, etc.) with Dapr building blocks, enabling infrastructure abstraction and vendor portability. The approach follows a phased deployment strategy that starts with cluster setup and proceeds through Dapr integration.

Key decisions to be documented:
- **Minikube driver & resource config**: Docker (default) vs Hyper-V vs VirtualBox with 2048-3072MiB memory and CPU allocation
- **Dapr installation method**: CLI init (`dapr init -k`) vs Helm chart for customization
- **Kafka deployment choice**: Strimzi operator (K8s-native) vs Redpanda Docker (single pod)
- **Helm chart organization**: Single chart vs separate charts for different services
- **Service exposure strategy**: NodePort vs LoadBalancer vs port-forward approach
- **Storage approach**: Ephemeral vs persistent storage for local development

## Constitution Check

- **Spec-Driven Development**: Following spec → plan → tasks → implement cycle as outlined in constitution
- **AI-Assisted Development**: Using Claude Code for implementation
- **Reproducible Environments**: Maintaining consistency across dev/test environments with Minikube
- **Security First**: Ensuring proper secret management through Dapr Secrets API
- **Minimal Viable Changes**: Implementing Dapr integration incrementally
- **Container-First Architecture**: Maintaining existing containerized architecture with Dapr sidecars
- **Immutable Infrastructure**: Following existing deployment patterns with Dapr additions
- **Observability**: Maintaining existing logging/monitoring with Dapr insights
- **Fail-Fast**: Proper error handling for Dapr API calls and service communications
- **Environment Parity**: Ensuring Dapr-enabled changes work in local Minikube environment
- **Backward Compatibility**: Preserving existing functionality during Dapr migration

## Gates

- [ ] All architectural decisions documented in ADR format
- [ ] Implementation plan reviewed and approved by team
- [ ] All decisions that meet significance criteria have ADRs created
- [ ] Security implications assessed for Dapr configuration
- [ ] Resource allocation validated for Minikube environment
- [ ] Dapr component configurations validated
- [ ] Backward compatibility verified with existing functionality

## Phase 0: Research & Architecture Decisions

### research.md

#### Decision: Minikube Driver & Resource Configuration
**Rationale**: Using Docker driver with 3072MiB memory and 4 CPUs to provide sufficient resources for the application stack plus Dapr sidecars and Kafka. Docker driver offers the best compatibility across platforms.
**Alternatives considered**:
- Docker: Best cross-platform compatibility, sufficient performance
- Hyper-V: Windows native, better performance on Windows but requires Windows Pro/Enterprise
- VirtualBox: Legacy option, less reliable than Docker

#### Decision: Dapr Installation Method
**Rationale**: Using `dapr init -k` CLI command for simplicity and quick setup. This provides a standard Dapr installation suitable for local development.
**Alternatives considered**:
- CLI init: Simpler, faster setup
- Helm chart: More customizable, greater control over components

#### Decision: Kafka Deployment Choice
**Rationale**: Using Strimzi operator for Kubernetes-native Kafka deployment that integrates well with Dapr pubsub component. This provides the best learning value and production-like setup.
**Alternatives considered**:
- Strimzi operator: Kubernetes-native, educational value, more complex setup
- Redpanda Docker: Simpler single pod deployment, less learning value

#### Decision: Helm Chart Organization
**Rationale**: Using a single chart with multiple deployments for simplicity and maintainability. This allows for coordinated deployments while keeping services logically separated.
**Alternatives considered**:
- Single chart: Simpler management, coordinated deployments
- Separate charts: More modular, independent deployments

#### Decision: Service Exposure Strategy
**Rationale**: Using LoadBalancer service type for easy access via `minikube service --url`. This provides the most straightforward access pattern for local development.
**Alternatives considered**:
- LoadBalancer: Easy access with minikube service command
- NodePort: Requires manual port management
- Port-forward: Requires separate terminal/command for each service

#### Decision: Storage Approach
**Rationale**: Using ephemeral storage for local development to maintain simplicity and avoid complex PV/PVC configurations. Data loss on restart is acceptable for local development.
**Alternatives considered**:
- Ephemeral: Simple, no persistent volume management
- Persistent: Preserves data across restarts, more complex setup

## Phase 1: Design & Contracts

### data-model.md

#### Kubernetes Resources
- **MinikubeCluster**: Local Kubernetes cluster with Docker driver, 3072MiB memory, 4 CPUs
- **DaprSystem**: Dapr control plane with sidecar injector, operator, placement service
- **KafkaCluster**: Strimzi-managed Kafka cluster with ephemeral storage
- **DaprComponents**: Configuration resources for pubsub, state, secrets, jobs
- **AppDeployments**: Backend, Frontend, Consumer services with Dapr sidecar annotations
- **Services**: LoadBalancer services for external access to frontend and backend

#### Dapr Component Entities
- **DaprPubSubComponent**: Kafka-based pubsub component (kafka-pubsub)
- **DaprStateStoreComponent**: PostgreSQL-based state store (state-postgresql)
- **DaprSecretStoreComponent**: Kubernetes secrets-based secret store
- **DaprJobComponent**: Jobs API configuration for reminder scheduling

### Architecture Diagram

```
┌─────────────────┐    Minikube Cluster     ┌──────────────────┐
│   Local Host    │ ──────────────────────▶ │  Minikube Node   │
│                 │                         │                  │
│ • dapr CLI      │                         │ • App Pod        │
│ • kubectl       │                         │   ┌─────────────┐│
│ • helm          │                         │   │ Backend     ││
│ • minikube      │                         │   │ w/ Dapr     ││
│                 │                         │   │ Sidecar     ││
└─────────────────┘                         │   └─────────────┘│
                                            │                  │
                                            │ • App Pod        │
                                            │   ┌─────────────┐│
                                            │   │ Consumer    ││
                                            │   │ w/ Dapr     ││
                                            │   │ Sidecar     ││
                                            │   └─────────────┘│
                                            │                  │
                                            │ • Dapr System    │
                                            │   ┌─────────────┐│
                                            │   │ sidecar-inj ││
                                            │   │ operator    ││
                                            │   │ placement   ││
                                            │   └─────────────┘│
                                            │                  │
                                            │ • Kafka Cluster  │
                                            │   ┌─────────────┐│
                                            │   │ zookeeper   ││
                                            │   │ kafka       ││
                                            │   └─────────────┘│
                                            └──────────────────┘
```

### Deployment Flow
1. Start Minikube with Docker driver and resource allocation
2. Initialize Dapr in Kubernetes mode
3. Deploy Strimzi operator and Kafka cluster
4. Apply Dapr component configurations
5. Update Helm charts with Dapr annotations
6. Deploy application stack with sidecars
7. Verify end-to-end functionality

### quickstart.md

#### Quick Start: Local Minikube + Dapr Deployment

1. **Prerequisites**:
   - Install minikube, kubectl, helm, dapr CLI
   - Ensure Docker is running
   - Verify sufficient system resources (≥4GB RAM recommended)

2. **Start Minikube**:
   ```bash
   minikube start --driver=docker --memory=3072 --cpus=4
   ```

3. **Initialize Dapr**:
   ```bash
   dapr init -k --enable-ha=false
   ```

4. **Verify Dapr Installation**:
   ```bash
   dapr status -k
   ```

5. **Deploy Kafka via Strimzi**:
   ```bash
   kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka'
   kubectl create namespace kafka
   kubectl apply -f 'https://strimzi.io/examples/latest/kafka/kafka-persistent-single.yaml' -n kafka
   ```

6. **Apply Dapr Components**:
   ```bash
   kubectl apply -f dapr-components/pubsub/kafka-pubsub.yaml
   kubectl apply -f dapr-components/state/postgresql-statestore.yaml
   kubectl apply -f dapr-components/secrets/kubernetes-secrets.yaml
   ```

7. **Update Helm Charts with Dapr Annotations**:
   - Add dapr.io annotations to deployment templates
   - Ensure proper app-id and app-port settings

8. **Deploy Application Stack**:
   ```bash
   helm upgrade --install todo-app charts/todo-app/ --set dapr.enabled=true
   ```

9. **Verify Deployment**:
   ```bash
   kubectl get pods  # Should show app pods with Dapr sidecars (1/1 Ready)
   kubectl get services  # Should show LoadBalancer services
   minikube service todo-frontend --url  # Get frontend URL
   ```

10. **End-to-End Testing**:
    - Create a task and verify event publishing/consuming
    - Check Dapr sidecar logs for activity
    - Verify all advanced features work as expected

## Phase 2: Implementation Strategy

### Layer 1: Minikube & Dapr Infrastructure Setup
1. Create Minikube start script with appropriate resource allocation
2. Document Dapr initialization process and verification steps
3. Set up Kubernetes namespaces for different components (kafka, dapr, app)
4. Create resource allocation validation tools

### Layer 2: Kafka/Redpanda Deployment
1. Install Strimzi operator on Minikube
2. Deploy Kafka cluster with ephemeral storage
3. Configure Kafka topics for task events and reminders
4. Test Kafka connectivity from within cluster

### Layer 3: Dapr Components Configuration
1. Create Dapr pubsub component for Kafka integration
2. Configure Dapr state store component for PostgreSQL
3. Set up Dapr secrets store component for Kubernetes secrets
4. Apply components to Minikube cluster and verify health

### Layer 4: Helm Chart Updates
1. Update existing Helm charts with Dapr sidecar annotations
2. Modify service configurations for proper exposure in Minikube
3. Add health checks and probes compatible with Dapr sidecars
4. Create values files for Minikube-specific configurations

### Layer 5: Application Deployment & Integration
1. Deploy application stack with updated Helm charts
2. Verify Dapr sidecars are injected and running
3. Test event publishing/subscribing through Dapr
4. Validate all existing functionality works with Dapr integration

### Layer 6: Testing & Validation
1. Create automated tests for Minikube deployment
2. Implement end-to-end functionality tests
3. Verify no regressions in existing features
4. Test service-to-service communication via Dapr

### Layer 7: Documentation & Verification
1. Update README with Minikube + Dapr deployment instructions
2. Create troubleshooting guide for common issues
3. Document verification and testing procedures
4. Prepare smoke test checklist

## Architecture Decision Records (ADRs)

The following architectural decisions require formal ADR documentation:

1. **ADR-001**: Minikube resource allocation and driver choice
2. **ADR-002**: Dapr installation and configuration approach
3. **ADR-003**: Kafka deployment strategy (Strimzi vs alternatives)
4. **ADR-004**: Service exposure and networking approach in Minikube

## Risk Analysis

- **Resource Exhaustion Risk**: Minikube with Dapr sidecars and Kafka may exceed system resources - monitor and adjust allocations as needed
- **Network Connectivity Risk**: Dapr sidecars need proper network access - ensure firewall/VPN doesn't block communication
- **Component Compatibility Risk**: Dapr components must be compatible with each other - validate configurations before deployment
- **Rollback Risk**: Changes to Helm charts could impact deployment - maintain backup configurations
- **Performance Risk**: Dapr sidecars may impact application performance - benchmark and optimize as needed

## Success Metrics

- [ ] Minikube cluster starts successfully with specified resources (docker driver, 3072MiB, 4 CPUs)
- [ ] Dapr initialized on Minikube with all control plane services running
- [ ] Kafka/Redpanda cluster deployed and accessible via Dapr pubsub component
- [ ] All Dapr components (pubsub, state, secrets) applied and healthy
- [ ] Helm charts updated with Dapr annotations and deployed successfully
- [ ] All application pods running with Dapr sidecars (1/1 Ready status)
- [ ] End-to-end event flow works: task creation → event publishing → consumer processing
- [ ] No regressions in existing functionality from previous phases
- [ ] Frontend accessible via minikube service URL
- [ ] Service-to-service communication working via Dapr invocation
- [ ] Secrets loaded securely via Dapr secrets API
- [ ] Complete deployment process documented and reproducible
- [ ] Troubleshooting guide created for common issues