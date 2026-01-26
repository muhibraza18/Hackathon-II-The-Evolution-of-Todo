# Deployment Runbook: Todo AI Chatbot

## Pre-Deployment Checklist

- [ ] All integration tests passing
- [ ] Performance benchmarks met
- [ ] Security scan completed
- [ ] Backup of current production environment
- [ ] Rollback plan prepared
- [ ] Stakeholders notified of deployment window

## Backend (FastAPI) Deployment

### Railway Deployment

1. **Prepare Environment Variables**
   ```bash
   # Required variables
   DATABASE_URL=postgresql://username:password@host:port/database
   BETTER_AUTH_SECRET=your-secret-key
   OPENAI_API_KEY=your-openai-api-key
   ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

2. **Deploy to Railway**
   ```bash
   # Login to Railway
   npx railway login

   # Link to project
   npx railway link <project-id>

   # Deploy
   npx railway up
   ```

3. **Run Database Migrations**
   ```bash
   # Execute migration command in Railway console
   python -m alembic upgrade head
   ```

4. **Verify Health Check**
   ```bash
   curl https://your-backend-domain.railway.app/health
   # Should return: {"status": "ok", "timestamp": "..."}
   ```

### Render Deployment

1. **Prepare Environment Variables**
   - Set variables in Render dashboard:
     - `DATABASE_URL`
     - `BETTER_AUTH_SECRET`
     - `OPENAI_API_KEY`
     - `ALLOWED_ORIGINS`

2. **Deploy via Git**
   ```bash
   git push render main
   ```

3. **Run Migrations**
   - Execute via Render console or post-deploy hook:
   ```bash
   python -m alembic upgrade head
   ```

## MCP Server Deployment

1. **Deploy Alongside Backend**
   - MCP server runs as part of the same backend service
   - Shares database connection with backend
   - Exposes tool endpoints to the agent

2. **Verify Tool Endpoints**
   ```bash
   curl https://your-backend-domain/tools/health
   # Should return: {"status": "ok", "tools_registered": 5}
   ```

## Frontend (ChatKit) Deployment

### Vercel Deployment

1. **Add Domain to OpenAI Allowlist**
   - Go to https://platform.openai.com/settings/organization/security/domain-allowlist
   - Add your Vercel domain (e.g., `your-app.vercel.app`)

2. **Configure Environment Variables in Vercel**
   - `NEXT_PUBLIC_API_URL`: Your backend URL (e.g., `https://your-backend.railway.app`)
   - `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`: Domain key from OpenAI (after allowlist approval)

3. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm install -g vercel

   # Deploy
   vercel --prod
   ```

### Netlify Deployment

1. **Add Domain to OpenAI Allowlist**
   - Add your Netlify domain (e.g., `your-app.netlify.app`)

2. **Configure Environment Variables in Netlify**
   - In Netlify dashboard, go to Site settings → Build & deploy → Environment
   - Add:
     - `NEXT_PUBLIC_API_URL`: Your backend URL
     - `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`: Domain key from OpenAI

3. **Deploy via Git Integration**
   - Connect your repository to Netlify
   - Configure build settings:
     - Build command: `npm run build`
     - Publish directory: `dist` or `build`

## Post-Deployment Verification

### Backend Verification
```bash
# 1. Check health endpoint
curl https://your-backend-domain/health

# 2. Test auth endpoint
curl -X POST https://your-backend-domain/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "TempPass123!"}'

# 3. Verify database connectivity
curl https://your-backend-domain/api/db/status
```

### Frontend Verification
1. Visit the deployed frontend URL
2. Complete registration flow
3. Send a test message to verify chat functionality
4. Verify logout functionality

### MCP Server Verification
```bash
# 1. Check tool endpoints
curl https://your-backend-domain/api/tools/list

# 2. Test a sample tool call
curl -X POST https://your-backend-domain/api/tools/add_task \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "title": "Test task"}'
```

## Rollback Procedure

### Backend Rollback
1. **Identify previous working version**
   ```bash
   git log --oneline -10
   ```

2. **Deploy previous version**
   - Via Railway/Render dashboard or CLI

3. **Revert database migrations if needed**
   ```bash
   # For specific migration
   python -m alembic downgrade <previous_revision_id>
   ```

### Frontend Rollback
1. **Deploy previous build**
   - Via Vercel/Netlify dashboard
   - Or roll back to previous commit and redeploy

## Monitoring and Alerts

### Health Checks
- Backend: `/health` endpoint (every 5 minutes)
- Frontend: Homepage load (every 5 minutes)
- Database: Connection test (every 10 minutes)

### Performance Monitoring
- Chat response times >2s (alert threshold)
- Authentication response times >500ms (alert threshold)
- Database query times >100ms (alert threshold)

### Error Monitoring
- 5xx error rates >1% (alert threshold)
- Authentication failures >5% of requests (alert threshold)

## Troubleshooting Common Issues

### 401 Unauthorized on Chat Endpoint
1. Check if token exists in localStorage
2. Verify Authorization header format
3. Confirm token is not expired
4. Check if backend ALLOWED_ORIGINS includes frontend domain

### Agent Doesn't Call Correct Tool
1. Review system prompt configuration
2. Verify MCP tools are registered correctly
3. Check OpenAI API key validity
4. Examine agent logs for intent recognition issues

### Conversation Not Persisting
1. Verify conversation_id is stored correctly
2. Check database connection
3. Confirm message table has records
4. Review backend logs for session management

### ChatKit Not Loading
1. Confirm OPENAI_DOMAIN_KEY is set correctly
2. Verify domain is in OpenAI allowlist
3. Check if API_URL points to correct backend
4. Verify CORS configuration allows frontend domain

## Emergency Contacts
- Development Team: [email/phone]
- Infrastructure Team: [email/phone]
- On-Call Schedule: [link]

## Deployment Schedule
- Production deployments: Weekdays 9 AM - 3 PM (your timezone)
- Notification: 30 minutes before deployment
- Maintenance window: 1 hour (extendable if needed)