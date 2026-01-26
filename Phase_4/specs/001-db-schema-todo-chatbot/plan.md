# Implementation Plan: Database Schema for Todo AI Chatbot

**Feature**: Database Schema for Todo AI Chatbot
**Branch**: 001-db-schema-todo-chatbot
**Created**: 2026-01-13
**Status**: Draft
**Author**: Claude Code

## Technical Context

### Known Information
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Models**: Task, Conversation, Message (3 required tables)
- **Architecture**: Stateless, database-first approach
- **Framework**: Python FastAPI
- **Authentication**: Better Auth (separate, user_id as string)

### Unknowns (NEEDS CLARIFICATION)
- **Migration Tool**: Alembic vs SQLModel.metadata.create_all (decision needed)
- **Async/Sync**: Async database operations vs sync (FastAPI compatibility)
- **Session Management**: Dependency injection vs context manager pattern
- **Environment Setup**: Specific Neon PostgreSQL connection parameters
- **Testing Framework**: Which framework to use for database testing

## Constitution Check

### Compliance Verification
- ✅ **Stateless Architecture**: All state persists to PostgreSQL only
- ✅ **MCP-First Design**: Database operations will be abstracted behind MCP tools
- ✅ **Conversation Persistence**: All chat history stored in database
- ✅ **Natural Language Interface**: Data models support NL processing
- ✅ **Agentic Development**: Implementation via Claude Code
- ✅ **Type Safety**: SQLModel provides strong typing with Pydantic
- ✅ **Technology Stack**: Uses Python FastAPI, SQLModel, Neon PostgreSQL
- ✅ **Database Models**: Implements required Task, Conversation, Message tables
- ✅ **Error Handling**: Includes comprehensive error handling
- ✅ **Async Operations**: Designed for async compatibility with FastAPI
- ✅ **User Data Isolation**: All models include user_id for data isolation
- ✅ **Timestamp Management**: Automatic created_at and updated_at fields
- ✅ **Foreign Key Relationships**: Proper relationships with cascade delete

### Gate Status
- [x] **Research Phase**: Complete all research tasks to resolve unknowns
- [x] **Design Phase**: Finalize data model and API contracts
- [ ] **Implementation Phase**: Build and test database schema
- [ ] **Validation Phase**: Verify all constitutional requirements met

## Phase 0: Research & Discovery

### Research Task 1: Migration Tool Decision
**Objective**: Decide between Alembic and SQLModel.metadata.create_all
**Approach**:
- Research benefits of Alembic for version control
- Compare complexity of SQLModel.metadata.create_all
- Consider project scale and maintenance needs
**Expected Outcome**: Clear recommendation for migration tool

### Research Task 2: Async vs Sync Database Operations
**Objective**: Determine optimal approach for FastAPI compatibility
**Approach**:
- Investigate async database drivers (asyncpg vs psycopg2)
- Assess performance implications
- Consider error handling differences
**Expected Outcome**: Decision on async/sync approach with rationale

### Research Task 3: Session Management Pattern
**Objective**: Choose optimal session management for FastAPI
**Approach**:
- Evaluate dependency injection approach
- Compare with context managers
- Assess thread safety for async operations
**Expected Outcome**: Recommended session management pattern

### Research Task 4: Neon PostgreSQL Configuration
**Objective**: Identify specific configuration requirements
**Approach**:
- Research Neon-specific connection parameters
- Identify pooling recommendations
- Document environment variable requirements
**Expected Outcome**: Complete connection configuration

## Phase 1: Design & Architecture

### Design Task 1: Data Model Definition
**Objective**: Create complete SQLModel definitions
**Deliverables**:
- `models.py` with Task, Conversation, Message classes
- Proper field types, constraints, and relationships
- Index definitions for performance
- Cascade delete configuration

**Requirements to Implement**:
- FR-001: Task model with all required fields
- FR-002: Conversation model with timestamps
- FR-003: Message model with foreign key
- FR-004: Foreign key relationship with cascade delete
- FR-005: user_id in all models for data isolation
- FR-006: Automatic timestamp population
- FR-007-009: Proper indexing strategy
- FR-010-015: Field constraints and validations
- FR-016-018: SQLModel usage and UTC timestamps

