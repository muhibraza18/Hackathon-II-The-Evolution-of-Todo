"""
Skill: Error Response Formatter
Purpose: Format errors into user-friendly messages
Reusable: Yes - used across all error handling
"""

from typing import Dict, Any

class ErrorFormatter:
    """Formats errors for user-friendly responses"""
    
    @staticmethod
    def format_error(error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Converts exceptions to friendly error responses
        """
        return {
            "error": True,
            "message": f"Sorry, something went wrong: {str(error)}",
            "context": context,
            "type": type(error).__name__
        }
    
    @staticmethod
    def format_validation_error(field: str, issue: str) -> Dict[str, Any]:
        """Formats validation errors"""
        return {
            "error": True,
            "message": f"Invalid {field}: {issue}",
            "type": "ValidationError"
        }