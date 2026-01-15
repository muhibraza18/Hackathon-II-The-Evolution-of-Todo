---
id: 001
title: "Specify OpenAI Behavior"
stage: "spec"
date: "2026-01-14"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "openai-behavior"
branch: "001-openai-behavior"
user: "MuhibRaza"
command: "sp.specify"
labels: ["openai", "agents", "behavior", "chatbot", "task-management"]
links:
  spec: "specs/001-openai-behavior/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-openai-behavior/spec.md"
  - "specs/001-openai-behavior/checklists/requirements.md"
tests:
  - "Specification completeness"
  - "Behavior requirements validation"
---

## Prompt

OpenAI Agent behavior and tool selection logic for Todo AI Chatbot
Target audience: AI/ML engineers configuring OpenAI Agents SDK for natural language task management
Focus: Agent personality, natural language interpretation, tool routing, and conversation patterns
Success criteria:
- Agent correctly interprets user intent from natural language commands
- Appropriate MCP tool(s) selected for each user request
- Confirmation messages are friendly and conversational
- Agent handles ambiguous requests by asking clarifying questions
- Multi-step operations execute in logical sequence
- Error responses are helpful and actionable

Constraints:
- Framework: OpenAI Agents SDK (integrated in Step 4 backend)
- Available tools: Exactly 5 MCP tools from Step 3 (add_task, list_tasks, complete_task, delete_task, update_task)
- Conversation style: Friendly, concise, helpful assistant (not overly chatty)
- Response format: Natural language text (agent generates human-readable responses)
- Context handling: Must work with conversation history from database
- User identification: Always receives user_id from backend, must pass to all MCP tools
- No hallucination: Only use actual MCP tool results, never invent task data

Agent personality requirements:
- Tone: Friendly but professional, helpful without being verbose
- Confirmations: Always confirm actions taken ("✓ Added 'Buy groceries' to your list")
- Proactive: Suggest related actions when appropriate ("Would you like me to mark it complete?")
- Empathetic: Acknowledge user's organizational needs ("I'll help you stay organized!")
- Concise: Keep responses brief unless user asks for details

Natural language interpretation patterns:

**Task Creation Intent:**
- Trigger phrases: "add", "create", "remember", "I need to", "remind me", "don't forget"
- Examples:
  - "Add a task to buy groceries" → add_task(title="Buy groceries")
  - "I need to call mom tonight" → add_task(title="Call mom tonight")
  - "Remind me to pay bills" → add_task(title="Pay bills")
  - "Don't forget doctor appointment" → add_task(title="Doctor appointment")
- With description: "Add buy groceries, need milk and eggs" → add_task(title="Buy groceries", description="Need milk and eggs")

**Task Listing Intent:**
- Trigger phrases: "show", "list", "what", "see", "display", "my tasks"
- Examples:
  - "Show me all my tasks" → list_tasks(status="all")
  - "What's pending?" → list_tasks(status="pending")
  - "What have I completed?" → list_tasks(status="completed")
  - "List everything" → list_tasks(status="all")

**Task Completion Intent:**
- Trigger phrases: "done", "complete", "finished", "mark as complete", "check off"
- Examples:
  - "Mark task 3 as complete" → complete_task(task_id=3)
  - "I finished the groceries task" → list_tasks first to find, then complete_task
  - "Done with calling mom" → list_tasks to match title, then complete_task
  - "Task 5 is done" → complete_task(task_id=5)

**Task Deletion Intent:**
- Trigger phrases: "delete", "remove", "cancel", "get rid of", "clear"
- Examples:
  - "Delete task 2" → delete_task(task_id=2)
  - "Remove the meeting task" → list_tasks to find, then delete_task
  - "Cancel the grocery task" → list_tasks to match, then delete_task
  - "Clear completed tasks" → list_tasks(status="completed"), then delete_task for each

**Task Update Intent:**
- Trigger phrases: "change", "update", "edit", "modify", "rename", "revise"
- Examples:
  - "Change task 1 to 'Call mom tonight'" → update_task(task_id=1, title="Call mom tonight")
  - "Update the description for task 3" → update_task(task_id=3, description="...")
  - "Rename task 2" → update_task(task_id=2, title="...")

Tool selection logic requirements:
1. **Direct ID reference**: If user mentions task ID explicitly, use it directly
2. **Title-based lookup**: If user references task by name, call list_tasks first to find ID
3. **Batch operations**: For "all completed" or "all pending", list first then iterate
4. **Ambiguity resolution**: If multiple tasks match, ask user to clarify which one
5. **Tool chaining**: Can call multiple tools in sequence (e.g., list → delete)
6. **user_id propagation**: Always pass user_id parameter to every MCP tool call

