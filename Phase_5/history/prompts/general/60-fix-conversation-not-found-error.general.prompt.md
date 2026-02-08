---
id: 60
title: Fix conversation not found error
stage: green
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-local-e2e-polish
user: Wajahat traders
command: /sp.analyze
labels: ["bug-fix","chat","conversation","error-handling"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/hooks/useChat.ts
tests:
 - Manual test: Try sending "Add a task Get medicine at 9:12 PM" after page refresh
---

## Prompt

Now the problem is when I run the input Add a task Get medicine add reminder at 9:12 PM to be notified. Than an error get Conversation 100 not found or doesn't belong to user 2
Here is the browser error Failed to load resource: the server responded with a status of 400 (Bad Request)Understand this error
117-df3024fe36accb84.js:1 Chat error: Error: Conversation 100 not found or doesn't belong to user 2  t o.request (page-573ba907ccf2dbb4.js:1:32898)
    at async page-573ba907ccf2dbb4.js:1:2826   at async D (page-573ba907ccf2dbb4.js:1:5601)
push.2304.window.console.error    @    117-df3024fe36accb84.js:1

## Response snapshot

## Root Cause Analysis

**Error**: `Conversation 100 not found or doesn't belong to user 2`

**Source**: Backend `agent.py:98` raises `ValueError` when conversation_id doesn't exist or belongs to different user

**Problem Flow**:
1. Frontend stores `conversationId` in Dapr state for persistence
2. On page load, frontend retrieves old `conversationId` (100) from Dapr
3. Frontend sends chat message with `conversation_id: 100`
4. Backend validates: conversation 100 doesn't exist (database was cleared/conversation deleted)
5. Backend returns 400 error with "Conversation 100 not found"
6. Chat fails for user

**Root Cause**: The frontend uses stale `conversationId` from Dapr state without handling the case where the conversation no longer exists on the backend.

### Fix Applied (`frontend/src/hooks/useChat.ts`)

Added automatic retry logic in `sendMessage()`:
```typescript
} catch (err: any) {
  console.error('Chat error:', err);
  const errorMessage = err.message || 'Failed to send message';

  // Check if error is about conversation not found
  if (errorMessage.includes('Conversation') && errorMessage.includes('not found') && conversationId) {
    console.log('♻️ Conversation not found, resetting and retrying with new conversation...');
    // Reset conversation ID and retry
    setConversationId(null);
    setError(null);

    // Remove the user message that failed
    setMessages((prev) => prev.filter(msg => msg.id !== userMessage.id));

    // Retry with null conversation ID (will create new conversation)
    setTimeout(() => {
      sendMessage(content);
    }, 100);
    return;
  }
```

**Behavior**: When conversation not found error occurs:
1. Reset `conversationId` to null
2. Remove the failed message from UI
3. Automatically retry the same message without conversation_id
4. Backend creates new conversation and responds successfully

## Outcome

- ✅ Impact: Fixed chat to automatically recover from stale conversation IDs
- 🧪 Tests: Manual test - send message after refreshing page with old conversation ID
- 📁 Files: frontend/src/hooks/useChat.ts
- 🔁 Next prompts: Test "Add a task Get medicine at 9:12 PM" after page refresh
- 🧠 Reflection: Client should be resilient to server state changes - auto-recover with new conversation

## Evaluation notes (flywheel)

- Failure modes observed: Stale conversation_id from Dapr state caused chat to fail permanently
- Graders run and results (PASS/FAIL): Pending user testing
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Add conversation validation endpoint to check validity before using
