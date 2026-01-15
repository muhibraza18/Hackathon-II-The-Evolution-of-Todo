"""
Intent Recognition Module for OpenAI Agent Behavior

This module implements the intent recognition patterns mapping trigger phrases to tool selection,
based on the specification requirements and research.md decisions.
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum
import re
from .data_models import IntentType



class IntentRecognizer:
    """Class for recognizing user intent from natural language input"""

    def __init__(self):
        # Intent recognition patterns from spec.md
        self.patterns = {
            IntentType.ADD_TASK: [
                r"(?:add|create|make|set up|establish|put in|include|enter)\s+(?:a\s+)?(?:task|todo|thing|item)\s+(?:to\s+)?",
                r"(?:add|create|remember|note|keep track of|i need to|remind me to|don't forget to)\s+",
                r"(?:make|create)\s+(?:a\s+)?(?:task|todo)\s+(?:for|to|that)\s+",
                r"add\s+(?!task)(?=\w)",
                r"create\s+(?!task)(?=\w)",
                r"i\s+need\s+to\s+",
                r"remind\s+me\s+(?:to|about)\s+",
                r"don't\s+forget\s+(?:to|about)\s+"
            ],

            IntentType.LIST_TASKS: [
                r"(?:show|list|display|see|view|tell me|what are|give me)\s+(?:my\s+)?(?:all\s+)?(?:tasks|todos|things|items)",
                r"(?:show|list|what|see|display|view)\s+(?:my\s+)?(?:pending|completed|done|all)\s+(?:tasks|todos|things)",
                r"what'?s?\s+(?:on\s+)?(?:my\s+)?(?:list|todo|tasks|todos)",
                r"list\s+(?:everything|all|my)\s+(?:tasks|todos)",
                r"(?:my\s+)?(?:tasks|todos|list|things)\s+(?:are|look like|show)",
                r"what\s+(?:do\s+i\s+have|am\s+i\s+supposed\s+to|should\s+i\s+)"
            ],

            IntentType.COMPLETE_TASK: [
                r"(?:mark|make|set|put|turn)\s+(?:task|it|the|this)\s+(?:as\s+)?(?:done|completed|finished|complete)",
                r"(?:i'?m\s+done|done\s+with|finished\s+with|complete|finish)\s+(?:task|the|this|that)",
                r"task\s+(\d+)\s+(?:is|are)\s+(?:done|completed|finished)",
                r"complete\s+(?:task|the|this|that)",
                r"check\s+(?:off|it|the)\s+(?:task|it|the)",
                r"finished\s+(?:with|doing|working on)\s+(?:task|the|this|that)"
            ],

            IntentType.DELETE_TASK: [
                r"(?:delete|remove|eliminate|get rid of|clear|cancel|trash|erase)\s+(?:task|the|this|that)",
                r"remove\s+(?:from|off)\s+(?:my\s+)?(?:list|tasks|todos)",
                r"delete\s+(?:task|it|the)",
                r"get\s+rid\s+of\s+(?:task|the|this|that)",
                r"cancel\s+(?:task|the|this|that)",
                r"clear\s+(?:completed|done|finished)\s+(?:tasks|todos)"
            ],

            IntentType.UPDATE_TASK: [
                r"(?:change|update|edit|modify|revise|alter|adjust)\s+(?:task|the|this|that)",
                r"(?:rename|switch|swap|replace)\s+(?:task|the|this|that)",
                r"update\s+(?:the|my)\s+(?:title|description|details?)\s+(?:of|for|to)",
                r"change\s+(?:the|my)\s+(?:title|description|details?)\s+(?:of|for|to)",
                r"edit\s+(?:the|my)\s+(?:task|title|description)"
            ]
        }

        # Additional pattern variants for better recognition
        self.variant_patterns = {
            IntentType.ADD_TASK: [
                r"add\s+(?!task|list)(?=\w)",  # "add buy groceries"
                r"create\s+(?!task|list)(?=\w)",  # "create meeting"
                r"remind\s+me",  # "remind me call mom"
                r"don't\s+forget"  # "don't forget doctor"
            ],

            IntentType.LIST_TASKS: [
                r"show\s+(?!me)(?=\w)",  # "show pending"
                r"what'?s\s+(?:on\s+)?my",  # "what's on my list"
                r"my\s+tasks",  # "my tasks"
                r"list\s+(?!tasks)(?=\w)"  # "list pending"
            ],

            IntentType.COMPLETE_TASK: [
                r"done\s+with",  # "done with task"
                r"i'?m\s+done",  # "I'm done with..."
                r"finish(?:ed)?\s+(?:with|doing)",  # "finish with task"
                r"task\s+\d+"  # "task 5" (when context suggests completion)
            ],

            IntentType.DELETE_TASK: [
                r"delete\s+(?!task)(?=\w)",  # "delete meeting"
                r"remove\s+(?!from)(?=\w)",  # "remove appointment"
                r"cancel\s+(?!meeting)(?=\w)"  # "cancel task"
            ],

            IntentType.UPDATE_TASK: [
                r"change\s+(?!to)(?=\w)",  # "change meeting time"
                r"update\s+(?!list)(?=\w)",  # "update title"
                r"edit\s+(?!profile)(?=\w)"  # "edit task"
            ]
        }

        # Confidence scores for different pattern matches
        self.confidence_weights = {
            "exact_phrase": 0.95,
            "keyword_match": 0.85,
            "pattern_match": 0.75,
            "contextual_match": 0.65,
            "fuzzy_match": 0.55
        }

    def recognize_intent(self, user_input: str) -> Tuple[IntentType, float, Dict[str, str]]:
        """
        Recognize the user's intent from their input

        Args:
            user_input: The raw user input string

        Returns:
            Tuple of (intent_type, confidence_score, extracted_parameters)
        """
        user_input_lower = user_input.lower().strip()

        # Check if the input is a greeting first
        greeting_patterns = [
            r"hi", r"hello", r"hey", r"greetings", r"good morning",
            r"good afternoon", r"good evening", r"what's up", r"howdy"
        ]

        # Don't return early for greetings since we handle them separately in the agent
        # Just continue with normal intent recognition

        # First, try to extract any potential task IDs from the input
        task_id = self._extract_task_id(user_input_lower)

        # Check each intent type for matches
        best_match = (IntentType.LIST_TASKS, 0.1, {})  # Default fallback

        for intent_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower, re.IGNORECASE)
                if match:
                    # Calculate confidence based on pattern strength
                    confidence = min(best_match[1] + 0.2, 0.9)  # Boost confidence

                    # Extract parameters if applicable
                    params = {}
                    if task_id:
                        params['task_id'] = str(task_id)

                    # Extract title if it's an add/update task
                    if intent_type in [IntentType.ADD_TASK, IntentType.UPDATE_TASK]:
                        title = self._extract_task_title(user_input_lower, intent_type)
                        if title:
                            params['title'] = title

                    if confidence > best_match[1]:
                        best_match = (intent_type, confidence, params)

        # Also check variant patterns
        for intent_type, patterns in self.variant_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower, re.IGNORECASE)
                if match:
                    # Lower confidence for variant patterns
                    confidence = min(best_match[1] + 0.15, 0.85)

                    # Extract parameters
                    params = {}
                    if task_id:
                        params['task_id'] = str(task_id)

                    if intent_type in [IntentType.ADD_TASK, IntentType.UPDATE_TASK]:
                        title = self._extract_task_title(user_input_lower, intent_type)
                        if title:
                            params['title'] = title

                    if confidence > best_match[1]:
                        best_match = (intent_type, confidence, params)

        # If no strong matches found, return default with low confidence
        if best_match[1] < 0.3:
            return (IntentType.LIST_TASKS, 0.2, {})

        return best_match

    def _extract_task_id(self, user_input: str) -> Optional[int]:
        """Extract task ID from user input"""
        # Look for patterns like "task 5", "task #5", "#5", etc.
        patterns = [
            r"task\s+#?(\d+)",
            r"#(\d+)",
            r"task\s+(\d+)",
            r"no\.?\s*(\d+)",
            r"number\s+(\d+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue

        return None

    def _extract_task_title(self, user_input: str, intent_type: IntentType) -> Optional[str]:
        """Extract task title from user input based on intent type"""
        user_input_clean = user_input.strip()

        # Remove common intent phrases to isolate the title
        if intent_type == IntentType.ADD_TASK:
            # Remove common add phrases
            phrases_to_remove = [
                r"(?:add|create|remember|i need to|remind me to|don't forget to)\s+",
                r"(?:a\s+)?(?:task|todo|thing|item)\s+(?:to\s+)?"
            ]

            for phrase in phrases_to_remove:
                user_input_clean = re.sub(phrase, "", user_input_clean, flags=re.IGNORECASE)

        elif intent_type == IntentType.UPDATE_TASK:
            # Remove common update phrases
            phrases_to_remove = [
                r"(?:change|update|edit|modify|rename)\s+(?:task|the|this|that)\s+",
                r"(?:the\s+)?(?:title|description)\s+(?:of\s+|to\s+|for\s+)?"
            ]

            for phrase in phrases_to_remove:
                user_input_clean = re.sub(phrase, "", user_input_clean, flags=re.IGNORECASE)

        # Clean up the remaining text
        user_input_clean = user_input_clean.strip(" .,!?")

        # If there's meaningful text left, consider it the title
        if user_input_clean and len(user_input_clean) >= 2:
            # Limit to reasonable length
            return user_input_clean[:100]  # Cap at 100 characters

        return None

    def get_intent_confidence_thresholds(self) -> Dict[str, float]:
        """Get confidence thresholds for different actions (per research.md decision 2)"""
        return {
            "high_confidence": 0.8,    # Proceed directly
            "medium_confidence": 0.6,  # Ask for clarification
            "low_confidence": 0.3      # Definitely ask for clarification
        }


# Global instance of the intent recognizer
intent_recognizer = IntentRecognizer()