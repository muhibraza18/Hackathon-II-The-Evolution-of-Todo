# Implementation Plan: Advanced Todo Features

**Feature Branch**: `001-advanced-todo-features`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Phase V – Sub-phase 1: Advanced Todo Features for Todo AI Chatbot"

## Technical Context

This plan details the implementation of advanced todo features including recurring tasks, due dates with reminders, task priorities, tags, and search/filter functionality. The implementation will extend the existing Phase IV backend (FastAPI + SQLModel + Neon PostgreSQL) and frontend (Next.js App Router) while preparing for future event-driven architecture with Kafka/Dapr integration.

Key decisions to be documented:
- **Recurring task configuration storage**: Simple fields (repeat: daily/weekly, interval: int) vs cron expression
- **Due date reminder logic**: Future event publishing vs DB polling approach
- **Priority representation**: String enum (low/medium/high/urgent) vs numeric scale (1-5)
- **Tag storage**: Array of strings vs separate Tag table with many-to-many relationship
- **Search/filter/sort implementation**: Server-side vs client-side processing
- **Event publishing triggers**: Points where task events are generated for future processing

## Constitution Check

- **Spec-Driven Development**: Following spec → plan → tasks → implement cycle as outlined in constitution
- **AI-Assisted Development**: Using Claude Code for implementation
- **Reproducible Environments**: Maintaining consistency across dev/test/prod
- **Security First**: Ensuring proper validation and sanitization of new fields
- **Minimal Viable Changes**: Implementing features incrementally
- **Container-First Architecture**: Maintaining existing containerized architecture
- **Immutable Infrastructure**: Following existing deployment patterns
- **Observability**: Maintaining existing logging/monitoring
- **Fail-Fast**: Proper error handling for new functionality
- **Environment Parity**: Ensuring changes work across all environments
- **Backward Compatibility**: Preserving existing functionality

## Gates

- [ ] All architectural decisions documented in ADR format
- [ ] Implementation plan reviewed and approved by team
- [ ] All decisions that meet significance criteria have ADRs created
- [ ] Security implications assessed for new data fields
- [ ] Performance impact evaluated for new queries/indexes
- [ ] Database migration strategy validated
- [ ] Backward compatibility verified with existing clients

## Phase 0: Research & Architecture Decisions

### research.md

#### Decision: Recurring Task Configuration Storage
**Rationale**: Using simple fields (repeat_type: str enum daily/weekly/monthly, repeat_interval: int) rather than cron expressions to maintain UI simplicity while providing necessary functionality. Cron expressions are powerful but complex for typical recurring task patterns.
**Alternatives considered**:
- Cron expression: More flexible but complex UI and parsing requirements
- Simple fields: Limited flexibility but simpler implementation and UI

#### Decision: Due Date Reminder Logic
**Rationale**: Implementing future event publishing mechanism that will integrate with Dapr Jobs/Kafka in later phases. For now, events will be logged and prepared for future processing without actual scheduling.
**Alternatives considered**:
- Direct scheduling: Immediate implementation but harder to migrate to distributed system
- Event preparation: Defers actual scheduling to later phase but maintains architecture

#### Decision: Priority Representation
**Rationale**: Using string enum (low/medium/high/urgent) for better readability and user experience. Sorting can be handled with mapping.
**Alternatives considered**:
- String enum: Better UX but requires sorting mapping
- Numeric scale: Natural sorting but less readable for users

#### Decision: Tag Storage
**Rationale**: Using array of strings stored in the task record for simplicity and performance. This avoids joins for basic operations while allowing flexible tagging.
**Alternatives considered**:
- Array of strings: Simpler queries but denormalized data
- Separate Tag table: Normalized but requires joins for tag operations

#### Decision: Search/Filter/Sort Implementation
**Rationale**: Implementing server-side processing to handle large datasets efficiently while maintaining good performance. Client-side is only for small result sets.
**Alternatives considered**:
- Server-side: Better for large datasets but more complex API
- Client-side: Simpler but limited by data transfer size

#### Decision: Event Publishing Triggers
**Rationale**: Publishing events on task creation, update, completion, and deletion to support future event-driven architecture. Events will be prepared but not necessarily delivered until later phases.
**Alternatives considered**:
- Minimal events: Fewer events but less flexibility for consumers
- Comprehensive events: More events but richer data for future consumers

## Phase 1: Data Model & Contracts

### data-model.md

