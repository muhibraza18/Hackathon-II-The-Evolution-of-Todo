---
id: "004"
title: "Add Legacy Auth Endpoints"
stage: "refactor"
date_iso: "2026-01-08"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "003-auth-jwt-integration"
branch: "003-auth-jwt-integration"
user: "Claude Sonnet 4.5"
command: "Add legacy authentication endpoints for frontend compatibility"
labels: ["authentication", "compatibility", "endpoints", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/auth_endpoint.py
tests_yaml: |
  - curl -X POST "http://localhost:8000/api/auth/sign-in/email" -H "Content-Type: application/json" -d "{\"email\":\"test2@example.com\",\"password\":\"password123\"}"
  - curl -X POST "http://localhost:8000/api/auth/sign-up/email" -H "Content-Type: application/json" -d "{\"email\":\"test3@example.com\",\"password\":\"password123\"}"
  - curl -X GET "http://localhost:8000/api/auth/get-session" -H "Authorization: Bearer <token>"
prompt_text: |
  PROBLEM: Authentication endpoints are returning 404 Not Found errors.

  Backend logs show:
  - POST /api/auth/sign-in/email HTTP/1.1" 404 Not Found (multiple times)
  - POST /api/auth/sign-up/email HTTP/1.1" 404 Not Found (multiple times)
  - GET /api/auth/get-session HTTP/1.1" 404 Not Found
  - GET /api/tasks HTTP/1.1" 401 Unauthorized
  - OPTIONS requests return 200 OK (CORS working)

  Frontend errors:
  - Login: "Invalid credentials or login failed"
  - Signup: "Signup failed. Please try again."

  My setup:
  - Backend: FastAPI on http://127.0.0.1:8000
  - Database: Neon PostgreSQL
  - Authentication: Better-Auth with JWT
  - Frontend: Next.js on localhost:3005

  Issues to fix:

  1. CRITICAL: All /api/auth/* endpoints return 404 - routes not properly registered
  2. The auth_router is not included in main.py or prefix is wrong
  3. Check if app.include_router(auth_router, prefix="/api/auth") is missing or incorrect
  4. Verify auth_endpoint.py has the correct route definitions
  5. The backend server is running but authentication routes don't exist
  6. Check if there's a path mismatch between frontend API calls and backend routes
  7. Ensure all authentication endpoints are properly defined:
     - POST /api/auth/sign-up/email
     - POST /api/auth/sign-in/email
     - GET /api/auth/get-session
  8. Fix the router registration in main.py

  Please check main.py and ensure the auth router is properly included with the correct prefix, and verify all authentication routes are correctly defined in auth_endpoint.py.
response_text: |
  ## Summary

  I have successfully fixed the 404 Not Found errors by adding legacy authentication endpoints that match the exact paths the frontend is calling.

  ### 🔧 **Legacy Endpoints Added**
  - **POST `/api/auth/sign-up/email`** - Legacy endpoint for signup compatibility
  - **POST `/api/auth/sign-in/email`** - Legacy endpoint for signin compatibility
  - **GET `/api/auth/get-session`** - Legacy endpoint for session compatibility

  ### 🔄 **Dual Endpoint Support**
  - **Standard endpoints** (Better Auth standard): `/api/auth/signup`, `/api/auth/signin`, `/api/auth/session`
  - **Legacy endpoints** (frontend compatibility): `/api/auth/sign-up/email`, `/api/auth/sign-in/email`, `/api/auth/get-session`

  ### ✅ **Testing Results**
  - ✅ Legacy sign-up: `POST /api/auth/sign-up/email` returns 200 OK
  - ✅ Legacy sign-in: `POST /api/auth/sign-in/email` returns 200 OK
  - ✅ Legacy session: `GET /api/auth/get-session` returns 200 OK
  - ✅ All endpoints reuse existing functionality (no code duplication)

  The 404 Not Found errors have been completely resolved. Both legacy frontend calls and modern Better Auth standard endpoints are now supported simultaneously.
outcome: "Successfully added legacy authentication endpoints to support frontend API calls. All previously 404 endpoints now return 200 OK with proper responses."
evaluation: "Both legacy and modern endpoint patterns now supported. Frontend should no longer encounter 404 errors when calling authentication endpoints."
---
