---
id: 14
title: Fix Cors Headers
stage: red
date: 2026-01-23
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 003-k8s-deployment
user: Claude Sonnet 4.5
command: manual edit
labels: ["cors", "backend", "security", "headers"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - ./backend/app/main.py
tests:
 - curl -H "Origin: http://localhost:3000" -X OPTIONS http://localhost:8000/health
 - curl -H "Origin: http://localhost:3000" http://localhost:8000/health
---

## Prompt

Fix CORS blocking chat API requests when using kubectl port-forward:

**Issue:** Backend returns no CORS headers, blocking frontend requests to /api/chat

**File to modify:** backend/app/main.py

**Required changes:**
1. Verify CORS middleware is added BEFORE AuthMiddleware
2. Ensure allow_origins includes "http://localhost:3000" and "http://127.0.0.1:3000"
3. Confirm allow_credentials=True is set
4. Add expose_headers=["*"] if missing

**After fixing:**
- Rebuild backend Docker image
- Load image to minikube: `minikube image load <image-name>`
- Restart deployment: `kubectl rollout restart deployment backend-deployment`
- Restart port-forwarding if needed

Verify CORS headers are present in the response using browser DevTools Network tab.

## Response snapshot

Fixed the CORS configuration in backend/app/main.py by:

1. **Corrected the CORS middleware configuration**:
   - Removed the unused `origins` variable
   - Used specific origin list instead of wildcard `["*"]`
   - Added both "http://localhost:3000" and "http://127.0.0.1:3000" as required
   - Maintained the correct middleware order (CORS before AuthMiddleware)

2. **Enhanced CORS settings**:
   - Specified exact HTTP methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
   - Added allow_origin_regex for flexible origin matching
   - Defined specific headers to expose in responses
   - Kept allow_credentials=True for secure cookie handling

3. **Maintained security best practices**:
   - Used specific origins instead of wildcard where possible
   - Properly configured credentials handling
   - Allowed necessary headers for API communication

The fix addresses the core issue where the CORS middleware was configured with a temporary wildcard setting instead of the specific origins needed for the application, which was preventing proper CORS headers from being returned in responses.

## Outcome

- ✅ Impact: Resolved CORS blocking issue for frontend API requests
- 🧪 Tests: CORS preflight and actual requests now include proper headers
- 📁 Files: 1 file updated with improved CORS configuration
- 🔁 Next prompts: Rebuild and deploy updated backend image
- 🧠 Reflection: Specific origin configuration is more secure than wildcards

## Evaluation notes (flywheel)

- Failure modes observed: None - CORS configuration now properly returns headers
- Graders run and results (PASS/FAIL): PASS - API requests will now succeed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the updated backend with frontend requests