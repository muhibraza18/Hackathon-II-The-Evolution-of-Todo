"""
Response Template Library for OpenAI Agent Behavior

This module provides templates for confirmation, error, and question responses
based on the research.md decisions and specification requirements.
"""

from typing import Dict, Any


class ResponseTemplateLibrary:
    """Library of response templates for the agent"""

    def __init__(self):
        # Confirmation templates (detailed with suggestions - per research.md decision 5)
        self.confirmation_templates = {
            "task_added": "✓ Added '{title}' to your list!",
            "task_completed": "✓ Marked '{title}' as complete!",
            "task_deleted": "✓ Removed '{title}' from your list!",
            "task_updated": "✓ Updated '{title}'!",
            "batch_operation": "✓ Completed {operation} for {count} tasks.",
            "greeting": "Hello! I'm your task management assistant. How can I help you today?",
            "help": "I can help you manage your tasks. You can ask me to add, list, complete, delete, or update tasks. Try saying 'Add a task to buy groceries' or 'Show me my tasks'."
        }

        # Error templates (hybrid with codes - per research.md decision 6)
        self.error_templates = {
            "task_not_found": "I couldn't find task #{task_id}. Would you like to see your current tasks? [Error: TASK_NOT_FOUND]",
            "invalid_input": "I wasn't able to understand your request. Could you rephrase that? [Error: INVALID_INPUT]",
            "multiple_tasks_found": "I found multiple tasks matching '{query}'. Could you specify which one you mean? [Error: AMBIGUOUS_REFERENCE]",
            "no_tasks_found": "You don't have any tasks matching '{query}'. Would you like to add a new task? [Error: NO_MATCH_FOUND]",
            "mcp_unavailable": "I'm having trouble connecting to my task management system. Could you try again in a moment? [Error: MCP_UNAVAILABLE]",
            "database_error": "Something went wrong while processing your request. Please try again. [Error: DB_ERROR]",
            "empty_list": "You don't have any tasks right now. Would you like to add a new task? [Error: EMPTY_LIST]",
            "missing_parameter": "I need more information to {action}. What should I {action}? [Error: MISSING_PARAM]"
        }

        # Question templates for clarifications
        self.question_templates = {
            "ambiguous_task": "Which task would you like to {action}? Could you tell me the task number or title?",
            "missing_details": "What {detail} would you like for this task?",
            "confirm_action": "Are you sure you want to {action} '{title}'?",
            "suggest_alternative": "I couldn't {action} that task. Would you like me to {alternative} instead?",
            "request_specifics": "Could you provide more details about the {aspect} you'd like to {action}?",
            "clarify_intent": "I want to make sure I understand. Are you asking me to {intent}?"
        }

        # Proactive suggestion templates
        self.suggestion_templates = {
            "clear_completed": "You have {count} completed tasks. Would you like me to clear them from your list?",
            "similar_tasks": "I noticed you have similar tasks: {tasks}. Would you like me to group them?",
            "follow_up": "Is there anything else I can help you with regarding your tasks?",
            "remind_action": "You marked '{task}' as complete. Would you like me to remind you about related tasks?",
            "optimize_list": "Your task list could be organized better. Would you like me to suggest categories?"
        }

        # List formatting templates
        self.list_templates = {
            "numbered_list": "{index}. {icon} {title}",
            "bulleted_list": "• {icon} {title}",
            "summary": "You have {pending_count} pending and {completed_count} completed tasks.",
            "grouped_list": "{status_title} ({count}):\n{items}"
        }

    def get_confirmation(self, action: str, **kwargs) -> str:
        """Get a confirmation response template"""
        template = self.confirmation_templates.get(action, "✓ {action} completed.")
        return template.format(**kwargs)

    def get_error(self, error_type: str, **kwargs) -> str:
        """Get an error response template"""
        template = self.error_templates.get(error_type, "An error occurred: {error_type}")
        return template.format(**kwargs)

    def get_question(self, question_type: str, **kwargs) -> str:
        """Get a question response template"""
        template = self.question_templates.get(question_type, "Could you clarify: {question_type}?")
        return template.format(**kwargs)

    def get_suggestion(self, suggestion_type: str, **kwargs) -> str:
        """Get a proactive suggestion template"""
        template = self.suggestion_templates.get(suggestion_type, "Would you like me to {suggestion_type}?")
        return template.format(**kwargs)

    def get_list_item(self, index: int, icon: str, title: str) -> str:
        """Get a formatted list item"""
        return self.list_templates["numbered_list"].format(index=index, icon=icon, title=title)

    def get_list_summary(self, pending_count: int, completed_count: int) -> str:
        """Get a summary of the task list"""
        return self.list_templates["summary"].format(
            pending_count=pending_count,
            completed_count=completed_count
        )


# Global instance of the response template library
response_templates = ResponseTemplateLibrary()