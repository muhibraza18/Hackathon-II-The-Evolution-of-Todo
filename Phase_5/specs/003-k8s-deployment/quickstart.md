# Quickstart Guide: Local Kubernetes Deployment of Todo AI Chatbot

**Created**: 2026-01-22
**Feature**: Local Kubernetes Deployment

## Prerequisites

### System Requirements
- **Operating System**: Ubuntu/WSL2, macOS, or Windows with WSL2
- **Memory**: At least 4GB free RAM (to accommodate Minikube with 3072MiB allocation)
- **Disk Space**: 5GB free space for Docker images and Minikube VM

### Required Tools
1. **Docker Desktop** with WSL integration (if on Windows)
   - Install from: https://docker.com
   - Enable WSL integration if using WSL2
2. **kubectl**: Kubernetes command-line tool
   - Install via package manager or from official site
3. **Helm**: Kubernetes package manager
   - Install via package manager: `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash`
4. **Minikube**: Local Kubernetes cluster
   - Install via package manager: `curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-windows-amd64.exe` (Windows)
   - Or via package managers: `brew install minikube` (macOS), `apt install minikube` (Ubuntu)
5. **kubectl-ai**: AI-assisted Kubernetes operations
   - Install via: `pip install kubectl-ai` or follow official installation guide

### Environment Setup
```bash
# Verify installations
docker --version
kubectl version --client
helm version
minikube version
kubectl ai --help
```

## Setup Process

### 1. Start Minikube Cluster
```bash
# Start Minikube with Docker driver and memory limit
minikube start --driver=docker --memory=3072mb

# Verify cluster is running
kubectl cluster-info
minikube status
```

### 2. Build Docker Images
```bash
# Build frontend image
cd frontend
docker build -t todo-frontend:latest .

# Build backend image
cd ../backend
docker build -t todo-backend:latest .

# Go back to root
cd ..
```

### 3. Load Images into Minikube
```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest

# Verify images are loaded
minikube ssh docker images | grep todo
```

### 4. Prepare Helm Charts
```bash
# Navigate to charts directory (created in next step)
# Helm charts will be created in the following structure:
# charts/
#   ├── frontend/
#   │   ├── Chart.yaml
#   │   ├── values.yaml
#   │   └── templates/
#   └── backend/
#       ├── Chart.yaml
#       ├── values.yaml
#       └── templates/
```

### 5. Deploy Application
```bash
# Install backend chart first (to ensure service is available)
helm install backend ./charts/backend

# Install frontend chart
helm install frontend ./charts/frontend

# Verify deployments
kubectl get pods
kubectl get services
```

### 6. Access the Application
```bash
# Get frontend service URL
minikube service frontend-service --url

# Or expose the service via NodePort
kubectl port-forward svc/frontend-service 3000:3000

# Access the application in your browser using the provided URL
```

## Verification Commands

### Basic Health Checks
```bash
# Check all pods are running
kubectl get pods

# Check all services are available
kubectl get services

# Check pod logs
kubectl logs -l app=backend-service
kubectl logs -l app=frontend-service
```

### AI-Assisted Kubernetes Operations
```bash
# Use kubectl-ai for natural language commands
kubectl ai "show me all pods"
kubectl ai "check backend logs for errors"
kubectl ai "describe the frontend service"
```

## Troubleshooting

### Common Issues
1. **Minikube won't start**
   - Solution: Check Docker is running and WSL integration is enabled
   - Run: `minikube delete` and restart

2. **Images not loading**
   - Solution: Ensure Docker images exist locally
   - Run: `docker images` to verify

3. **Services not accessible**
   - Solution: Check if pods are in Running state
   - Run: `kubectl get pods -o wide`

4. **Application not responding**
   - Solution: Check backend service is reachable from frontend
   - Run: `kubectl logs -l app=frontend-service` for frontend logs

### Reset Process
```bash
# Uninstall Helm releases
helm uninstall frontend
helm uninstall backend

# Delete Minikube cluster (if needed)
minikube delete

# Restart with clean slate
minikube start --driver=docker --memory=3072mb
```

## Cleanup
```bash
# Uninstall Helm releases
helm uninstall frontend
helm uninstall backend

# Stop Minikube
minikube stop

# Optional: Delete Minikube cluster
minikube delete
```

## Demo Commands for Judges
```bash
# Show running pods
kubectl ai "show me all pods and their status"

# Check backend logs
kubectl ai "show me the backend service logs"

# Describe the frontend service
kubectl ai "describe the frontend service and how to access it"

# Scale the backend service
kubectl ai "scale the backend deployment to 2 replicas"
```