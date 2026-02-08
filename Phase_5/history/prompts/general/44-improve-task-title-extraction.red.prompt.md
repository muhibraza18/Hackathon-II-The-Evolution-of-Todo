---
id: 44
title: improve-task-title-extraction
stage: red
date_iso: 2026-01-27
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: Wajahat traders
command: /sp.analyze
labels:
  - backend
  - agent
  - task-extraction
  - intent-classification
  - complete-task
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - backend/app/services/agent.py
tests_yaml:
  - task title extraction
  - complete task operations
  - intent recognition
---

# Improve Task Title Extraction Logic

## Prompt Text
```
still this behavor was persisting please resolve this from root and made agent If we said it to rename task so it rename. If we said marks tasks as complete so it complete also After makes changes make a task complete with MCP and check the logs
```

## Response Text

Identified and fixed the task title extraction issue:

1. The system was not properly extracting task titles from complete requests like "Mark Updated task title to complete"
2. Enhanced `_extract_task_title_from_message` method to handle different intent types properly
3. Added specific extraction patterns for COMPLETE_TASK and DELETE_TASK intents
4. Improved regex patterns to extract task titles from "mark [title] to complete" style requests
5. Added better cleanup for extracted titles with proper space normalization
6. Restarted backend service to apply changes

## Outcome

Task title extraction now properly handles complete and update requests with natural language patterns.

## Evaluation

The task title extraction logic now properly handles various natural language request patterns.