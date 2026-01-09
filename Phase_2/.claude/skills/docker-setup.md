# Skill: Docker Setup

## Description
Creates or updates Docker configuration for the monorepo.

## Usage
/docker-setup

## Instructions
- Create `docker-compose.yml` in root directory
- Add services: frontend, backend, database (optional for local dev)
- Configure environment variables
- Set up port mappings:
  - Frontend: 3000:3000
  - Backend: 8000:8000
- Add volume mounts for hot-reload during development
- Configure networks for service communication
- Reference `@CLAUDE.md` for project structure

## Docker Compose Structure
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
    volumes:
      - ./backend:/app
```

## Examples
- `/docker-setup`