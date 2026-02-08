# Data Model: Event-Driven Foundation (Kafka/PubSub)

## Event Schema Definitions

### Base Event Structure
- **event_type** (str): Type of event (task.created, task.updated, etc.)
- **task_id** (str): Unique identifier for the task
- **user_id** (str): Identifier for the user who triggered the event
- **timestamp** (datetime): When the event was created
- **payload** (dict): Additional data specific to the event type

### Event Types

#### Task Created Event
- **event_type**: "task.created"
- **task_id**: Unique task identifier
- **user_id**: Creator's user ID
- **timestamp**: Creation time
- **payload**: { title, description, due_date, priority, tags, recurring_config, status }

#### Task Updated Event
- **event_type**: "task.updated"
- **task_id**: Updated task identifier
- **user_id**: Updater's user ID
- **timestamp**: Update time
- **payload**: { title, description, due_date, priority, tags, recurring_config, status }

#### Task Completed Event
- **event_type**: "task.completed"
- **task_id**: Completed task identifier
- **user_id**: Completer's user ID
- **timestamp**: Completion time
- **payload**: { title, due_date, priority, tags, next_occurrence_id }

#### Task Deleted Event
- **event_type**: "task.deleted"
- **task_id**: Deleted task identifier
- **user_id**: Deleter's user ID
- **timestamp**: Deletion time
- **payload**: { title }

#### Reminder Event
- **event_type**: "task.reminder"
- **task_id**: Task identifier for reminder
- **user_id**: Associated user ID
- **timestamp**: Reminder trigger time
- **payload**: { title, due_date, priority, notification_method }

### Kafka Topics Structure
- **task-events**: Contains all task lifecycle events (created, updated, completed, deleted)
- **reminders**: Contains reminder events for upcoming due dates
- **task-updates**: Contains real-time task updates (optional, for future use)

### Event Validation Rules
- All events must have required fields (event_type, task_id, user_id, timestamp)
- event_type must be one of the predefined values
- task_id and user_id must be valid identifiers
- timestamp must be in ISO format
- payload structure must match the event_type requirements

### Event State Transitions
- Task lifecycle events follow create → update → complete/delete sequence
- Reminder events are generated based on due_date proximity
- Recurring task completion triggers new task creation events