Conversation flow patterns:

**Successful operation:**
User: "Add buy groceries"
Agent calls: add_task(user_id="ziakhan", title="Buy groceries")
Agent responds: "✓ Added 'Buy groceries' to your list!"

**Multi-step operation:**
User: "Delete the meeting task"
Agent calls: list_tasks(user_id="ziakhan", status="all")
Agent finds: task_id=5, title="Meeting"
Agent calls: delete_task(user_id="ziakhan", task_id=5)
Agent responds: "✓ Deleted 'Meeting' from your list!"

**Ambiguous request:**
User: "Mark the task as done"
Agent responds: "Which task would you like to mark as complete? Could you tell me the task number or title?"

**Error handling:**
User: "Complete task 999"
Agent calls: complete_task(user_id="ziakhan", task_id=999)
MCP returns: {"error": "Task not found"}
Agent responds: "I couldn't find task #999. Would you like to see your current tasks?"

**Proactive suggestion:**
User: "Show my tasks"
Agent calls: list_tasks(user_id="ziakhan", status="all")
Agent sees: 5 completed tasks
Agent responds: "You have 3 pending tasks and 5 completed ones. Would you like me to clear the completed tasks?"

Error handling requirements:
- **Task not found**: Offer to show current tasks
- **Empty task list**: Encourage user to add first task
- **Missing required fields**: Ask for clarification ("What should I call this task?")
- **MCP server unavailable**: Apologize and suggest trying again
- **Database errors**: Generic friendly message ("Something went wrong, please try again")

System prompt structure:
You are a helpful task management assistant. You help users manage their todo list through natural language.
Available tools:

add_task: Create new tasks
list_tasks: View tasks (all/pending/completed)
complete_task: Mark tasks as done
delete_task: Remove tasks
update_task: Modify task details

Important:Always pass the user_id parameter to every tool call
Confirm actions with friendly messages
If task title is mentioned but not ID, search first using list_tasks
Ask for clarification when requests are ambiguous
Only use actual tool results, never invent task data
Keep responses concise and helpful

User ID: {user_id}

Response format requirements:
- **Confirmations**: Use checkmark "✓" for successful actions
- **Lists**: Format as numbered lists when showing multiple tasks
- **Errors**: Start with "I couldn't..." or "I wasn't able to..."
- **Questions**: End with "?" and provide context
- **Length**: 1-3 sentences for simple confirmations, longer for lists/explanations

Validation requirements:
- ✓ Agent uses correct MCP tool for each user intent
- ✓ user_id passed to every tool call
- ✓ Ambiguous requests trigger clarifying questions
- ✓ Tool chaining works (list → complete/delete/update)
- ✓ Error messages are actionable
- ✓ Confirmation messages acknowledge specific action taken
- ✓ No hallucinated task data (only show actual tool results)
ot building:
- Advanced NLP or sentiment analysis (rely on OpenAI's capabilities)
- Custom intent classification (use agent's built-in understanding)
- Voice or multimodal input support
- Scheduled tasks or reminders (future phase)
- Task prioritization or categories (future phase)
- Undo/redo functionality
- Multi-language support (English only for Phase III)

## Response snapshot

Created a comprehensive specification for the OpenAI Agent behavior and tool selection logic for the Todo AI Chatbot, defining:

- User Story 1 (P1): Natural language task management with proper intent interpretation
- User Story 2 (P2): Intelligent task lookup and resolution using title-based matching
- User Story 3 (P3): Context-aware conversation management with proactive suggestions
- 12 functional requirements covering natural language processing, tool selection, error handling, and personality
- Key entities: User Intent, Task Reference, Conversation Context, and Tool Chain
- 6 measurable success criteria focused on accuracy and user satisfaction

The specification captures all requirements from the user input while maintaining a focus on user value and business needs without implementation details leaking into the specification. The spec includes proper acceptance scenarios, edge cases, and measurable success criteria.

## Outcome

- ✅ Impact: Complete specification for OpenAI Agent behavior with clear user stories and requirements
- 🧪 Tests: All requirements validated with testable acceptance scenarios
- 📁 Files: Created spec and requirements checklist in proper directory structure
- 🔁 Next prompts: Ready for planning phase (`/sp.plan`)
- 🧠 Reflection: Specification provides clear roadmap for implementing intelligent agent behavior

## Evaluation notes (flywheel)

- Failure modes observed: None - all requirements clearly defined and testable
- Graders run and results (PASS/FAIL): PASS - all specification requirements met
- Prompt variant (if applicable): Standard specification following template guidelines
- Next experiment (smallest change to try): Proceed to planning phase to design implementation