### Design Task 2: Database Connection Layer
**Objective**: Create database connection infrastructure
**Deliverables**:
- `database.py` with engine and session setup
- Connection pooling configuration
- Error handling mechanisms
- Environment variable integration

### Design Task 3: CRUD Operations Layer
**Objective**: Create data access functions
**Deliverables**:
- `crud.py` with create, read, update, delete functions
- User-isolated queries (filter by user_id)
- Transaction management
- Error handling for database operations

### Design Task 4: API Contracts
**Objective**: Define interface for MCP tools
**Deliverables**:
- OpenAPI-compatible endpoints
- Input/output schemas
- Error response definitions
- Validation rules

## Phase 2: Implementation

### Implementation Task 1: Database Setup
**Objective**: Establish database connection infrastructure
**Steps**:
- Install required dependencies (sqlmodel, psycopg2-binary, etc.)
- Configure database engine with Neon settings
- Test connectivity
- Implement connection pooling

### Implementation Task 2: Model Implementation
**Objective**: Create SQLModel classes
**Steps**:
- Implement Task model with all constraints
- Implement Conversation model with timestamps
- Implement Message model with foreign key
- Add relationship properties
- Add validation methods

### Implementation Task 3: Migration Setup
**Objective**: Configure database schema management
**Steps**:
- Initialize chosen migration tool
- Generate initial migration
- Apply to Neon database
- Verify table creation

### Implementation Task 4: CRUD Functions
**Objective**: Create data access layer
**Steps**:
- Implement task CRUD operations
- Implement conversation CRUD operations
- Implement message CRUD operations
- Add user isolation filtering
- Add error handling

## Phase 3: Validation & Testing

### Validation Task 1: Model Validation
**Objective**: Verify data models meet requirements
**Tests**:
- SC-001: All 3 models defined and accessible
- SC-002: Foreign key relationships established
- SC-003: Timestamps auto-populate
- SC-004: User data isolation via user_id
- SC-005: SQLModel compatibility with Neon
- SC-006: Migration creates tables correctly

### Validation Task 2: Functional Testing
**Objective**: Test all CRUD operations
**Tests**:
- Task creation with required fields
- Task creation without optional description
- Task creation failure without user_id/title
- Conversation creation and retrieval
- Message creation with valid conversation_id
- Message creation failure with invalid conversation_id

### Validation Task 3: Relationship Testing
**Objective**: Verify foreign key relationships
**Tests**:
- Message.conversation returns correct Conversation
- Conversation.messages returns associated messages
- Cascade delete removes messages when conversation deleted
- Task operations don't affect conversations

### Validation Task 4: Performance Testing
**Objective**: Verify query performance
**Tests**:
- User_id filtering works efficiently
- Conversation lookup by ID is fast
- Message ordering by created_at works
- Task filtering by completed status works

## Dependencies & Resources

### Required Dependencies
- sqlmodel
- psycopg2-binary (or asyncpg for async)
- python-dotenv
- alembic (if using Alembic for migrations)

### Development Timeline
- Phase 0: 1 day (Research)
- Phase 1: 2 days (Design)
- Phase 2: 2 days (Implementation)
- Phase 3: 1 day (Validation)

## Success Criteria

This implementation plan is successful when:
1. All research tasks are completed and unknowns resolved
2. Data models are designed meeting all functional requirements
3. Database schema is implemented and tested
4. All constitutional compliance gates are passed
5. Migration tool is configured and working
6. CRUD operations are implemented and validated
7. Performance requirements are met

## Risk Assessment

### High Risk Items
- Neon PostgreSQL connectivity issues
- Async vs sync database operation complications
- Foreign key constraint conflicts

### Mitigation Strategies
- Thorough testing with local PostgreSQL before Neon deployment
- Clear decision matrix for async/sync approach
- Careful foreign key constraint design and testing