#### Task Entity Extension
- **due_date** (datetime | None): Scheduled completion date for the task
- **priority** (str | None): Enum values ['low', 'medium', 'high', 'urgent']
- **tags** (list[str]): Array of tag strings for categorization
- **recurring_config** (dict | None): Configuration object with:
  - type: 'daily' | 'weekly' | 'monthly'
  - interval: positive integer
  - end_condition: None | specific date | occurrence count
- **next_occurrence_id** (str | None): Reference to next occurrence in recurring series
- **parent_task_id** (str | None): Reference to parent task for recurring instances

#### Relationships
- Recurring tasks form parent-child relationships through parent_task_id/next_occurrence_id
- Tasks maintain existing user relationship

#### Validation Rules
- due_date must be in the future if set
- recurring interval must be positive if recurring is enabled
- priority must be one of allowed values
- tags array length must be reasonable (e.g., max 10 tags)

### API Contracts

#### Task Creation Endpoint
```
POST /api/tasks
Request Body:
{
  "title": "string",
  "description": "string",
  "due_date": "datetime",
  "priority": "low|medium|high|urgent",
  "tags": ["string"],
  "recurring_config": {
    "type": "daily|weekly|monthly",
    "interval": "positive integer",
    "end_condition": "null|date|occurrence_count"
  }
}
```

#### Task Retrieval with Filtering
```
GET /api/tasks?priority=high&tag=work&due_before=2023-12-31&sort_by=due_date&order=asc
Response:
[
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "due_date": "datetime",
    "priority": "low|medium|high|urgent",
    "tags": ["string"],
    "recurring_config": {...},
    "status": "pending|completed"
  }
]
```

#### Task Update with New Fields
```
PUT /api/tasks/{id}
Request Body:
{
  "title": "string",
  "description": "string",
  "due_date": "datetime",
  "priority": "low|medium|high|urgent",
  "tags": ["string"],
  "recurring_config": {...}
}
```

### quickstart.md

#### Quick Start: Advanced Todo Features Implementation

1. **Extend Task Model**:
   - Update backend/models.py to add new fields
   - Create and run Alembic migration

2. **Update API Endpoints**:
   - Modify existing task endpoints to handle new fields
   - Add filtering and sorting parameters
   - Implement recurring task logic

3. **Frontend Updates**:
   - Update task form with new input fields
   - Enhance task list view with priority/tags display
   - Add filtering and sorting UI controls

4. **Event Preparation**:
   - Add event publishing hooks for new operations
   - Log events for future processing

5. **Testing**:
   - Unit tests for new model validations
   - API integration tests with new fields
   - Frontend component tests

## Phase 2: Implementation Strategy

### Layer 1: Model + Migration
1. Extend Task model in backend/models.py with new fields
2. Create Alembic migration for database schema changes
3. Implement model validation for new fields
4. Update existing model tests

### Layer 2: API Endpoints + Business Logic
1. Extend /api/tasks endpoints with new field support
2. Add filtering and sorting capabilities to GET endpoint
3. Implement recurring task generation logic
4. Add due date reminder preparation
5. Update API tests

### Layer 3: Frontend UI + API Client
1. Update task creation/edit forms with new fields
2. Enhance task list view to display priorities and tags
3. Add filtering and sorting UI controls
4. Update API client to handle new fields
5. Add UI for recurring task configuration

### Layer 4: Testing & Validation
1. Unit tests for new model validations
2. API integration tests with filtering/sorting
3. Frontend component tests for new UI elements
4. End-to-end tests for complete workflows

### Layer 5: Documentation Updates
1. Update README with new features
2. Document API changes
3. Update user guides for new functionality

## Architecture Decision Records (ADRs)

The following architectural decisions require formal ADR documentation:

1. **ADR-001**: Data storage approach for recurring task configurations
2. **ADR-002**: Event-driven architecture preparation strategy
3. **ADR-003**: Search and filtering implementation approach

## Risk Analysis

- **Database Migration Risk**: Schema changes could impact existing data - implement with careful backup strategy
- **Performance Risk**: Additional fields and queries could impact performance - optimize with proper indexing
- **Compatibility Risk**: New fields might break existing clients - maintain backward compatibility
- **Complexity Risk**: Recurring tasks introduce complex business logic - implement with thorough testing

## Success Metrics

- [ ] All new fields properly stored and retrieved from database
- [ ] Recurring tasks generate next occurrence correctly
- [ ] Due date reminders are prepared for future processing
- [ ] Search, filter, and sort functionality works as expected
- [ ] All existing functionality remains intact (backward compatibility)
- [ ] API endpoints handle new fields without breaking changes
- [ ] Frontend properly displays and accepts new task attributes
- [ ] Event publishing hooks are in place for future integration