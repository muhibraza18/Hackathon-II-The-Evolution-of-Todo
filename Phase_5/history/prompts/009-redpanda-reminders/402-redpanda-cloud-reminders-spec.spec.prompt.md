---
id: 402
title: Redpanda Cloud Reminders Spec
stage: spec
date: 2025-02-07
surface: agent
model: claude-opus-4-6
feature: 009-redpanda-reminders
branch: 009-redpanda-reminders
user: Wajahat traders
command: /sp.specify
labels: ["phase-v","redpanda","dapr","reminders","event-driven"]
links:
  spec: specs/009-redpanda-reminders/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/009-redpanda-reminders/spec.md
  - specs/009-redpanda-reminders/checklists/requirements.md
tests:
  - No tests run (spec creation phase)

## Prompt

Phase V – Local Completion: Redpanda Cloud Integration + Real-Time Reminders (No Cloud Deployment)

Target audience: Hackathon judges evaluating full event-driven maturity, Dapr usage, real-time UI, and local readiness before cloud.  Focus:
- Replace in-memory Pub/Sub with Redpanda Cloud (Kafka-compatible)
- Add visible UI toast/notification when reminder due time arrives  - Make overdue badge update automatically (real-time via polling)
- Verify reminders trigger at exact time + UI reflects changes
- Confirm all Phase V local requirements fulfilled (no deployment yet)  Redpanda Cloud credentials:
- Bootstrap server URL: d63i6urt489913voun8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
- SASL Username: todo-phase5  - SASL Password: bflLeIafHKGKvshzwRwcIZqvudhMjG
- SASL Mechanism: SCRAM-SHA-256
- Security protocol: SASL_SSL Success criteria:
- Dapr Pub/Sub component updated & healthy (kafka-pubsub using Redpanda Cloud)
- Create task with due time + 3 mins → after 3 mins:  - Toast appears: "Reminder: [title] is due now!"
  - Overdue badge shows automatically (no reload)  - Task list refreshes every 30s (polling) → real-time changes
- Backend logs show event publish + reminder trigger
- Chat agent creates tasks with reminders - All advanced features visible & functional (recurring, due dates with time, priorities, tags, search/filter/sort)
- No regressions (fast load, instant checkbox, persistent session)  Constraints:
- Local Minikube deployment with helm charts and kubectlPrefer polling (every 30s) for real-time – no new WebSocket service
- Use react-hot-toast for UI notifications
- Use existing Helm charts & Dapr components - Timeline: Complete this before cloud sub-phase  Not building:
- Cloud deployment (AKS/GKE/OKE) – defer to next phase
- Advanced monitoring/logging stack (Prometheus/Grafana) – defer - CI/CD pipeline – defer
- Multi-region or high-availability – local only   Now:  update Dapr YAML → apply Redpanda Cloud → add toast UI → polling logic → testing  - Include verification commands (dapr components, logs, toast test)  All changes traceable to this spec.

## Response snapshot

Created feature specification for Phase V – Redpanda Cloud Integration + Real-Time Reminders with:
- Feature branch: 009-redpanda-reminders
- 5 prioritized user stories (P1-P3)
- 15 functional requirements
- 12 measurable success criteria
- 15 edge cases identified
- Complete out-of-scope items

Spec focuses on:
- Redpanda Cloud integration with Dapr Pub/Sub (SASL_SSL, SCRAM-SHA-256)
- Real-time reminder notifications via toast (react-hot-toast)
- 30-second polling for task list auto-refresh
- Chat agent natural language time parsing
- Advanced task features (recurring, priorities, tags, search/filter/sort)
- No regressions in performance (load time <2s, instant checkbox)

Quality checklist: All items PASSED ✅

## Outcome

- ✅ Impact: Complete specification created for Phase V local deployment with Redpanda Cloud and real-time reminders
- 🧪 Tests: No tests run (specification phase)
- 📁 Files: 2 files created (spec.md, requirements checklist)
- 🔁 Next prompts: /sp.plan (create implementation plan), /sp.tasks (generate actionable tasks)
- 🧠 Reflection: Specification is technology-agnostic and focused on user outcomes. Redpanda Cloud credentials must be secured during implementation.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script had parameter error but branch creation succeeded; worked around by creating spec directory manually
- Graders run and results (PASS/FAIL): All quality checklist items PASSED
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None - spec is complete
