# Data Model: Modern UI Redesign for Taskify

**Feature Branch**: `004-modern-ui-redesign` | **Date**: 2026-01-09 | **Spec**: ../004-modern-ui-redesign/spec.md

## Overview

This document defines the data models for the new UI components and enhanced features in the Taskify modern UI redesign. The models build upon the existing authentication and task management systems while adding new data structures for the enhanced user interface elements.

## New UI Component Data Models

### 1. Password Strength Indicator

**Purpose**: Track and display password strength in real-time during signup

```typescript
interface PasswordStrength {
  score: number; // 0-4 representing (0: "Weak", 1: "Medium", 2: "Strong", 3: "Very Strong")
  label: "Weak" | "Medium" | "Strong" | "Very Strong"; // Human-readable label
  color: "red" | "yellow" | "green" | "dark-green"; // Color for visual indicator
  feedback: string[]; // Array of feedback items for password improvement
  isValid: boolean; // Whether password meets minimum requirements
}

interface PasswordCriteria {
  minLength: boolean; // Length >= 8
  hasUppercase: boolean; // Contains uppercase letter
  hasLowercase: boolean; // Contains lowercase letter
  hasNumber: boolean; // Contains number
  hasSpecialChar: boolean; // Contains special character
}
```

**Validation Logic**:
- Weak: <8 characters
- Medium: 8+ characters
- Strong: 8+ characters + uppercase + lowercase + number
- Very Strong: 8+ characters + uppercase + lowercase + number + special character

### 2. Navigation State

**Purpose**: Manage navigation state including authentication status and mobile menu

```typescript
interface NavigationState {
  isAuthenticated: boolean; // Whether user is currently authenticated
  user?: {
    id: string;
    name: string;
    email: string;
    avatar?: string; // User avatar URL
  };
  currentPage: string; // Current page for active link highlighting
  isMobileMenuOpen: boolean; // Mobile menu open/closed state
  isScrolled: boolean; // Whether navbar should have scrolled appearance
}

interface NavItem {
  id: string; // Unique identifier for the navigation item
  label: string; // Display text for the navigation item
  href: string; // Destination URL
  isActive: boolean; // Whether this item is the current page
  requiresAuth: boolean; // Whether this page requires authentication
  icon?: string; // Optional icon name (for mobile menu)
}
```

### 3. Task Display Enhancement

**Purpose**: Enhanced data model for improved task display with additional UI elements

```typescript
interface EnhancedTask extends Task {
  // Inherit all properties from existing Task model
  priority: 'low' | 'medium' | 'high' | 'urgent'; // Priority level for color coding
  dueDate?: string; // Due date in ISO format
  isOverdue: boolean; // Whether task is past due
  category?: string; // Optional category for filtering
  tags?: string[]; // Optional tags for organization
  isExpanded: boolean; // Whether task details are expanded
}

interface TaskTabState {
  activeTab: 'today' | 'pending' | 'overdue'; // Currently selected tab
  todayCount: number; // Number of tasks due today
  pendingCount: number; // Number of pending tasks
  overdueCount: number; // Number of overdue tasks
}

interface TaskFilterOptions {
  showCompleted: boolean; // Whether to show completed tasks
  priorityFilter: 'all' | 'low' | 'medium' | 'high' | 'urgent';
  categoryFilter?: string; // Filter by specific category
  searchQuery: string; // Text search query
}
```

### 4. Landing Page Content

**Purpose**: Structured data for landing page sections

```typescript
interface LandingPageData {
  hero: {
    title: string; // "Organize Your Life with Taskify"
    subtitle: string; // Supporting subheading text
    ctaText: string; // "Get Started" or similar
    ctaLink: string; // Link destination for CTA button
    backgroundImage?: string; // Optional background image URL
  };
  features: FeatureCard[];
  testimonials?: Testimonial[];
  faq?: FAQItem[];
}

interface FeatureCard {
  id: string; // Unique identifier
  title: string; // Feature title
  description: string; // Feature description
  icon?: string; // Optional icon name
  imageUrl?: string; // Optional feature image
}

interface Testimonial {
  id: string; // Unique identifier
  quote: string; // Testimonial text
  author: string; // Person's name
  role?: string; // Person's role or company
  avatar?: string; // Avatar image URL
}

interface FAQItem {
  id: string; // Unique identifier
  question: string; // FAQ question
  answer: string; // FAQ answer
  category?: string; // Optional category for grouping
}
```

### 5. Responsive Design Configuration

**Purpose**: Configuration for responsive design breakpoints and behavior

