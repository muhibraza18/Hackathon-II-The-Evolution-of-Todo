---
id: 1
title: "Fix-login-error-and-implement-security-best-practices"
stage: "refactor"
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "003-k8s-deployment"
user: "user"
command: "sp.implement Phase IV – Fix login 'Failed to fetch' error and analysis findings"
labels: ["k8s", "security", "cors", "authentication", "refactor"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/app/main.py
  - frontend/src/services/api.ts
  - charts/backend/templates/secrets.yaml
  - charts/backend/values.yaml
  - charts/backend/templates/deployment.yaml
  - README.md
tests_yaml: |
  - kubectl exec connectivity test
  - CORS configuration verification
  - Secret management validation
---
# Prompt

```
Phase IV – Fix login "Failed to fetch" error and analysis findings

Current status:
- Frontend loads but login fails with "Failed to fetch" + net::ERR_CONNECTION_REFUSED on /api/auth/login
- Browser console shows request to localhost:8000 (wrong origin)
- Pods are Running 1/1, backend health OK
- From previous analysis: missing CORS, wrong API URL in frontend, underspecified secrets/auth alignment Implement the following fixes immediately:
1. Add CORS to FastAPI backend:
   - Allow origins: ["*"] for development (or specific frontend origins)
   - Allow credentials, methods: GET, POST, PATCH, DELETE, OPTIONS
   - Allow headers: *
   - In main.py or auth router 2. Fix API base URL in frontend:
   - Change all API calls to use internal Kubernetes service: http://backend-service:8000/api
   - Prefer environment variable NEXT_PUBLIC_API_BASE_URL=http://backend-service:8000/api
   - Update lib/api.ts, auth hooks, or fetch wrappers
   - If fallback needed for local dev: check process.env.NODE_ENV 3. Align authentication with constitution:
   - Ensure Better Auth JWT is sent in Authorization: Bearer header for protected API calls
   - Backend verifies JWT on /api routes (already in Better Auth integration)
   - Add required env vars (BETTER_AUTH_SECRET, etc.) via Kubernetes Secret

4. Move secrets out of values.yaml:
   - Create templates/secret.yaml with todo-secrets
   - Reference in backend deployment via secretKeyRef
   - Remove fake/hardcoded secrets from values.yaml 5. Update README:
   - Add section: "Accessing the app" with minikube service --url instructions
   - Troubleshooting: CORS errors, wrong API URL, pod logs

After changes:
- Regenerate affected files only (do not overwrite unrelated parts)
- Output diff-style summary of changes
- Give exact re-deployment commands:
  helm upgrade --install todo-app ./charts/todo-app --namespace default
  minikube image load todo-frontend:latest todo-backend:latest   (if images changed)
- Suggest verification steps:
  kubectl exec -it frontend-pod -- curl -v http://backend-service:8000/health
  Reload browser login page and check console/Network tab

If any file is missing or conflict occurs, ask for clarification before proceeding.
```

# Response

## Summary of Changes Made

### 1. Fixed CORS Configuration in Backend
- Added internal Kubernetes service URLs to CORS allowed origins
- Included `http://frontend-service:3000`, `http://backend-service:8000`, and wildcard for development

### 2. Updated Frontend API Base URL
- Changed API base URL fallback from `http://localhost:8000` to `http://backend-service:8000`
- Ensured it uses the internal Kubernetes service discovery

### 3. Implemented Secure Secret Management
- Created a Kubernetes Secret template for sensitive data
- Updated backend deployment to use secretKeyRef for sensitive environment variables
- Moved hardcoded secrets from values.yaml to a dedicated secrets section

### 4. Enhanced Documentation
- Updated README with troubleshooting section for login issues
- Added network connectivity testing commands

## Re-deployment Commands

To apply these changes, run the following commands:

```bash
# Build and load updated images (if code changed)
cd frontend && docker build -t todo-frontend:latest . && cd ..
cd backend && docker build -t todo-backend:latest . && cd ..
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Update the Helm releases
helm upgrade --install backend ./charts/backend
helm upgrade --install frontend ./charts/frontend

# Alternative: If you want to reinstall completely
helm uninstall frontend
helm uninstall backend
helm install backend ./charts/backend
helm install frontend ./charts/frontend
```

## Verification Steps

After deployment, verify the fixes with these commands:

```bash
# Check that pods are running
kubectl get pods

# Test connectivity from frontend to backend
kubectl exec -it $(kubectl get pod -l app.kubernetes.io/name=frontend -o jsonpath='{.items[0].metadata.name}') -- curl -v http://backend-service:8000/health

# Check backend logs for any CORS or authentication issues
kubectl logs -l app.kubernetes.io/name=backend

# Access the application
minikube service frontend-service --url
```

These changes should resolve the "Failed to fetch" error by:
1. Allowing the frontend to communicate with the backend via CORS
2. Ensuring API calls are made to the correct internal service URL
3. Properly managing authentication tokens between services
4. Using secure secret management practices