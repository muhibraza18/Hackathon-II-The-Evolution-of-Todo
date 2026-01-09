# Skill: Responsive UI

## Description
Makes frontend UI responsive across mobile, tablet, and desktop using Tailwind CSS.

## Usage
/responsive-ui <target>

## Instructions
- Update specified page or component with Tailwind responsive classes
- Use mobile-first approach (base styles for mobile)
- Add breakpoints: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`
- Follow component patterns in `@frontend/components`
- Test breakpoints:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px
- Ensure touch-friendly targets (min 44x44px)
- Handle navigation for mobile (hamburger menu)
- Test with browser dev tools responsive mode

## Common Patterns
- Flex direction: `flex-col md:flex-row`
- Grid columns: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Padding: `p-4 md:p-6 lg:p-8`
- Text size: `text-sm md:text-base lg:text-lg`
- Hidden/visible: `hidden md:block`

## Examples
- `/responsive-ui "Task list page"`
- `/responsive-ui "Navigation component"`