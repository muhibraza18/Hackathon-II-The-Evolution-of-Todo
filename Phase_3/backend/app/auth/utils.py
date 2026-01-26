"""
Authentication utility functions for password hashing, token generation, and validation.
"""

import bcrypt
import secrets
import re
from typing import Dict, Any
from datetime import datetime, timedelta


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with 12 rounds"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    try:
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        return False


def generate_session_token() -> str:
    """Generate a secure random session token (32 bytes = 43 chars in base64)"""
    return secrets.token_urlsafe(32)


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    if not email or len(email) > 254:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password: Password to validate
        
    Returns:
        Dict with 'strong' boolean and 'message' string
    """
    if not password:
        return {
            'strong': False,
            'message': 'Password is required'
        }
    
    if len(password) < 8:
        return {
            'strong': False,
            'message': 'Password must be at least 8 characters long'
        }
    
    if not re.search(r'[A-Z]', password):
        return {
            'strong': False,
            'message': 'Password must contain at least one uppercase letter'
        }
    
    if not re.search(r'[a-z]', password):
        return {
            'strong': False,
            'message': 'Password must contain at least one lowercase letter'
        }
    
    if not re.search(r'\d', password):
        return {
            'strong': False,
            'message': 'Password must contain at least one digit'
        }
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return {
            'strong': False,
            'message': 'Password must contain at least one special character'
        }
    
    return {
        'strong': True,
        'message': 'Password meets all requirements'
    }


class RateLimiter:
    """Simple in-memory rate limiter for login attempts"""
    
    def __init__(self, max_attempts: int = 10, window_minutes: int = 1):
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes
        self.attempts: Dict[str, list] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed based on rate limit.
        
        Args:
            identifier: IP address or user identifier
            
        Returns:
            True if allowed, False if rate limit exceeded
        """
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=self.window_minutes)
        
        # Clean old attempts
        if identifier in self.attempts:
            self.attempts[identifier] = [
                timestamp for timestamp in self.attempts[identifier]
                if timestamp > cutoff
            ]
        else:
            self.attempts[identifier] = []
        
        # Check if limit exceeded
        if len(self.attempts[identifier]) >= self.max_attempts:
            return False
        
        # Add current attempt
        self.attempts[identifier].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(max_attempts=10, window_minutes=1)




# """
# Utilities for authentication functionality in Todo AI Chatbot.

# This module contains password hashing, token generation, email validation,
# and rate limiting utilities for the authentication system.
# """

# import bcrypt
# import secrets
# import re
# from datetime import datetime, timedelta
# from typing import Dict, List, Optional
# from collections import defaultdict


# def hash_password(password: str, rounds: int = 12) -> str:
#     """
#     Hash a password using bcrypt with specified rounds.

#     Args:
#         password: Plain text password to hash
#         rounds: Number of bcrypt rounds (default 12 for security)

#     Returns:
#         Hashed password as string
#     """
#     salt = bcrypt.gensalt(rounds=rounds)
#     hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed.decode('utf-8')


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verify a plain password against a hashed password.

#     Args:
#         plain_password: Plain text password to verify
#         hashed_password: Previously hashed password

#     Returns:
#         True if password matches, False otherwise
#     """
#     return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# def generate_session_token(length: int = 32) -> str:
#     """
#     Generate a cryptographically secure session token.

#     Args:
#         length: Length of token in bytes (default 32 for 256 bits of entropy)

#     Returns:
#         Random URL-safe string token
#     """
#     return secrets.token_urlsafe(length)


# def validate_email(email: str) -> bool:
#     """
#     Validate email format using regex.

#     Args:
#         email: Email address to validate

#     Returns:
#         True if valid format, False otherwise
#     """
#     pattern = r'^[^@]+@[^@]+\.[^@]+$'
#     return bool(re.match(pattern, email))


# def validate_password_strength(password: str) -> Dict[str, bool]:
#     """
#     Validate password strength requirements.

#     Args:
#         password: Password to validate

#     Returns:
#         Dictionary with validation results for each requirement
#     """
#     results = {
#         'length': len(password) >= 8,
#         'has_uppercase': any(c.isupper() for c in password),
#         'has_lowercase': any(c.islower() for c in password),
#         'has_digit': any(c.isdigit() for c in password),
#         'has_special': any(not c.isalnum() for c in password)
#     }

#     # Overall strength is True if all requirements are met
#     results['strong'] = all(results.values())

#     return results


# # Simple in-memory rate limiter for auth endpoints
# class RateLimiter:
#     """
#     Simple in-memory rate limiter for authentication endpoints.
#     Note: This doesn't persist across server restarts - for Phase III simplicity.
#     """

#     def __init__(self, max_attempts: int = 10, window_minutes: int = 1):
#         self.max_attempts = max_attempts
#         self.window_seconds = window_minutes * 60
#         self.attempts: Dict[str, List[datetime]] = defaultdict(list)

#     def is_allowed(self, identifier: str) -> bool:
#         """
#         Check if the identifier is allowed to make a request.

#         Args:
#             identifier: Unique identifier (e.g., IP address or user ID)

#         Returns:
#             True if allowed, False if rate limit exceeded
#         """
#         now = datetime.utcnow()

#         # Remove old attempts outside the window
#         self.attempts[identifier] = [
#             attempt for attempt in self.attempts[identifier]
#             if (now - attempt).seconds < self.window_seconds
#         ]

#         # Check if we're under the limit
#         if len(self.attempts[identifier]) < self.max_attempts:
#             self.attempts[identifier].append(now)
#             return True

#         return False

#     def reset_attempts(self, identifier: str):
#         """
#         Reset rate limit attempts for an identifier.

#         Args:
#             identifier: Unique identifier to reset
#         """
#         if identifier in self.attempts:
#             del self.attempts[identifier]


# # Global rate limiter instance
# rate_limiter = RateLimiter()