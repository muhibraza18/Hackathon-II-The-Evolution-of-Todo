# Frontend Development Guide - Next.js 16+

## Framework Conventions

This guide outlines the conventions and patterns for frontend development in the Todo Full-Stack Web Application.

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS 3.4+
- **UI Library**: TBD (likely shadcn/ui in future phases)

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx       # Root layout with metadata
│   ├── page.tsx         # Home page
│   └── globals.css      # Global styles
├── components/          # Reusable components (future)
├── lib/                 # Utility functions (future)
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── tailwind.config.ts   # Tailwind CSS configuration
└── .env.example         # Environment variable template
```

## App Router Conventions

### Server Components (Default)
- Use Server Components for static content and data fetching
- No hooks (useState, useEffect, etc.)
- Can directly access databases (when implemented)
- Render on the server for better performance

### Client Components (When Needed)
- Add `"use client"` directive at the top of the file
- Use only when interactivity is required (forms, modals, etc.)
- Can use React hooks (useState, useEffect, etc.)
- Minimize usage for optimal performance

### File-Based Routing
- Route structure mirrors file structure in `app/` directory
- `app/page.tsx` → `/`
- `app/dashboard/page.tsx` → `/dashboard`
- `app/tasks/[id]/page.tsx` → `/tasks/{id}`

## TypeScript Guidelines

### Strict Mode
- Enable strict mode in `tsconfig.json`
- Use type annotations for all function parameters
- Define interfaces for data models

### Type Safety
- Avoid `any` type
- Use proper type definitions from backend API
- Validate prop types with TypeScript

## Tailwind CSS Guidelines

### Utility-First Approach
- Use utility classes for styling
- Avoid custom CSS unless necessary
- Follow Tailwind's design system

### Responsive Design
- Mobile-first approach
- Use Tailwind breakpoints (`sm:`, `md:`, `lg:`, `xl:`)
- Test on multiple screen sizes

## Environment Variables

### Frontend-Specific Variables
- Prefix with `NEXT_PUBLIC_` for client-side access
- Never commit secrets to version control
- Use `.env.local` for local development
- See `.env.example` for required variables

### Example `.env.local`
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
BETTER_AUTH_PUBLIC_KEY=your-public-key
```

## Development Workflow

### Running the Development Server
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:3000

### Building for Production
```bash
npm run build
npm start
```

### Linting and Formatting
```bash
npm run lint       # Run ESLint
npm run format     # Run Prettier (when configured)
```

## Integration with Backend

### API Calls
- Use `fetch` API or a data fetching library (future)
- Handle loading and error states
- Validate responses with TypeScript types

### Authentication (Future)
- Integrate Better Auth SDK
- Store JWT tokens securely
- Include auth tokens in API requests

## Related Documentation

- **Project Overview**: `@specs/overview.md` - Tech stack and scope
- **Architecture**: `@specs/architecture.md` - Frontend responsibilities
- **Database Schema**: `@specs/database/schema.md` - Data models for type definitions
- **Quickstart**: `@specs/001-foundation-setup/quickstart.md` - Setup instructions
- **Root Guide**: `CLAUDE.md` - Overall development workflow

## Common Patterns

### Fetching Data (Future)
```typescript
// Server Component example
async function getTasks() {
  const response = await fetch('http://localhost:8000/api/tasks', {
    cache: 'no-store',
  })
  if (!response.ok) {
    throw new Error('Failed to fetch tasks')
  }
  return response.json()
}
```

### Client Component Example
```typescript
'use client'

import { useState } from 'react'

export function TaskForm() {
  const [title, setTitle] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    // Submit to backend API
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <button type="submit">Add Task</button>
    </form>
  )
}
```

## Best Practices

1. **Performance**: Use Server Components by default, Client Components only when needed
2. **Accessibility**: Use semantic HTML and ARIA attributes
3. **SEO**: Optimize metadata and use proper heading hierarchy
4. **Error Handling**: Graceful error boundaries and user-friendly messages
5. **Type Safety**: Leverage TypeScript for type safety across the application

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000 (macOS/Linux)
lsof -i :3000
kill -9 <PID>

# On Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Dependency Issues
```bash
rm -rf node_modules package-lock.json
npm install
```
