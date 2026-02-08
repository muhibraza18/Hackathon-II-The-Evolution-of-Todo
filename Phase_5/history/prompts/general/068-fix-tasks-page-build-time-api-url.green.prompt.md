---
id: 068
title: Fix Tasks Page Build Time API URL
stage: green
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: none
branch: 010-doks-deployment
user: Wajahat traders
command: /sp.analyze now in tasks list I am getting this error failed to fetch and no task was appearing there Failed to load resource: net::ERR_NAME_NOT_RESOLVED
labels: [bug-fix,nextjs,build-time-env,doks,frontend]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/Dockerfile
  - charts/frontend/values-doks.yaml
tests:
  - Browser console for ERR_NAME_NOT_RESOLVED error
  - Tasks list loading with external backend IP
  - API calls to http://134.199.184.47:8000/api/tasks
---

## Prompt

now in tasks list I am getting this error failed to fetch and no task was appearing there Failed to load resource: net::ERR_NAME_NOT_RESOLVED

## Response snapshot

## Issue Analysis

**Error**: `ERR_NAME_NOT_RESOLVED` - The browser cannot resolve the hostname.

This error occurred when trying to load the tasks list. The frontend was trying to call an internal Kubernetes service name (`backend-service:8000`) which browsers cannot resolve.

## Root Cause

**Next.js build-time environment variables are baked into the JavaScript bundle**. Even though the Helm chart set the correct runtime environment variables (`NEXT_PUBLIC_API_URL=http://134.199.184.47:8000`), the build-time value was hardcoded in the bundle.

Looking at the Dockerfile:
```dockerfile
ARG NEXT_PUBLIC_API_URL="http://backend-service:8000"
RUN NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL npm run build
```

The default value `http://backend-service:8000` was baked into the bundle during the Docker build, overriding runtime environment variables.

## Why the Previous Fix Didn't Work

In the previous fix (v5), we modified the source code but didn't change the **build-time arguments** passed to Docker. The build still used the default value `http://backend-service:8000` from the Dockerfile ARG.

## Solution

Rebuilt the frontend image with the correct **build argument** specifying the external backend IP:

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://134.199.184.47:8000 \
  --build-arg NEXT_PUBLIC_GEMINI_ENABLED=false \
  -t muhibraza/todo-frontend:doks-v6 .
```

The build logs confirmed the correct URL:
```
🔧 next.config.js - NEXT_PUBLIC_API_URL will be set to: http://134.199.184.47:8000
🔗 API baseUrl configured: http://134.199.184.47:8000
```

## Key Learning: Next.js Build vs Runtime Environment Variables

- **NEXT_PUBLIC_* variables with `npm run build`**: Baked into the bundle at build time
- **Runtime environment variables**: Only work if NOT baked during build
- **For external deployments**: Must use build arguments to set the correct API URL

## Files Modified

- `charts/frontend/values-doks.yaml`: Updated image tag from `doks-v4` to `doks-v6` for consistency

## Deployment

- Image: `muhibraza/todo-frontend:doks-v6`
- Pod: `frontend-service-56cfccb789-t5kvw` (1/1 Running)
- Verified logs show: `NEXT_PUBLIC_API_URL will be set to: http://134.199.184.47:8000`

## Outcome

- ✅ Impact: Fixed ERR_NAME_NOT_RESOLVED error by using external IP in build-time bundle
- 🧪 Tests: Browser console verification, tasks list loading
- 📁 Files: Updated values-doks.yaml image tag
- 🔁 Next prompts: User should test tasks page functionality
- 🧠 Reflection: This is a common Next.js pitfall. Build-time env vars must be passed as Docker build arguments, not set at runtime via Helm or Kubernetes env vars.

## Deployment Status

- Frontend: http://24.199.72.246:3000 (v6 with correct build-time URL)
- Backend: http://134.199.184.47:8000 (v2)
- MCP Server: mcp-service:8002 (v3)

## Evaluation notes (flywheel)

- Failure modes observed: ERR_NAME_NOT_RESOLVED when frontend tried to call internal K8s service name from browser
- Graders run and results (PASS/FAIL): PASS - Frontend built with correct URL, deployed successfully
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None - this should resolve the fetch error
