# Data Model: Advanced Todo Features

## Task Entity Extension

### Fields
- **due_date** (datetime | None): Scheduled completion date for the task
- **priority** (str | None): Enum values ['low', 'medium', 'high', 'urgent']
- **tags** (list[str]): Array of tag strings for categorization
- **recurring_config** (dict | None): Configuration object with:
  - type: 'daily' | 'weekly' | 'monthly'
  - interval: positive integer
  - end_condition: None | specific date | occurrence count
- **next_occurrence_id** (str | None): Reference to next occurrence in recurring series
- **parent_task_id** (str | None): Reference to parent task for recurring instances
- **original_task_id** (str | None): Reference to the original task in a recurring series

### Relationships
- Recurring tasks form parent-child relationships through parent_task_id/next_occurrence_id
- Tasks maintain existing user relationship
- Original_task_id creates lineage from recurring series

### Validation Rules
- due_date must be in the future if set
- recurring interval must be positive if recurring is enabled
- priority must be one of allowed values ['low', 'medium', 'high', 'urgent']
- tags array length must be reasonable (e.g., max 10 tags)
- recurring_config.type must be one of allowed values if recurring is enabled
- recurring_config.interval must be a positive integer if recurring is enabled

### State Transitions
- Pending → Completed (triggers recurring task generation if applicable)
- Completed → Pending (undo completion, potentially removes next occurrence if recurring)
- Active recurring task can generate next occurrence when completed

### Indexes for Performance
- Index on due_date for efficient date-based queries
- Index on priority for priority-based filtering
- Index on tags for tag-based filtering (using GIN index for array fields)
- Composite index on (user_id, status, due_date) for common query patterns
- Index on parent_task_id for recurring task navigation