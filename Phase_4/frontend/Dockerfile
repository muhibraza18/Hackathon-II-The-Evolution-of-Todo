# Multi-stage build for Next.js frontend
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

# Copy source files (but .dockerignore will exclude .env.local)
COPY . .

# Set build-time arguments for environment variables
ARG NEXT_PUBLIC_API_URL="http://localhost:8000"
ARG NEXT_PUBLIC_GEMINI_ENABLED=false

# CRITICAL: Set these BEFORE npm run build
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_GEMINI_ENABLED=$NEXT_PUBLIC_GEMINI_ENABLED

# Build with the API URL
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production && npm cache clean --force

# Set environment variables for runtime with defaults (build-time variables are already set)
# For container runtime, these can be overridden but won't affect the bundled code
ENV NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
ENV NEXT_PUBLIC_GEMINI_ENABLED=false

# Copy built application from builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/package.json ./
COPY --from=builder /app/vercel.json ./

# Expose port
EXPOSE 3000

# Health check with longer start period
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Start the application
CMD ["npm", "start"]