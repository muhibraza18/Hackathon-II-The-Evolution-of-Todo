# System Integration Diagram: Todo AI Chatbot

## Component Interaction Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │    Database     │
│   (React/Vite)  │◄──►│   (FastAPI)      │◄──►│  (PostgreSQL)   │
│                 │    │                  │    │                 │
│ - User Interface│    │ - Auth endpoints │    │ - User accounts │
│ - Chat interface│    │ - Chat endpoint  │    │ - Sessions      │
│ - Auth flows    │    │ - Agent proxy    │    │ - Tasks         │
│ - Token mgmt    │    │ - Middleware     │    │ - Conversations │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐    ┌─────────────────┐
                    │   MCP Server     │    │    OpenAI       │
                    │                  │◄──►│   (Agent)       │
                    │ - Task tools     │    │                 │
                    │ - CRUD ops       │    │ - Intent recog. │
                    │ - Tool registry  │    │ - Tool calling  │
                    │ - DB interface   │    │ - Responses     │
                    └──────────────────┘    └─────────────────┘
```

## Data Flow Paths

### 1. User Registration Flow
```
Frontend Register Form
         │
         ▼
POST /api/auth/register
         │
         ▼
Backend Auth Middleware
         │
         ▼
Database User Creation
         │
         ▼
Token Generation & Return
         │
         ▼
Frontend Token Storage
```

### 2. Chat Message Flow
```
Frontend Chat Input
         │
         ▼
POST /api/chat (with token)
         │
         ▼
Backend Auth Validation
         │
         ▼
Agent Request Construction
         │
         ▼
MCP Tool Selection & Execution
         │
         ▼
Database Task Operation
         │
         ▼
Response Formation
         │
         ▼
Frontend Message Display
```

### 3. Authentication Validation Flow
```
API Request with Token
         │
         ▼
Auth Middleware Extraction
         │
         ▼
Database Token Verification
         │
         ▼
Session Validation
         │
         ▼
User Context Injection
         │
         ▼
Proceed with Request
```

## Integration Points

### Frontend ↔ Backend
- **Protocol**: HTTPS/REST API
- **Authentication**: Bearer tokens in headers
- **Endpoints**: /api/auth/*, /api/chat
- **CORS**: Configured for frontend domain

### Backend ↔ MCP Server
- **Protocol**: Internal HTTP/HTTPS
- **Communication**: Tool execution requests
- **Data Format**: JSON
- **Authentication**: Internal token or direct connection

### MCP Server ↔ Database
- **Protocol**: Direct database connection
- **Operations**: CRUD operations on user, task, session tables
- **Security**: Connection pooling, parameterized queries

### Backend ↔ OpenAI Agent
- **Protocol**: HTTPS to OpenAI API
- **Authentication**: API key
- **Data Format**: JSON with message and tool definitions
- **Response Processing**: Tool call interpretation and execution

## Error Handling Paths

### Authentication Failure
```
Invalid Token → 401 Unauthorized → Frontend Login Redirect
```

### Database Unavailable
```
DB Connection Fail → Graceful Degradation → User-Friendly Error Message
```

### MCP Server Down
```
Tool Execution Fail → Error Response → Frontend Error Display
```

## Performance Considerations

- **Response Times**: Frontend should receive responses within 2 seconds
- **Database Queries**: Optimized with proper indexing
- **Token Validation**: Cached where appropriate
- **Concurrent Users**: Connection pooling and rate limiting