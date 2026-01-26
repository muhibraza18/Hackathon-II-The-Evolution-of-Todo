# Quickstart Guide: End-to-End Integration Testing for Todo AI Chatbot

## Prerequisites

- Python 3.8+ installed for backend testing
- Node.js 18+ installed for frontend testing
- Docker and docker-compose for test environment setup
- Access to all system components (Frontend, Backend, MCP Server, Database)
- Environment variables configured for test environment

## Setup

1. Ensure you have the testing environment configured:
   ```bash
   # Navigate to test directory
   cd tests

   # Install backend testing dependencies
   pip install -r requirements-test.txt

   # Install frontend testing dependencies (if needed)
   cd ../frontend && npm install && cd ..
   ```

2. Configure test environment variables in `.env.test`:
   ```
   TEST_DATABASE_URL=postgresql://test:test@localhost:5432/todo_chatbot_test
   TEST_BACKEND_URL=http://localhost:8001
   TEST_FRONTEND_URL=http://localhost:3001
   ```

## Running Integration Tests

### Unit Tests (Component Level)
```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific component tests
pytest tests/unit/test_auth.py
pytest tests/unit/test_mcp_tools.py
```

### Integration Tests (Component Interaction)
```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific integration tests
pytest tests/integration/test_auth_integration.py
pytest tests/integration/test_chat_integration.py
pytest tests/integration/test_task_integration.py
```

### End-to-End Tests (User Journeys)
```bash
# Run complete user journey tests
pytest tests/e2e/test_user_journey.py -v

# Run deployment validation tests
pytest tests/e2e/test_deployment.py -v
```

### Performance Tests
```bash
# Run performance benchmark tests
pytest tests/performance/test_response_times.py

# Run concurrent user tests
pytest tests/performance/test_concurrent_users.py
```

## System Integration Diagram

The system integration diagram showing all component connections is located at:
`system_integration/diagrams/component_interaction.svg`

## Test Execution Matrix

The test execution matrix tracking test cases, status, and results is located at:
`system_integration/test_matrix/execution_matrix.csv`

## Deployment Runbook

The step-by-step deployment runbook is located at:
`system_integration/deployment/runbook.md`

## Bug Tracking Template

The bug tracking template is located at:
`system_integration/bug_tracking/template.md`

## Documentation Structure

The final documentation structure outline is located at:
`system_integration/documentation/structure_outline.md`

## Running the Complete Test Suite

To run the complete integration test suite:

```bash
# Run all tests in order
pytest tests/unit/ tests/integration/ tests/e2e/ -v --tb=short

# Run with coverage report
pytest --cov=src/ --cov-report=html tests/

# Run performance tests separately
pytest tests/performance/ -v
```

## Smoke Test Checklist

Execute the following manual tests to validate system functionality:

- [ ] Frontend loads without errors
- [ ] User can register with valid credentials
- [ ] User can login with registered credentials
- [ ] User can send message to chat interface
- [ ] User can add a task via chat ("Add buy groceries")
- [ ] User can list tasks via chat ("Show my tasks")
- [ ] User can complete a task via chat ("Mark groceries as done")
- [ ] User can delete a task via chat ("Delete groceries task")
- [ ] User can logout and session is cleared
- [ ] Token persists across page refresh
- [ ] Error messages are displayed appropriately for invalid inputs

## Performance Monitoring

Monitor response times during testing:

```python
# Target metrics:
# - Chat response time: <2 seconds (95th percentile)
# - Authentication: <500ms
# - Task operations: <300ms
# - Database queries: <100ms
```

## Troubleshooting Common Issues

### 401 Unauthorized on /api/chat
- Check token in localStorage
- Verify Authorization header format
- Confirm token is not expired
- Ensure backend ALLOWED_ORIGINS includes frontend URL

### Tasks not showing in chat
- Verify user_id is correctly extracted from token
- Check database connection
- Confirm MCP server is running and accessible
- Review agent logs for tool calling issues

### Agent calls wrong tool
- Review system prompt configuration
- Verify MCP tools are registered correctly
- Check OpenAI API key validity
- Examine agent logs for intent recognition problems

### Conversation not persisting
- Confirm conversation_id is stored correctly
- Verify database connection
- Check message table has records
- Review backend logs for session management

## Environment Variables

Required environment variables for testing:

| Variable | Purpose | Example |
|----------|---------|---------|
| TEST_DATABASE_URL | Test database connection | postgresql://test:test@localhost:5432/todo_chatbot_test |
| TEST_BACKEND_URL | Test backend endpoint | http://localhost:8001 |
| TEST_FRONTEND_URL | Test frontend endpoint | http://localhost:3001 |
| TEST_OPENAI_API_KEY | Test OpenAI API key | sk-... |
| TEST_BETTER_AUTH_SECRET | Test auth secret | test_secret_value |