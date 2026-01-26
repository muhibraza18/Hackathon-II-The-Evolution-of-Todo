"""
Authentication middleware for Todo AI Chatbot.

This module contains the authentication middleware that validates session tokens
and injects user_id into request context for protected endpoints.
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlmodel import select
from typing import Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import traceback

from ..database.models import SessionModel
from ..database.connection import get_db_session


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware to validate session tokens and inject user_id.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process incoming request and validate authentication if required.
        """
        # Allow OPTIONS requests (CORS preflight) to pass through
        if request.method == "OPTIONS":
            return await call_next(request)

        # Skip authentication for public endpoints
        if self._is_public_endpoint(request.url.path):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        token = self._extract_token_from_header(auth_header)

        if not token:
            print(f"❌ No token found in request to {request.url.path}")
            print(f"Authorization header: {auth_header}")
            print(f"About to set CORS headers for missing token response")
            # Create response with proper CORS headers
            try:
                response = JSONResponse(
                    status_code=401,
                    content={"detail": "Missing authentication token"}
                )
                print("Response object created successfully")

                # Add CORS headers to error response based on the incoming request
                origin = request.headers.get("Origin", "*")
                print(f"Origin from request: {origin}")
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Allow-Headers"] = request.headers.get(
                    "Access-Control-Request-Headers", "*"
                )
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD"
                print(f"All CORS headers set: {dict(response.headers)}")
                print(f"Header keys: {list(response.headers.keys())}")

                print("About to return response")
                result = response
                print("Returning response with headers")
                return result
            except Exception as e:
                print(f"Exception occurred: {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                # Fallback response without CORS headers (not ideal but functional)
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Missing authentication token"}
                )

        # Validate the session token
        user_id = self._validate_session_token(token)

        if not user_id:
            print(f"❌ Token validation failed for {request.url.path}")
            print(f"About to set CORS headers for invalid token response")
            # Create response with proper CORS headers
            response = JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired authentication token"}
            )
            try:
                # Add CORS headers to error response based on the incoming request
                origin = request.headers.get("Origin", "*")
                print(f"Origin from request: {origin}")
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Allow-Headers"] = request.headers.get(
                    "Access-Control-Request-Headers", "*"
                )
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD"
                print(f"All CORS headers set: {dict(response.headers)}")
                print(f"Header keys: {list(response.headers.keys())}")
            except Exception as e:
                print(f"Exception in setting headers: {e}")

            print("Returning response with headers")
            return response

        # Add user_id to request state for downstream handlers
        request.state.user_id = user_id
        print(f"✅ User {user_id} authenticated for {request.url.path}")

        return await call_next(request)

    def _is_public_endpoint(self, path: str) -> bool:
        """Check if the endpoint is public (doesn't require authentication)."""
        # Exact match paths (only root for now)
        exact_match_paths = ["/"]
        if path in exact_match_paths:
            return True

        # Prefix match paths
        prefix_paths = [
            "/health",
            "/api/auth/register",
            "/api/auth/login",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]
        return any(path.startswith(pub_path) for pub_path in prefix_paths)

    def _extract_token_from_header(self, auth_header: Optional[str]) -> Optional[str]:
        """Extract session token from Authorization header."""
        if not auth_header:
            return None

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]

    def _validate_session_token(self, token: str) -> Optional[int]:
        """Validate session token against database and check expiration."""
        print(f"🔍 Starting token validation for token: {token[:20]}...")

        db_gen = get_db_session()
        try:
            db = next(db_gen)
            print(f"✅ Got database session for token validation")

            # Query for the session with the given token
            statement = select(SessionModel).where(SessionModel.token == token)
            session_record = db.exec(statement).first()

            if not session_record:
                print(f"❌ No session found for token: {token[:20]}...")
                print(f"📝 Token length: {len(token)}, Token preview: {token[:30]}...")

                # Let's also try to check if there are any sessions in the database for debugging
                try:
                    all_sessions_result = db.exec(select(SessionModel))
                    all_sessions = all_sessions_result.all()
                    print(f"📊 Total sessions in DB: {len(all_sessions)}")

                    # Let's also check if there are sessions with similar beginning
                    similar_sessions_result = db.exec(select(SessionModel).where(
                        SessionModel.token.startswith(token[:10])
                    ))
                    similar_sessions = similar_sessions_result.all()
                    print(f"📊 Sessions with similar beginning: {len(similar_sessions)}")

                    # Let's also print a sample of tokens to see what's in the DB
                    if all_sessions:
                        print(f"📝 Sample tokens in DB: {[s.token[:20] + '...' for s in all_sessions[:5]]}")

                except Exception as e:
                    print(f"⚠️ Error checking session count: {e}")

                return None

            current_time = datetime.utcnow()
            print(f"✅ Session found for user_id: {session_record.user_id}")
            print(f"📅 Session expires at: {session_record.expires_at}")
            print(f"📅 Current time: {current_time}")
            print(f"⏰ Is expired: {session_record.expires_at < current_time}")

            if session_record.expires_at < current_time:
                print(f"❌ Session expired at {session_record.expires_at}")
                db.delete(session_record)
                db.commit()
                print(f"🗑️ Expired session deleted from database")
                return None

            print(f"✅ Valid session found for user_id: {session_record.user_id}")
            return session_record.user_id

        except SQLAlchemyError as e:
            print(f"❌ Database error during token validation: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error during token validation: {e}")
            return None
        finally:
            try:
                db.close()
                print(f"🔒 Database session closed")
            except Exception as close_error:
                print(f"⚠️ Error closing database session: {close_error}")