```typescript
interface ResponsiveConfig {
  breakpoints: {
    sm: number; // Small screens (mobile): 640px
    md: number; // Medium screens (tablet): 768px
    lg: number; // Large screens (desktop): 1024px
    xl: number; // Extra large screens: 1280px
  };
  layout: {
    mobile: MobileLayoutConfig;
    tablet: TabletLayoutConfig;
    desktop: DesktopLayoutConfig;
  };
}

interface MobileLayoutConfig {
  navStyle: 'hamburger' | 'bottom-tabs' | 'drawer';
  gridColumns: number; // Number of columns in grid layouts
  fontSizeScale: number; // Scale factor for font sizes
  spacingScale: number; // Scale factor for spacing
}

interface TabletLayoutConfig {
  navStyle: 'top-bar' | 'side-bar' | 'hybrid';
  gridColumns: number;
  fontSizeScale: number;
  spacingScale: number;
}

interface DesktopLayoutConfig {
  navStyle: 'top-bar' | 'side-bar' | 'hybrid';
  gridColumns: number;
  fontSizeScale: number;
  spacingScale: number;
}
```

### 6. Animation and Interaction States

**Purpose**: Track animation states for micro-interactions and transitions

```typescript
interface AnimationState {
  hoverElement?: string; // ID of currently hovered element
  activeElement?: string; // ID of currently active (pressed) element
  transitionStage: 'enter' | 'active' | 'exit' | 'idle'; // Current transition stage
  fadeInElements: string[]; // Elements currently fading in
  slideInElements: string[]; // Elements currently sliding in
}

interface LoadingState {
  isLoading: boolean; // Global loading state
  loadingMessage?: string; // Optional loading message
  loadingElements: string[]; // Specific elements currently loading
}
```

## Integration with Existing Models

### Authentication Context Extension
The new UI components will extend the existing AuthContext with additional properties:

```typescript
interface ExtendedAuthContext extends AuthContext {
  // Inherit all existing properties
  userAvatar?: string; // User avatar URL for navbar display
  lastLoginTime?: string; // For welcome messages
  unreadNotifications: number; // For notification badge
}
```

### Task API Response Enhancement
The existing Task API responses will be enhanced with additional UI-specific fields:

```typescript
interface EnhancedTaskResponse extends TaskResponse {
  // Inherit all existing properties
  priority: 'low' | 'medium' | 'high' | 'urgent';
  isOverdue: boolean;
  formattedDueDate?: string; // Human-readable due date
}
```

## Design System Tokens

### Color Palette
```typescript
interface ColorTokens {
  primary: {
    DEFAULT: '#22c55e'; // Primary green
    50: '#f0fdf4'; // Lightest shade
    100: '#dcfce7';
    200: '#bbf7d0';
    300: '#86efac';
    400: '#4ade80';
    500: '#22c55e'; // Base color
    600: '#16a34a';
    700: '#15803d';
    800: '#166534';
    900: '#14532d';
  };
  secondary: {
    blue: '#3b82f6';
    purple: '#8b5cf6';
    amber: '#f59e0b';
  };
  neutral: {
    50: '#fafafa';
    100: '#f5f5f5';
    200: '#e5e5e5';
    300: '#d4d4d4';
    400: '#a3a3a3';
    500: '#737373';
    600: '#525252';
    700: '#404040';
    800: '#262626';
    900: '#171717';
  };
}
```

### Typography Scale
```typescript
interface TypographyTokens {
  sizes: {
    xs: { fontSize: '0.75rem', lineHeight: '1rem' };
    sm: { fontSize: '0.875rem', lineHeight: '1.25rem' };
    base: { fontSize: '1rem', lineHeight: '1.5rem' };
    lg: { fontSize: '1.125rem', lineHeight: '1.75rem' };
    xl: { fontSize: '1.25rem', lineHeight: '1.75rem' };
    '2xl': { fontSize: '1.5rem', lineHeight: '2rem' };
    '3xl': { fontSize: '1.875rem', lineHeight: '2.25rem' };
    '4xl': { fontSize: '2.25rem', lineHeight: '2.5rem' };
    '5xl': { fontSize: '3rem', lineHeight: '1' };
    '6xl': { fontSize: '3.75rem', lineHeight: '1' };
  };
  weights: {
    thin: 100;
    extralight: 200;
    light: 300;
    normal: 400;
    medium: 500;
    semibold: 600;
    bold: 700;
    extrabold: 800;
    black: 900;
  };
}
```

## Validation Rules

### Password Strength Validation
- Minimum length: 8 characters for "Medium" rating
- Uppercase requirement: At least one uppercase letter for "Strong" rating
- Lowercase requirement: At least one lowercase letter for "Strong" rating
- Number requirement: At least one number for "Strong" rating
- Special character: At least one special character for "Very Strong" rating

### Responsive Behavior Validation
- Mobile navigation must collapse at 640px width
- Tablet layouts should use 2-column grids where appropriate
- Desktop layouts should use multi-column layouts with max-width of 1280px
- All interactive elements must have minimum touch target of 44px

### Accessibility Compliance
- All color combinations must meet WCAG AA contrast ratios (4.5:1 for normal text)
- Keyboard navigation must be fully supported for all interactive elements
- ARIA attributes must be properly implemented for screen readers
- Focus indicators must be visible for all interactive elements