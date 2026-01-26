---
id: 002
title: "Plan Auth Integration"
stage: "plan"
date: "2026-01-14"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "auth-integration"
branch: "001-auth-integration"
user: "MuhibRaza"
command: "sp.plan"
labels: ["auth", "authentication", "better-auth", "session-management", "security", "architecture"]
links:
  spec: "specs/001-auth-integration/spec.md"
  plan: "specs/001-auth-integration/plan.md"
  research: "specs/001-auth-integration/research.md"
  data-model: "specs/001-auth-integration/data-model.md"
  contracts: "specs/001-auth-integration/contracts/auth-api.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-auth-integration/plan.md"
  - "specs/001-auth-integration/research.md"
  - "specs/001-auth-integration/data-model.md"
  - "specs/001-auth-integration/quickstart.md"
  - "specs/001-auth-integration/contracts/auth-api.md"
  - "specs/001-auth-integration/checklists/requirements.md"
tests:
  - "Architecture decision validation"
  - "Data model verification"
  - "API contract specification"
---

## Prompt

sp.plan

Create:
- Better Auth integration architecture diagram (FastAPI → Better Auth → Database)
- Authentication middleware flow diagram
- Database schema for User and Session models
- API endpoint specifications with request/response examples
- Session validation logic flowchart
- Security checklist for password handling and token management

Decisions needing documentation:
1. **Session Storage Mechanism**
   - Option A: Database-backed sessions (stateless, survives restarts, slower)
   - Option B: JWT tokens (stateless, no DB lookup, can't invalidate)
   - Option C: Hybrid (JWT + session table for revocation) (flexible, complex)
   - Tradeoff: Statelessness vs. revocation capability vs. performance
   - Recommendation: Align with Step 4 stateless architecture

2. **Token Delivery Method**
   - Option A: HTTP-only cookies (secure, automatic, CSRF risk)
   - Option B: Authorization header (explicit, flexible, frontend managed)
   - Option C: Both (redundant, most compatible, complex)
   - Tradeoff: Security vs. simplicity vs. frontend convenience

3. **Password Hashing Algorithm**
   - Option A: Bcrypt (proven, slower, configurable rounds)
   - Option B: Argon2 (modern, winner of password hashing competition, newer)
   - Option C: PBKDF2 (older standard, widely supported, slower)
   - Tradeoff: Security strength vs. performance vs. library support

4. **Session Expiration Strategy**
   - Option A: Fixed expiration (7 days, simple, forces re-login)
   - Option B: Sliding expiration (extends on activity, better UX, complex)
   - Option C: Short-lived + refresh tokens (secure, OAuth-like, over-engineered for Phase III)
   - Tradeoff: UX vs. security vs. implementation complexity

5. **Email Validation Level**
   - Option A: Format-only validation (regex, fast, allows fake emails)
   - Option B: Format + DNS check (verify domain exists, slower, more accurate)
   - Option C: Format + verification email (most secure, adds complexity)
   - Tradeoff: Registration friction vs. data quality vs. complexity
   - Recommendation: Format-only for Phase III, upgrade later

6. **Rate Limiting Implementation**
   - Option A: In-memory counter (simple, doesn't survive restart)
   - Option B: Database counter (persistent, slower)
   - Option C: Redis/external service (optimal, adds dependency)
   - Tradeoff: Simplicity vs. persistence vs. performance

## Response snapshot

Completed the implementation plan for the Better Auth integration feature, creating all required documentation:

1. **plan.md** - Comprehensive implementation plan with technical context, architecture decisions, and project structure
2. **research.md** - Research document addressing all 6 key architectural decisions with rationale and alternatives
3. **data-model.md** - Detailed data model for User, Session, and Authentication Token entities with validation rules
4. **quickstart.md** - Complete quickstart guide with setup instructions, API examples, and testing scenarios
5. **contracts/auth-api.md** - Detailed API contract specification for all authentication endpoints
6. **checklists/requirements.md** - Updated specification quality checklist marking all items as complete

The plan addresses all architectural decisions with clear rationale:
- Database-backed sessions for statelessness and revocation capability
- Authorization header for token delivery for explicit control
- Bcrypt for password hashing due to proven security track record
- Fixed expiration for simplicity and security boundaries
- Format-only email validation for Phase III requirements
- In-memory rate limiting for simplicity in initial phase

The implementation plan extends the existing backend architecture with a new auth module that includes routes, middleware, models, and utilities, while updating the chat endpoint to use authentication middleware instead of user_id in the URL path.

## Outcome

- ✅ Impact: Complete implementation plan for Better Auth integration with all architectural decisions documented
- 🧪 Tests: All API contracts and data models validated with examples
- 📁 Files: Created comprehensive planning documentation in proper directory structure
- 🔁 Next steps: Ready for task breakdown phase (`/sp.tasks`)
- 🧠 Reflection: Plan aligns with existing architecture and meets all security requirements