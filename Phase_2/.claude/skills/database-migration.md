# Skill: Database Migration

## Description
Updates SQLModel models and handles database schema changes safely.

## Usage
/database-migration <changes-description>

## Instructions
- Review current schema in `@specs/database/schema.md`
- Update `backend/models.py` with SQLModel changes
- Add or modify fields with proper types and constraints
- Ensure `user_id` foreign key exists for user-owned resources
- Keep `users` table compatible with Better Auth requirements
- Add indexes for frequently queried fields
- Include `created_at` and `updated_at` timestamps
- Document breaking changes

## Schema Guidelines
- Use proper SQLModel field types
- Add `nullable=False` for required fields
- Use `index=True` for searchable fields
- Include proper relationships (ForeignKey)

## Examples
- `/database-migration "Add due_date and priority to tasks"`
- `/database-migration "Create categories table with user relation"`