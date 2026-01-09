# Skill: Frontend Pages

## Description
Creates or updates Next.js App Router pages with proper layout and data fetching.

## Usage
/frontend-pages <page-name>

## Instructions
- Read `@specs/ui/pages.md` for page specifications
- Create page in `frontend/app/<page-name>/page.tsx`
- Use Server Components by default for data fetching
- Use Client Components only for interactivity (mark with 'use client')
- Implement proper loading and error states
- Add metadata for SEO
- Use API client from `@frontend/lib/api.ts`
- Follow responsive design patterns
- Include proper authentication checks
- Follow patterns in `@frontend/CLAUDE.md`

## Page Structure
```typescript
// Server Component (default)
export default async function TasksPage() {
  const tasks = await api.getTasks();
  return <TaskList tasks={tasks} />;
}

// Client Component (when needed)
'use client'
export default function TaskForm() {
  const [title, setTitle] = useState('');
  // Interactive logic
}
```

## Examples
- `/frontend-pages "tasks list"`
- `/frontend-pages "login"`