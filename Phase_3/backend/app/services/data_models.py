"""
Data models for OpenAI Agent behavior in Todo AI Chatbot

This module defines the core data models based on the data-model.md specifications:
- User Intent
- Task Reference
- Conversation Context
- Tool Chain
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class IntentType(Enum):
    """Type of action the user wants to perform"""
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"


@dataclass
class UserIntent:
    """
    Represents the user's desired action derived from natural language input.

    Attributes:
        intent_type: Type of action (string, values: "add_task", "list_tasks", "complete_task", "delete_task", "update_task")
        confidence_score: Confidence level in intent recognition (float, 0.0-1.0)
        parameters: Extracted parameters from user input (dict, varies by intent type)
        original_input: Raw user input for context (string)
    """
    intent_type: IntentType
    confidence_score: float
    parameters: Dict[str, Any] = field(default_factory=dict)
    original_input: str = ""

    def validate(self) -> bool:
        """Validate the User Intent entity"""
        if self.intent_type.value not in [item.value for item in IntentType]:
            raise ValueError(f"intent_type must be one of {[item.value for item in IntentType]}")

        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("confidence_score must be between 0.0 and 1.0")

        return True


@dataclass
class TaskReference:
    """
    Represents how a task is identified (by ID or by name/title) and resolved to an actual task.

    Attributes:
        identifier_type: How the task is identified (string, values: "id", "title", "partial_match")
        identifier_value: The actual value (int for ID, string for title)
        resolved_task_id: The actual task ID after resolution (int, nullable)
        confidence_score: Confidence in the match (float, 0.0-1.0)
    """
    identifier_type: str  # "id", "title", "partial_match"
    identifier_value: Any  # int for ID, str for title
    resolved_task_id: Optional[int] = None
    confidence_score: float = 1.0

    def validate(self) -> bool:
        """Validate the Task Reference entity"""
        valid_types = ["id", "title", "partial_match"]
        if self.identifier_type not in valid_types:
            raise ValueError(f"identifier_type must be one of {valid_types}")

        if self.identifier_value is None:
            raise ValueError("identifier_value must be provided")

        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("confidence_score must be between 0.0 and 1.0")

        return True


@dataclass
class ConversationContext:
    """
    Represents the ongoing dialogue state and user's task-related needs.

    Attributes:
        conversation_id: The current conversation (int)
        previous_intents: Recent user intents for context (list of Intent objects)
        active_tasks: Tasks currently being discussed (list of TaskReference objects)
        user_preferences: Personalization preferences (dict)
        context_summary: Brief summary of current conversation state (string)
    """
    conversation_id: int
    previous_intents: List[UserIntent] = field(default_factory=list)
    active_tasks: List[TaskReference] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    context_summary: str = ""

    def validate(self) -> bool:
        """Validate the Conversation Context entity"""
        if self.conversation_id <= 0:
            raise ValueError("conversation_id must be a positive integer")

        # Validate lists don't exceed reasonable limits
        if len(self.previous_intents) > 50:  # Reasonable limit
            raise ValueError("previous_intents list too long")

        if len(self.active_tasks) > 10:  # Reasonable limit
            raise ValueError("active_tasks list too long")

        return True


@dataclass
class ToolChainStep:
    """Represents a single step in a tool chain"""
    tool_name: str
    arguments: Dict[str, Any]


@dataclass
class ToolChain:
    """
    Represents sequences of MCP tool calls needed to fulfill complex user requests.

    Attributes:
        chain_id: Unique identifier for the chain (string)
        steps: Ordered list of tool calls to execute (list of ToolCall objects)
        status: Current status of the chain (string, values: "pending", "executing", "completed", "failed")
        results: Results from each step (list of dict)
        error_info: Error details if chain failed (dict, nullable)
    """
    chain_id: str
    steps: List[ToolChainStep] = field(default_factory=list)
    status: str = "pending"  # "pending", "executing", "completed", "failed"
    results: List[Dict[str, Any]] = field(default_factory=list)
    error_info: Optional[Dict[str, Any]] = None

    def validate(self) -> bool:
        """Validate the Tool Chain entity"""
        if not self.steps:
            raise ValueError("steps must be a non-empty list")

        valid_statuses = ["pending", "executing", "completed", "failed"]
        if self.status not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")

        if self.chain_id is None or self.chain_id.strip() == "":
            raise ValueError("chain_id must be provided and not empty")

        return True