# API Contracts: Modern UI Redesign for Taskify

**Feature Branch**: `004-modern-ui-redesign` | **Date**: 2026-01-09 | **Spec**: ../004-modern-ui-redesign/spec.md

## Overview

This document defines the API contracts for the new UI components and enhanced features in the Taskify modern UI redesign. These contracts ensure consistency between frontend components and backend services while maintaining compatibility with existing functionality.

## Authentication API Contracts

### Enhanced Password Strength Endpoint
**Purpose**: Validate password strength in real-time during signup

**Request**:
```
POST /api/auth/password-strength
```

**Headers**:
- `Content-Type: application/json`
- `Authorization: Bearer <token>` (optional, for validation without signup)

**Body**:
```json
{
  "password": "string",
  "userId": "string" (optional, for additional checks)
}
```

**Response (Success)**:
```json
{
  "score": 0-4,
  "label": "Weak|Medium|Strong|Very Strong",
  "color": "red|yellow|green|dark-green",
  "feedback": ["string"],
  "isValid": true|false
}
```

**Response (Error)**:
```json
{
  "error": "string",
  "code": "INVALID_PASSWORD|INTERNAL_ERROR"
}
```

## Task Management API Contracts

### Enhanced Task Response Format
**Purpose**: Extend existing task API responses with UI-specific fields

**Existing Response**:
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "ISO date string",
  "updated_at": "ISO date string",
  "user_id": "string"
}
```

**Enhanced Response**:
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "ISO date string",
  "updated_at": "ISO date string",
  "user_id": "string",
  "priority": "low|medium|high|urgent",
  "due_date": "ISO date string (optional)",
  "is_overdue": "boolean",
  "category": "string (optional)",
  "tags": ["string"],
  "formatted_due_date": "human-readable string (optional)"
}
```

### Task Filtering Endpoint
**Purpose**: Retrieve tasks with filtering and categorization options

**Request**:
```
GET /api/tasks?filter=today|pending|overdue&show_completed=true|false&priority=all|low|medium|high|urgent&category=string&search=string
```

**Headers**:
- `Authorization: Bearer <token>`

**Response (Success)**:
```json
{
  "tasks": [
    // Array of enhanced task objects
  ],
  "counts": {
    "today": 0,
    "pending": 0,
    "overdue": 0
  },
  "filters": {
    "active": "today|pending|overdue",
    "show_completed": true|false,
    "priority": "all|low|medium|high|urgent",
    "category": "string|null",
    "search_query": "string"
  }
}
```

## User Session API Contracts

### Enhanced Session Response
**Purpose**: Extend existing session API with UI-specific user data

**Existing Response**:
```json
{
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  },
  "session": {
    "accessToken": "string",
    "expiresAt": "ISO date string"
  }
}
```

**Enhanced Response**:
```json
{
  "user": {
    "id": "string",
    "email": "string",
    "name": "string",
    "avatar": "URL string (optional)",
    "unread_notifications": 0
  },
  "session": {
    "accessToken": "string",
    "expiresAt": "ISO date string"
  },
  "preferences": {
    "theme": "light|dark|system",
    "notifications_enabled": true|false,
    "timezone": "string"
  }
}
```

## Navigation API Contracts

### Dynamic Navigation Configuration
**Purpose**: Retrieve navigation configuration based on user authentication status

**Request**:
```
GET /api/navigation/config
```

**Headers**:
- `Authorization: Bearer <token>` (optional)

**Response (Authenticated User)**:
```json
{
  "navigation": [
    {
      "id": "dashboard",
      "label": "Dashboard",
      "href": "/dashboard",
      "icon": "home",
      "requiresAuth": true
    },
    {
      "id": "tasks",
      "label": "Tasks",
      "href": "/tasks",
      "icon": "check-circle",
      "requiresAuth": true
    },
    {
      "id": "profile",
      "label": "Profile",
      "href": "/profile",
      "icon": "user",
      "requiresAuth": true
    }
  ],
  "authSection": {
    "user": {
      "name": "string",
      "avatar": "URL string (optional)"
    },
    "actions": [
      {
        "id": "logout",
        "label": "Logout",
        "action": "/api/auth/logout"
      }
    ]
  }
}
```

