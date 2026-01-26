---
id: "004"
title: "Fix frontend useChat.js import error"
stage: "general"
date_iso: "2026-01-14"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "002-chatkit-frontend"
user: "Wajahat traders"
command: "sp.analyze My frontend was using useChat.js but I deleted it just now because we have to use useChat.ts now js so please resolve this and frontend have to use useChat.ts"
labels: ["frontend", "nextjs", "import", "troubleshooting"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "./frontend/.next"
  - "./frontend/src/components/ChatInterface.tsx"
  - "./frontend/src/hooks/useChat.ts"
tests_yaml: []
---

## Prompt

```
 My frontend was using useChat.js but I deleted it just now because we have to use useChat.ts now js so please resolve this and frontend have to use useChat.ts
```

## Response

Resolved the frontend error caused by Next.js cache referencing a deleted useChat.js file. The issue occurred because:

1. There was likely an old useChat.js file that was deleted and replaced with useChat.ts
2. Next.js had cached build artifacts in the .next directory that still referenced the old useChat.js file
3. The ChatInterface.tsx file correctly imports from '../hooks/useChat' which resolves to useChat.ts

The fix involved clearing the Next.js cache by removing the .next directory, which forced a fresh build. The import statement in ChatInterface.tsx (import { useChat } from '../hooks/useChat';) correctly resolves to the useChat.ts file and works as expected. The frontend now runs successfully.