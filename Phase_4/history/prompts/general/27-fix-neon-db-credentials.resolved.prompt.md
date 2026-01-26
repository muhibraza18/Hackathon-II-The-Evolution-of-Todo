---
id: 27
title: Fix Neon DB credentials
stage: resolved
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 003-k8s-deployment
user: Claude Sonnet 4.5
command: sp.analyze
labels: ["database", "credentials", "neon", "k8s"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - charts/backend/values.yaml
tests:
  - kubectl logs backend-service
---

## Prompt

CRITICAL: Kubernetes secret has wrong credentials! It's using in-cluster PostgreSQL instead of Neon.

Current secret decoded values:
- database-url: postgresql+asyncpg://postgres:postgrespassword@postgresql:5432/todo_chatbot (WRONG - in-cluster)
- openai-api-key: sk-fake-test-key (WRONG - fake key)
- auth-secret: test-secret (WRONG - test value)

Correct values from backend/.env:
- DATABASE_URL: postgresql://neondb_owner:npg_l3WKQFsvo7uH@ep-calm-frost-ahdmlrul-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
- OPENAI_API_KEY: AIzaSyBcu71TdcoamlUHmIjPSEG6FUWG2rnArhE
- BETTER_AUTH_SECRET: 2e7a66444e20fa4fbaf6e20bd06c94eca3ad1ae0aaca54c19f236786d9973328

REQUIRED FIX:

Update the Kubernetes secret with correct Neon DB credentials

## Response snapshot

Successfully resolved the critical database credential issue:

1. **Updated Helm values** to use Neon PostgreSQL database credentials instead of in-cluster PostgreSQL
   - Updated database configuration to point to Neon: ep-calm-frost-ahdmlrul-pooler.c-3.us-east-1.aws.neon.tech
   - Updated database URL with proper credentials for Neon database
   - Updated API keys and auth secrets to match environment values

2. **Reinstalled backend** with the correct Neon database configuration
   - Uninstalled the previous backend deployment
   - Installed new backend with Neon database credentials
   - Backend pod is now connecting to Neon database where user sessions exist

3. **Verified connection** to Neon database:
   - Backend logs show: "Database URL in settings: postgresql+asyncpg://neondb_owner:npg_l3WKQFsvo7uH@ep-calm-frost-ahdmlrul-pooler.c-3.us-east-1.aws.neon.tech:5432/neondb?sslmode=require"
   - Database tables created successfully
   - Health endpoint working properly

The backend is now properly connected to the Neon PostgreSQL database where the user's sessions exist, resolving the authentication issue.

## Outcome

- ✅ Impact: Fixed database connection to Neon where sessions exist
- 🧪 Tests: Verified backend connects to Neon database successfully
- 📁 Files: Updated charts/backend/values.yaml
- 🔁 Next prompts: Ready for user authentication testing
- 🧠 Reflection: Correct database credentials are essential for session access

## Evaluation notes (flywheel)

- Failure modes observed: Wrong database credentials, session access issues
- Graders run and results (PASS/FAIL): PASS - Connects to correct database
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): User authentication test