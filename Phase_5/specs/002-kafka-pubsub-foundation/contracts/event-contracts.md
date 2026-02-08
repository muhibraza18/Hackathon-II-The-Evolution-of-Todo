# Event Contracts: Event-Driven Foundation (Kafka/PubSub)

## Overview
This document defines the event contracts for the event-driven architecture using Kafka/Redpanda in the Todo AI Chatbot system. The contracts specify the structure, schema, and behavior of events published and consumed by different services.

## Event Schema Format
All events follow a standardized JSON schema with the following structure:

```json
{
  "event_type": "string",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "ISO 8601 datetime string",
  "payload": {
    // event-specific data
  }
}
```

### Common Fields
- **event_type**: The type of event (e.g., "task.created", "task.completed")
- **task_id**: The unique identifier of the task involved in the event
- **user_id**: The identifier of the user who triggered the event
- **timestamp**: The time when the event occurred in ISO 8601 format
- **payload**: Event-specific data payload

## Topic Definitions

### task-events Topic
**Purpose**: Contains all task lifecycle events including creation, updates, completion, and deletion.

**Event Types**:
1. **task.created**
   ```json
   {
     "event_type": "task.created",
     "task_id": "12345",
     "user_id": "user-67890",
     "timestamp": "2026-01-28T10:00:00.000Z",
     "payload": {
       "title": "Sample Task",
       "description": "A sample task description",
       "due_date": "2026-02-01T10:00:00.000Z",
       "priority": "medium",
       "tags": ["work", "important"],
       "recurring_config": {
         "type": "daily",
         "interval": 1
       },
       "status": "pending"
     }
   }
   ```

2. **task.updated**
   ```json
   {
     "event_type": "task.updated",
     "task_id": "12345",
     "user_id": "user-67890",
     "timestamp": "2026-01-28T11:00:00.000Z",
     "payload": {
       "title": "Updated Sample Task",
       "description": "An updated task description",
       "due_date": "2026-02-02T10:00:00.000Z",
       "priority": "high",
       "tags": ["work", "important", "urgent"],
       "recurring_config": {
         "type": "daily",
         "interval": 1
       },
       "status": "pending"
     }
   }
   ```

3. **task.completed**
   ```json
   {
     "event_type": "task.completed",
     "task_id": "12345",
     "user_id": "user-67890",
     "timestamp": "2026-01-28T12:00:00.000Z",
     "payload": {
       "title": "Sample Task",
       "due_date": "2026-02-01T10:00:00.000Z",
       "priority": "medium",
       "tags": ["work", "important"],
       "next_occurrence_id": "12346"
     }
   }
   ```

4. **task.deleted**
   ```json
   {
     "event_type": "task.deleted",
     "task_id": "12345",
     "user_id": "user-67890",
     "timestamp": "2026-01-28T13:00:00.000Z",
     "payload": {
       "title": "Sample Task"
     }
   }
   ```

### reminders Topic
**Purpose**: Contains reminder events for tasks with upcoming due dates.

**Event Types**:
1. **task.reminder**
   ```json
   {
     "event_type": "task.reminder",
     "task_id": "12345",
     "user_id": "user-67890",
     "timestamp": "2026-01-28T09:00:00.000Z",
     "payload": {
       "title": "Sample Task",
       "due_date": "2026-01-28T17:00:00.000Z",
       "priority": "high",
       "notification_method": "email"
     }
   }
   ```

### task-updates Topic
**Purpose**: Contains real-time task updates for potential future use cases.

**Event Types**:
1. **task.status_changed**
   ```json
   {
     "event_type": "task.status_changed",
     "task_id": "12345",
     "user_id": "user-67890",
     "timestamp": "2026-01-28T14:00:00.000Z",
     "payload": {
       "title": "Sample Task",
       "previous_status": "pending",
       "new_status": "in_progress"
     }
   }
   ```

## Producer Contract
Services publishing to Kafka must:
- Use the standardized event schema
- Include all required fields
- Validate event payloads before publishing
- Handle publishing errors gracefully
- Use async publishing to avoid blocking operations

## Consumer Contract
Services consuming from Kafka must:
- Acknowledge successful event processing
- Implement proper error handling
- Support graceful shutdown and restart
- Track consumer group offsets
- Log event processing for traceability

## Error Handling
- Failed event publishing should be retried with exponential backoff
- Failed event consumption should trigger dead-letter queue placement after retries
- All errors should be logged with sufficient context for debugging

## Security Considerations
- Event payloads should not contain sensitive information
- Access to Kafka topics should be properly authenticated and authorized
- Encryption should be used for data in transit