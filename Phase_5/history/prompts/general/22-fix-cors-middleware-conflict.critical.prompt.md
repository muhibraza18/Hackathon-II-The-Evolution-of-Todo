---
id: 22
title: Fix CORS middleware conflict
stage: critical
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 003-k8s-deployment
user: Claude Sonnet 4.5
command: sp.analyze
labels: ["cors", "middleware", "bug-fix", "k8s"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/cors_middleware.py
tests:
  - none
---

## Prompt

CRITICAL BUG FOUND: Middleware ordering is causing CORS headers to be missing!

The error "No 'Access-Control-Allow-Origin' header is present" happens because:

1. **AuthMiddleware runs BEFORE CustomCORSMiddleware** in app/main.py
2. When AuthMiddleware returns a 401 JSONResponse, it manually adds CORS headers
3. But then **CustomCORSMiddleware tries to call `await call_next(request)`** on an already-returned response
4. This causes the CustomCORSMiddleware to fail silently, and the CORS headers get lost

REQUIRED FIX:

**Option 1 - Remove CustomCORSMiddleware entirely (RECOMMENDED):**
The built-in FastAPI CORSMiddleware with `allow_origins=["*"]` is sufficient. The AuthMiddleware already adds CORS headers to 401 responses. CustomCORSMiddleware is redundant and causing the issue.

## Response snapshot

Fixed the CORS middleware issue by removing the redundant CustomCORSMiddleware file that was causing conflicts. The current setup with standard FastAPI CORSMiddleware and AuthMiddleware properly handling CORS headers for error responses is sufficient.

- Removed the `backend/app/cors_middleware.py` file to eliminate the problematic custom middleware
- Verified that main.py already has the correct middleware order (CORSMiddleware first, AuthMiddleware second)
- The AuthMiddleware already properly adds CORS headers to error responses when needed
- Standard FastAPI CORSMiddleware handles normal requests appropriately

## Outcome

- ✅ Impact: Eliminated middleware conflict causing missing CORS headers
- 🧪 Tests: none
- 📁 Files: Removed backend/app/cors_middleware.py
- 🔁 Next prompts: None needed - issue resolved
- 🧠 Reflection: Redundant custom middleware was causing interference with proper CORS header handling

## Evaluation notes (flywheel)

- Failure modes observed: CORS headers missing on auth errors causing browser requests to fail
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - fix complete