# Skill: Generate Plan

## Description
Breaks down a feature or phase into a detailed, actionable implementation plan.

## Usage
/generate-plan <feature-or-phase>

## Instructions
- Read the relevant spec(s) using `@specs/<path>.md`
- Output a numbered step-by-step plan following Agentic Dev Stack workflow
- Clearly separate concerns: database schema → backend API → frontend UI
- Include dependencies between steps
- Specify which files need to be created or modified
- Reference relevant documentation with `@frontend/CLAUDE.md` or `@backend/CLAUDE.md`

## Plan Structure
1. Database/Schema changes
2. Backend implementation (models, routes, logic)
3. Frontend implementation (components, pages, API calls)
4. Testing and validation

## Examples
- `/generate-plan "Implement authentication"`
- `/generate-plan "Phase 1: Core task management"`