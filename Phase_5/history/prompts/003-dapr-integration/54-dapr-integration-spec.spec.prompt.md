---
id: 54
title: "Dapr Integration Spec"
stage: "spec"
date_iso: "2026-01-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "dapr-integration"
branch: "003-dapr-integration"
user: "Wajahat traders"
command: "/sp.specify"
labels: ["spec", "dapr", "integration", "microservices", "abstraction"]
links:
  spec: "specs/003-dapr-integration/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/003-dapr-integration/spec.md"
  - "specs/003-dapr-integration/checklists/requirements.md"
tests_yaml: []
---

# Dapr Integration Spec

## Prompt Text
```
Phase V – Sub-phase 3: Dapr Integration for Todo AI Chatbot

Target audience: Hackathon judges evaluating portability, microservices best practices, abstraction of infrastructure, and event-driven maturity

Focus:
- Fully integrate Dapr as sidecar for all services (backend, recurring task consumer, notification consumer, etc.)
- Use Dapr building blocks to abstract Kafka Pub/Sub, PostgreSQL state, scheduled jobs (reminders), secrets, and service invocation
- Replace direct Kafka/DB calls from Step 2 with Dapr HTTP/gRPC APIs
- Enable Dapr Jobs API for exact-time reminder triggers (no polling)
- Ensure app code remains clean and vendor-agnostic (swap Kafka → RabbitMQ via YAML only)  Success criteria:
- Dapr sidecars injected into all relevant pods via Helm annotations
- Dapr Pub/Sub component configured for Kafka/Redpanda (kafka-pubsub)
- Publish/subscribe fully working via Dapr API (no kafka-python/aiokafka in code)
- Dapr state store (state.postgresql) used for conversation/task cache
- Dapr Jobs API schedules reminders at exact due time + triggers callback
- Dapr secrets store (kubernetes-secrets) loads API keys/DB creds securely  - Service invocation used for frontend → backend calls (with retries/mTLS)
- No regressions in Step 1 (advanced features) or Step 2 (event publishing/consuming)
- Dapr components deployed via YAML (kubectl apply) or Helm
- Local Minikube verification: dapr init -k + app runs with sidecars
- All changes traceable to this spec (@specs/dapr/dapr-integration.md)  Constraints:
- Use Dapr CLI + Kubernetes mode (dapr init -k)
- Prefer Dapr HTTP API over gRPC for simplicity
- No direct infrastructure libraries in app code (kafka-python, psycopg2, etc.)
- Keep existing Phase V Step 1 & 2 code as base – refactor minimally
- Secrets must use Kubernetes Secret or Dapr secret store – no env vars
- Dapr Jobs API for reminders (not cron bindings)
- Timeline: Complete this sub-phase before moving to local/cloud deployment  Not building:
- Dapr mTLS between services (use if stretch goal)
- Advanced Dapr features (actors, workflows, output bindings)
- Custom Dapr middleware or plugins
- Production-grade observability (tracing/metrics) – defer to later
- Multi-tenancy or RBAC in Dapr
- Swap to non-Kafka Pub/Sub (e.g., Redis, RabbitMQ) – Kafka only for now
- Cloud-specific Dapr config (defer to cloud sub-phase)
```

## Response Text
Created comprehensive specification for Dapr Integration for Todo AI Chatbot, including user stories for Dapr sidecar integration, Pub/Sub abstraction, state store integration, Jobs API for reminders, secrets management, and service invocation. The spec includes functional requirements, success criteria, and maintains backward compatibility with existing features.

## Outcome
Successfully created the Dapr integration specification with detailed user scenarios, functional requirements, and success criteria focused on infrastructure abstraction and vendor-agnostic design.

## Evaluation
The specification comprehensively addresses all requirements from the prompt with clear acceptance criteria and measurable outcomes. The spec maintains focus on user value while avoiding implementation details, making it suitable for the next phase of the spec-driven development process.