# Dapr API Contracts: Dapr Integration for Todo AI Chatbot

## Overview

This document defines the API contracts for the Dapr-integrated Todo AI Chatbot. The contracts specify how the application communicates with Dapr building blocks using Dapr's HTTP API.

## Base Dapr API Endpoints

### Dapr Sidecar Information
```
GET http://localhost:3500/v1.0/metadata
Response:
{
  "id": "string",
  "actors": [],
  "components": [
    {
      "name": "string",
      "type": "string",
      "version": "string",
      "scopes": []
    }
  ],
  "subscriptions": [
    {
      "pubsubname": "string",
      "topic": "string",
      "route": "string"
    }
  ]
}
```

## Pub/Sub API Contracts

### Publish Event via Dapr
```
POST http://localhost:3500/v1.0/publish/{pubsub-component-name}/{topic-name}
Content-Type: application/json

Request Body:
{
  "event_type": "string",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "string",
  "payload": {
    // Event-specific data
  }
}

Response: 204 No Content
Errors: 400, 404, 500
```

### Subscribe to Events via Dapr
```
Endpoint: /dapr/subscribe
Method: GET
Response:
[
  {
    "pubsubname": "kafka-pubsub",
    "topic": "task-events",
    "route": "/webhooks/task-events"
  }
]

Webhook Callback:
POST /webhooks/task-events
Content-Type: application/json
{
  "event_type": "string",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "string",
  "payload": {
    // Event-specific data
  }
}
```

## State API Contracts

### Get State from Dapr
```
GET http://localhost:3500/v1.0/state/{state-store-name}/{key}
Response: mixed (stored value)
Headers:
- X-ETag: string (for concurrency control)
- X-ContentType: string (content type of stored value)

Errors: 404 (key not found), 500 (storage error)
```

### Save State via Dapr
```
POST http://localhost:3500/v1.0/state/{state-store-name}
Content-Type: application/json

Request Body:
[
  {
    "key": "string",
    "value": {},
    "etag": "string (optional)",
    "options": {
      "concurrency": "first-write" | "last-write",
      "consistency": "strong" | "eventual"
    }
  }
]

Response: 204 No Content
Errors: 500 (storage error)
```

### Bulk Get State from Dapr
```
POST http://localhost:3500/v1.0/state/{state-store-name}/bulk
Content-Type: application/json

Request Body:
{
  "keys": ["string"],
  "parallelism": 1
}

Response:
[
  {
    "key": "string",
    "data": "mixed",
    "etag": "string",
    "error": "string (if error occurred)"
  }
]
```

## Secrets API Contracts

### Get Secret from Dapr
```
GET http://localhost:3500/v1.0/secrets/{secret-store-name}/{key}?metadata.key1=value1&metadata.key2=value2
Response:
{
  "key": "value"
}

With Metadata:
GET http://localhost:3500/v1.0/secrets/{secret-store-name}/{key}?metadata.namespace=default
```

### Bulk Get Secrets from Dapr
```
GET http://localhost:3500/v1.0/secrets/{secret-store-name}/bulk
Response:
{
  "secret1": "value1",
  "secret2": "value2"
}
```

## Service Invocation Contracts

### Invoke Service via Dapr
```
POST http://localhost:3500/v1.0/invoke/{app-id}/method/{method-path}
Content-Type: application/json (or original content type)

Request Body: (any valid content)
{
  // Any request body
}

Response: (any valid response from target service)
{
  // Any response body from target service
}

Headers:
- Dapr-Forward-[Header]: Forward original headers
- X-Forwarded-Host: Original host
- X-Forwarded-For: Original client IP
```

## Dapr Component Configuration Contracts

### Kafka Pub/Sub Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: authRequired
    value: "false"
  - name: consumerGroup
    value: "todo-ai-chatbot-group"
  - name: disableTls
    value: "true"
  - name: version
    value: "2.8.0"
```

### PostgreSQL State Store Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://user:password@host:5432/database"
  - name: actorStateStore
    value: "true"
  - name: keyPrefix
    value: "dapr"
  - name: tableName
    value: "dapr_state_store"
```

### Kubernetes Secrets Store Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
  metadata:
  - name: namespace
    value: "default"
```

## Application-Specific Contracts

### Task Event Payload Schema (via Dapr Pub/Sub)
```json
{
  "event_type": "task.created|task.updated|task.completed|task.reminder|task.deleted",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "ISO 8601 datetime string",
  "correlation_id": "string (optional)",
  "payload": {
    // Based on event_type:
    // task.created: { title, description, due_date, priority, tags, recurring_config, status }
    // task.updated: { title, description, due_date, priority, tags, recurring_config, status }
    // task.completed: { title, due_date, priority, tags, next_occurrence_id }
    // task.reminder: { title, due_date, priority, notification_method }
    // task.deleted: { title }
  }
}
```

### State Key Patterns
- **Task State**: `task:{task_id}`
- **User Task List**: `user_tasks:{user_id}`
- **Conversation State**: `conversation:{conversation_id}`
- **Cache Keys**: `cache:{namespace}:{key}`

### Secret Keys Expected by Application
- **Database Connection**: `db-connection-string`
- **Kafka Brokers**: `kafka-brokers`
- **API Keys**: `openai-api-key`, `other-service-api-keys`

## Error Handling Contracts

### Dapr API Error Responses
```json
{
  "errorCode": "string (e.g., ERR_PUBSUB_EMPTY_MESSAGE)",
  "message": "string (detailed error message)"
}
```

### Common Error Codes
- `ERR_PUBSUB_EMPTY_MESSAGE`: Empty message published
- `ERR_PUBSUB_MALFORMED_REQUEST`: Invalid request format
- `ERR_STATE_GET`: Failed to retrieve state
- `ERR_STATE_SAVE`: Failed to save state
- `ERR_SECRET_GET`: Failed to retrieve secret
- `ERR_INVOKE_CALLBACK`: Error in service invocation callback

## Health and Monitoring Contracts

### Dapr Health Check
```
GET http://localhost:3500/v1.0/healthz
Response: 204 No Content (healthy) or 500 Internal Server Error (unhealthy)
```

### Dapr Metrics
- Metrics available at `http://localhost:3500/v1.0/metrics` (Prometheus format)
- Component-specific metrics prefixed with `dapr_`
- App-specific metrics prefixed with `app_`

## Security Considerations

- All Dapr API calls must originate from localhost (sidecar pattern)
- Use Dapr's built-in service invocation for inter-service communication with automatic mTLS
- Store sensitive data only through Dapr Secrets API
- Validate all data received from Dapr before processing
- Implement proper authentication and authorization checks in application endpoints that receive Dapr callbacks