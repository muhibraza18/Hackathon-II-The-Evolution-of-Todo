/** @type {import('next').NextConfig} */
// CRITICAL: These env variables are substituted at build time
// For Kubernetes deployment, use http://backend-service:8000
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://backend-service:8000';

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Explicitly set environment variables for build-time substitution
  env: {
    NEXT_PUBLIC_API_URL: API_URL,
    NEXT_PUBLIC_GEMINI_ENABLED: process.env.NEXT_PUBLIC_GEMINI_ENABLED || 'false',
  },
  // Rewrite API requests to backend service (for local development and Kubernetes)
  // In development: rewrites to http://localhost:8000/api/*
  // In production: rewrites to http://backend-service:8000/api/*
  async rewrites() {
    const backendUrl = process.env.BACKEND_URL || API_URL;
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
}

// Debug: log the value to ensure it's being read correctly
console.log('🔧 next.config.js - NEXT_PUBLIC_API_URL will be set to:', API_URL);
console.log('🔧 next.config.js - Backend rewrites to:', process.env.BACKEND_URL || API_URL);

module.exports = nextConfig