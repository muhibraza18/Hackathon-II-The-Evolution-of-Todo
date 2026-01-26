---
id: 4
title: "Fix-frontend-environment-variables-runtime-and-build"
stage: "green"
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "003-k8s-deployment"
user: "user"
command: "sp.analyze Still getting error with localhost:8000 API calls"
labels: ["k8s", "environment-variables", "nextjs", "build", "runtime", "debugging"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - frontend/Dockerfile
tests_yaml: |
  - frontend rebuild with environment variables for build and runtime
  - minikube image load
  - helm upgrade
  - deployment restart
---
# Prompt

```
Still getting error 🔍 AuthProvider checking existing session: Object
502-5aae0dc72d6dacc3.js:1 ❌ No existing session found
favicon.ico:1  Failed to load resource: the server responded with a status of 404 (Not Found)Understand this error
page-40a1040c28ea489c.js:1 🔐 LoginForm.handleSubmit() - initiating login process
502-5aae0dc72d6dacc3.js:1 🔐 authService.login() called with credentials: Object
localhost:8000/api/auth/login:1  Failed to load resource: net::ERR_CONNECTION_REFUSEDUnderstand this error
117-d0aa9486d6cf1a7a.js:1 ❌ Login error in authService: TypeError: Failed to fetch     at a.request (502-5aae0dc72d6dacc3.js:1:2468)
    at a.login (502-5aae0dc72d6dacc3.js:1:3466)
    at Object.login (502-5aae0dc72d6dacc3.js:1:4635)
    at h (page-40a1040c28ea489c.js:1:746)
    at Object.a_ (fd9d1056-f8a2d551cbb94c85.js:1:72144)
    at aR (fd9d1056-f8a2d551cbb94c85.js:1:72298)
    at fd9d1056-f8a2d551cbb94c85.js:1:139237
    at sF (fd9d1056-f8a2d551cbb94c85.js:1:139336)
    at sM (fd9d1056-f8a2d551cbb94c85.js:1:139750)
    at fd9d1056-f8a2d551cbb94c85.js:1:145893
window.console.error @ 117-d0aa9486d6cf1a7a.js:1Understand this error
page-40a1040c28ea489c.js:1 ✅ AuthService login result: Object
117-d0aa9486d6cf1a7a.js:1 ❌ Login failed at authService level: Failed to fetch
```

# Response

## Continued Issue Analysis

Despite previous fixes, the error continued to show that the frontend was still trying to connect to `localhost:8000/api/auth/login` instead of the internal Kubernetes service URL. This indicated that the environment variables were not properly available to the JavaScript bundle.

## Root Cause

The issue was that while the build-time environment variables were set in the Dockerfile, the runtime environment variables were not properly configured for Next.js applications running in containers. Next.js applications need both build-time and runtime environment variables properly configured for containerized deployments.

## Solution Applied

Updated the frontend Dockerfile to ensure environment variables are available both during the build process and at runtime:

```dockerfile
# Set environment variables for the build
ENV NEXT_PUBLIC_API_URL=http://backend-service:8000
ENV NEXT_PUBLIC_API_BASE_URL=http://backend-service:8000
ENV NEXT_PUBLIC_GEMINI_ENABLED=false

# ... build process ...

# Set environment variables for runtime as well
ENV NEXT_PUBLIC_API_URL=http://backend-service:8000
ENV NEXT_PUBLIC_API_BASE_URL=http://backend-service:8000
ENV NEXT_PUBLIC_GEMINI_ENABLED=false
```

## Actions Taken

1. **Updated the frontend Dockerfile** to include environment variables for both build and runtime
2. **Rebuilt the frontend Docker image** with the proper environment variables for both stages
3. **Loaded the updated image into minikube**
4. **Upgraded the frontend Helm deployment** with the new image
5. **Restarted the frontend deployment** to ensure it picked up the new image

## Result

The frontend application should now have the proper environment variables available both at build time and runtime, allowing it to correctly connect to the internal Kubernetes service URL (`http://backend-service:8000`) instead of the default localhost URL.