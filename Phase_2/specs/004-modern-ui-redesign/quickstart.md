# Quickstart: Modern UI Redesign for Taskify

**Feature Branch**: `004-modern-ui-redesign` | **Date**: 2026-01-09 | **Spec**: ../004-modern-ui-redesign/spec.md

## Overview

This quickstart guide provides essential information to begin implementing the modern UI redesign for Taskify. It covers the new component architecture, design system tokens, and implementation patterns needed to build the enhanced user interface.

## Getting Started

### Prerequisites

1. **Node.js**: Version 18+ installed
2. **Next.js**: Version 16+ installed
3. **Tailwind CSS**: Configured in the project
4. **TypeScript**: With strict mode enabled
5. **Better Auth**: For authentication system

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Install Tailwind CSS if not already installed:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

4. Start the development server:
```bash
npm run dev
```

## New Component Architecture

### 1. Design System Tokens

The new UI uses a comprehensive design system with these key tokens:

**Colors**:
- Primary: `#22c55e` (Green for main actions)
- Secondary: Various blues, purples, ambers for accents
- Neutrals: Grayscale from 50 (lightest) to 900 (darkest)

**Typography**:
- Font family: Inter (or similar modern sans-serif)
- Sizes: `xs` (0.75rem) to `6xl` (3.75rem)
- Weights: `normal` to `black`

**Spacing**: Using Tailwind's default spacing scale (0 to 96 in 4px increments)

### 2. Core New Components

#### PasswordStrengthIndicator
```tsx
// components/PasswordStrengthIndicator.tsx
import { PasswordStrength, PasswordCriteria } from '@/types';

interface PasswordStrengthIndicatorProps {
  password: string;
  onStrengthChange?: (strength: PasswordStrength) => void;
}

// Usage
<PasswordStrengthIndicator
  password={password}
  onStrengthChange={setPasswordStrength}
/>
```

#### Navbar
```tsx
// components/Navbar.tsx
import { NavigationState, NavItem } from '@/types';

interface NavbarProps {
  navigationState: NavigationState;
  onNavToggle?: (item: NavItem) => void;
}

// Usage
<Navbar navigationState={navState} />
```

#### TaskCard (Enhanced)
```tsx
// components/TaskCard.tsx
import { EnhancedTask } from '@/types';

interface TaskCardProps {
  task: EnhancedTask;
  onEdit?: (task: EnhancedTask) => void;
  onDelete?: (taskId: string) => void;
  onComplete?: (taskId: string, completed: boolean) => void;
}

// Usage
<TaskCard
  task={enhancedTask}
  onEdit={handleEdit}
  onComplete={handleComplete}
/>
```

## Implementation Patterns

### 1. Responsive Design Pattern

Use the mobile-first approach with Tailwind's responsive prefixes:

```tsx
// Example of responsive layout
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards will be stacked on mobile, 2-column on tablet, 3-column on desktop */}
</div>
```

### 2. Password Strength Validation

Implement real-time password validation with the following logic:

```tsx
// Example password strength calculation
const calculatePasswordStrength = (password: string): PasswordStrength => {
  let score = 0;
  const feedback: string[] = [];

  if (password.length >= 8) score++;
  else feedback.push("Use at least 8 characters");

  if (/[A-Z]/.test(password)) score++;
  else feedback.push("Add an uppercase letter");

  if (/[a-z]/.test(password)) score++;
  else feedback.push("Add a lowercase letter");

  if (/\d/.test(password)) score++;
  else feedback.push("Add a number");

  if (/[^A-Za-z0-9]/.test(password)) score++;
  else feedback.push("Add a special character");

  const labels = ["Weak", "Medium", "Strong", "Very Strong"];
  const colors = ["red", "yellow", "green", "dark-green"];

  return {
    score,
    label: labels[Math.min(score, 3)],
    color: colors[Math.min(score, 3)],
    feedback,
    isValid: score >= 3
  };
};
```

### 3. Authentication State Integration

Connect the new UI components with the existing AuthContext:

```tsx
// Example of using authentication state in Navbar
import { useAuth } from '@/contexts/AuthContext';

const Navbar = () => {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) return <div className="animate-pulse">Loading...</div>;

  return (
    <nav className="sticky top-0 z-50 bg-white shadow-md">
      {/* Navigation content */}
    </nav>
  );
};
```

## Page Implementation Guide

