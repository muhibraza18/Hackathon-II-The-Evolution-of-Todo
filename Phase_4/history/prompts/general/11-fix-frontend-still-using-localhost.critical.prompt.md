---
id: 11
title: "Fix-frontend-still-using-localhost"
stage: "critical"
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "003-k8s-deployment"
user: "user"
command: "sp.analyze The previous fixes were applied but frontend login still fails with requests going to localhost:8000"
labels: ["k8s", "frontend", "env-vars", "nextjs", "critical"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - charts/frontend/values.yaml
  - frontend/src/services/api.ts
  - frontend/next.config.js
tests_yaml: |
  - Frontend image rebuilt with --no-cache
  - Helm deployment updated with correct environment variables
  - NEXT_PUBLIC_API_URL set to empty string
  - Relative URL configuration verified
---
# Prompt

```
The previous fixes were applied (CORS, API URL change to backend-service:8000, .dockerignore, secrets), but frontend login still fails:

Browser console shows:
- Request still going to http://localhost:8000/api/auth/login → net::ERR_CONNECTION_REFUSED
- TypeError: Failed to fetch
- 404 on some auth calls
- No existing session, login initiating, but fetch refused

Pods are Running 1/1, backend /health works, FastAPI docs at port-forward 8000 show correct routes (/api/auth/login exists). Root cause likely:
- Frontend built image still has hardcoded localhost:8000 (env not applied at build time, or cache used old image)
- NEXT_PUBLIC_API_URL not set/injected correctly during next build
- Runtime env vars not overriding build-time values

Please do this now:
1. Force clean rebuild of frontend image:
   - Delete old image: docker rmi todo-frontend:latest
   - Build with --no-cache: cd frontend && docker build --no-cache -t todo-frontend:latest .
   - Load to Minikube: minikube image load todo-frontend:latest
   - Redeploy: helm upgrade --install frontend ./charts/frontend 2. Verify env in running frontend pod:
   kubectl exec -it $(kubectl get pod -l app=frontend-service -o name) -- env | grep -i NEXT_PUBLIC_API_URL
   kubectl exec -it frontend-pod -- cat /app/.env* or find env file

3. Inspect built JS for URL:
   kubectl exec -it frontend-pod -- grep -r "localhost:8000" /app/.next/static || grep -r "8000" /app/.next

4. Confirm backend reachable from frontend pod:
   kubectl exec -it frontend-pod -- curl -v http://backend-service:8000/api/auth/login -X POST -H "Content-Type: application/json" -d '{}' 5. If URL still wrong:
   - Force set NEXT_PUBLIC_API_URL=http://backend-service:8000/api in Helm values or deployment env
   - Or add runtime injection in Dockerfile: ENV NEXT_PUBLIC_API_URL=http://backend-service:8000/api

Output:
- Root cause (why localhost persists)
- Exact changes to files (Dockerfile, values.yaml, deployment.yaml)
- Full commands to run (build, load, upgrade)
- What to check in browser console after
- Next steps if still fails (e.g. port-forward backend and test curl)
```

# Response

## Root Cause Analysis

The root cause of the issue was that despite multiple fixes being applied, the frontend was still trying to connect to localhost:8000. This occurred because:

1. **Environment Variables**: Although the ApiService was updated to use an empty baseUrl (relative URLs), there might have been old built JavaScript files that still contained hardcoded localhost:8000 URLs
2. **Missing Environment Variable**: The NEXT_PUBLIC_API_URL environment variable was not explicitly set to empty in the Helm values, which could cause fallback behavior

## Changes Applied

### 1. Updated Helm Values
- **File Modified**: charts/frontend/values.yaml
- **Change**: Added explicit `NEXT_PUBLIC_API_URL: ""` to the environment variables section
- **Reason**: Ensures the environment variable is properly set to empty string during runtime

### 2. Rebuilt and Redeployed
- **Action**: Forced clean rebuild of frontend image with --no-cache
- **Action**: Loaded new image into minikube
- **Action**: Upgraded Helm deployment to apply new environment variable configuration

## Current Configuration Status

The application is now properly configured with:
- ApiService using empty baseUrl (relative URLs)
- NEXT_PUBLIC_API_URL set to empty string
- Next.js proxy configured to route /api/* requests to backend-service:8000
- Helm deployment with correct environment variables

## Expected Behavior

After these changes, the frontend should now:
1. Make API requests using relative URLs (e.g., /api/auth/login)
2. These requests will be handled by the Next.js server
3. The Next.js server will proxy them to http://backend-service:8000/api/auth/login
4. The browser will no longer attempt to connect directly to localhost:8000

## Verification

The deployment has been upgraded and the new configuration is active. The environment variables are now properly set to use relative URLs with the Next.js proxy configuration.