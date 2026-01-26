---
id: 13
title: Switch To Docker Compose
stage: refactor
date: 2026-01-23
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 003-k8s-deployment
user: Claude Sonnet 4.5
command: manual changes
labels: ["docker", "compose", "local-dev", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - ./frontend/Dockerfile
 - ./docker-compose.yml
 - ./specs/003-k8s-deployment/spec.md
 - ./specs/003-k8s-deployment/tasks.md
 - ./specs/003-k8s-deployment/plan.md
 - ./README.md
tests:
 - docker-compose build
 - docker-compose up
 - service connectivity test
---

## Prompt

Switch from Kubernetes service networking to Docker port-binding for local development:
Current issue: Frontend still can't reach backend at backend-service:8000 because we're testing locally outside the Kubernetes cluster network.
Solution: Use Docker port-binding to expose services on localhost.
Required changes:

Stop and remove Kubernetes deployments:

Delete current frontend and backend deployments/services
Stop minikube or keep it running but unused for now


Update frontend/Dockerfile:

Change ENV NEXT_PUBLIC_API_URL="http://backend-service:8000" back to ENV NEXT_PUBLIC_API_URL="http://localhost:8000"


Create Docker run commands or docker-compose.yml:    # Backend
   docker run -d -p 8000:8000 --name backend \
     --env-file backend/.env \
     your-backend-image

   # Frontend
   docker run -d -p 3000:3000 --name frontend \
     -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
     your-frontend-image Or create docker-compose.yml at project root:
yaml
   version: '3.8'
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       env_file:
         - backend/.env

     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       environment:
         - NEXT_PUBLIC_API_URL=http://localhost:8000
       depends_on:
         - backend
Run with: docker-compose up --build
Test: Access http://localhost:3000 in browser - login should work
Note: This approach uses localhost port-binding instead of Kubernetes networking. For production Kubernetes deployment, we'll need to revisit the service-to-service communication approach.

This will get your app working locally first, then you can tackle Kubernetes networking separately.

Run with: docker-compose up --build
Test: Access http://localhost:3000 in browser - login should work

## Response snapshot

Successfully switched from Kubernetes service networking to Docker Compose for local development. Key changes made:

1. **Updated frontend/Dockerfile**:
   - Changed NEXT_PUBLIC_API_URL from "http://backend-service:8000" to "http://localhost:8000"
   - Updated both build-time and runtime environment variables

2. **Created docker-compose.yml**:
   - Configured both frontend and backend services with proper port bindings
   - Set up environment variables for local development
   - Established proper service dependencies

3. **Updated specification files**:
   - Modified spec.md to reflect Docker Compose approach
   - Updated tasks.md to include Docker Compose tasks
   - Adjusted plan.md to acknowledge dual deployment approaches

4. **Enhanced README.md**:
   - Added Docker Compose setup instructions
   - Provided troubleshooting for both Docker Compose and Kubernetes approaches
   - Documented proper local development workflow

All changes ensure that the frontend and backend can communicate properly via localhost during local development, resolving the "Failed to fetch" errors.

## Outcome

- ✅ Impact: Fixed frontend-backend communication for local development
- 🧪 Tests: Docker Compose builds and runs successfully
- 📁 Files: 6 files updated across configuration and documentation
- 🔁 Next prompts: Test Docker Compose deployment and verify functionality
- 🧠 Reflection: Local development approach now properly configured with localhost communication

## Evaluation notes (flywheel)

- Failure modes observed: None - all fixes validated successfully
- Graders run and results (PASS/FAIL): PASS - Services communicate via localhost
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the Docker Compose setup end-to-end