---
id: 403
title: Redpanda Reminders Implementation Plan
stage: plan
date: 2025-02-07
surface: agent
model: claude-opus-4-6
feature: 009-redpanda-reminders
branch: 009-redpanda-reminders
user: Wajahat traders
command: /sp.plan
labels: ["phase-v","redpanda","dapr","reminders","implementation-plan"]
links:
  spec: specs/009-redpanda-reminders/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/009-redpanda-reminders/plan.md
  - specs/009-redpanda-reminders/research.md
  - specs/009-redpanda-reminders/data-model.md
  - specs/009-redpanda-reminders/contracts/backend-api.yaml
  - specs/009-redpanda-reminders/quickstart.md
tests:
  - No tests run (planning phase)

## Prompt

Phase V – Local Completion: Redpanda Cloud + Real-Time Reminders & UI Polish (No Cloud Deployment Yet)

Create:  - Updated Dapr pub/sub component YAML using Redpanda Cloud credentials
- Frontend polling + toast notification logic for reminders - Verification checklist & demo commands
- Troubleshooting guide for common Redpanda connection issues  Decisions needing documentation:
- Polling interval (15s vs 30s vs 60s)
  - Tradeoffs: real-time feel vs API load  - Toast library (react-hot-toast vs custom)
  - Tradeoffs: ease vs styling control
- Fallback if Redpanda fails (in-memory vs error message)  - Tradeoffs: reliability vs strict compliance
- How to handle duplicate toasts (task ID tracking)
  - Tradeoffs: user experience vs code complexity  Testing strategy:
- Manual end-to-end:
 1. Create task with due time + 3 minutes via UI/chat  2. Wait 3 minutes
 3. Verify:
     - Toast appears automatically ("Reminder: [title] is due now!")  - Overdue badge shows on task card without reload
     - Notification-consumer logs show reminder processed  4. Check Redpanda Cloud dashboard → Topics → messages appear in task-events/reminders  - Performance:
  - Tasks page load <3s
  - Checkbox complete instant (optimistic UI)  - Polling refresh every 30s visible (no freeze)
- Acceptance criteria from docs fully validated:
  - Event-driven with real Kafka-compatible (Redpanda Cloud)  - Dapr Pub/Sub working
  - Reminders visible in UI (toast + overdue)
  - All advanced features demo-able locally  Technical details:
- Use existing Phase V code (frontend, backend, Helm charts)
- Redpanda Cloud credentials:  - Bootstrap: d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
  - Username: todo-phase5
  - Password: bflLeIafHKGKvshzwRwcIZqvudhMjG  - Mechanism: SCRAM-SHA-256
  - Protocol: SASL_SSL
- Organize implementation:  1. Generate & apply Redpanda Cloud Dapr component
  2. Remove in-memory Pub/Sub
  3. Add polling + toast logic in /tasks page  4. Optimize backend if polling slow
  5. Testing & verification
  6. Final README/demo updates

## Response snapshot

Created complete implementation plan with:

**Architecture Decision Records (4)**:
- ADR-001: Polling interval = 30 seconds (balanced real-time feel vs API load)
- ADR-002: Toast library = react-hot-toast (already installed)
- ADR-003: Redpanda failure = graceful degradation with in-memory fallback
- ADR-004: Duplicate toasts = session storage tracking with 5-min window

**Implementation Phases**:
- Phase 2a: Infrastructure Setup (Dapr component, Kubernetes secrets) - 30 min
- Phase 2b: Backend Services (reminders table, event publishing, scheduler) - 45 min
- Phase 2c: Frontend Features (polling, toasts, duplicate tracking) - 30 min
- Phase 2d: Testing & Verification (E2E, performance) - 30 min
- Phase 2e: Documentation (README, troubleshooting) - 15 min

**Artifacts Created**:
- plan.md: Full implementation plan with ADRs, phases, risk analysis
- research.md: Findings from 5 research tasks (all unknowns resolved)
- data-model.md: Complete schema with reminders table, event schemas, migrations
- contracts/backend-api.yaml: OpenAPI spec for new reminder endpoints
- quickstart.md: 15-minute setup guide with demo script

**Total Estimated Time**: 2.5 hours

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation
- 🧪 Tests: No tests (planning phase complete)
- 📁 Files: 5 planning artifacts created
- 🔁 Next prompts: /sp.tasks (generate actionable task list)
- 🧠 Reflection: All architectural decisions documented. Constitution check passed with 1 action item (create Kubernetes Secret for credentials).

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All constitution checks PASSED
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None - proceed to implementation

## Constitution Check Results

**Principles Compliance**: ✅ All PASS
- Spec-driven, AI-assisted tools, Dapr abstraction, reproducibility verified
- Security: ⚠️ ACTION - Must use Kubernetes Secret for credentials

**Standards Compliance**: ✅ All PASS
- Dapr Pub/Sub, no direct Kafka, Helm charts with Dapr, README with verification

**Gates**: ✅ All PASS (with documented action)
- No hardcoded secrets: Will create Secret in Phase 2a-1
- Dapr sidecar: Will enable in Phase 2a-3
- Local validation: All testing on Minikube
