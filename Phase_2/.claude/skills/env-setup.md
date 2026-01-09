# Skill: Environment Setup

## Description
Creates or updates environment configuration files for frontend and backend.

## Usage
/env-setup <part>

## Instructions
### For `frontend`:
- Create/update `frontend/.env.local`
- Add required environment variables:
  - `NEXT_PUBLIC_API_URL` - Backend API URL
  - `BETTER_AUTH_SECRET` - JWT secret key (same as backend)
  - `BETTER_AUTH_URL` - Frontend URL for Better Auth
  - `DATABASE_URL` - Neon PostgreSQL connection (for Better Auth)
- Create `.env.example` template for reference
- Add `.env.local` to `.gitignore`

### For `backend`:
- Create/update `backend/.env`
- Add required environment variables:
  - `DATABASE_URL` - Neon PostgreSQL connection string
  - `BETTER_AUTH_SECRET` - JWT secret key (same as frontend)
  - `CORS_ORIGINS` - Allowed frontend origins
  - `JWT_ALGORITHM` - JWT algorithm (usually HS256)
- Create `.env.example` template for reference
- Add `.env` to `.gitignore`

## Security Notes
- Never commit actual `.env` files to git
- Use different secrets for development and production
- Keep `BETTER_AUTH_SECRET` identical in frontend and backend
- Use strong random strings for secrets (32+ characters)

## Examples
- `/env-setup frontend`
- `/env-setup backend`