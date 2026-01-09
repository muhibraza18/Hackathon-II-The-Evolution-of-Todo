# Skill: Components

## Description
Creates or updates reusable React components with TypeScript and Tailwind CSS.

## Usage
/components <component-name>

## Instructions
- Read `@specs/ui/components.md` for component specifications
- Create component in `frontend/components/<component-name>.tsx`
- Use TypeScript with proper prop types
- Style with Tailwind CSS (mobile-first approach)
- Make components reusable and composable
- Add loading and error states where needed
- Use Client Component ('use client') only if interactive
- Follow existing component patterns in `@frontend/components`
- Include JSDoc comments for complex props
- Follow patterns in `@frontend/CLAUDE.md`

## Component Structure
```typescript
// Client Component (interactive)
'use client'

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
}

export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <div className="p-4 border rounded-lg hover:shadow-md transition">
      {/* Component JSX */}
    </div>
  );
}
```

## Examples
- `/components "TaskItem"`
- `/components "TaskForm"`