# Skill: Write Spec

## Description
Creates or updates a Spec-Kit specification file in the /specs directory.

## Usage
/write-spec <path> <purpose>

## Instructions
- Write or update the markdown file at `specs/<path>.md`
- Use proper Spec-Kit conventions: headings, user stories, acceptance criteria
- Reference other specs with `@specs/...` when relevant
- Follow existing style and structure in the project
- Include sections: Overview, User Stories, Acceptance Criteria, Technical Notes

## Examples
- `/write-spec features/task-crud "Basic task CRUD operations"`
- `/write-spec database/schema "Database schema for tasks"`