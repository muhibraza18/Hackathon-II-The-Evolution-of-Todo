# Todo AI Chatbot Frontend

A React-based frontend for the Todo AI Chatbot with Google Gemini AI integration and secure authentication.

## Features

- User registration and login with secure token management
- Real-time chat interface with AI assistant
- Task management through natural language conversations
- Session persistence across page refreshes
- Responsive design for all device sizes

## Prerequisites

- Node.js 18+ installed
- Access to the backend API (FastAPI server from Step 4/6)
- Backend API with Google Gemini integration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment configuration:
```bash
cp .env.example .env
```

4. Update the `.env` file with your configuration:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
NEXT_PUBLIC_GEMINI_ENABLED=true  # Enable Gemini integration
```

## Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Production Build

Build the application for production:
```bash
npm run build
```

Serve the production build:
```bash
npm run preview
```

## Configuration

### Backend Configuration

1. Ensure backend API is running with Google Gemini integration
2. Configure the API URL in environment variables
3. Set up Google Gemini API key in the backend

### Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_GEMINI_ENABLED`: Enable Google Gemini integration (default: true)

## Deployment

### Vercel

The application is optimized for deployment on Vercel:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "NEXT_PUBLIC_API_URL": "https://your-backend.com",
    "NEXT_PUBLIC_GEMINI_ENABLED": "true"
  }
}
```

### Other Platforms

For Netlify or GitHub Pages, ensure environment variables are properly configured in the deployment settings.

## API Integration

The frontend communicates with the backend API for:
- User authentication (registration, login, logout)
- Chat message processing
- Task management operations

All API requests include authentication tokens in the Authorization header.

## Security Considerations

- Authentication tokens are stored in localStorage with 7-day expiration
- All API requests include proper authentication headers
- Input validation is performed before API calls
- XSS prevention is implemented for message display
- Secure communication with HTTPS in production

## Architecture

- React with Vite for fast development
- Custom authentication context for state management
- Service modules for API and chat functionality
- Hooks for reusable logic
- Component-based architecture

## Support

For support, please contact the development team or refer to the documentation.