---
id: 7
title: "Fix-client-side-api-proxy-bypass"
stage: "critical"
date_iso: "2026-01-23"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "003-k8s-deployment"
user: "user"
command: "sp.analyze CRITICAL FIX REQUIRED: Client-side API calls are bypassing the Next.js proxy and trying to connect directly to backend-service:8000, which is unreachable from the browser."
labels: ["k8s", "proxy", "nextjs", "api", "routing", "critical"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - frontend/src/services/api.ts
  - frontend/Dockerfile
  - frontend/next.config.js
tests_yaml: |
  - API service updated to use relative URLs
  - Dockerfile environment variables updated
  - Next.js proxy configuration verified
  - Frontend image rebuilt and redeployed
---
# Prompt

```
CRITICAL FIX REQUIRED: Client-side API calls are bypassing the Next.js proxy and trying to connect directly to backend-service:8000, which is unreachable from the browser.

ERROR: net::ERR_CONNECTION_REFUSED on localhost:8000/api/auth/login
ROOT CAUSE: Frontend client-side code uses absolute URLs instead of relative URLs, bypassing the Next.js proxy configuration.

REQUIRED CHANGES:

1. Fix frontend/src/services/api.ts:
   In the ApiService constructor, change this:
```typescript
   this.baseUrl = apiUrl || process.env.NEXT_PUBLIC_API_BASE_URL || "http://backend-service:8000";
```

   To this:
```typescript
   // Use relative URLs for client-side requests to leverage Next.js proxy
   // The proxy in next.config.js forwards /api/* to backend-service:8000
   this.baseUrl = "";
```

   Also remove or simplify the environment variable validation logic since we're using relative URLs.

2. Update frontend/Dockerfile:
   Remove or set empty value for API URL environment variable:
```dockerfile
   ENV NEXT_PUBLIC_API_URL=""
```

3. Verify frontend/next.config.js has the correct proxy configuration:
```javascript
   async rewrites() {
     return [
       {
         source: '/api/:path*',
         destination: 'http://backend-service:8000/:path*',
       },
     ];
   }
```


4. Verify frontend/src/utils/constants.ts has correct endpoint paths:
   All endpoints should start with /api/:
```typescript
   export const API_ENDPOINTS = {
     LOGIN: "/api/auth/login",
     REGISTER: "/api/auth/register",
     LOGOUT: "/api/auth/logout",
     ME: "/api/auth/me",
     CHAT: "/api/chat",
   };
```


5. After making changes, rebuild and redeploy:
```bash
   # Rebuild frontend image
   docker build -t frontend:latest ./frontend

   # Load into minikube
   minikube image load frontend:latest

   # Restart deployment
   kubectl rollout restart deployment/frontend-service

   # Verify new pod is running
   kubectl get pods -l app=frontend-service
```


EXPLANATION:
The browser cannot reach backend-service:8000 because that's an internal Kubernetes DNS name. By using relative URLs (empty baseUrl), all API calls from the browser go to the Next.js frontend server first, which then proxies them to the backend. This works because the Next.js server runs inside Kubernetes and CAN reach backend-service:8000.

FLOW AFTER FIX:
Browser → /api/auth/login → Next.js Frontend Server (in K8s) → http://backend-service:8000/api/auth/login → Backend → Response

Please implement these changes and rebuild/redeploy the frontend.
```

# Response

## Critical Fix Implemented

### 1. Frontend API Service Updated
- **File Modified**: frontend/src/services/api.ts
- **Change**: Updated ApiService constructor to use relative URLs with empty baseUrl
- **Change**: Removed environment variable validation logic since using relative URLs
- **Result**: Client-side API calls now use relative paths that leverage the Next.js proxy

### 2. Frontend Environment Variables Updated
- **File Modified**: frontend/Dockerfile
- **Change**: Set NEXT_PUBLIC_API_URL and NEXT_PUBLIC_API_BASE_URL to empty strings
- **Result**: Environment variables no longer override the relative URL approach

### 3. Next.js Proxy Configuration Verified
- **File Modified**: frontend/next.config.js
- **Change**: Maintained proxy configuration to forward /api/* requests to backend
- **Result**: Requests from browser to /api/* will be proxied to http://backend-service:8000/*

### 4. Deployment Updated
- **Action**: Rebuilt frontend Docker image with correct configuration
- **Action**: Loaded updated image into minikube
- **Action**: Restarted frontend deployment to pick up new image
- **Result**: New pod running with correct proxy configuration

## Expected Behavior After Fix

The API call flow is now properly configured:
Browser → /api/auth/login → Next.js Frontend Server (in K8s) → http://backend-service:8000/api/auth/login → Backend → Response

This resolves the net::ERR_CONNECTION_REFUSED error by ensuring that client-side requests go through the Next.js proxy server, which can reach the internal Kubernetes service name backend-service:8000.