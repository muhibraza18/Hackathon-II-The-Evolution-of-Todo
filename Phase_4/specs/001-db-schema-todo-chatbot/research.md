# Research Findings: Database Schema for Todo AI Chatbot

**Feature**: Database Schema for Todo AI Chatbot
**Date**: 2026-01-13
**Status**: Completed

## Research Task 1: Migration Tool Decision

### Decision: SQLModel.metadata.create_all for initial implementation
### Rationale:
For the Todo AI Chatbot project, starting with SQLModel.metadata.create_all provides the simplest path to getting the database schema operational. Since this is a new project with a limited scope (just 3 tables), the overhead of Alembic migration management isn't immediately necessary. We can add Alembic later if the project grows in complexity.

### Alternatives Considered:
- **Alembic**: Industry standard with excellent version control for database schemas, but introduces additional complexity for a simple 3-table schema
- **SQLModel.metadata.create_all**: Simpler to implement initially, but lacks migration history and version control capabilities

### Conclusion:
Start with SQLModel.metadata.create_all and plan to migrate to Alembic if needed later.

## Research Task 2: Async vs Sync Database Operations

### Decision: Async database operations using asyncpg
### Rationale:
Since the project uses FastAPI, which is designed for async operations, using async database operations will provide better performance and scalability. This approach aligns with FastAPI's architecture and allows for handling more concurrent connections efficiently.

### Alternatives Considered:
- **Async (asyncpg)**: Better performance for concurrent operations, fits well with FastAPI's async nature, but slightly more complex error handling
- **Sync (psycopg2)**: Simpler to understand and debug, but potentially blocking operations that could impact performance

### Conclusion:
Use async operations with asyncpg for better integration with FastAPI.

## Research Task 3: Session Management Pattern

### Decision: Dependency Injection Pattern
### Rationale:
Dependency injection is the recommended approach for FastAPI applications as it provides clean separation of concerns, automatic cleanup of resources, and follows FastAPI best practices. It also handles async context management properly.

### Alternatives Considered:
- **Dependency Injection**: Clean, follows FastAPI best practices, automatic resource cleanup, but more verbose
- **Context Manager**: Simple, familiar pattern, but requires manual management in async context
- **Global Session**: Simple to implement, but problematic for concurrent operations and testing

### Conclusion:
Use dependency injection pattern for session management.

## Research Task 4: Neon PostgreSQL Configuration

### Decision: Connection Pooling via Neon's Built-in Pooler
### Rationale:
Neon provides built-in connection pooling which is optimized for serverless environments. This eliminates the need for additional connection pooling libraries and leverages Neon's infrastructure.

### Configuration Details:
- Use connection string format: postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
- Enable connection pooling via Neon's pooled connections
- Use environment variables for connection parameters
- Implement graceful timeout handling

### Environment Variables Needed:
- DATABASE_URL: Full connection string to Neon database
- POOL_MIN_SIZE: Minimum connection pool size (default: 1)
- POOL_MAX_SIZE: Maximum connection pool size (default: 16)

### Conclusion:
Use Neon's built-in connection pooling with proper environment variable configuration.

## Research Task 5: Testing Framework

### Decision: pytest with pytest-asyncio
### Rationale:
pytest is the most popular Python testing framework with excellent async support through pytest-asyncio. It integrates well with SQLModel and FastAPI applications and has extensive ecosystem support.

### Conclusion:
Use pytest with pytest-asyncio for database testing.

## Additional Findings

### SQLModel Best Practices:
- Use `table=True` when defining models that map to database tables
- Use `Field(default=None)` for optional fields
- Use `Field(sa_column=Column(...))` for specific database column configurations
- Use `relationship()` for defining relationships between models
- Use Pydantic's `validator` for custom field validation

### Timestamp Management:
- Use `datetime.utcnow()` for created_at (UTC timezone)
- Use `func.now()` or similar for automatic database-level timestamp updates
- Consider using `DateTime(timezone=True)` for timezone-aware operations

### Foreign Key Relationships:
- Define relationships using SQLModel's `Relationship()` function
- Use `cascade="all, delete-orphan"` for cascade delete behavior
- Use proper indexing on foreign key columns for performance

## Action Items for Implementation

1. **Database Setup**: Implement async engine with Neon connection string
2. **Model Definitions**: Create Task, Conversation, Message models with proper relationships
3. **Session Management**: Create dependency injection function for database sessions
4. **Migration Strategy**: Use SQLModel.metadata.create_all initially
5. **Testing Strategy**: Implement pytest fixtures for database testing
6. **Error Handling**: Add proper exception handling for database operations