import asyncio
from typing import Dict, Any, List, Optional, Tuple
from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlmodel import select
from ..database.models import Conversation as ConversationModel, Message as MessageModel
from sqlmodel import Session

from .mcp_client import mcp_client
from .data_models import (
    UserIntent, IntentType, TaskReference, ConversationContext,
    ToolChain, ToolChainStep
)
from .response_templates import response_templates
from .intent_recognition import intent_recognizer

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
        db: Session
    ) -> Dict[str, Any]:
        """
        Process a chat request by:
        1. Loading conversation history
        2. Creating a new user message
        3. Running the Google Gemini agent to generate a response
        4. Capturing any tool calls made by the agent
        5. Saving the assistant response
        6. Returning the response with tool call details
        """
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
            message_lower = message.lower().strip()
            is_greeting = any(greeting in message_lower for greeting in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'])

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
        """Handle add_task requests"""
        tool_calls = []

        # Extract title from message or params
        title = params.get('title') or self._extract_task_title_from_message(message, IntentType.ADD_TASK)

        if not title:
            return response_templates.get_error("missing_parameter", action="add"), tool_calls

        try:
            # Call the add_task MCP tool with user_id propagation (per spec requirement)
            tool_result = await mcp_client.add_task(user_id=user_id, title=title)

            tool_call = {
                "name": "add_task",
                "arguments": {"user_id": user_id, "title": title},
                "result": tool_result
            }
            tool_calls.append(tool_call)

            # Return friendly confirmation message (per spec requirement)
            response_text = response_templates.get_confirmation("task_added", title=title)

            # Add proactive suggestion if needed
            # (per spec requirement: proactive suggestions)
            return response_text, tool_calls

        except Exception as e:
            import traceback
            print(f"❌ Error in add_task handler: {str(e)}")  # Log for debugging
            print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
            return response_templates.get_error("database_error"), tool_calls

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
            tool_result = await mcp_client.list_tasks(user_id=user_id, status=status)

            tool_call = {
                "name": "list_tasks",
                "arguments": {"user_id": user_id, "status": status},
                "result": tool_result
            }
            tool_calls.append(tool_call)

            if tool_result:
                # Format the task list with numbered items (per spec requirement)
                formatted_tasks = []
                for i, task in enumerate(tool_result, 1):
                    status_icon = "✓" if task.get("completed") else "○"
                    formatted_tasks.append(f"{i}. {status_icon} {task.get('title', 'Untitled')}")

                task_list = "\n".join(formatted_tasks)

                # Count pending and completed tasks for summary
                pending_count = sum(1 for t in tool_result if not t.get("completed"))
                completed_count = sum(1 for t in tool_result if t.get("completed"))

                response_text = f"{task_list}\n\n{response_templates.get_list_summary(pending_count, completed_count)}"

                # Add proactive suggestion if many completed tasks
                if completed_count > 3:
                    response_text += f"\n\n{response_templates.get_suggestion('clear_completed', count=completed_count)}"
            else:
                # Handle empty list case
                response_text = response_templates.get_error("empty_list", status=status)

            return response_text, tool_calls

        except Exception as e:
            import traceback
            print(f"❌ Error in list_tasks handler: {str(e)}")  # Log for debugging
            print(f"❌ Error details: {traceback.format_exc()}")  # Log full stack trace
            return response_templates.get_error("database_error"), tool_calls

    async def _handle_complete_task(self, user_id: str, message: str, params: Dict[str, str]) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle complete_task requests"""
        tool_calls = []

        # Extract task ID from message or params
        task_id_str = params.get('task_id') or self._extract_task_id_from_message(message)

        if task_id_str:
            try:
                task_id = int(task_id_str)

                # Call the complete_task MCP tool with user_id propagation
                tool_result = await mcp_client.complete_task(user_id=user_id, task_id=task_id)

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
        """Handle delete_task requests"""
        tool_calls = []

        # Extract task ID from message or params
        task_id_str = params.get('task_id') or self._extract_task_id_from_message(message)

        if task_id_str:
            try:
                task_id = int(task_id_str)

                # Call the delete_task MCP tool with user_id propagation
                tool_result = await mcp_client.delete_task(user_id=user_id, task_id=task_id)

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
        """Handle update_task requests"""
        tool_calls = []

        # Extract task ID from message or params
        task_id_str = params.get('task_id') or self._extract_task_id_from_message(message)

        if task_id_str:
            try:
                task_id = int(task_id_str)

                # For now, just update the title based on the message
                new_title = params.get('title') or self._extract_task_title_from_message(message, IntentType.UPDATE_TASK)

                if new_title:
                    # Call the update_task MCP tool with user_id propagation
                    tool_result = await mcp_client.update_task(
                        user_id=user_id,
                        task_id=task_id,
                        title=new_title
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

    async def _handle_title_based_lookup(self, user_id: str, message: str, intent_type: IntentType) -> Tuple[str, List[Dict[str, Any]]]:
        """Handle title-based task lookup for operations that require it"""
        tool_calls = []

        # First, list all tasks to find the one matching the title
        try:
            list_result = await mcp_client.list_tasks(user_id=user_id, status="all")

            tool_call = {
                "name": "list_tasks",
                "arguments": {"user_id": user_id, "status": "all"},
                "result": list_result
            }
            tool_calls.append(tool_call)

            # Extract the task title from the message
            search_title = self._extract_task_title_from_message(message, intent_type)

            if not search_title:
                return response_templates.get_question("ambiguous_task", action=self._get_action_word(intent_type)), tool_calls

            # Find tasks that match the title (with fuzzy matching - per research.md best practices)
            matching_tasks = []
            search_lower = search_title.lower()

            for task in list_result:
                if search_lower in task.get('title', '').lower():
                    matching_tasks.append(task)

            if len(matching_tasks) == 0:
                return response_templates.get_error("no_tasks_found", query=search_title), tool_calls
            elif len(matching_tasks) == 1:
                # Found exactly one match, proceed with the operation
                task = matching_tasks[0]
                task_id = task.get('id')

                if intent_type == IntentType.COMPLETE_TASK:
                    complete_result = await mcp_client.complete_task(user_id=user_id, task_id=task_id)

                    tool_call = {
                        "name": "complete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id},
                        "result": complete_result
                    }
                    tool_calls.append(tool_call)

                    response_text = response_templates.get_confirmation("task_completed", title=task.get('title'))

                elif intent_type == IntentType.DELETE_TASK:
                    delete_result = await mcp_client.delete_task(user_id=user_id, task_id=task_id)

                    tool_call = {
                        "name": "delete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id},
                        "result": delete_result
                    }
                    tool_calls.append(tool_call)

                    response_text = response_templates.get_confirmation("task_deleted", title=task.get('title'))

                elif intent_type == IntentType.UPDATE_TASK:
                    # For update, we need to extract the new title from the message
                    new_title = self._extract_task_title_from_message(message, intent_type)
                    update_result = await mcp_client.update_task(user_id=user_id, task_id=task_id, title=new_title)

                    tool_call = {
                        "name": "update_task",
                        "arguments": {"user_id": user_id, "task_id": task_id, "title": new_title},
                        "result": update_result
                    }
                    tool_calls.append(tool_call)

                    response_text = response_templates.get_confirmation("task_updated", title=new_title)

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
        message_clean = message.strip()

        # Remove common intent phrases to isolate the title
        if intent_type == IntentType.ADD_TASK:
            # Remove common add phrases
            import re
            phrases_to_remove = [
                r"(?:add|create|remember|i need to|remind me to|don't forget to)\s+",
                r"(?:a\s+)?(?:task|todo|thing|item)\s+(?:to\s+)?"
            ]

            for phrase in phrases_to_remove:
                message_clean = re.sub(phrase, "", message_clean, flags=re.IGNORECASE)

        elif intent_type == IntentType.UPDATE_TASK:
            # Remove common update phrases
            import re
            phrases_to_remove = [
                r"(?:change|update|edit|modify|rename)\s+(?:task|the|this|that)\s+",
                r"(?:the\s+)?(?:title|description)\s+(?:of\s+|to\s+|for\s+)?"
            ]

            for phrase in phrases_to_remove:
                message_clean = re.sub(phrase, "", message_clean, flags=re.IGNORECASE)

        # Clean up the remaining text
        message_clean = message_clean.strip(" .,!?")

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
    db: Session
) -> Dict[str, Any]:
    """Wrapper function to maintain backward compatibility"""
    return await agent_service.process_chat_request(user_id, conversation_id, message, db)