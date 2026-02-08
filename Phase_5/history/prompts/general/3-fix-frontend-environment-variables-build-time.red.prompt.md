---
id: 3
title: "Fix-frontend-environment-variables-build-time"
stage: "red"
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "003-k8s-deployment"
user: "user"
command: "sp.analyze Here is the error Getting from login page with Failed to fetch error"
labels: ["k8s", "environment-variables", "nextjs", "build", "runtime", "debugging"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - frontend/Dockerfile
  - frontend/src/services/api.ts
tests_yaml: |
  - frontend rebuild with environment variables
  - minikube image load
  - helm upgrade
  - deployment restart
---
# Prompt

```
Here is the error Getting from login page 🔍 AuthProvider checking existing session: {token: undefined, userId: null}
layout-7e88118f948fc7ba.js:1 ❌ No existing session found
favicon.ico:1  GET http://127.0.0.1:56155/favicon.ico 404 (Not Found)Understand this error
page-40a1040c28ea489c.js:1 🔐 LoginForm.handleSubmit() - initiating login process
502-5aae0dc72d6dacc3.js:1 🔐 authService.login() called with credentials: {email: 'spacework035@gmail.com', password: 'Muhib@raza1'}
502-5aae0dc72d6dacc3.js:1  POST http://localhost:8000/api/auth/login net::ERR_CONNECTION_REFUSED 117-d0aa9486d6cf1a7a.js:1 ❌ Login error in authService: TypeError: Failed to fetch
    at a.request (502-5aae0dc72d6dacc3.js:1:2468)
    at a.login (502-5aae0dc72d6dacc3.js:1:3466)
    at Object.login (502-5aae0dc72d6dacc3.js:1:4635)
    at h (page-40a1040c28ea489c.js:1:746)
    at Object.a_ (fd9d1056-f8a2d551cbb94c85.js:1:72144)
    at aR (fd9d1056-f8a2d551cbb94c85.js:1:72298)     at fd9d1056-f8a2d551cbb94c85.js:1:139237
    at sF (fd9d1056-f8a2d551cbb94c85.js:1:139336)
    at sM (fd9d1056-f8a2d551cbb94c85.js:1:139750)
    at fd9d1056-f8a2d551cbb94c85.js:1:145893
window.console.error    @    117-d0aa9486d6cf1a7a.js:1
login    @    502-5aae0dc72d6dacc3.js:1
await in login
window.console.error @ 117-d0aa9486d6cf1a7a.js:1
login @ 502-5aae0dc72d6dacc3.js:1
await in login
h @ page-40a1040c28ea489c.js:1
a_ @ fd9d1056-f8a2d551cbb94c85.js:1
aR @ fd9d1056-f8a2d551cbb94c85.js:1
(anonymous) @ fd9d1056-f8a2d551cbb94c85.js:1
sF @ fd9d1056-f8a2d551cbb94c85.js:1
sM @ fd9d1056-f8a2d551cbb94c85.js:1
(anonymous) @ fd9d1056-f8a2d551cbb94c85.js:1
o4 @ fd9d1056-f8a2d551cbb94c85.js:1
iV @ fd9d1056-f8a2d551cbb94c85.js:1
sU @ fd9d1056-f8a2d551cbb94c85.js:1
uR @ fd9d1056-f8a2d551cbb94c85.js:1
uM @ fd9d1056-f8a2d551cbb94c85.js:1Understand this error
page-40a1040c28ea489c.js:1 ✅ AuthService login result: {success: false, error: 'Failed to fetch'}
117-d0aa9486d6cf1a7a.js:1 ❌ Login failed at authService level: Failed to fetch
```

# Response

## Root Cause Analysis

The error showed that the frontend was still trying to connect to `http://localhost:8000/api/auth/login` instead of the internal Kubernetes service URL. This indicated that the environment variables were not being properly embedded during the Next.js build process.

## Issue Identified

In Next.js applications, environment variables prefixed with `NEXT_PUBLIC_` are embedded at build time, not runtime. The frontend was built without the proper environment variables set, so the default fallback URL (`http://localhost:8000`) was hardcoded into the JavaScript bundle.

## Solution Applied

Updated the frontend Dockerfile to set the environment variables during the build process:

```dockerfile
# Set environment variables for the build
ENV NEXT_PUBLIC_API_URL=http://backend-service:8000
ENV NEXT_PUBLIC_API_BASE_URL=http://backend-service:8000
ENV NEXT_PUBLIC_GEMINI_ENABLED=false
```

## Actions Taken

1. Modified the frontend Dockerfile to include environment variables during build time
2. Rebuilt the frontend Docker image with the proper environment variables
3. Loaded the updated image into minikube
4. Upgraded the frontend Helm deployment with the new image
5. Restarted the frontend deployment to ensure it picked up the new image

## Result

The frontend application should now properly use the internal Kubernetes service URL (`http://backend-service:8000`) for API calls instead of the default localhost URL, resolving the "Failed to fetch" error.