# Todo AI Chatbot - Local Development & Deployment

This repository contains the Todo AI Chatbot application with support for both local Docker Compose development and Kubernetes deployment.

## Architecture

The application consists of two main services:
- **Frontend**: Next.js application with OpenAI ChatKit (Node.js)
- **Backend**: FastAPI application with OpenAI Agents SDK and MCP server (Python)

## Deployment Options

### Option 1: Local Development (Docker Compose) - Recommended for Development
- **Orchestration**: Docker Compose
- **Container Runtime**: Docker
- **Access**: Frontend at http://localhost:3000, Backend at http://localhost:8000
- **Service Communication**: Via localhost

### Option 2: Kubernetes Deployment (Minikube) - For Cloud-Native Testing
- **Orchestration**: Kubernetes via Minikube
- **Container Runtime**: Docker
- **Package Manager**: Helm for deployment
- **Service Type**:
  - Frontend: NodePort (accessible externally)
  - Backend: ClusterIP (internal communication only)

## Prerequisites

### For Docker Compose (Local Development - Recommended)
- Docker Desktop with WSL integration (if on Windows)
- Node.js (for local development)

### For Kubernetes Deployment (Advanced)
- Docker Desktop with WSL integration (if on Windows)
- Minikube with Docker driver
- kubectl
- Helm
- Node.js (for local development)

## Setup Instructions

### Option 1: Docker Compose (Local Development - Recommended)

1. **Set up environment variables**
   Create a `.env` file in the `backend/` directory with your database URL and API keys:
   ```bash
   # backend/.env
   DATABASE_URL=postgresql+asyncpg://username:password@your-neon-db-url:5432/todo_chatbot
   OPENAI_API_KEY=your_openai_api_key
   BETTER_AUTH_SECRET=your_auth_secret
   ```

2. **Start the services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Option 2: Kubernetes Deployment (Minikube)

1. **Start Minikube Cluster**
   ```bash
   minikube start --driver=docker --memory=3072mb
   ```

2. **Build Docker Images**
   ```bash
   # Build frontend image
   cd frontend
   docker build -t todo-frontend:latest .
   cd ..

   # Build backend image
   cd backend
   docker build --no-cache -t todo-backend:latest .
   cd ..
   ```

3. **Load Images into Minikube**
   ```bash
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   ```

4. **Deploy Using Helm**
   ```bash
   # Install backend chart
   helm install backend ./charts/backend

   # Install frontend chart
   helm install frontend ./charts/frontend
   ```

5. **Access the Application**

   #### Frontend Service
   The frontend is accessible via NodePort:

   ```bash
   minikube service frontend-service --url
   ```

   This will return a URL like `http://127.0.0.1:PORT` where you can access the application in your browser.

   #### Backend Service
   The backend service is available internally within the cluster at:
   - `http://backend-service:8000`

   To access the backend service externally for testing:
   ```bash
   minikube service backend-service --url
   ```

## Kubernetes Resources

### Deployments
- `backend-service`: FastAPI backend application
- `frontend-service`: Next.js frontend application

### Services
- `backend-service`: ClusterIP type (internal communication)
- `frontend-service`: NodePort type (external access)

### Configuration
- Environment variables are configured via Helm values
- Database connection is configured via environment variables
- Health checks are configured for both services

## Verification Commands

### Check Pod Status
```bash
kubectl get pods
```

### Check Service Status
```bash
kubectl get services
```

### Check Deployment Status
```bash
kubectl get deployments
```

### View Pod Logs
```bash
kubectl logs -l app.kubernetes.io/name=backend
kubectl logs -l app.kubernetes.io/name=frontend
```

## Troubleshooting

### Docker Compose Issues (Local Development)

#### Login "Failed to fetch" Error (Docker Compose)
If you encounter a "Failed to fetch" error during login with Docker Compose:
- Check CORS errors in browser console
- Verify the frontend can reach the backend service at http://localhost:8000
- Ensure the `NEXT_PUBLIC_API_URL` is set to "http://localhost:8000" in the frontend Dockerfile
- Check backend logs: `docker-compose logs backend`
- Ensure your backend service is running and accessible: `curl http://localhost:8000/health`

#### Docker Compose Startup Issues
- Ensure Docker Desktop is running
- Check if services started properly: `docker-compose ps`
- View detailed logs: `docker-compose logs -f`
- If getting permission errors, try: `docker-compose down` then `docker-compose up --build`

