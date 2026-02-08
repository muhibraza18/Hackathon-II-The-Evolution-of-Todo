# Data Model: Local Kubernetes Deployment of Todo AI Chatbot

**Created**: 2026-01-22
**Feature**: Local Kubernetes Deployment

## Kubernetes Resource Entities

### Frontend Service Entity
- **Name**: frontend-service
- **Type**: Kubernetes Deployment + Service
- **Fields**:
  - image: todo-frontend:{version}
  - replicas: 1 (scalable)
  - ports: 3000 (Next.js server)
  - environment variables:
    - BACKEND_URL: http://backend-service:8000
    - NEXT_PUBLIC_API_BASE_URL: http://backend-service:8000
  - resource requests/limits:
    - memory: 256Mi/512Mi
    - cpu: 100m/500m
  - health checks:
    - readiness probe: HTTP GET /api/health
    - liveness probe: HTTP GET /api/health

### Backend Service Entity
- **Name**: backend-service
- **Type**: Kubernetes Deployment + Service
- **Fields**:
  - image: todo-backend:{version}
  - replicas: 1 (scalable)
  - ports: 8000 (FastAPI server)
  - environment variables:
    - DATABASE_URL: postgresql://user:pass@neon-db-host/dbname
    - OPENAI_API_KEY: sk-xxx
    - BETTER_AUTH_SECRET: secret-key
    - FRONTEND_URL: http://frontend-service:3000
  - resource requests/limits:
    - memory: 512Mi/1Gi
    - cpu: 100m/500m
  - health checks:
    - readiness probe: HTTP GET /health
    - liveness probe: HTTP GET /health

### Kubernetes Service Entity
- **Name**: frontend-service, backend-service
- **Type**: Kubernetes Service
- **Fields**:
  - type: NodePort (frontend), ClusterIP (backend)
  - selector: app={service-name}
  - ports:
    - port: service port
    - targetPort: container port
    - nodePort: dynamically assigned (frontend only)

### Kubernetes ConfigMap Entity
- **Name**: app-config
- **Type**: Kubernetes ConfigMap
- **Fields**:
  - data: key-value pairs for non-sensitive configuration
  - used by: frontend and backend deployments
  - examples: API timeouts, feature flags, logging levels

### Kubernetes Secret Entity
- **Name**: app-secrets
- **Type**: Kubernetes Secret
- **Fields**:
  - data: base64 encoded sensitive information
  - used by: backend deployment
  - examples: database passwords, API keys, auth secrets

## Deployment Relationships

### Frontend ↔ Backend
- **Relationship**: HTTP communication
- **Protocol**: REST API
- **Configuration**: Backend URL passed via environment variable
- **Service Discovery**: Kubernetes DNS (backend-service.default.svc.cluster.local)

### Backend ↔ Database
- **Relationship**: PostgreSQL connection
- **Protocol**: PostgreSQL wire protocol
- **Configuration**: Connection string via environment variable
- **External**: Database hosted externally (Neon PostgreSQL)

### Frontend ↔ External Access
- **Relationship**: Browser access
- **Protocol**: HTTP/HTTPS
- **Access Method**: NodePort service via minikube service command
- **External IP**: Minikube's external IP with assigned NodePort

## State Management

### Persistent State
- **Location**: External Neon PostgreSQL database
- **Components**: User data, tasks, conversations, messages
- **Recovery**: Survives pod restarts and minikube stop/start cycles

### Transient State
- **Location**: Pod memory (ephemeral)
- **Components**: Session caches, temporary processing data
- **Recovery**: Recreated on pod restart

## Validation Rules

### Resource Validation
- Memory requests must be ≤ limits
- CPU requests should be ≤ limits
- NodePort must be in valid range (30000-32767)

### Service Validation
- Service selectors must match deployment labels
- Port specifications must match container ports
- External access must be properly configured

### Environment Validation
- Required environment variables must be provided
- Database connection string format must be valid
- API key formats must be validated