# Testing API Contract: End-to-End Integration Testing for Todo AI Chatbot

## Test Execution API

### Execute Test Suite
**Method**: POST
**Endpoint**: `/api/tests/execute`
**Headers**:
```
Content-Type: application/json
Authorization: Bearer {admin_token}
```

**Request Body**:
```json
{
  "suite": "integration",
  "components": ["auth", "chat", "tasks"],
  "environment": "staging",
  "include_performance": true
}
```

**Validation**:
- `suite`: Required, valid test suite name
- `components`: Optional, array of component names to test
- `environment`: Required, valid environment name
- `include_performance`: Optional, boolean (default: false)

**Success Response (200)**:
```json
{
  "execution_id": "exec_abc123",
  "status": "started",
  "total_tests": 24,
  "estimated_duration": 300
}
```

**Error Responses**:
- **400 Bad Request**: Invalid request format
- **401 Unauthorized**: Missing or invalid token
- **500 Internal Server Error**: Backend service failure

### Get Test Results
**Method**: GET
**Endpoint**: `/api/tests/results/{execution_id}`
**Headers**:
```
Authorization: Bearer {admin_token}
```

**Success Response (200)**:
```json
{
  "execution_id": "exec_abc123",
  "status": "completed",
  "passed": 22,
  "failed": 1,
  "skipped": 1,
  "duration_seconds": 245,
  "results": [
    {
      "test_id": "auth_001",
      "scenario": "User registration flow",
      "component": "auth",
      "status": "pass",
      "duration_ms": 1200,
      "error_message": null
    }
  ]
}
```

**Error Responses**:
- **401 Unauthorized**: Missing or invalid token
- **404 Not Found**: Execution ID not found
- **500 Internal Server Error**: Backend service failure

## Component Health Check API

### Get Component Status
**Method**: GET
**Endpoint**: `/api/health/components`
**Headers**:
```
Authorization: Bearer {admin_token}
```

**Success Response (200)**:
```json
{
  "timestamp": "2026-01-14T10:30:00Z",
  "components": [
    {
      "name": "frontend",
      "status": "healthy",
      "response_time_ms": 150,
      "details": {}
    },
    {
      "name": "backend",
      "status": "healthy",
      "response_time_ms": 80,
      "details": {}
    },
    {
      "name": "mcp_server",
      "status": "degraded",
      "response_time_ms": 1200,
      "details": {
        "warning": "Higher than normal response time"
      }
    }
  ]
}
```

**Error Responses**:
- **401 Unauthorized**: Missing or invalid token
- **500 Internal Server Error**: Backend service failure

## Performance Metrics API

### Get Performance Baseline
**Method**: GET
**Endpoint**: `/api/performance/baseline`
**Headers**:
```
Authorization: Bearer {admin_token}
```

**Success Response (200)**:
```json
{
  "baselines": [
    {
      "metric": "chat_response_time",
      "component": "backend",
      "baseline_value": 1500,
      "unit": "milliseconds",
      "threshold": 500
    },
    {
      "metric": "authentication_time",
      "component": "auth",
      "baseline_value": 500,
      "unit": "milliseconds",
      "threshold": 100
    }
  ]
}
```

**Error Responses**:
- **401 Unauthorized**: Missing or invalid token
- **500 Internal Server Error**: Backend service failure

### Submit Performance Results
**Method**: POST
**Endpoint**: `/api/performance/results`
**Headers**:
```
Content-Type: application/json
Authorization: Bearer {admin_token}
```

**Request Body**:
```json
{
  "test_execution_id": "exec_abc123",
  "metrics": [
    {
      "metric": "chat_response_time",
      "component": "backend",
      "value": 1200,
      "unit": "milliseconds",
      "timestamp": "2026-01-14T10:32:00Z"
    }
  ]
}
```

**Success Response (200)**:
```json
{
  "status": "accepted",
  "metrics_recorded": 1
}
```

**Error Responses**:
- **400 Bad Request**: Invalid request format
- **401 Unauthorized**: Missing or invalid token
- **500 Internal Server Error**: Backend service failure

## Test Configuration API

### Get Test Configuration
**Method**: GET
**Endpoint**: `/api/tests/config`
**Headers**:
```
Authorization: Bearer {admin_token}
```

**Success Response (200)**:
```json
{
  "environments": ["development", "staging", "production"],
  "test_suites": ["unit", "integration", "e2e", "performance"],
  "default_timeout": 30,
  "retry_attempts": 2
}
```

**Error Responses**:
- **401 Unauthorized**: Missing or invalid token
- **500 Internal Server Error**: Backend service failure

## Testing Event Handling

### Test Event Types
- `TEST_EXECUTION_STARTED`: Triggered when test suite starts
- `TEST_CASE_COMPLETED`: Triggered when individual test completes
- `TEST_SUITE_COMPLETED`: Triggered when entire suite completes
- `COMPONENT_HEALTH_CHANGED`: Triggered when component status changes

### Event Format
```json
{
  "event_type": "TEST_CASE_COMPLETED",
  "timestamp": "2026-01-14T10:30:00Z",
  "payload": {
    "test_id": "auth_001",
    "execution_id": "exec_abc123",
    "status": "pass",
    "duration_ms": 1200
  }
}
```

## Error Handling Contract

### Error Response Format
All error responses follow this format:
```json
{
  "error": "Descriptive error message",
  "status_code": 401,
  "timestamp": "2026-01-14T10:30:00Z",
  "details": {}
}
```

### Expected Error Scenarios
- Network connectivity issues between test runner and components
- API timeout errors during test execution
- Invalid authentication tokens for test APIs
- Server-side processing errors during test execution
- Malformed request data to test APIs
- Component unavailability during testing

## Security Requirements
- All testing API endpoints require authentication
- Test results contain no sensitive user data
- Performance metrics are aggregated and anonymized
- Access to test configuration is restricted
- Audit logs maintained for all test executions