#### Database Connection Issues
- Ensure your Neon PostgreSQL database is accessible from your network
- Check that the DATABASE_URL in `backend/.env` is correct
- Verify the database allows connections from your IP address

### Kubernetes Issues (Minikube)

#### Login "Failed to fetch" Error (Kubernetes)
If you encounter a "Failed to fetch" error during login with Kubernetes:
- Check CORS errors in browser console
- Verify the frontend can reach the backend service
- Ensure API calls are made to the correct internal service URL (http://backend-service:8000)
- Check backend logs for authentication errors: `kubectl logs -l app.kubernetes.io/name=backend`

#### Pods in CrashLoopBackOff
If pods are in `CrashLoopBackOff` status, check the logs:
```bash
kubectl logs <pod-name>
```

Common issues:
- Database connection issues
- Missing environment variables
- Incorrect image tags

#### Service Not Accessible
- Verify the service is running: `kubectl get services`
- Check if the correct NodePort is exposed
- Ensure Minikube tunnel is running (if needed)

#### Minikube Issues
- Ensure Docker is running
- Check Minikube status: `minikube status`
- Restart Minikube if needed: `minikube stop && minikube start`

#### Network Connectivity Issues
To test connectivity between services:
```bash
kubectl exec -it <frontend-pod-name> -- curl -v http://backend-service:8000/health
kubectl exec -it <frontend-pod-name> -- nslookup backend-service
```

## Kubernetes Operations (kubectl commands)

### Common Operations
```bash
# Get all resources
kubectl get all

# Scale deployments
kubectl scale deployment <deployment-name> --replicas=<number>

# Update deployments
kubectl set image deployment/<deployment-name> <container>=<new-image>

# Port forward for debugging
kubectl port-forward service/<service-name> <local-port>:<service-port>
```

## Cleanup

To remove the deployment:
```bash
helm uninstall frontend
helm uninstall backend
```

To stop Minikube:
```bash
minikube stop
```

---

## Phase V: Advanced Features & Dapr Integration

This section covers the Phase V advanced features including recurring tasks, due date reminders, event-driven architecture, and Dapr integration.

### Phase V Features

- **Recurring Tasks**: Tasks that automatically regenerate when completed
- **Due Date Reminders**: Scheduled notifications via Dapr Jobs API
- **Event-Driven Architecture**: Kafka-based pub/sub for task events
- **Priority & Tag Filtering**: Organize and filter tasks by priority and custom tags
- **Full-Text Search**: Search across task titles and descriptions
- **Advanced Sorting**: Sort tasks by due date, priority, or creation date

### Phase V Prerequisites

Before deploying Phase V features, ensure you have:

1. **Minikube Running** with adequate resources:
   ```bash
   minikube start --driver=docker --memory=3072 --cpus=4
   ```

2. **Dapr Installed** on the cluster:
   ```bash
   # Install Dapr CLI (Windows)
   winget install Dapr.CLI

   # Initialize Dapr in Kubernetes
   dapr init -k --enable-ha=false
   ```

3. **Kafka/Redpanda** for pub/sub messaging

4. **PostgreSQL** database with Phase V schema

### Phase V Deployment Status

**Current Status**: Phase V Step 4 (Minikube + Dapr Deployment) is a prerequisite for this testing phase.

To verify if Phase V is deployed:
```bash
# Check for Dapr control plane
kubectl get pods -n dapr-system

# Check for Dapr sidecars in app pods
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'

# Check for Dapr components
kubectl get components.dapr.io

# Check for consumer services
kubectl get deployments -l app=todo-consumers
```

---

## Local Setup for Phase V Testing

This section provides detailed instructions for setting up the Phase V environment on Minikube for local testing and hackathon evaluation.

### Prerequisites Checklist

Before starting Phase V setup, ensure you have:

- [ ] Docker Desktop installed and running
- [ ] Minikube installed (`minikube version`)
- [ ] kubectl installed (`kubectl version --client`)
- [ ] Helm installed (`helm version`)
- [ ] Dapr CLI installed (`dapr version`)
- [ ] At least 4GB RAM available (8GB recommended)
- [ ] 4+ CPU cores available

### Step 1: Start Minikube

```bash
# Start Minikube with Docker driver and adequate resources
minikube start --driver=docker --memory=3072 --cpus=4

# Verify Minikube is running
minikube status
```

**Expected output**: All components showing "Running"

### Step 2: Initialize Dapr

```bash
# Install Dapr to Kubernetes cluster
dapr init -k --enable-ha=false --log-as-json

# Verify Dapr installation
dapr status -k
```

**Expected output**: Dapr control plane services showing "Healthy"

### Step 3: Deploy Kafka/Redpanda

```bash
# Create Kafka namespace
kubectl create namespace kafka

# Install Strimzi operator
kubectl create -f https://strimzi.io/install/latest?namespace=kafka -n kafka

# Deploy Kafka cluster (ephemeral storage for local)
kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-persistent-single.yaml -n kafka

# Wait for Kafka to be ready
kubectl wait kafka/my-cluster -n kafka --for=condition=Ready --timeout=300s
```

### Step 4: Build and Load Docker Images

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..

# Build consumers image
cd consumers
docker build -t todo-consumers:latest .
cd ..

# Load images into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
minikube image load todo-consumers:latest
```

### Step 5: Deploy Application with Dapr

```bash
# Update Helm chart values for Dapr
# (Ensure dapr.enabled=true in values files)

# Deploy backend with Dapr sidecar
helm upgrade --install todo-backend charts/backend/ --set dapr.enabled=true

# Deploy frontend with Dapr sidecar
helm upgrade --install todo-frontend charts/frontend/ --set dapr.enabled=true

# Deploy consumers with Dapr sidecar
helm upgrade --install todo-consumers charts/consumers/ --set dapr.enabled=true

# Wait for deployments to be ready
kubectl rollout status deployment/todo-backend
kubectl rollout status deployment/todo-frontend
kubectl rollout status deployment/todo-consumers
```

### Step 6: Apply Dapr Components

```bash
# Apply Dapr component configurations
kubectl apply -f dapr-components/pubsub/kafka-pubsub.yaml
kubectl apply -f dapr-components/state/postgresql-statestore.yaml
kubectl apply -f dapr-components/secrets/kubernetes-secrets.yaml

# Verify components are loaded
kubectl get components.dapr.io
```

### Step 7: Verify Deployment

```bash
# Check all pods are running
kubectl get pods

# Expected: All pods show 2/2 Ready (app container + Dapr sidecar)

# Check Dapr sidecars
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'

# Expected: Each app pod shows "app" and "daprd" containers

# Get frontend URL
minikube service todo-frontend --url
```

---

## Verification Commands for Phase V

### Automated Health Checks

```bash
# 1. Check all pods Running
kubectl get pods
# Expected: All STATUS=Running, READY=2/2 or 1/1

# 2. Verify Dapr sidecars present
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
# Expected: Each app pod shows daprd container

# 3. Check Dapr system status
dapr status -k
# Expected: All apps HEALTHY

# 4. Check Dapr components loaded
kubectl get components.dapr.io
# Expected: STATUS=Loaded for all components

# 5. Get frontend URL
FRONTEND_URL=$(minikube service todo-frontend --url)
echo "Frontend: $FRONTEND_URL"

# 6. Test health endpoints
curl $FRONTEND_URL/health
# Expected: HTTP 200

# 7. Check for critical errors in logs
kubectl logs deployment/todo-backend --tail=100 | grep -i "ERROR\|CRITICAL"
# Expected: No critical errors

# 8. Check consumer logs for event processing
kubectl logs deployment/todo-consumers --tail=50 | grep "event"
# Expected: Event processing logs visible
```

### Manual E2E Test Scenarios

#### Test 1: Recurring Tasks (P1)

1. Login to the application via frontend URL
2. Create a new task with:
   - Title: "Daily Standup"
   - Recurrence: Daily
   - Due date: Tomorrow
   - Priority: High
   - Tag: "work"
3. Verify task appears in task list with recurrence indicator
4. Complete the task (mark as done)
5. **Verify**: A new instance is auto-created for tomorrow
6. **Check logs**: `kubectl logs deployment/todo-consumers --tail=50 | grep "task.completed"`

#### Test 2: Due Date Reminders (P1)

1. Create a task with due date 2 minutes in the future
2. Note the current time
3. Wait for due date to pass
4. **Check logs**: `kubectl logs deployment/todo-consumers -f | grep "reminder"`
5. **Verify**: Reminder notification appears in logs at scheduled time

#### Test 3: Priority & Tag Filtering (P1)

1. Create multiple tasks with different priorities (high, medium, low)
2. Create tasks with different tags (work, personal, urgent)
3. Apply priority filter: "High only"
4. **Verify**: Only high-priority tasks displayed
5. Apply tag filter: "work"
6. **Verify**: Only tasks with "work" tag displayed

#### Test 4: Event Flow Verification (P2)

1. Open terminal to watch consumer logs:
   ```bash
   kubectl logs deployment/todo-consumers -f
   ```
2. In the UI, create a new task
3. **Verify**: Task creation triggers event publish
4. **Verify**: All three consumers log processing (recurring, notification, audit)

---

## Troubleshooting Guide for Phase V

### Issue: Pods in CrashLoopBackOff

**Diagnosis**:
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Common Causes**:
- Database connection failure
- Missing environment variables
- Dapr sidecar not starting
- Image pull errors

**Resolution**:
- Check database is accessible
- Verify secrets are mounted: `kubectl get secrets`
- Check Dapr sidecar logs: `kubectl logs <pod-name> -c daprd`
- Restart Dapr: `dapr uninstall -k && dapr init -k`

### Issue: Dapr Sidecar Not Starting

**Diagnosis**:
```bash
kubectl logs <pod-name> -c daprd
dapr status -k
```

**Resolution**:
- Verify Dapr annotations in pod spec: `kubectl describe pod <pod-name> | grep dapr.io`
- Reinstall Dapr: `dapr uninstall -k && dapr init -k`
- Check sidecar-injector is running: `kubectl get pods -n dapr-system`

### Issue: Events Not Publishing

**Diagnosis**:
```bash
kubectl logs deployment/todo-backend | grep "publish"
kubectl logs deployment/todo-consumers | grep "subscribe"
kubectl get components.dapr.io
```

**Resolution**:
- Verify Kafka is running: `kubectl get pods -n kafka`
- Check Dapr pubsub component: `kubectl describe component kafka-pubsub`
- Restart backend pod: `kubectl delete pod -l app=todo-backend`

### Issue: Frontend Not Accessible

**Diagnosis**:
```bash
minikube service todo-frontend --url
kubectl get services
kubectl get pods -l app=todo-frontend
```

**Resolution**:
- Check Minikube tunnel is running (if using LoadBalancer)
- Verify frontend pod is Running
- Restart Minikube if needed: `minikube stop && minikube start`

### Issue: Jobs API Not Scheduling Reminders

**Diagnosis**:
```bash
kubectl logs deployment/todo-backend -c daprd | grep "job"
kubectl logs deployment/todo-consumers | grep "reminder"
```

**Resolution**:
- Verify Dapr Jobs API is enabled
- Check component configuration for jobs
- Test job scheduling manually with Dapr API

---

## Demo Preparation Guide

This section provides guidance for preparing a hackathon demo showcasing the Phase V features.

### Demo Script (90 Seconds)

**0:00-0:15: Introduction & Login**
- Show frontend URL: `minikube service todo-frontend --url`
- Login with demo credentials
- Mention: "Todo AI Chatbot with advanced features"

**0:15-0:35: Create Recurring Task**
- Click "New Task"
- Enter title: "Daily Standup"
- Set Recurrence: Daily
- Set Priority: High
- Add Tag: "work"
- Set Due Date: Tomorrow
- Click Save
- Show task in list with recurrence indicator

**0:35-0:55: Show Event Flow**
- Switch to terminal with logs running
- Point out: "Event published to Kafka"
- Show: "Consumer processed the event"
- Show: "Audit log recorded"

**0:55-0:75: Schedule Reminder**
- Create task with due date 2 minutes out
- Show: "Dapr Jobs API schedules reminder"
- Wait (fast forward if needed)
- Show: "Reminder fired at scheduled time"

**0:75-0:90: Summary**
- Show all working features
- Mention: "Recurring tasks, reminders, events, Dapr"
- End demo

### Screenshot Checklist

Capture screenshots at these key moments:

1. **Login Screen** - Show authentication UI
2. **Task List** - Show varied tasks with priorities/tags
3. **Create Task Form** - Show filled form with recurrence, priority, tags
4. **New Task Created** - Show task in list with all attributes
5. **Consumer Logs** - Show event processing logs
6. **Dapr Components** - Show `kubectl get components.dapr.io` output
7. **Pod Status** - Show `kubectl get pods` with sidecars

### Pre-Demo Checklist

- [ ] Minikube running with all pods healthy
- [ ] Frontend URL accessible
- [ ] Demo user credentials ready
- [ ] Terminal open with log tailing command ready
- [ ] Screenshots captured as backup
- [ ] Log excerpts prepared for event flow section
- [ ] Demo practiced and timed (<90 seconds)

---

## Notes

- This is a local development deployment
- For production deployment, additional security and configuration would be needed
- The application uses environment variables for configuration
- Health checks are implemented for both services
- Phase V features require Dapr and Kafka to be fully operational