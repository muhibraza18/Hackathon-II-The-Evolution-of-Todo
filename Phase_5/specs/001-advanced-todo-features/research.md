# Research: Advanced Todo Features Implementation

## Decision: Recurring Task Configuration Storage
**Rationale**: Using simple fields (repeat_type: str enum daily/weekly/monthly, repeat_interval: int) rather than cron expressions to maintain UI simplicity while providing necessary functionality. Cron expressions are powerful but complex for typical recurring task patterns.
**Alternatives considered**:
- Cron expression: More flexible but complex UI and parsing requirements
- Simple fields: Limited flexibility but simpler implementation and UI

## Decision: Due Date Reminder Logic
**Rationale**: Implementing future event publishing mechanism that will integrate with Dapr Jobs/Kafka in later phases. For now, events will be logged and prepared for future processing without actual scheduling.
**Alternatives considered**:
- Direct scheduling: Immediate implementation but harder to migrate to distributed system
- Event preparation: Defers actual scheduling to later phase but maintains architecture

## Decision: Priority Representation
**Rationale**: Using string enum (low/medium/high/urgent) for better readability and user experience. Sorting can be handled with mapping.
**Alternatives considered**:
- String enum: Better UX but requires sorting mapping
- Numeric scale: Natural sorting but less readable for users

## Decision: Tag Storage
**Rationale**: Using array of strings stored in the task record for simplicity and performance. This avoids joins for basic operations while allowing flexible tagging.
**Alternatives considered**:
- Array of strings: Simpler queries but denormalized data
- Separate Tag table: Normalized but requires joins for tag operations

## Decision: Search/Filter/Sort Implementation
**Rationale**: Implementing server-side processing to handle large datasets efficiently while maintaining good performance. Client-side is only for small result sets.
**Alternatives considered**:
- Server-side: Better for large datasets but more complex API
- Client-side: Simpler but limited by data transfer size

## Decision: Event Publishing Triggers
**Rationale**: Publishing events on task creation, update, completion, and deletion to support future event-driven architecture. Events will be prepared but not necessarily delivered until later phases.
**Alternatives considered**:
- Minimal events: Fewer events but less flexibility for consumers
- Comprehensive events: More events but richer data for future consumers