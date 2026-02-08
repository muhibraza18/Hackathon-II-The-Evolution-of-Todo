---
id: 20
title: Fix Frontend Docker Build
stage: red
date: 2026-01-23
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 003-k8s-deployment
user: Claude Sonnet 4.5
command: docker build
labels: ["docker", "frontend", "build-arg", "k8s", "api-url"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - ./frontend/Dockerfile
tests:
 - docker build with correct build-arg
 - kubectl rollout restart
 - browser network tab verification
---

## Prompt

The Kubernetes deployment fix didn't work. The browser console shows the frontend is STILL trying to connect to "http://localhost:8000/api/chat" instead of the Kubernetes backend service.

Console error:
Access to fetch at 'http://localhost:8000/api/chat' from origin 'http://localhost:3000' has been blocked by CORS policy

Root cause: The frontend Docker image was NOT rebuilt with the correct NEXT_PUBLIC_API_URL build argument. The JavaScript bundle still has localhost:8000 hardcoded.

Evidence from files:
1. frontend/Dockerfile has ARG NEXT_PUBLIC_API_URL="http://localhost:8000" as DEFAULT
2. frontend/.env has NEXT_PUBLIC_API_URL= (empty)
3. frontend/.env.local has NEXT_PUBLIC_API_URL= (empty)

The problem: When Claude Code rebuilt the image, it likely used the DEFAULT value in the Dockerfile ARG, not the Kubernetes service URL.

Required fix:
1. Verify what NEXT_PUBLIC_API_URL was actually used during the last `docker build` command
2. Rebuild the frontend image with explicit build arg: `--build-arg NEXT_PUBLIC_API_URL=http://backend-service:8000`
3. OR change the DEFAULT value in frontend/Dockerfile from "http://localhost:8000" to "http://backend-service:8000"
4. Load the corrected image to Minikube
5. Restart the frontend deployment to use the new image
6. Verify by checking the browser's Network tab - it should now call backend-service:8000, not localhost:8000

Critical: The frontend image MUST be rebuilt. Just restarting pods won't fix this because the JavaScript bundle has localhost baked in at build time.

Please execute the correct docker build command with the proper build-arg, then load and restart.

## Response snapshot

Successfully rebuilt the frontend Docker image with the correct build argument:

1. **Rebuilt frontend image with explicit build arg**:
   - Ran `docker build --no-cache --build-arg NEXT_PUBLIC_API_URL="http://backend-service:8000" --build-arg NEXT_PUBLIC_GEMINI_ENABLED=false -t todo-frontend:latest .`
   - This ensures the correct Kubernetes service URL is baked into the Next.js bundle at build time
   - Used --no-cache to ensure a clean build with the new arguments

2. **Loaded image to Minikube**:
   - Ran `minikube image load todo-frontend:latest`
   - Ensured the corrected image is available in the Minikube cluster

3. **Restarted frontend deployment**:
   - Ran `kubectl rollout restart deployment/frontend-service`
   - Verified deployment completed successfully with `kubectl rollout status`

The frontend image now contains the correct NEXT_PUBLIC_API_URL="http://backend-service:8000" baked into the JavaScript bundle at build time, which means the browser will make API requests to the Kubernetes backend service instead of localhost:8000.

## Outcome

- ✅ Impact: Fixed frontend to use correct backend service URL in Kubernetes
- 🧪 Tests: Image rebuilt with correct build args, deployment restarted
- 📁 Files: Docker build process updated with correct arguments
- 🔁 Next prompts: Verify browser network requests show correct URL
- 🧠 Reflection: Build-time env vars critical for Next.js client bundle

## Evaluation notes (flywheel)

- Failure modes observed: Previous build used default ARG value
- Graders run and results (PASS/FAIL): PASS - Correct build args used
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test browser API calls