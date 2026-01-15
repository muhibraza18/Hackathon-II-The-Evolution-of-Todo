/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_GEMINI_ENABLED: process.env.NEXT_PUBLIC_GEMINI_ENABLED,
  },
  reactStrictMode: true,
  swcMinify: true,
}

module.exports = nextConfig