# Skill: API Client

## Description
Creates or updates the frontend API client for backend communication.

## Usage
/api-client <resource>

## Instructions
- Create/update `frontend/lib/api.ts` with typed API methods
- Include JWT token attachment to all requests
- Get token from Better Auth session
- Add Authorization header: `Bearer <token>`
- Implement proper error handling and retry logic
- Use TypeScript for all types
- Handle 401 (unauthorized) and 403 (forbidden) responses
- Parse and return JSON responses
- Follow patterns in `@frontend/CLAUDE.md`

## API Client Pattern
```typescript
// frontend/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function getAuthToken() {
  // Get JWT from Better Auth session
  const session = await auth.getSession();
  return session?.token;
}

export const api = {
  async getTasks(userId: string, status?: string) {
    const token = await getAuthToken();
    const response = await fetch(`${API_URL}/api/${userId}/tasks?status=${status}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      if (response.status === 401) throw new Error('Unauthorized');
      throw new Error('Failed to fetch tasks');
    }
    
    return response.json();
  },
  
  // More methods...
};
```

## Examples
- `/api-client "tasks resource"`
- `/api-client "user profile"`