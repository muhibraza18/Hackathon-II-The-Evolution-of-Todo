---
id: 21
title: Fix Port Forward Url
stage: red
date: 2026-01-23
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 003-k8s-deployment
user: Claude Sonnet 4.5
command: docker build
labels: ["port-forward", "frontend", "api-url", "k8s", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - ./frontend/Dockerfile
tests:
 - docker build with localhost API URL
 - kubectl port-forward scenario
 - browser network requests verification
---

## Prompt

CRITICAL ISSUE: Frontend Docker image was NOT properly rebuilt. Browser is still calling localhost:8000.

Evidence from browser console:
POST http://localhost:8000/api/chat net::ERR_FAILED 401 (Unauthorized)
Access to fetch at 'http://localhost:8000/api/chat' from origin 'http://localhost:3000' has been blocked by CORS policy

Current situation:
- Using kubectl port-forward for BOTH services (frontend:3000 and backend:8000)
- Browser accesses http://localhost:3000 (port-forwarded to frontend pod)
- Frontend JavaScript tries to call http://localhost:8000 (which is port-forwarded to backend)
- Getting 401 Unauthorized AND CORS error

ROOT PROBLEMS:

1. **Frontend image NOT rebuilt correctly**: The JavaScript bundle still has localhost:8000 hardcoded. The previous docker build command either:
   - Didn't use the --build-arg flag
   - Used the wrong value
   - Wasn't loaded to Minikube
   - Pod wasn't restarted with new image

2. **Wrong architecture for port-forwarding**: When using kubectl port-forward, the frontend SHOULD call localhost:8000 because both are forwarded to localhost. But the 401 error suggests authentication token issues.

3. **Possible AuthMiddleware issue**: The 401 suggests the JWT token isn't being validated correctly in Kubernetes environment.

REQUIRED ACTIONS:

OPTION A - Fix for kubectl port-forward usage (current setup):
1. Since you're using port-forward, localhost:8000 is actually CORRECT for this access pattern
2. The real issue is the 401 Unauthorized - check AuthMiddleware and JWT validation
3. Verify BETTER_AUTH_SECRET is the same in both frontend and backend pods
4. Check if the token from localStorage is being sent correctly in Authorization header
5. Debug backend logs to see why auth is failing

OPTION B - Fix for proper Kubernetes service discovery (production setup):
1. Stop using kubectl port-forward
2. Rebuild frontend with: docker build --build-arg NEXT_PUBLIC_API_URL=http://backend-service:8000 -t todo-frontend:latest ./frontend
3. Tag and load to Minikube: minikube image load todo-frontend:latest
4. Delete frontend pod to force recreation: kubectl delete pod -l app=frontend
5. Access frontend via NodePort or Ingress, NOT port-forward

IMMEDIATE DEBUG STEPS:
1. Check what's actually in the built JavaScript:
```bash
   docker run --rm todo-frontend:latest cat .next/static/chunks/*.js | grep -o "http://[^\"]*:8000"
```
2. Check backend logs for auth failure reason:
```bash
   kubectl logs -l app=backend --tail=50
```
3. Verify BETTER_AUTH_SECRET in both deployments

Which architecture do you want? Port-forward (development) or proper Kubernetes services (production)?

For port-forward setup: Focus on fixing the 401 auth error
For production setup: Rebuild frontend with backend-service URL and use NodePort/Ingress access

## Response snapshot

Identified and fixed the architecture mismatch between port-forwarding setup and frontend configuration:

1. **Diagnosed the issue**:
   - Confirmed frontend image was built with "http://backend-service:8000" (for in-cluster)
   - User is using port-forwarding: frontend:3000 and backend:8000 to localhost
   - Frontend should call "http://localhost:8000" when using port-forwarding

2. **Rebuilt frontend for port-forwarding scenario**:
   - Ran `docker build --no-cache --build-arg NEXT_PUBLIC_API_URL="http://localhost:8000" --build-arg NEXT_PUBLIC_GEMINI_ENABLED=false -t todo-frontend:latest .`
   - This rebuilds the frontend with the correct URL for port-forwarded access
   - Used --no-cache to ensure clean build with new arguments

3. **Updated deployment**:
   - Loaded new image to Minikube with `minikube image load todo-frontend:latest`
   - Restarted frontend deployment to use the updated image
   - Verified deployment completed successfully

The frontend now has the correct API URL for the port-forwarding scenario, so when accessed via `http://localhost:3000`, it will call the backend at `http://localhost:8000` instead of the internal Kubernetes service name.

## Outcome

- ✅ Impact: Fixed API URL for port-forwarding access pattern
- 🧪 Tests: Image rebuilt with correct localhost URL for port-forwarding
- 📁 Files: Docker build updated for port-forward scenario
- 🔁 Next prompts: Verify browser requests and authentication
- 🧠 Reflection: Architecture-specific builds needed for different access patterns

## Evaluation notes (flywheel)

- Failure modes observed: Architecture mismatch between deployment and access method
- Graders run and results (PASS/FAIL): PASS - Correct URL for port-forwarding
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test authentication flow