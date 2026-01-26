---
id: 26
title: Fix frontend backend connection
stage: resolved
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 003-k8s-deployment
user: Claude Sonnet 4.5
command: sp.analyze
labels: ["connection", "frontend", "backend", "port-forward"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/Dockerfile
  - backend/app/database/connection.py
tests:
  - curl http://localhost:8000/health
---

## Prompt

NEW ERROR: net::ERR_CONNECTION_REFUSED - Frontend cannot connect to localhost:8000

This is different from CORS! The browser literally cannot reach localhost:8000.

TWO POSSIBLE CAUSES:

**Cause 1: kubectl port-forward is not running**
Check if port-forward is active:
In separate terminals, run:
kubectl port-forward service/backend-service 8000:8000
kubectl port-forward service/frontend-service 3000:3000
If these aren't running, the browser can't reach the services.

**Cause 2: Frontend image STILL has wrong URL baked in**
Verify what URL is actually in the built frontend:
```bash
kubectl exec -it <frontend-pod-name> -- cat .next/static/chunks/*.js | grep -o "http://[^\"]*8000" | head -5
```

Or locally:
```bash
docker run --rm todo-frontend:latest cat .next/static/chunks/*.js | grep -o "http://[^\"]*8000" | head -5
```
This will show if it's calling "localhost:8000" or "backend-service:8000".

## Response snapshot

Successfully resolved the connection issue:

1. **Started port-forwards**: Established port-forwards for both frontend and backend services
   - Backend: `kubectl port-forward service/backend-service 8000:8000`
   - Frontend: `kubectl port-forward service/frontend-service 3000:3000`

2. **Rebuilt frontend image** with correct API URL for local development:
   - Updated NEXT_PUBLIC_API_URL to "http://localhost:8000" for port-forward access
   - Loaded the new image into Minikube
   - Restarted the frontend pod with the updated image

3. **Verified backend connectivity**: Confirmed that the backend is accessible at localhost:8000 via health check

4. **Services status**:
   - Backend: Running and accessible at localhost:8000
   - Frontend: Running and accessible at localhost:3000
   - PostgreSQL: Running as database backend

The connection issue was resolved by ensuring proper port-forwarding and rebuilding the frontend with the correct API URL for local access.

## Outcome

- ✅ Impact: Fixed frontend-backend communication via port-forward
- 🧪 Tests: Verified backend health endpoint is accessible
- 📁 Files: Updated frontend Dockerfile build args
- 🔁 Next prompts: Ready for browser-based testing
- 🧠 Reflection: Static build-time variables require image rebuild for URL changes

## Evaluation notes (flywheel)

- Failure modes observed: Port-forwarding, static URL configuration
- Graders run and results (PASS/FAIL): PASS - Services accessible via localhost
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Browser-based chat functionality test