---
id: 51
title: "Kafka PubSub Foundation Plan"
stage: "plan"
date_iso: "2026-01-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "kafka-pubsub-foundation"
branch: "002-kafka-pubsub-foundation"
user: "Wajahat traders"
command: "/sp.plan"
labels: ["plan", "architecture", "event-driven", "kafka", "pubsub"]
links:
  spec: "specs/002-kafka-pubsub-foundation/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/002-kafka-pubsub-foundation/plan.md"
  - "specs/002-kafka-pubsub-foundation/research.md"
  - "specs/002-kafka-pubsub-foundation/data-model.md"
  - "specs/002-kafka-pubsub-foundation/quickstart.md"
  - "specs/002-kafka-pubsub-foundation/contracts/event-contracts.md"
tests_yaml: []
---

# Kafka PubSub Foundation Plan

## Prompt Text
```
Phase V – Sub-phase 2: Event-Driven Foundation (Kafka / PubSub) for Todo AI Chatbot

Create:
- High-level event-driven architecture sketch (text or mermaid diagram)
- Kafka/Redpanda topic structure and event schema definitions (JSON examples)
- Producer wrapper architecture (abstraction layer for future Dapr swap)
- Consumer service skeleton structure (recurring, notification, audit)
- Deployment & bootstrap strategy for local Kafka (Strimzi or Redpanda Docker)
- Quality validation checklist (publish/consume tests, log verification)  Decisions needing documentation:
- Kafka implementation choice (Strimzi operator vs Redpanda Docker vs Redpanda Cloud)
  - Options: Strimzi (K8s-native), Redpanda Docker (single binary), Redpanda Cloud (managed)
  - Tradeoffs: learning value vs setup speed vs future cloud migration
- Event schema format (plain JSON vs Avro with schema registry)
  - Tradeoffs: simplicity vs type safety & evolution
- Producer library (aiokafka direct vs Dapr-ready HTTP wrapper) - Tradeoffs: performance vs portability to Dapr in next sub-phase
- Consumer deployment model (separate Deployment per consumer vs single multi-consumer pod)
  - Tradeoffs: isolation vs resource efficiency
- Topic partitioning & replication (single partition vs multiple)
  - Tradeoffs: scalability vs simplicity in local Minikube
- Error handling & retry policy (dead-letter queue vs simple retry)
  - Tradeoffs: reliability vs complexity  Testing strategy:
- Unit tests for producer wrapper (mock publish success/failure)
- Integration tests for consumer logic (mock consume → assert next task created)
- Manual verification:
  - Create task → see task-created event in logs
  - Complete recurring task → see next instance created by consumer
  - Set due date → see reminder event published
  - Check Kafka consumer group status (offset committed)
- Acceptance criteria from spec fully validated (topics exist, events published/consumed, no direct Kafka in app code)
- Smoke test: restart Kafka pod → consumers reconnect & resume  Technical details:
- Use existing Phase V Step 1 backend as base
- Prefer Strimzi operator for Kafka on Minikube (kubectl apply install)
- Topics: task-events (CRUD), reminders (due date triggers), task-updates (optional real-time)
- Event schema: JSON with event_type, task_id, user_id, timestamp, payload object
- Producer: async wrapper function publish_event(topic, payload)
- Consumers: separate FastAPI services (or background tasks) consuming via aiokafka
- Organize implementation by layers:
  1. Kafka/Redpanda deployment & topic creation
  2. Event schema design & documentation
  3. Producer wrapper in backend
  4. Consumer services (recurring, notification, audit)
  5. Integration & testing
  6. Documentation & README updates
```

## Response Text
Created a comprehensive implementation plan for the Event-Driven Foundation (Kafka/PubSub) including research decisions, data models, architecture contracts, and quickstart guide. The plan covers all aspects of implementing event-driven architecture with Kafka topics, event schemas, producer/consumer services, and abstraction layers for future Dapr integration.

## Outcome
Successfully created the implementation plan with detailed technical context, architectural decisions, data models, event contracts, and implementation strategy for the event-driven foundation with Kafka integration.

## Evaluation
The implementation plan comprehensively addresses all requested functionality (Kafka topics, event schemas, producer/consumer services, abstraction layer) with detailed technical specifications and preparation for future Dapr integration. All architectural decisions were documented with rationale and alternatives considered.