---
id: 5
title: "Fix-frontend-backend-proxy-configuration"
stage: "red"
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "003-k8s-deployment"
user: "user"
command: "sp.analyze Still getting error with localhost:8000 API calls from browser"
labels: ["k8s", "nextjs", "proxy", "architecture", "debugging"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - frontend/next.config.js
  - frontend/Dockerfile
tests_yaml: |
  - next.config.js proxy rewrites
  - frontend rebuild with proxy configuration
  - minikube image load
  - helm upgrade
  - deployment restart
---
# Prompt

```
Still getting error from login check the docker or minikube logs that error coming thier when I I login from here why this was not working 🔍 AuthProvider checking existing session: Object
layout-7e88118f948fc7ba.js:1 ❌ No existing session found
page-40a1040c28ea489c.js:1 🔐 LoginForm.handleSubmit() - initiating login process
502-5aae0dc72d6dacc3.js:1 🔐 authService.login() called with credentials: Object
localhost:8000/api/auth/login:1  Failed to load resource: net::ERR_CONNECTION_REFUSEDUnderstand this error
117-d0aa9486d6cf1a7a.js:1 ❌ Login error in authService: TypeError: Failed to fetch
    at a.request (502-5aae0dc72d6dacc3.js:1:2468)
    at a.login (502-5aae0dc72d6dacc3.js:1:3466)     at Object.login (502-5aae0dc72d6dacc3.js:1:4635)
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

## Root Cause Analysis

The error analysis revealed an architectural issue with the Kubernetes deployment. The problem was that:

1. The frontend was accessed from outside the cluster via NodePort (browser)
2. The JavaScript code in the browser tried to call the backend using the internal Kubernetes service name `http://backend-service:8000`
3. This internal service name is not resolvable from outside the cluster (from the user's browser)
4. The code fell back to `localhost:8000` which is also unreachable from the user's browser
5. The backend service was already exposed as a NodePort but the frontend wasn't configured to use it properly

## Architectural Solution

Implemented a proxy configuration approach by:

1. **Updated next.config.js** to add rewrite rules that proxy `/api/*` requests to the backend service:
   ```javascript
   async rewrites() {
     return [
       {
         source: '/api/:path*',
         destination: 'http://backend-service:8000/:path*', // Proxy to backend
       },
     ]
   }
   ```

2. **Updated environment variables** in the Dockerfile to use relative paths:
   - Changed from `http://backend-service:8000` to `/api`
   - This allows the frontend server to proxy requests to the backend

## Actions Taken

1. **Modified frontend/next.config.js** to add proxy rewrites
2. **Updated frontend/Dockerfile** to set environment variables to use relative paths
3. **Rebuilt the frontend Docker image** with the new configuration
4. **Loaded the updated image into minikube**
5. **Upgraded the frontend Helm deployment** with the new image
6. **Restarted the frontend deployment** to pick up the changes

## Result

The frontend application should now properly proxy API requests to the backend service through the Next.js server, allowing the browser to access backend APIs via relative paths (`/api/auth/login`) which get internally proxied to `http://backend-service:8000` within the cluster.