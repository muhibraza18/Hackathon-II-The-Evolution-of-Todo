# Cache bust: v4 - 2026-02-08
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlmodel import select
from ..database.models import Conversation as ConversationModel, Message as MessageModel
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from .mcp_client import mcp_client
from .. import crud
from .data_models import (
    UserIntent, IntentType, TaskReference, ConversationContext,
    ToolChain, ToolChainStep
)
from .response_templates import response_templates
from .intent_recognition import intent_recognizer
from ..database.connection import get_async_db_session

# Load environment variables
load_dotenv()

# Initialize OpenAI client with Google Gemini API
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class AgentService:
    """Main service class for the AI Agent behavior (using Google Gemini via OpenAI-compatible API)"""

    def __init__(self):
        # System prompt template with user_id placeholder (detailed with examples - per research.md decision 1)
        self.system_prompt_template = """
        You are a helpful task management assistant. You help users manage their todo list through natural language.

        Available tools:

        add_task: Create new tasks
        list_tasks: View tasks (all/pending/completed)
        complete_task: Mark tasks as done
        delete_task: Remove tasks
        update_task: Modify task details

        Important:
        - Always pass the user_id parameter to every tool call
        - Confirm actions with friendly messages
        - If task title is mentioned but not ID, search first using list_tasks
        - Ask for clarification when requests are ambiguous
        - Only use actual tool results, never invent task data
        - Keep responses concise and helpful
        - Use checkmarks (✓) for successful actions
        - Format lists as numbered lists when showing multiple tasks
        - Start error responses with "I couldn't..." or "I wasn't able to..."
        - End questions with "?" and provide context
        - Be concise (1-3 sentences for simple confirmations, longer for lists/explanations)

        User ID: {user_id}
        """

    def get_system_prompt(self, user_id: str) -> str:
        """Return the system prompt with user_id filled in"""
        return self.system_prompt_template.format(user_id=user_id)

    async def process_chat_request(
        self,
        user_id: str,
        conversation_id: Optional[int],
        message: str,
        db: Session,
        auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat request by:
        1. Loading conversation history
        2. Creating a new user message
        3. Running the Google Gemini agent to generate a response
        4. Capturing any tool calls made by the agent
        5. Saving the assistant response
        6. Returning the response with tool call details

        Args:
            user_id: The authenticated user's ID
            conversation_id: Optional existing conversation ID
            message: The user's message
            db: Database session
            auth_token: Optional authentication token to pass to MCP server
        """
        # Store auth_token for use in MCP calls
        self._auth_token = auth_token

        # Step 1: Load or create conversation
        if conversation_id is None:
            # Create a new conversation
            conversation = ConversationModel(user_id=user_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            conversation_id = conversation.id
        else:
            # Verify conversation exists and belongs to user
            conversation_query = select(ConversationModel).where(
                ConversationModel.id == conversation_id,
                ConversationModel.user_id == user_id
            )
            conversation_result = db.exec(conversation_query)
            conversation = conversation_result.first()

            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found or doesn't belong to user {user_id}")

        # Step 2: Save user message to database
        user_message = MessageModel(
            user_id=user_id,
            conversation_id=conversation_id,
            role="user",
            content=message
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)

        # Step 3: Load conversation history for context
        # Get all messages in the conversation, ordered by creation time
        history_query = select(MessageModel).where(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.created_at)
        history_result = db.exec(history_query)
        messages = history_result.all()

        # Format messages for the agent
        formatted_history = []
        for msg in messages[:-1]:  # Exclude the current message we just added
            formatted_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add the current user message
        formatted_history.append({
            "role": "user",
            "content": message
        })

        # Step 4: Process the user's request using intent recognition and tool chaining
        tool_calls = []
        response_text = ""

        try:
            # Check if this is likely a greeting first
            import re
            message_lower = message.lower().strip()

            # Use word boundary matching to avoid partial matches like "hi" in "washing"
            greeting_patterns = [
                r'\bhi\b',
                r'\bhello\b',
                r'\bhey\b',
                r'\bgreetings\b',
                r'\bgood morning\b',
                r'\bgood afternoon\b',
                r'\bgood evening\b'
            ]

            is_greeting = any(re.search(pattern, message_lower) for pattern in greeting_patterns)

            print(f"🔍 DEBUG: message = '{message}'")
            print(f"🔍 DEBUG: message_lower = '{message_lower}'")
            print(f"🔍 DEBUG: is_greeting = {is_greeting}")

            if is_greeting:
                # Handle greetings specifically
                response_text = "Hello! I'm your task management assistant. You can ask me to add, list, complete, update, or delete tasks. What would you like to do?"
                tool_calls = []
            elif any(keyword in message_lower for keyword in ['show', 'list', 'all', 'my tasks', 'what tasks', 'see tasks', 'view tasks', 'display tasks']):
                # Directly handle list requests without intent recognition
                print(f"🔍 DEBUG: Detected list request keyword, bypassing intent recognition")
                response_text, tool_calls = await self._handle_list_tasks(user_id, message, {})
                print(f"🔍 DEBUG: List handler returned response length: {len(response_text)}")
                print(f"🔍 DEBUG: Tool calls count: {len(tool_calls)}")
            elif any(keyword in message_lower for keyword in ['mark', 'complete', 'done', 'finish', 'completed', 'finished']):
                # Directly handle complete requests
                print(f"🔍 DEBUG: Detected complete request keyword, bypassing intent recognition")
                response_text, tool_calls = await self._handle_complete_task(user_id, message, {})
                print(f"🔍 DEBUG: Complete handler returned")
            elif any(keyword in message_lower for keyword in ['delete', 'remove', 'cancel', 'trash']):
                # Directly handle delete requests
                print(f"🔍 DEBUG: Detected delete request keyword, bypassing intent recognition")
                response_text, tool_calls = await self._handle_delete_task(user_id, message, {})
                print(f"🔍 DEBUG: Delete handler returned")
            elif any(keyword in message_lower for keyword in ['update', 'change', 'edit', 'modify', 'rename']):
                # Directly handle update requests
                print(f"🔍 DEBUG: Detected update request keyword, bypassing intent recognition")
                response_text, tool_calls = await self._handle_update_task(user_id, message, {})
                print(f"🔍 DEBUG: Update handler returned")
            elif any(keyword in message_lower for keyword in ['create task:', 'add task:', 'remind me to', 'schedule', 'remember to', 'don\'t forget to']):
                # Directly handle task creation with natural language parsing
                print(f"🔍 DEBUG: Detected task creation command, using full NL parsing")
                response_text, tool_calls = await self._handle_add_task(user_id, message, {})
                print(f"🔍 DEBUG: Task creation handler returned")
            else:
                print(f"🔍 DEBUG: No bypass match, going to intent recognition")
                # Recognize the user's intent
                intent_type, confidence, params = intent_recognizer.recognize_intent(message)
                print(f"🔍 DEBUG: Intent = {intent_type}, Confidence = {confidence}")

                # Apply confidence-based threshold for ambiguity resolution (per research.md decision 2)
                thresholds = intent_recognizer.get_intent_confidence_thresholds()

                if confidence < thresholds["medium_confidence"]:
                    # Ask for clarification when confidence is low
                    print(f"🔍 DEBUG: Low confidence, asking for clarification")
                    response_text = response_templates.get_question(
                        "ambiguous_task",
                        action=self._get_action_word(intent_type)
                    )
                else:
                    print(f"🔍 DEBUG: High confidence, processing intent")
                    # Process the request based on intent
                    if intent_type == IntentType.ADD_TASK:
                        response_text, tool_calls = await self._handle_add_task(user_id, message, params)
                    elif intent_type == IntentType.LIST_TASKS:
                        response_text, tool_calls = await self._handle_list_tasks(user_id, message, params)
                    elif intent_type == IntentType.COMPLETE_TASK:
                        response_text, tool_calls = await self._handle_complete_task(user_id, message, params)
                    elif intent_type == IntentType.DELETE_TASK:
                        response_text, tool_calls = await self._handle_delete_task(user_id, message, params)
                    elif intent_type == IntentType.UPDATE_TASK:
                        response_text, tool_calls = await self._handle_update_task(user_id, message, params)
                    else:
                        # Default to list tasks if unrecognized intent
                        response_text, tool_calls = await self._handle_list_tasks(user_id, message, params)

        except Exception as e:
            # Handle errors gracefully with user-friendly messages (hybrid with codes - per research.md decision 6)
            import traceback
            print(f"❌ Error processing chat request: {str(e)}")  # Log for debugging
            print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
            response_text = response_templates.get_error("database_error")

        # Step 5: Save assistant response to database
        assistant_message = MessageModel(
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=response_text
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)

        # Step 6: Return response with tool call details
        return {
            "conversation_id": conversation_id,
            "response": response_text,
            "tool_calls": tool_calls
        }

    async def _handle_add_task(self, user_id: str, message: str, params: Dict[str, str]) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle add_task requests with full natural language parsing"""
        tool_calls = []

        # Parse task details from natural language
        task_details = self._parse_task_details_from_message(message)

        if not task_details.get('title'):
            return response_templates.get_error("missing_parameter", action="add"), tool_calls

        try:
            # Build confirmation message with all details
            confirmation_parts = []
            confirmation_parts.append(f"✅ Task created: {task_details['title']}")

            if task_details.get('due_date'):
                confirmation_parts.append(f"due {task_details['due_date_display']}")
            if task_details.get('priority'):
                confirmation_parts.append(f"({task_details['priority']} priority)")
            if task_details.get('tags'):
                tags_str = ', '.join(task_details['tags'])
                confirmation_parts.append(f"tags: {tags_str}")
            if task_details.get('recurring_config'):
                freq = task_details['recurring_config'].get('frequency', 'recurring')
                confirmation_parts.append(f"recurring: {freq}")

            # Call the add_task MCP tool with all parameters
            tool_result = await mcp_client.add_task(
                user_id=user_id,
                title=task_details['title'],
                description=task_details.get('description'),
                due_date=task_details.get('due_date'),
                priority=task_details.get('priority'),
                tags=task_details.get('tags'),
                recurring_config=task_details.get('recurring_config'),
                auth_token=getattr(self, '_auth_token', None)
            )

            tool_call = {
                "name": "add_task",
                "arguments": {
                    "user_id": user_id,
                    "title": task_details['title'],
                    **{k: v for k, v in task_details.items() if k not in ['title', 'due_date_display'] and v is not None}
                },
                "result": tool_result
            }
            tool_calls.append(tool_call)

            # Return friendly confirmation message with all details
            response_text = ' '.join(confirmation_parts)

            return response_text, tool_calls

        except Exception as e:
            import traceback
            print(f"❌ Error in add_task handler: {str(e)}")  # Log for debugging
            print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
            return response_templates.get_error("database_error"), tool_calls

    def _parse_task_details_from_message(self, message: str) -> Dict[str, Any]:
        """Parse task details from natural language message.

        Examples:
        - "Create task: Buy a Lamborghini tomorrow at 10 AM priority high"
        - "Remind me to drink water in 5 minutes tag health"
        - "Add daily recurring task: Gym every morning at 7 AM"
        """
        import re
        from datetime import datetime, timedelta

        result = {
            'title': None,
            'description': None,
            'due_date': None,
            'due_date_display': None,
            'priority': None,
            'tags': None,
            'recurring_config': None
        }

        message_lower = message.lower().strip()

        # Extract priority
        priority_keywords = {
            'high': 'high',
            'urgent': 'urgent',
            'important': 'high',
            'medium': 'medium',
            'normal': 'medium',
            'low': 'low',
            'minor': 'low'
        }
        for keyword, priority_value in priority_keywords.items():
            if keyword in message_lower:
                result['priority'] = priority_value
                # Remove priority keyword from message for title extraction
                message_lower = message_lower.replace(keyword, '')
                break

        # Extract tags (after "tag", "tags", "labeled", "category")
        tag_match = re.search(r'(?:tag|tags|labeled|category)\s+([\w\s,]+?)(?:\s+(?:priority|due|at|in|on)|$)', message_lower)
        if tag_match:
            tags_str = tag_match.group(1).strip()
            result['tags'] = [t.strip() for t in tags_str.split(',') if t.strip()]
            # Remove tags from message for title extraction
            message_lower = re.sub(r'(?:tag|tags|labeled|category)\s+([\w\s,]+?)(?:\s+(?:priority|due|at|in|on)|$)', '', message_lower)

        # Extract recurring info
        recurring_patterns = [
            (r'(?:daily|every day)\b', {'enabled': True, 'frequency': 'daily', 'interval': 1}),
            (r'(?:weekly|every week)\b', {'enabled': True, 'frequency': 'weekly', 'interval': 1}),
            (r'(?:monthly|every month)\b', {'enabled': True, 'frequency': 'monthly', 'interval': 1}),
            (r'\b(?:recurring|repeat|repeats)\b', {'enabled': True, 'frequency': 'daily', 'interval': 1}),
        ]
        for pattern, config in recurring_patterns:
            if re.search(pattern, message_lower):
                result['recurring_config'] = config
                message_lower = re.sub(pattern, '', message_lower)
                break

        # Extract and parse due date/time
        due_date = None
        due_date_display = None
        now = datetime.now()

        # Pattern: "at X AM/PM" or "at X:XX" OR "X:XX AM/PM" directly (at/@ is now optional)
        # Supports: "at 5:40PM", "5:40PM", "5:40 pm", "17:40", "5pm", etc.
        time_match = re.search(r'(?:(?:at|@)\s*)?(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?', message_lower)
        hour = None
        minute = None
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            am_pm = time_match.group(3)
            if am_pm and 'pm' in am_pm.lower() and hour < 12:
                hour += 12
            elif am_pm and 'am' in am_pm.lower() and hour == 12:
                hour = 0

        # Pattern: "tomorrow"
        if 'tomorrow' in message_lower:
            target_date = now + timedelta(days=1)
            if hour is not None:
                target_date = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            due_date = target_date.isoformat()
            due_date_display = "tomorrow" + (f" at {hour}:{minute:02d} AM" if hour < 12 else f" at {hour-12}:{minute:02d} PM" if hour is not None else "")

        # Pattern: "today"
        elif 'today' in message_lower:
            if hour is not None:
                target_date = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                due_date = target_date.isoformat()
                due_date_display = f"today at {hour}:{minute:02d} AM" if hour < 12 else f"today at {hour-12}:{minute:02d} PM"
            else:
                due_date = now.isoformat()
                due_date_display = "today"

        # Pattern: "in X minutes/hours/days"
        elif 'in ' in message_lower:
            time_match = re.search(r'in\s+(\d+)\s+(minute|minutes|hour|hours|day|days)', message_lower)
            if time_match:
                amount = int(time_match.group(1))
                unit = time_match.group(2)
                if 'minute' in unit:
                    target_date = now + timedelta(minutes=amount)
                elif 'hour' in unit:
                    target_date = now + timedelta(hours=amount)
                elif 'day' in unit:
                    target_date = now + timedelta(days=amount)

                if hour is not None:
                    target_date = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

                due_date = target_date.isoformat()
                if amount == 1:
                    due_date_display = f"in 1 {unit.rstrip('s')}"
                else:
                    due_date_display = f"in {amount} {unit.rstrip('s')}"

        # Pattern: specific date "MM/DD", "DD-MM", etc.
        else:
            date_match = re.search(r'\b(\d{1,2})[\/\-](\d{1,2})(?:[\/\-](\d{2,4}))?\b', message)
            if date_match:
                try:
                    month = int(date_match.group(1))
                    day = int(date_match.group(2))
                    year = int(date_match.group(3)) if date_match.group(3) else now.year

                    # Validate date
                    if 1 <= month <= 12 and 1 <= day <= 31:
                        if hour is not None:
                            target_date = datetime(year, month, day, hour, minute)
                        else:
                            target_date = datetime(year, month, day, 12, 0)
                        due_date = target_date.isoformat()
                        due_date_display = target_date.strftime("%B %d") + (f" at {hour}:{minute:02d}" if hour is not None else "")
                except:
                    pass  # Invalid date, skip

        # IMPORTANT: If time was parsed but no date context was found, default to today
        # This handles cases like "Add a task Get medicine at 9:12 PM" where only time is given
        if due_date is None and hour is not None:
            target_date = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            due_date = target_date.isoformat()
            due_date_display = f"today at {hour}:{minute:02d} AM" if hour < 12 else f"today at {hour-12}:{minute:02d} PM"

        if due_date:
            result['due_date'] = due_date
            result['due_date_display'] = due_date_display

        # Extract title by removing all the patterns we've processed
        title = message_lower
        # Remove command prefixes
        title = re.sub(r'^(create|add|remind me to|schedule|set)(?:\s+(?:a\s+)?)?(?:task|todo|reminder|alarm)?:?\s*', '', title, flags=re.IGNORECASE)
        # Remove processed keywords - enhanced with more patterns
        title = re.sub(r'\s+(?:priority|tag|tags|labeled|category)\s+[\w\s,]+', '', title)
        title = re.sub(r'\s+(?:tomorrow|today|in\s+\d+\s+(?:minute|hour|day)s?)', '', title)
        # Remove time patterns (including "at 5:40PM", "5:40PM", etc.)
        title = re.sub(r'\s+(?:at|@|due\s+at)\s*\d{1,2}(?::\d{2})?\s*(?:am|pm|a\.m\.|p\.m\.)?', '', title)
        title = re.sub(r'\s+\d{1,2}:\d{2}\s*(?:am|pm|a\.m\.|p\.m\.)?', '', title)  # Direct time like "5:40PM"
        # Remove "due task", "with due", "due", "time", "reminder" related phrases
        title = re.sub(r'\s+(?:due\s+(?:task|date|time)?|with\s+due|time|reminder|remind)\s*', ' ', title, flags=re.IGNORECASE)
        title = re.sub(r'\s+(?:daily|weekly|monthly|every\s+(?:day|week|month)|recurring)', '', title)
        title = re.sub(r'\s+(?:high|urgent|important|medium|normal|low|minor)', '', title)
        # Clean up extra spaces and capitalize
        title = re.sub(r'\s+', ' ', title).strip().capitalize()

        if title:
            result['title'] = title

        return result

    async def _handle_list_tasks(self, user_id: str, message: str, params: Dict[str, str]) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle list_tasks requests"""
        tool_calls = []

        # Determine status filter from message
        status = "all"
        message_lower = message.lower()
        if "pending" in message_lower:
            status = "pending"
        elif "completed" in message_lower:
            status = "completed"

        try:
            # Call the list_tasks MCP tool with user_id propagation
            tool_result = await mcp_client.list_tasks(user_id=user_id, status=status, auth_token=getattr(self, '_auth_token', None))

            tool_call = {
                "name": "list_tasks",
                "arguments": {"user_id": user_id, "status": status},
                "result": tool_result
            }
            tool_calls.append(tool_call)

            if tool_result:
                # Format the task list with numbered items and actual IDs (per spec requirement)
                formatted_tasks = []
                for i, task in enumerate(tool_result, 1):
                    status_icon = "✓" if task.get("completed") else "○"
                    task_id = task.get('id')
                    title = task.get('title', 'Untitled')
                    # Show both list number and actual task ID
                    formatted_tasks.append(f"{i}. {status_icon} {title} (ID: {task_id})")

                task_list = "\n".join(formatted_tasks)

                # Count pending and completed tasks for summary
                pending_count = sum(1 for t in tool_result if not t.get("completed"))
                completed_count = sum(1 for t in tool_result if t.get("completed"))

                response_text = f"{task_list}\n\n{response_templates.get_list_summary(pending_count, completed_count)}"

                # Add note about using list numbers for updates
                response_text += "\n\n💡 Tip: Use the list number (1, 2, 3...) to update or complete tasks."

                # Add proactive suggestion if many completed tasks
                if completed_count > 3:
                    response_text += f"\n\n{response_templates.get_suggestion('clear_completed', count=completed_count)}"
            else:
                # Handle empty list case
                response_text = response_templates.get_error("empty_list", status=status)

            return response_text, tool_calls

        except Exception as e:
            import traceback
            error_msg = str(e)
            print(f"❌ Error in list_tasks handler: {error_msg}")
            print(f"❌ Error details: {traceback.format_exc()}")

            # Check if this is an MCP connection error - if so, fall back to direct database query
            if "Name or service not known" in error_msg or "Failed to connect to MCP server" in error_msg:
                print("🔄 MCP server unavailable, falling back to direct database query...")
                try:
                    async with get_async_db_session() as db_session:
                        # Determine completed filter based on status
                        completed_filter = None
                        if status == "completed":
                            completed_filter = True
                        elif status == "pending":
                            completed_filter = False

                        # Query tasks directly from database
                        tasks = await crud.get_tasks(db_session, user_id=user_id, completed=completed_filter)

                        # Convert Task models to dict format similar to MCP response
                        tool_result = []
                        for task in tasks:
                            tool_result.append({
                                "id": task.id,
                                "title": task.title,
                                "description": task.description,
                                "completed": task.completed,
                                "due_date": task.due_date.isoformat() if task.due_date else None,
                                "priority": task.priority,
                                "tags": task.tags
                            })

                        tool_call = {
                            "name": "list_tasks",
                            "arguments": {"user_id": user_id, "status": status},
                            "result": tool_result,
                            "fallback": "direct_database"
                        }
                        tool_calls.append(tool_call)

                        if tool_result:
                            # Format the task list
                            formatted_tasks = []
                            for i, task in enumerate(tool_result, 1):
                                status_icon = "✓" if task.get("completed") else "○"
                                task_id = task.get('id')
                                title = task.get('title', 'Untitled')
                                formatted_tasks.append(f"{i}. {status_icon} {title} (ID: {task_id})")

                            task_list = "\n".join(formatted_tasks)

                            pending_count = sum(1 for t in tool_result if not t.get("completed"))
                            completed_count = sum(1 for t in tool_result if t.get("completed"))

                            response_text = f"{task_list}\n\n{response_templates.get_list_summary(pending_count, completed_count)}"
                            response_text += "\n\n💡 Tip: Use the list number (1, 2, 3...) to update or complete tasks."

                            if completed_count > 3:
                                response_text += f"\n\n{response_templates.get_suggestion('clear_completed', count=completed_count)}"
                        else:
                            response_text = response_templates.get_error("empty_list", status=status)

                        return response_text, tool_calls

                except Exception as db_error:
                    print(f"❌ Database fallback also failed: {str(db_error)}")
                    print(f"❌ Database error details: {traceback.format_exc()}")
                    return response_templates.get_error("database_error"), tool_calls

            # For other types of errors, return the standard error message
            return response_templates.get_error("database_error"), tool_calls

    async def _handle_complete_task(self, user_id: str, message: str, params: Dict[str, str]) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle complete_task requests with list number to task ID mapping"""
        tool_calls = []

        # Extract task ID from message or params
        task_id_str = params.get('task_id') or self._extract_task_id_from_message(message)

        if task_id_str:
            try:
                # First, try to get the actual task ID from the list position
                actual_task_id = await self._get_task_id_from_list_number(user_id, task_id_str)
                if actual_task_id:
                    task_id = actual_task_id
                    print(f"🔍 DEBUG: Mapped list number {task_id_str} to actual task_id {task_id}")
                else:
                    task_id = int(task_id_str)

                # Call the complete_task MCP tool with user_id propagation
                tool_result = await mcp_client.complete_task(user_id=user_id, task_id=task_id, auth_token=getattr(self, '_auth_token', None))

                tool_call = {
                    "name": "complete_task",
                    "arguments": {"user_id": user_id, "task_id": task_id},
                    "result": tool_result
                }
                tool_calls.append(tool_call)

                # Find the task title for the confirmation message
                title = f"Task {task_id}"  # Default if we can't find the title

                # Return friendly confirmation message
                response_text = response_templates.get_confirmation("task_completed", title=title)

                return response_text, tool_calls

            except ValueError:
                return response_templates.get_error("invalid_input"), tool_calls
            except Exception as e:
                import traceback
                print(f"❌ Error in complete_task handler: {str(e)}")  # Log for debugging
                print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
                return response_templates.get_error("task_not_found", task_id=task_id_str), tool_calls
        else:
            # Handle case where no task ID was found - might need to do title-based lookup
            return await self._handle_title_based_lookup(user_id, message, IntentType.COMPLETE_TASK)

    async def _handle_delete_task(self, user_id: str, message: str, params: Dict[str, str]) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle delete_task requests with list number to task ID mapping"""
        tool_calls = []

        # Extract task ID from message or params
        task_id_str = params.get('task_id') or self._extract_task_id_from_message(message)

        if task_id_str:
            try:
                # First, try to get the actual task ID from the list position
                actual_task_id = await self._get_task_id_from_list_number(user_id, task_id_str)
                if actual_task_id:
                    task_id = actual_task_id
                    print(f"🔍 DEBUG: Mapped list number {task_id_str} to actual task_id {task_id}")
                else:
                    task_id = int(task_id_str)

                # Call the delete_task MCP tool with user_id propagation
                tool_result = await mcp_client.delete_task(user_id=user_id, task_id=task_id, auth_token=getattr(self, '_auth_token', None))

                tool_call = {
                    "name": "delete_task",
                    "arguments": {"user_id": user_id, "task_id": task_id},
                    "result": tool_result
                }
                tool_calls.append(tool_call)

                # Find the task title for the confirmation message
                title = f"Task {task_id}"  # Default if we can't find the title

                # Return friendly confirmation message
                response_text = response_templates.get_confirmation("task_deleted", title=title)

                return response_text, tool_calls

            except ValueError:
                return response_templates.get_error("invalid_input"), tool_calls
            except Exception as e:
                import traceback
                print(f"❌ Error in delete_task handler: {str(e)}")  # Log for debugging
                print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
                return response_templates.get_error("task_not_found", task_id=task_id_str), tool_calls
        else:
            # Handle case where no task ID was found - might need to do title-based lookup
            return await self._handle_title_based_lookup(user_id, message, IntentType.DELETE_TASK)

    async def _handle_update_task(self, user_id: str, message: str, params: Dict[str, str]) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle update_task requests with list number to task ID mapping"""
        tool_calls = []

        # Extract task ID from message or params
        task_id_str = params.get('task_id') or self._extract_task_id_from_message(message)

        if task_id_str:
            try:
                # First, try to get the actual task ID from the list position
                actual_task_id = await self._get_task_id_from_list_number(user_id, task_id_str)
                if actual_task_id:
                    task_id = actual_task_id
                    print(f"🔍 DEBUG: Mapped list number {task_id_str} to actual task_id {task_id}")
                else:
                    task_id = int(task_id_str)

                # For now, just update the title based on the message
                new_title = params.get('title') or self._extract_task_title_from_message(message, IntentType.UPDATE_TASK)

                # Special handling for "task X to Y" pattern - extract text after "to"
                message_lower = message.lower()
                if ' to ' in message_lower or ' to: ' in message_lower:
                    # Find the part after "to" as the new title
                    import re
                    to_pattern = r'(?:to|into)\s+(.+)'
                    match = re.search(to_pattern, message_lower)
                    if match:
                        extracted_after_to = match.group(1).strip()
                        # Clean up common articles
                        extracted_after_to = re.sub(r'^(the|a|an)\s+', '', extracted_after_to, flags=re.IGNORECASE)
                        # Take the extracted title if it's more meaningful than the originally extracted one
                        if len(extracted_after_to) >= 2:
                            new_title = extracted_after_to

                if new_title:
                    # Call the update_task MCP tool with user_id propagation
                    tool_result = await mcp_client.update_task(
                        user_id=user_id,
                        task_id=task_id,
                        title=new_title,
                        auth_token=getattr(self, '_auth_token', None)
                    )

                    tool_call = {
                        "name": "update_task",
                        "arguments": {"user_id": user_id, "task_id": task_id, "title": new_title},
                        "result": tool_result
                    }
                    tool_calls.append(tool_call)

                    # Return friendly confirmation message
                    response_text = response_templates.get_confirmation("task_updated", title=new_title)

                    return response_text, tool_calls
                else:
                    return response_templates.get_error("missing_parameter", action="update"), tool_calls

            except ValueError:
                return response_templates.get_error("invalid_input"), tool_calls
            except Exception as e:
                import traceback
                print(f"❌ Error in update_task handler: {str(e)}")  # Log for debugging
                print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
                return response_templates.get_error("task_not_found", task_id=task_id_str), tool_calls
        else:
            # Handle case where no task ID was found - might need to do title-based lookup
            return await self._handle_title_based_lookup(user_id, message, IntentType.UPDATE_TASK)

    async def _get_task_id_from_list_number(self, user_id: str, list_number_str: str) -> Optional[int]:
        """
        Map a list number to the actual task ID.
        For example, if user says "task #6", this returns the ID of the 6th task in the list.
        """
        try:
            list_number = int(list_number_str)
            # Get all tasks
            tool_result = await mcp_client.list_tasks(user_id=user_id, status="all", auth_token=getattr(self, '_auth_token', None))
            if tool_result and list_number <= len(tool_result):
                # Get the task at the list position (1-indexed)
                actual_task_id = tool_result[list_number - 1].get('id')
                print(f"🔍 DEBUG: List position {list_number} -> Task ID {actual_task_id}")
                return actual_task_id
        except:
            pass
        return None

    async def _handle_title_based_lookup(self, user_id: str, message: str, intent_type: IntentType) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle title-based task lookup for operations that require it"""
        tool_calls = []

        # First, list all tasks to find the one matching the title
        try:
            list_result = await mcp_client.list_tasks(user_id=user_id, status="all", auth_token=getattr(self, '_auth_token', None))

            tool_call = {
                "name": "list_tasks",
                "arguments": {"user_id": user_id, "status": "all"},
                "result": list_result
            }
            tool_calls.append(tool_call)

            if intent_type == IntentType.UPDATE_TASK:
                # Special handling for "add a reminder at [time]" pattern
                # This should update the due time, NOT rename the task
                import re
                message_lower = message.lower()

                # Check for "add a reminder at [time]" or "remind me at [time]" pattern
                reminder_time_pattern = r'(?:add|set)(?:\s+a)?\s*reminder\s*(?:at|to|for)?\s*(\d{1,2}):(\d{2})\s*(am|pm)'
                reminder_match = re.search(reminder_time_pattern, message_lower)

                if reminder_match:
                    print(f"🔍 DEBUG: Detected reminder time pattern - treating as time update")
                    # Extract the task title before "add a reminder"
                    # Remove everything from "add" or "set" onwards
                    task_title_pattern = r'(?:update|change|modify|edit|rename)\s+(?:the\s+)?(?:recurring\s+)?(?:task\s+)?(.+?)\s+(?:add|set)\s+reminder'
                    task_title_match = re.search(task_title_pattern, message_lower)

                    if task_title_match:
                        search_title = task_title_match.group(1).strip()
                        print(f"🔍 DEBUG: Extracted task title: '{search_title}'")

                        # Find the task matching this title
                        matching_tasks = []
                        for task in list_result:
                            task_title_lower = task.get('title', '').lower()
                            if search_title.lower() in task_title_lower or task_title_lower in search_title.lower():
                                matching_tasks.append(task)

                        # If no direct match, try fuzzy matching
                        if not matching_tasks:
                            from difflib import SequenceMatcher
                            threshold = 0.6
                            for task in list_result:
                                task_title_lower = task.get('title', '').lower()
                                similarity = SequenceMatcher(None, search_title.lower(), task_title_lower).ratio()
                                if similarity >= threshold:
                                    matching_tasks.append(task)

                        if len(matching_tasks) == 1:
                            task = matching_tasks[0]
                            task_id = task.get('id')

                            # Parse the time
                            hour = int(reminder_match.group(1))
                            minute = int(reminder_match.group(2))
                            am_pm = reminder_match.group(3)
                            if 'pm' in am_pm and hour < 12:
                                hour += 12
                            elif 'am' in am_pm and hour == 12:
                                hour = 0

                            # Create new due date with today's date but new time
                            from datetime import datetime, timedelta
                            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                            new_due_date = today.replace(hour=hour, minute=minute).isoformat()

                            # Prepare update params - preserve everything except due date/time
                            update_params = {
                                "user_id": user_id,
                                "task_id": task_id,
                                "due_date": new_due_date,
                                "auth_token": getattr(self, '_auth_token', None)
                            }

                            # Preserve recurring config
                            if task.get('recurring_config'):
                                update_params['recurring_config'] = task.get('recurring_config')

                            # Preserve title (don't rename it!)
                            if task.get('title'):
                                update_params['title'] = task['title']

                            # Preserve other attributes
                            if task.get('priority'):
                                update_params['priority'] = task.get('priority')
                            if task.get('tags'):
                                update_params['tags'] = task.get('tags')

                            print(f"🔍 DEBUG: Updating task {task_id} due time to {new_due_date}")
                            print(f"🔍 DEBUG: Preserving title: {task.get('title')}")
                            print(f"🔍 DEBUG: Preserving recurring_config: {task.get('recurring_config')}")

                            update_result = await mcp_client.update_task_full(**update_params)

                            tool_call = {
                                "name": "update_task",
                                "arguments": update_params,
                                "result": update_result
                            }
                            tool_calls.append(tool_call)

                            # Build friendly confirmation message
                            time_str = f"{hour}:{minute:02d} {'AM' if hour < 12 else 'PM'}"
                            response_text = f"✅ Updated '{task.get('title')}' reminder time to {time_str}"

                            if task.get('recurring_config'):
                                freq = task['recurring_config'].get('frequency', 'recurring')
                                response_text += f" ({freq})"

                            return response_text, tool_calls
                        elif len(matching_tasks) > 1:
                            return response_templates.get_error("multiple_tasks_found", query=search_title), tool_calls
                        else:
                            return response_templates.get_error("no_tasks_found", query=search_title), tool_calls
                    else:
                        # Couldn't extract task title, fall through to normal rename handling
                        print(f"🔍 DEBUG: Could not extract task title from reminder pattern")
                else:
                    # No reminder pattern, proceed with normal rename/update logic
                    # For update tasks, we need to parse the message to find both the original task and the new title
                    original_title, new_title = self._extract_rename_titles(message)

                    if not original_title:
                        return response_templates.get_question("ambiguous_task", action=self._get_action_word(intent_type)), tool_calls

                    # Find tasks that match the original title (with fuzzy matching)
                    # Use more sophisticated matching that finds the closest matches
                    matching_tasks = []
                    search_lower = original_title.lower().strip()

                    print(f"🔍 DEBUG RENAME: Searching for tasks matching '{search_lower}'")
                    print(f"🔍 DEBUG RENAME: Available tasks: {list_result}")

                    # First, try exact match or substring match
                    for task in list_result:
                        task_title_lower = task.get('title', '').lower()
                        print(f"🔍 DEBUG RENAME: Checking task title '{task_title_lower}'")
                        if search_lower == task_title_lower or search_lower in task_title_lower or task_title_lower in search_lower:
                            print(f"🔍 DEBUG RENAME: Match found!")
                            matching_tasks.append(task)

                    # If no matches found, try fuzzy matching with similarity
                    if not matching_tasks:
                        from difflib import SequenceMatcher
                        threshold = 0.6  # Minimum similarity ratio

                        for task in list_result:
                            task_title_lower = task.get('title', '').lower()
                            similarity = SequenceMatcher(None, search_lower, task_title_lower).ratio()

                            if similarity >= threshold:
                                matching_tasks.append(task)

                    if len(matching_tasks) == 0:
                        return response_templates.get_error("no_tasks_found", query=original_title), tool_calls
                    elif len(matching_tasks) == 1:
                        # Found exactly one match, proceed with the update
                        task = matching_tasks[0]
                        task_id = task.get('id')

                        if new_title:
                            # Parse the new due time if specified
                            new_due_time = None

                            # Check if the new title contains a time specification
                            time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)', new_title)
                            if time_match:
                                hour = int(time_match.group(1))
                                minute = int(time_match.group(2))
                                am_pm = time_match.group(3)
                                if 'pm' in am_pm and hour < 12:
                                    hour += 12
                                elif 'am' in am_pm and hour == 12:
                                    hour = 0

                                # Create new due date with the original date but new time
                                original_due_date = task.get('due_date')
                                if original_due_date:
                                    from datetime import datetime
                                    try:
                                        original_dt = datetime.fromisoformat(original_due_date.replace('Z', '+00:00'))
                                        # Preserve the original date but update the time
                                        new_due_date = original_dt.replace(hour=hour, minute=minute, second=0, microsecond=0).isoformat()
                                        new_due_time = new_due_date
                                        print(f"🔍 DEBUG: Updated due time from {original_due_date} to {new_due_date}")
                                    except:
                                        pass

                            # Update task while preserving recurring config and other attributes
                            # First, get the task's current attributes
                            update_params = {
                                "user_id": user_id,
                                "task_id": task_id,
                                "title": new_title,
                                "auth_token": getattr(self, '_auth_token', None)
                            }

                            # Preserve recurring config if it exists
                            if task.get('recurring_config'):
                                update_params['recurring_config'] = task.get('recurring_config')
                                print(f"🔍 DEBUG: Preserving recurring_config: {task.get('recurring_config')}")

                            # Update due date if we parsed a new time
                            if new_due_time:
                                update_params['due_date'] = new_due_time

                            # Preserve priority if it exists
                            if task.get('priority'):
                                update_params['priority'] = task.get('priority')

                            # Preserve tags if they exist
                            if task.get('tags'):
                                update_params['tags'] = task.get('tags')

                            update_result = await mcp_client.update_task_full(**update_params)

                            tool_call = {
                                "name": "update_task",
                                "arguments": update_params,
                                "result": update_result
                            }
                            tool_calls.append(tool_call)

                            # Build friendly confirmation message
                            confirmation_parts = [f"✅ Updated to '{new_title}'"]
                            if task.get('recurring_config'):
                                confirmation_parts.append("(recurring)")
                            response_text = ' '.join(confirmation_parts)
                        else:
                            return response_templates.get_error("missing_parameter", action="update"), tool_calls

                        return response_text, tool_calls

                # Multiple matches found, ask for clarification
                return response_templates.get_error("multiple_tasks_found", query=original_title), tool_calls
            else:
                # Extract the task title from the message for other operations
                search_title = self._extract_task_title_from_message(message, intent_type)

                if not search_title:
                    return response_templates.get_question("ambiguous_task", action=self._get_action_word(intent_type)), tool_calls

                # Find tasks that match the title (with fuzzy matching - per research.md best practices)
                # Use more sophisticated matching that finds the closest matches
                matching_tasks = []
                search_lower = search_title.lower().strip()

                # First, try exact match or substring match
                for task in list_result:
                    task_title_lower = task.get('title', '').lower()
                    if search_lower == task_title_lower or search_lower in task_title_lower or task_title_lower in search_lower:
                        matching_tasks.append(task)

                # If no matches found, try fuzzy matching with similarity
                if not matching_tasks:
                    from difflib import SequenceMatcher
                    threshold = 0.6  # Minimum similarity ratio

                    for task in list_result:
                        task_title_lower = task.get('title', '').lower()
                        similarity = SequenceMatcher(None, search_lower, task_title_lower).ratio()

                        if similarity >= threshold:
                            matching_tasks.append(task)

                if len(matching_tasks) == 0:
                    return response_templates.get_error("no_tasks_found", query=search_title), tool_calls
                elif len(matching_tasks) == 1:
                    # Found exactly one match, proceed with the operation
                    task = matching_tasks[0]
                    task_id = task.get('id')

                    if intent_type == IntentType.COMPLETE_TASK:
                        complete_result = await mcp_client.complete_task(user_id=user_id, task_id=task_id, auth_token=getattr(self, '_auth_token', None))

                        tool_call = {
                            "name": "complete_task",
                            "arguments": {"user_id": user_id, "task_id": task_id},
                            "result": complete_result
                        }
                        tool_calls.append(tool_call)

                        response_text = response_templates.get_confirmation("task_completed", title=task.get('title'))

                    elif intent_type == IntentType.DELETE_TASK:
                        delete_result = await mcp_client.delete_task(user_id=user_id, task_id=task_id, auth_token=getattr(self, '_auth_token', None))

                        tool_call = {
                            "name": "delete_task",
                            "arguments": {"user_id": user_id, "task_id": task_id},
                            "result": delete_result
                        }
                        tool_calls.append(tool_call)

                        response_text = response_templates.get_confirmation("task_deleted", title=task.get('title'))

                    else:
                        response_text = response_templates.get_error("invalid_input")

                    return response_text, tool_calls
                else:
                    # Multiple matches found, ask for clarification
                    return response_templates.get_error("multiple_tasks_found", query=search_title), tool_calls

        except Exception as e:
            import traceback
            print(f"❌ Error in title_based_lookup handler: {str(e)}")  # Log for debugging
            print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
            return response_templates.get_error("database_error"), tool_calls

    def _extract_rename_titles(self, message: str) -> tuple[Optional[str], Optional[str]]:
        """
        Extract original and new titles from a rename/update message.
        Examples:
        "rename buying fruits to buy luxury watch" -> ("buying fruits", "buy luxury watch")
        "Rename tasks Updated task title" -> ("tasks", "Updated task title")
        """
        import re

        message_lower = message.lower().strip()

        # Pattern for rename/update: "rename X to Y", "change X to Y", "update X to Y"
        patterns = [
            r'(?:rename|change|update|modify|edit)\s+(?:the\s+)?(?:task\s+)?(.+?)\s+(?:to|into)\s+(.+)',
            r'(?:rename|change|update|modify|edit)\s+(?:the\s+)?(?:task\s+)?(.+?)\s+to\s+(.+)',
            r'(?:rename|change|update|modify|edit)\s+(.+?)\s+(?:to|into)\s+(.+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                original_title = match.group(1).strip()
                new_title = match.group(2).strip()

                # Clean up common articles and prepositions
                original_title = re.sub(r'^(the|a|an)\s+', '', original_title)
                new_title = re.sub(r'^(the|a|an)\s+', '', new_title)

                print(f"🔍 DEBUG RENAME: Extracted original_title='{original_title}', new_title='{new_title}'")
                return original_title, new_title

        # For cases like "Rename tasks Updated task title" (without 'to')
        # Split the message after the command word
        command_pattern = r'(?:rename|change|update|modify|edit)\s+(?:the\s+)?(?:task\s+)?(.+)'
        match = re.search(command_pattern, message_lower)
        if match:
            rest_of_message = match.group(1).strip()

            # Look for common separators or try to intelligently split
            # For "tasks Updated task title", we need to identify where the original title ends

            # First, try to see if there's an existing task title in the message
            # Get all tasks to compare against
            # For now, we'll use a simple heuristic: split on common words like "to", "as", "into"
            # Or assume the first word is the original title if it matches an existing pattern

            # For now, return the entire rest as original title and None for new
            # The actual splitting will need to be done in the calling function with context
            # But let's try to be smarter about it
            words = rest_of_message.split()
            if len(words) >= 2:
                # Heuristic: first word or first phrase might be the original title
                # Look for a reasonable split point
                for i in range(1, len(words)):
                    potential_original = ' '.join(words[:i]).strip()
                    potential_new = ' '.join(words[i:]).strip()

                    # If potential_new seems like a reasonable title (has content), use this split
                    if len(potential_new.strip()) > 0 and len(potential_original.strip()) > 0:
                        # Clean up common articles
                        potential_original = re.sub(r'^(the|a|an)\s+', '', potential_original)
                        potential_new = re.sub(r'^(the|a|an)\s+', '', potential_new)
                        return potential_original, potential_new

        # If no clear rename pattern found, try to extract a single title and return None for new title
        # This allows fallback to the original extraction method for simple updates
        extracted_title = self._extract_task_title_from_message(message, IntentType.UPDATE_TASK)
        return extracted_title, None

    def _extract_task_id_from_message(self, message: str) -> Optional[str]:
        """Extract task ID from a message"""
        import re
        # Look for digits in the message which might represent a task ID
        matches = re.findall(r'\d+', message)
        if matches:
            return matches[0]  # Return the first match
        return None

    def _extract_task_title_from_message(self, message: str, intent_type: IntentType) -> Optional[str]:
        """Extract task title from a message based on intent type"""
        import re
        message_clean = message.strip()

        # Remove common intent phrases to isolate the title
        if intent_type == IntentType.ADD_TASK:
            # Remove common add phrases
            phrases_to_remove = [
                r"(?:add|create|remember|i need to|remind me to|don't forget to)\s+",
                r"(?:a\s+)?(?:task|todo|thing|item)\s+(?:to\s+)?"
            ]

            for phrase in phrases_to_remove:
                message_clean = re.sub(phrase, "", message_clean, flags=re.IGNORECASE)

        elif intent_type == IntentType.UPDATE_TASK:
            # Remove common update phrases
            phrases_to_remove = [
                r"(?:change|update|edit|modify|rename)\s+(?:task|the|this|that)\s+",
                r"(?:the\s+)?(?:title|description)\s+(?:of\s+|to\s+|for\s+)?"
            ]

            for phrase in phrases_to_remove:
                message_clean = re.sub(phrase, "", message_clean, flags=re.IGNORECASE)

        elif intent_type == IntentType.COMPLETE_TASK:
            # Remove common complete phrases like "mark [task] to complete", "complete [task]", etc.
            phrases_to_remove = [
                r"(?:mark|make|set|put|turn|complete|finish|do)\s+",  # "mark ", "complete "
                r"(?:the|this|that)\s+",  # "the ", "this "
                r"(?:task|it)\s+",  # "task ", "it "
                r"(?:as\s+)?(?:done|completed|finished|complete|to complete)\s*",  # "done", "completed", "to complete"
                r"\s+(?:as\s+)?(?:done|completed|finished|complete)$",  # trailing "done", "completed", etc.
                r"\s+to\s+(?:done|completed|finished|complete)$",  # trailing "to done", "to completed", etc.
            ]

            for phrase in phrases_to_remove:
                message_clean = re.sub(phrase, " ", message_clean, flags=re.IGNORECASE)

        elif intent_type == IntentType.DELETE_TASK:
            # Remove common delete phrases like "delete [task]", "remove [task]", etc.
            phrases_to_remove = [
                r"(?:delete|remove|eliminate|get rid of|clear|cancel|trash|erase)\s+",  # "delete ", "remove "
                r"(?:the|this|that)\s+",  # "the ", "this "
                r"(?:task|it)\s+",  # "task ", "it "
                r"(?:please|now|immediately|right away)?\s*$",  # trailing words
            ]

            for phrase in phrases_to_remove:
                message_clean = re.sub(phrase, " ", message_clean, flags=re.IGNORECASE)

        # Clean up the remaining text - remove extra spaces and punctuation
        message_clean = re.sub(r'\s+', ' ', message_clean).strip(" .,!?\"'")

        # If there's meaningful text left, consider it the title
        if message_clean and len(message_clean) >= 2:
            # Limit to reasonable length
            return message_clean[:100]  # Cap at 100 characters

        return None

    def _get_action_word(self, intent_type: IntentType) -> str:
        """Get the action word for a given intent type"""
        action_map = {
            IntentType.ADD_TASK: "add",
            IntentType.LIST_TASKS: "list",
            IntentType.COMPLETE_TASK: "complete",
            IntentType.DELETE_TASK: "delete",
            IntentType.UPDATE_TASK: "update"
        }
        return action_map.get(intent_type, "perform")


# Global agent service instance
agent_service = AgentService()


# Wrapper function to maintain backward compatibility
async def process_chat_request(
    user_id: str,
    conversation_id: Optional[int],
    message: str,
    db: Session,
    auth_token: Optional[str] = None
) -> Dict[str, Any]:
    """Wrapper function to maintain backward compatibility"""
    return await agent_service.process_chat_request(user_id, conversation_id, message, db, auth_token)