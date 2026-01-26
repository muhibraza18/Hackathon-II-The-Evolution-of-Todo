# Implementation Plan: Local Kubernetes Deployment of Todo AI Chatbot

**Feature Branch**: `003-k8s-deployment`
**Created**: 2026-01-22
**Status**: Draft
**Input**: User description: "Phase IV: Local Kubernetes Deployment of Todo AI Chatbot"

## Technical Context

### Architecture Overview
The Todo AI Chatbot consists of two main components that need to be containerized and deployed to a local Minikube cluster:
- **Frontend**: Next.js application with OpenAI ChatKit
- **Backend**: FastAPI application with OpenAI Agents SDK and MCP server
- **Database**: Neon PostgreSQL (external to cluster)

### Infrastructure Components
- **Container Runtime**: Docker for containerization
- **Orchestration**: Docker Compose for local development, Kubernetes via Minikube for cloud-native deployment
- **Package Manager**: Helm for Kubernetes deployment, Docker Compose for local development
- **AI-Assisted Operations**: kubectl-ai for natural language Kubernetes commands (future)

### Unknowns to Resolve
- **Docker base images**: RESOLVED - Using multi-stage builds with node:18-alpine for frontend and python:3.11-slim for backend based on research findings
- **Helm chart organization**: RESOLVED - Separate Helm charts for frontend and backend based on research findings
- **Image loading strategy**: RESOLVED - Using minikube image load for local development based on research findings
- **Service type**: RESOLVED - NodePort service type for frontend access based on research findings
- **Resource allocation**: RESOLVED - Conservative allocation of 256Mi/512Mi for frontend and 512Mi/1Gi for backend based on research findings

## Constitution Check

### Compliance Status
- ✅ **Spec-Driven Development**: Following spec → plan → tasks → implement cycle
- ✅ **AI-Assisted Development**: Using AI tools for Dockerfile/Helm chart generation and kubectl-ai operations
- ✅ **Reproducible Environments**: Containerized deployment ensures consistency
- ✅ **Container-First Architecture**: Creating Docker images for both services with optimized base images
- ✅ **Immutable Infrastructure**: Using Helm charts for version-controlled deployments
- ✅ **Environment Parity**: Local Minikube mirrors cloud Kubernetes
- ✅ **Observability**: Health checks and logging configured for both services

### Potential Violations
None identified - all planned activities align with constitutional principles.

## Gates

### Gate 1: Architecture Feasibility
✅ **PASSED**: Kubernetes deployment is technically feasible for the application architecture

### Gate 2: Resource Constraints
✅ **PASSED**: Minikube with ≤3072MiB memory is achievable on development machines

### Gate 3: Constitutional Compliance
✅ **PASSED**: All planned activities align with project constitution

### Gate 4: Specification Alignment
✅ **PASSED**: Implementation plan directly addresses all functional requirements from spec

## Phase 0: Research & Architecture

### Research Tasks
1. **Docker Base Images Selection**
   - Task: Research optimal base images for Node.js (frontend) and Python (backend)
   - Decision: Choose between Alpine, Debian, or Ubuntu bases
   - Tradeoff: Size vs build speed vs security

2. **Helm Chart Organization**
   - Task: Evaluate single vs separate charts approach
   - Decision: Separate charts for better maintainability
   - Tradeoff: Simplicity vs flexibility

3. **Service Exposure Strategy**
   - Task: Determine best approach for exposing frontend service
   - Decision: Use NodePort for Minikube access
   - Tradeoff: Ease of access vs production similarity

4. **Resource Allocation Planning**
   - Task: Determine appropriate CPU/memory requests and limits
   - Decision: Conservative allocation to fit memory constraints
   - Tradeoff: Stability vs performance

