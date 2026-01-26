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

## Notes

- This is a local development deployment
- For production deployment, additional security and configuration would be needed
- The application uses environment variables for configuration
- Health checks are implemented for both services