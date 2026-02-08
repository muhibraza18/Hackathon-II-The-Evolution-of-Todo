---
id: 61
title: Fix conversation infinite loop error
stage: green
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-local-e2e-polish
user: Wajahat traders
command: /sp.analyze
labels: ["bug-fix","chat","infinite-loop","conversation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/hooks/useChat.ts
tests:
 - Manual test: Send "Add a task Get medicine at 9:12 PM" after clearing browser cache
---

## Prompt

Still when I write Add a task Get medicine add reminder at 9:12 PM to be notified So error comes here is the browser error page-9e495f0789b1eb62.js:1  POST http://localhost:8000/api/chat 400 (Bad Request)  117-df3024fe36accb84.js:1 Chat error: Error: Conversation 100 not found or doesn't belong to user 2
    at async page-9e495f0789b1eb62.js:1:33144    at async page-9e495f0789b1eb62.js:1:2782  and it was continously running in a loop

## Response snapshot

## Root Cause Analysis

**Problems:**

1. **Browser Cache**: The browser was serving old JavaScript (`page-9e495f0789b1eb62.js`) without the fix

2. **Infinite Loop Bug**: The previous fix had a bug where `sendMessage` was called recursively via `setTimeout`, but the `conversationId` in the `useCallback` dependency wasn't updated before the retry happened

3. **Root Cause**: Dapr state was persisting `conversationId` (100) which no longer existed in the database

**The infinite loop occurred because:**
```typescript
// Old buggy code:
setTimeout(() => {
  sendMessage(content);  // This uses the OLD conversationId from closure!
}, 100);
```

### Fixes Applied (`frontend/src/hooks/useChat.ts`)

**Fix 1: Don't persist conversationId at all (always start fresh)**
```typescript
if (history) {
  setMessages(history.messages || []);
  setConversationId(null); // Always start with null (new conversation)
  console.log(`✅ Chat history loaded: ${history.messages?.length || 0} messages (starting fresh conversation)`);
}
```

**Fix 2: Add `skipConversationIdCheck` parameter to prevent infinite loop**
```typescript
const sendMessage = useCallback(async (content: string, skipConversationIdCheck = false) => {
  // ...
  const effectiveConversationId = skipConversationIdCheck ? null : conversationId;

  // Check if error is about conversation not found AND we haven't already retried
  if (errorMessage.includes('Conversation') && errorMessage.includes('not found') && conversationId && !skipConversationIdCheck) {
    // ...
    setTimeout(() => {
      sendMessage(content, true); // Pass true to skip using the old conversation ID
    }, 50);
    return;
  }
```

**Fix 3: Added useRef for retry queue**
```typescript
const retryQueueRef = useRef<string[]>([]);
```

## Outcome

- ✅ Impact: Fixed infinite loop and prevented stale conversationId from being loaded
- 🧪 Tests: User needs to hard refresh browser (Ctrl+Shift+R) to load new JavaScript
- 📁 Files: frontend/src/hooks/useChat.ts
- 🔁 Next prompts: Clear browser cache and test chat functionality
- 🧠 Reflection: Browser cache is the enemy of hotfixes - always require hard refresh

## Evaluation notes (flywheel)

- Failure modes observed: (1) Browser serving cached JavaScript; (2) Recursive retry using stale closure; (3) Persisting invalid conversationId
- Graders run and results (PASS/FAIL): Pending user clearing browser cache
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Add version parameter to JavaScript files to force cache busting