### Architecture Diagram
```
┌─────────────────┐    ┌──────────────────────┐
│   Browser/      │    │                      │
│   Client        │    │   Minikube Cluster   │
│                 │    │                      │
└─────────┬───────┘    └──────────┬───────────┘
          │                       │
          │   HTTP Request        │
          │──────────────────────▶│
          │                       │
          │◀──────────────────────┤
          │   Response            │
          │                       │
          │              ┌────────▼────────┐
          │              │  Frontend Pod   │
          │              │  (Next.js)      │
          │              └────────┬────────┘
          │                       │
          │              ┌────────▼────────┐
          │              │  Backend Pod    │
          │              │  (FastAPI)      │
          │              └────────┬────────┘
          │                       │
          │              ┌────────▼────────┐
          │              │  Database       │
          │              │  (Neon PG)      │
          │              └─────────────────┘
```

### Folder Structure Updates
```
├── charts/
│   ├── frontend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       └── _helpers.tpl
│   └── backend/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── _helpers.tpl
├── frontend/
│   └── Dockerfile
└── backend/
    └── Dockerfile
```

## Phase 1: Design & Contracts

### Data Model Considerations
- **Frontend Service**: Configuration parameters including NEXT_PUBLIC_API_URL for connecting to backend service
- **Backend Service**: Environment variables for database connection (DATABASE_URL), API keys (OPENAI_API_KEY), and authentication secrets (BETTER_AUTH_SECRET)
- **Kubernetes Resources**: Deployments, Services, ConfigMaps, Secrets

### API Contract Patterns
- Frontend ↔ Backend: RESTful API communication
- Backend ↔ Database: PostgreSQL connection
- Services: Kubernetes service discovery

### Quickstart Guide Elements
1. Prerequisites installation
2. Minikube cluster setup
3. Docker image building and loading
4. Helm chart deployment
5. Service access verification

## Phase 2: Implementation Sequence

### Phase 2A: Preparation & Environment Setup
1. Verify Minikube installation and start cluster
2. Configure Docker to use Minikube's container registry
3. Create necessary directory structures

### Phase 2B: Containerization
1. Create optimized Dockerfiles for frontend and backend
2. Build Docker images locally
3. Load images into Minikube

### Phase 2C: Helm Charts Creation
1. Generate separate Helm charts for frontend and backend
2. Configure appropriate resource allocations
3. Set up service discovery between components

### Phase 2D: Deployment & Validation
1. Deploy Helm charts to Minikube
2. Verify pod readiness and service connectivity
3. Test application functionality

### Phase 2E: AI-Assisted Operations Setup
1. Configure kubectl-ai for natural language commands
2. Demonstrate at least 3 different kubectl-ai operations
3. Document command examples

## Quality Validation & Verification Checklist

### Pre-deployment Checks
- [ ] Docker images build successfully for both frontend and backend
- [ ] Images are loaded into Minikube registry
- [ ] Helm charts pass linting and dependency checks
- [ ] Resource allocations comply with memory constraints

### Deployment Validation
- [ ] Helm install succeeds without errors
- [ ] All pods reach Ready status within 5 minutes
- [ ] Services are accessible and responding
- [ ] Frontend can connect to backend service
- [ ] Backend can connect to external database

### Post-deployment Verification
- [ ] kubectl-ai "show all pods" lists running pods with status
- [ ] kubectl-ai "check backend logs" shows healthy startup
- [ ] Frontend is accessible via browser
- [ ] Application functionality works end-to-end
- [ ] minikube stop/start preserves application state

### Success Criteria Verification
- [ ] SC-001: Docker images build successfully
- [ ] SC-002: Helm charts install and pods reach Ready status
- [ ] SC-003: Frontend accessible via browser
- [ ] SC-004: 3+ kubectl-ai commands work successfully
- [ ] SC-005: Application survives minikube restart
- [ ] SC-006: Memory usage under 3072MiB
- [ ] SC-007: README updated with access instructions

## Risk Mitigation

### High-Risk Areas
1. **Resource Constraints**: Careful memory allocation to prevent pod evictions
2. **Network Connectivity**: Proper service discovery between frontend and backend
3. **External Dependencies**: Reliable database connection from within cluster

### Contingency Plans
- If memory allocation fails: Reduce resource requests further
- If networking fails: Use ClusterIP with port forwarding
- If image loading fails: Use alternative loading strategies

## Next Steps
1. Complete Phase 0 research to resolve all NEEDS CLARIFICATION items
2. Proceed to Phase 1 with final design decisions
3. Execute implementation sequence in Phase 2