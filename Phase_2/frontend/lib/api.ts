import { Task, TaskCreate, TaskUpdate, ApiResponse } from './types';

// Use environment variable for flexibility (Vercel + local dev)
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://muhib-dev-hackathon-2-phase-2.hf.space';

// Optional: Log the base URL during development (helps debugging)
if (process.env.NODE_ENV === 'development') {
  console.log('API Base URL:', API_BASE);
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  // Get token from localStorage (Better Auth JWT)
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      credentials: 'include', // Keep if using cookies/sessions, otherwise can remove
      ...options,
    });

    if (!response.ok) {
      // Handle 401 Unauthorized → token expired/invalid
      if (response.status === 401) {
        if (token) {
          localStorage.removeItem('auth_token');
        }
        // Optional: redirect to login
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        `HTTP ${response.status}: ${response.statusText} - ${
          errorData.detail || 'No details'
        }`
      );
    }

    const data = await response.json();
    return { data, error: null };
  } catch (err) {
    console.error('API Error:', err);
    return {
      data: null,
      error: err instanceof Error ? err.message : 'Unknown error occurred',
    };
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// API Functions (endpoints match your backend spec)
// ──────────────────────────────────────────────────────────────────────────────

export async function fetchTasks(): Promise<ApiResponse<Task[]>> {
  return fetchApi<Task[]>('/api/tasks');
}

export async function createTask(task: TaskCreate): Promise<ApiResponse<Task>> {
  return fetchApi<Task>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(task),
  });
}

export async function updateTask(
  id: string,
  task: TaskUpdate
): Promise<ApiResponse<Task>> {
  return fetchApi<Task>(`/api/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(task),
  });
}

export async function deleteTask(id: string): Promise<ApiResponse<void>> {
  return fetchApi<void>(`/api/tasks/${id}`, {
    method: 'DELETE',
  });
}

export async function toggleComplete(id: string): Promise<ApiResponse<Task>> {
  // Note: Check your backend exact endpoint name
  // Some use /complete, some /toggle-complete, some PATCH /tasks/{id} with {completed: true}
  return fetchApi<Task>(`/api/tasks/${id}/toggle-complete`, {
    method: 'PATCH',
  });
}




// import { Task, TaskCreate, TaskUpdate, ApiResponse } from './types';

// const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// async function fetchApi<T>(
//   endpoint: string,
//   options: RequestInit = {}
// ): Promise<ApiResponse<T>> {
//   // Get token from localStorage
//   const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

//   try {
//     const response = await fetch(`${API_BASE}${endpoint}`, {
//       headers: {
//         'Content-Type': 'application/json',
//         ...(token && { 'Authorization': `Bearer ${token}` }), // Include JWT token in Authorization header
//         ...options.headers,
//       },
//       credentials: 'include', // Include cookies for authentication
//       ...options,
//     });

//     if (!response.ok) {
//       // Handle 401 Unauthorized responses
//       if (response.status === 401) {
//         // Clear invalid token from localStorage
//         if (token) {
//           localStorage.removeItem('auth_token');
//         }
//         // Redirect to login page
//         window.location.href = '/login';
//         throw new Error('Unauthorized - redirecting to login');
//       }
//       throw new Error(`HTTP ${response.status}: ${response.statusText}`);
//     }

//     const data = await response.json();
//     return { data, error: null };
//   } catch (err) {
//     return {
//       data: null,
//       error: err instanceof Error ? err.message : 'Unknown error',
//     };
//   }
// }

// export async function fetchTasks(): Promise<ApiResponse<Task[]>> {
//   return fetchApi<Task[]>('/api/tasks');
// }

// export async function createTask(task: TaskCreate): Promise<ApiResponse<Task>> {
//   return fetchApi<Task>('/api/tasks', {
//     method: 'POST',
//     body: JSON.stringify(task),
//   });
// }

// export async function updateTask(
//   id: string,
//   task: TaskUpdate
// ): Promise<ApiResponse<Task>> {
//   return fetchApi<Task>(`/api/tasks/${id}`, {
//     method: 'PUT',
//     body: JSON.stringify(task),
//   });
// }

// export async function deleteTask(id: string): Promise<ApiResponse<void>> {
//   return fetchApi<void>(`/api/tasks/${id}`, {
//     method: 'DELETE',
//   });
// }

// export async function toggleComplete(id: string): Promise<ApiResponse<Task>> {
//   return fetchApi<Task>(`/api/tasks/${id}/toggle-complete`, {
//     method: 'PATCH',
//   });
// }