---
id: 9
title: "Critical-fix-frontend-env-vars-build-time"
stage: "critical"
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "003-k8s-deployment"
user: "user"
command: "sp.analyze CRITICAL FIX: frontend/.env.local has NEXT_PUBLIC_API_URL=http://localhost:8000 which overrides everything and hardcodes localhost into the build."
labels: ["k8s", "env-vars", "nextjs", "build", "critical"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - frontend/next.config.js
  - frontend/.env
  - frontend/.env.local
tests_yaml: |
  - Environment variables updated to empty values
  - Next.js proxy configuration updated
  - Frontend image rebuilt with --no-cache
  - Pod recreated with new configuration
---
# Prompt

```
CRITICAL FIX: frontend/.env.local has NEXT_PUBLIC_API_URL=http://localhost:8000 which overrides everything and hardcodes localhost into the build.

FIXES NEEDED:

1. Update frontend/.env.local:
   Change: NEXT_PUBLIC_API_URL=http://localhost:8000
   To: NEXT_PUBLIC_API_URL=

2. Update frontend/.env:
   Add: NEXT_PUBLIC_API_URL=

3. Fix frontend/next.config.js rewrites destination:
   Change: destination: 'http://backend-service:8000/:path*'
   To: destination: 'http://backend-service:8000/api/:path*'

4. Remove the env section from next.config.js (we don't need it with relative URLs)


5. Force complete rebuild:
   docker build --no-cache -t frontend:latest ./frontend
   minikube image rm frontend:latest
   minikube image load frontend:latest
   kubectl delete pod -l app=frontend-service
   kubectl wait --for=condition=ready pod -l app=frontend-service --timeout=180s

6. After rebuild, clear browser cache (Ctrl+Shift+Delete) and hard refresh (Ctrl+Shift+R)

The .env.local file takes precedence over Dockerfile and is baking localhost:8000 into the JavaScript bundle at build time.
```

# Response

## Critical Fixes Applied

### 1. Updated Environment Files
- **frontend/.env.local**: Added `NEXT_PUBLIC_API_URL=` (empty value)
- **frontend/.env**: Added `NEXT_PUBLIC_API_URL=` (empty value)
- This ensures that the environment variable is properly set to empty during the build process

### 2. Updated Next.js Configuration
- **frontend/next.config.js**:
  - Removed the `env` section that was no longer needed
  - Updated the rewrite destination from `'http://backend-service:8000/:path*'` to `'http://backend-service:8000/api/:path*'`
  - This ensures API requests are properly forwarded to the backend with the correct path structure

### 3. Force Complete Rebuild
- Rebuilt the frontend Docker image with `--no-cache` to ensure environment variables are properly applied
- Loaded the updated image into minikube
- Deleted and recreated the frontend pod to ensure the new configuration is used

## Result

The critical issue has been resolved:
- The `.env.local` file no longer has `NEXT_PUBLIC_API_URL=http://localhost:8000` that was overriding everything
- The Next.js proxy configuration now correctly forwards `/api/*` requests to `http://backend-service:8000/api/*`
- The environment variables are properly set to empty values during the build process
- The JavaScript bundle will no longer have localhost:8000 hardcoded into it

The frontend will now properly use relative URLs and leverage the Next.js proxy configuration to route API requests to the backend service within the Kubernetes cluster.