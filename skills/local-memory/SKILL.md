---
name: local-memory
description: |
  Local file-based memory system for OpenClaw.
  Stores user info, conversation history, and task tracking in markdown files.
  
  Files:
  - memory/USER.md - User profile and preferences
  - memory/HISTORY.md - Conversation history
  - memory/TASKS.md - Task tracking
  - memory/YYYY-MM-DD.md - Daily logs
---

# Local Memory Skill

## Quick Start

1. Read user info at session start:
```
read: memory/USER.md
```

2. Read recent history:
```
read: memory/HISTORY.md
```

3. Log new info:
```
edit: memory/USER.md (append)
edit: memory/2026-03-08.md (create if not exists)
```

## File Structure

```
memory/
├── USER.md          # User profile (email, prefs, etc.)
├── HISTORY.md       # Recent conversation summaries
├── TASKS.md         # Ongoing tasks
├── README.md        # This documentation
└── 2026-03-08.md    # Daily log (auto-created)
```

## Usage in Conversations

When user provides new info:
1. Immediately update memory/USER.md
2. Log conversation to daily file
3. Update HISTORY.md with summary

Example updates:
- New email → update USER.md
- New preference → update USER.md  
- Completed task → update TASKS.md
- Important decision → update HISTORY.md
