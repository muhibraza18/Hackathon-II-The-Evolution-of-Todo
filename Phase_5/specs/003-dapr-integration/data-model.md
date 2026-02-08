# Data Model: Dapr Integration for Todo AI Chatbot

## Dapr-Integrated Task Entity

### Extended Fields (via Dapr integration)
- **pubsub_topic** (derived): "task-events" - determines which topic events are published to
- **state_key** (derived): "task-{id}" - key used for state operations in Dapr state store
- **job_id** (derived): "reminder-{task_id}" - ID for scheduled reminder jobs
- **dapr_metadata** (computed): Metadata for Dapr operations (consistency, etc.)

### Original Task Fields (unchanged)
- **id** (int | None): Primary key identifier
- **user_id** (int): Foreign key reference to user
- **title** (str): Task title (min_length=1, max_length=200)
- **description** (str | None): Task description (max_length=1000)
- **completed** (bool): Completion status (default False)
- **created_at** (datetime): Creation timestamp
- **updated_at** (datetime): Last update timestamp
- **due_date** (datetime | None): Due date for the task (from Phase V Step 1)
- **priority** (str | None): Priority level (low/medium/high/urgent) (from Phase V Step 1)
- **tags** (str | None): JSON string of tags array (from Phase V Step 1)
- **recurring_config** (str | None): JSON string of recurring configuration (from Phase V Step 1)
- **next_occurrence_id** (str | None): Reference to next recurring occurrence (from Phase V Step 1)
- **parent_task_id** (str | None): Reference to parent task for recurring instances (from Phase V Step 1)
- **original_task_id** (str | None): Reference to original task in recurring series (from Phase V Step 1)

### Validation Rules (maintained from existing)
- title must be 1-200 characters
- description must be ≤1000 characters if provided
- due_date must be in future if set
- recurring interval must be positive if recurring is enabled
- priority must be one of allowed values ['low', 'medium', 'high', 'urgent']
- tags array length must be reasonable (e.g., max 10 tags)

## Dapr Component Entities

### DaprPubSubComponent
- **name** (str): Unique name for the component (e.g., "kafka-pubsub")
- **type** (str): Component type ("pubsub.kafka")
- **version** (str): Component version (e.g., "v1")
- **metadata** (dict): Configuration properties:
  - brokers: List of Kafka broker addresses
  - authRequired: Whether authentication is required
  - consumerGroup: Default consumer group
  - disableTls: Whether TLS is disabled
  - version: Kafka version

### DaprStateStoreComponent
- **name** (str): Unique name for the component (e.g., "postgresql-statestore")
- **type** (str): Component type ("state.postgresql")
- **version** (str): Component version (e.g., "v1")
- **metadata** (dict): Configuration properties:
  - connectionString: PostgreSQL connection string
  - actorStateStore: Whether this is used for actor state
  - keyPrefix: Prefix for state keys
  - tableName: Name of the table to store state

### DaprSecretStoreComponent
- **name** (str): Unique name for the component (e.g., "kubernetes-secrets")
- **type** (str): Component type ("secretstores.kubernetes")
- **version** (str): Component version (e.g., "v1")
- **metadata** (dict): Configuration properties:
  - namespace: Kubernetes namespace to look for secrets

### DaprJobComponent (Conceptual - as Dapr Jobs API may evolve)
- **name** (str): Unique name for the component (e.g., "reminder-jobs")
- **type** (str): Component type ("jobs.scheduler") - conceptual
- **version** (str): Component version
- **metadata** (dict): Configuration properties:
  - schedulerEndpoint: Endpoint for job scheduler
  - maxRetries: Maximum number of job execution retries

## State Key Patterns

### Task State Keys
- **Task Data**: `task:{task_id}` - Stores the full task object
- **Task Cache**: `task_cache:{user_id}:{task_id}` - Caches frequently accessed task data
- **Recurring Relations**: `recurrence:{parent_task_id}:children` - Tracks child tasks of recurring tasks

### Conversation State Keys
- **Active Conversations**: `conversation:active:{user_id}` - Tracks active conversations per user
- **Conversation History**: `conversation:history:{conversation_id}` - Stores conversation history

## Event Schema Adaptation for Dapr

### Dapr-Compatible Task Events
All existing event schemas remain the same but are published through Dapr:

#### TaskCreatedEvent (via Dapr pubsub)
```json
{
  "event_type": "task.created",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "datetime",
  "payload": {
    "title": "string",
    "description": "string",
    "due_date": "datetime | null",
    "priority": "string | null",
    "tags": "array | null",
    "recurring_config": "object | null",
    "status": "string"
  }
}
```

#### TaskReminderEvent (via Dapr pubsub)
```json
{
  "event_type": "task.reminder",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "datetime",
  "payload": {
    "title": "string",
    "due_date": "datetime",
    "priority": "string",
    "notification_method": "string"
  }
}
```

## Dapr Service Invocation Patterns

### Service-to-Service Communication
- **Frontend → Backend**: `invoke backend-app-id method /api/tasks`
- **Backend → Consumers**: `invoke recurring-consumer-app-id method /webhook/task-completed`
- **Consumer → Backend**: `invoke backend-app-id method /api/internal/callbacks`

## Relationships with Dapr Integration

### Task to Dapr Components
- Each Task can trigger publish operations to Dapr PubSub component
- Task state can be cached in Dapr State Store component
- Task reminders are scheduled via Dapr Jobs (conceptual) component
- Task operations may access secrets via Dapr Secret Store component

### Component Dependencies
- Dapr PubSub component depends on Kafka/Redpanda infrastructure
- Dapr State Store component depends on PostgreSQL database
- Dapr Secret Store component depends on Kubernetes secrets
- Dapr Jobs component depends on scheduling infrastructure

## Migration Path Considerations

### From Direct Infrastructure to Dapr
- **Direct Kafka → Dapr PubSub**: Replace aiokafka producers/consumers with Dapr HTTP API calls
- **Direct DB → Dapr State**: Replace SQLModel operations with Dapr state API calls
- **Direct Secrets → Dapr Secrets**: Replace environment variables with Dapr secrets API calls
- **Custom Scheduler → Dapr Jobs**: Replace custom reminder scheduler with Dapr Jobs API

### Backward Compatibility
- Existing Task model structure remains unchanged
- Dapr integration is added at the service/api layer
- Direct infrastructure paths remain as fallback during migration