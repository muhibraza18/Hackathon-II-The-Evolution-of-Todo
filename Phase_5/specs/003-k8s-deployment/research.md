# Research: Local Kubernetes Deployment of Todo AI Chatbot

**Created**: 2026-01-22
**Feature**: Local Kubernetes Deployment

## Research Findings

### Decision 1: Docker Base Images Selection

**Decision**: Use multi-stage builds with node:18-alpine for frontend and python:3.11-slim for backend

**Rationale**:
- **node:18-alpine**: Small image size (~170MB), optimized for production builds, widely used in Next.js applications
- **python:3.11-slim**: Minimal footprint (~120MB), includes only essential packages, secure base image
- Multi-stage builds allow for optimized final images by separating build and runtime environments

**Alternatives Considered**:
- node:18-bullseye: Larger size (~900MB), more packages but unnecessary for production
- python:3.11-alpine: Potential compatibility issues with certain Python packages requiring compilation
- node:alpine-latest: Less stable, version conflicts possible

**Tradeoffs**: Build time vs final image size vs compatibility

### Decision 2: Helm Chart Organization

**Decision**: Separate Helm charts for frontend and backend

**Rationale**:
- Independent deployment and scaling of services
- Clear separation of concerns
- Easier maintenance and updates
- Independent configuration management
- Ability to version each service independently

**Alternatives Considered**:
- Single umbrella chart: Simpler initial setup but harder to maintain and scale independently
- Monorepo with shared templates: Increased complexity and coupling between services

**Tradeoffs**: Initial setup complexity vs long-term maintainability

### Decision 3: Image Loading Strategy

**Decision**: Use minikube image load for local development

**Rationale**:
- Simplest approach for local Minikube deployment
- No need to set up local registry
- Direct loading of locally built images to Minikube's container runtime
- Perfect for demonstration and development purposes
- Aligns with Phase IV constitution (local only)

**Alternatives Considered**:
- Local registry: More complex setup, unnecessary for local demonstration
- External registry: Against constitution (local only requirement)

**Tradeoffs**: Simplicity vs production realism

### Decision 4: Service Type Selection

**Decision**: NodePort service type for frontend access

**Rationale**:
- Works reliably with Minikube
- Allows external access via minikube service command
- Simple to set up and access
- Good for demonstration purposes

**Alternatives Considered**:
- ClusterIP: Internal access only, requires port forwarding
- LoadBalancer: May not work reliably with Minikube without additional configuration

**Tradeoffs**: Simplicity vs production similarity

### Decision 5: Resource Allocation

**Decision**: Conservative resource allocation to stay within memory constraints

**Rationale**:
- Frontend: 256Mi memory request, 512Mi limit
- Backend: 512Mi memory request, 1Gi limit
- CPU: 100m request, 500m limit for both services
- Well within 3072MiB total constraint
- Allows for safe operation on development machines

**Alternatives Considered**:
- Higher allocations: Risk of exceeding host memory limits
- No limits: Potential resource exhaustion

**Tradeoffs**: Performance vs stability on resource-constrained hosts

## Technical Architecture Decisions

### Network Communication
- Services communicate via Kubernetes DNS service discovery
- Backend service exposed as `backend-service.default.svc.cluster.local`
- Frontend configured with backend service URL

### Health Checks
- Liveness and readiness probes for both services
- Backend: HTTP GET /health endpoint
- Frontend: HTTP GET /api/health endpoint

### Configuration Management
- Environment variables passed via Helm values
- Database connection details via environment variables
- API keys and secrets managed separately

## Implementation Considerations

### Dockerfile Optimization
- Multi-stage builds to minimize attack surface
- Non-root user execution where possible
- Layer caching optimization
- Security scanning integration

### Helm Chart Best Practices
- Proper templating with values.yaml defaults
- Support for overrides and customization
- Proper labels and annotations
- Dependency management for subcharts

### Minikube Configuration
- Memory limit set to 3072MiB maximum
- Docker driver for optimal performance
- Proper resource allocation to prevent OOM kills