**Response (Unauthenticated User)**:
```json
{
  "navigation": [
    {
      "id": "features",
      "label": "Features",
      "href": "/#features",
      "icon": "lightbulb",
      "requiresAuth": false
    },
    {
      "id": "pricing",
      "label": "Pricing",
      "href": "/#pricing",
      "icon": "tag",
      "requiresAuth": false
    }
  ],
  "authSection": {
    "actions": [
      {
        "id": "login",
        "label": "Log in",
        "href": "/login"
      },
      {
        "id": "signup",
        "label": "Sign up",
        "href": "/signup"
      }
    ]
  }
}
```

## Landing Page API Contracts

### Dynamic Landing Page Content
**Purpose**: Retrieve configurable content for the landing page

**Request**:
```
GET /api/landing/content
```

**Headers**:
- No authentication required

**Response**:
```json
{
  "hero": {
    "title": "Organize Your Life with Taskify",
    "subtitle": "A modern task management solution for productive individuals",
    "cta_text": "Get Started",
    "cta_link": "/signup",
    "background_image": "URL string (optional)"
  },
  "features": [
    {
      "id": "task-management",
      "title": "Task Management",
      "description": "Easily create, organize, and track your tasks",
      "icon": "clipboard-list",
      "image_url": "URL string (optional)"
    },
    {
      "id": "smart-organization",
      "title": "Smart Organization",
      "description": "Intelligent sorting and categorization of tasks",
      "icon": "folder-open",
      "image_url": "URL string (optional)"
    },
    {
      "id": "secure-private",
      "title": "Secure & Private",
      "description": "Your data is encrypted and never shared",
      "icon": "shield-check",
      "image_url": "URL string (optional)"
    },
    {
      "id": "cross-device-sync",
      "title": "Cross-Device Sync",
      "description": "Access your tasks from anywhere, anytime",
      "icon": "sync",
      "image_url": "URL string (optional)"
    }
  ],
  "testimonials": [
    {
      "id": "1",
      "quote": "Taskify has completely transformed how I manage my daily tasks.",
      "author": "Jane Smith",
      "role": "Product Manager",
      "avatar": "URL string (optional)"
    }
  ],
  "faq": [
    {
      "id": "pricing",
      "question": "How much does Taskify cost?",
      "answer": "We offer both free and paid plans with different features."
    }
  ]
}
```

## Error Response Contracts

### Standardized Error Format
All API endpoints should return errors in this standardized format:

```json
{
  "error": {
    "code": "string (machine-readable error code)",
    "message": "string (human-readable error message)",
    "details": "object (optional, detailed error information)",
    "timestamp": "ISO date string",
    "path": "string (request path that caused the error)"
  }
}
```

**Common Error Codes**:
- `UNAUTHORIZED`: User not authenticated
- `FORBIDDEN`: User lacks required permissions
- `VALIDATION_ERROR`: Request data doesn't meet validation requirements
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `INTERNAL_ERROR`: Server-side error occurred
- `RATE_LIMIT_EXCEEDED`: Too many requests from the same client

## Compatibility Considerations

### Backward Compatibility
- All new API enhancements must maintain backward compatibility with existing clients
- Enhanced responses should include all fields from the original response format
- Optional fields should not break existing clients that don't expect them
- Pagination and filtering parameters should be optional

### Forward Compatibility
- API responses should include version information for future updates
- New optional fields should be clearly marked as such
- Deprecation notices should be provided for fields that will be removed

## Validation Rules

### Request Validation
- All string fields must be validated for length and content type
- Email fields must follow standard email format validation
- Date fields must be in ISO 8601 format
- Enum fields must match allowed values exactly

### Response Validation
- All required fields must be present in responses
- Field types must match the contract specification
- Arrays must not exceed maximum size limits (typically 100 items)
- Responses must not exceed size limits (typically 1MB)