### 1. Landing Page (/)

Structure the landing page with these sections:

```tsx
// app/page.tsx
import Hero from '@/components/Hero';
import Features from '@/components/Features';
import { LandingPageData } from '@/types';

export default function LandingPage() {
  const pageData: LandingPageData = {
    hero: {
      title: "Organize Your Life with Taskify",
      subtitle: "A modern task management solution for productive individuals",
      ctaText: "Get Started",
      ctaLink: "/signup"
    },
    features: [
      {
        id: "1",
        title: "Task Management",
        description: "Easily create, organize, and track your tasks"
      },
      // ... more features
    ]
  };

  return (
    <div className="min-h-screen">
      <Hero data={pageData.hero} />
      <Features features={pageData.features} />
    </div>
  );
}
```

### 2. Authentication Pages

Enhance the signup page with password strength indicator:

```tsx
// app/signup/page.tsx
import PasswordStrengthIndicator from '@/components/PasswordStrengthIndicator';

export default function SignupPage() {
  const [password, setPassword] = useState("");
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength | null>(null);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg">
        <form className="mt-8 space-y-6">
          {/* Email and name fields */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500"
            />
            <PasswordStrengthIndicator
              password={password}
              onStrengthChange={setPasswordStrength}
            />
          </div>
          {/* Rest of form */}
        </form>
      </div>
    </div>
  );
}
```

### 3. Tasks Page (/tasks)

Enhance the tasks page with tabbed interface:

```tsx
// app/tasks/page.tsx
import { TaskTabState, EnhancedTask } from '@/types';

export default function TasksPage() {
  const [activeTab, setActiveTab] = useState<'today' | 'pending' | 'overdue'>('pending');

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <div className="mt-4 flex space-x-1" role="tablist">
            <button
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                activeTab === 'today'
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('today')}
            >
              Today
            </button>
            <button
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                activeTab === 'pending'
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('pending')}
            >
              Pending
            </button>
            <button
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                activeTab === 'overdue'
                  ? 'bg-red-100 text-red-700'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('overdue')}
            >
              Overdue
            </button>
          </div>
        </div>
        {/* Task list based on active tab */}
      </div>
    </div>
  );
}
```

## Development Workflow

### 1. Component Development

1. Create new components in `frontend/components/`
2. Use TypeScript interfaces for props
3. Implement responsive design with Tailwind classes
4. Add proper accessibility attributes (aria-* roles)
5. Test component in isolation before integrating

### 2. Testing Strategy

1. **Visual Testing**: Verify layout on mobile, tablet, and desktop
2. **Interactive Testing**: Check all interactive elements work as expected
3. **Accessibility Testing**: Ensure keyboard navigation and screen reader compatibility
4. **Performance Testing**: Monitor loading times and render performance

### 3. Responsive Breakpoints

Use these Tailwind breakpoints for consistent responsive design:

- `sm:` (640px) - Small screens (mobile)
- `md:` (768px) - Medium screens (small tablets)
- `lg:` (1024px) - Large screens (tablets/desktop)
- `xl:` (1280px) - Extra large screens (large desktops)

## Common Implementation Patterns

### 1. Loading States
```tsx
// Use consistent loading indicators
{loading ? (
  <div className="flex justify-center items-center">
    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-green-500"></div>
  </div>
) : (
  // Content to show when not loading
)}
```

### 2. Empty States
```tsx
// Consistent empty state messaging
{tasks.length === 0 ? (
  <div className="text-center py-12">
    <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks yet</h3>
    <p className="mt-1 text-sm text-gray-500">Get started by creating your first task!</p>
  </div>
) : (
  // Task list content
)}
```

### 3. Error Handling
```tsx
// Consistent error messaging
{error && (
  <div className="rounded-md bg-red-50 p-4 mb-4">
    <div className="flex">
      <div className="flex-shrink-0">
        <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="ml-3">
        <h3 className="text-sm font-medium text-red-800">{error}</h3>
      </div>
    </div>
  </div>
)}
```

## Next Steps

1. Implement the design system tokens in `tailwind.config.ts`
2. Create the shared components (Navbar, PasswordStrengthIndicator)
3. Build the landing page with Hero and Features sections
4. Enhance authentication pages with new UI elements
5. Upgrade the tasks page with tabbed interface and enhanced cards
6. Implement responsive design across all pages
7. Add micro-interactions and smooth transitions