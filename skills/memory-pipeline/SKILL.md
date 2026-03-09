---
name: memory-pipeline
description: |
  Structured memory pipeline for OpenClaw agents.
  Provides memory briefing, checklist-based recall, and after-action reviews.
---

# Memory Pipeline

Structured memory pipeline for OpenClaw agents.

## Features

- 📋 **Memory Briefing** - Automatic context summarization before tasks
- ✅ **Checklists** - Structured recall prompts for consistent behavior
- 📝 **After-Action Reviews** - Automatic documentation of completed tasks
- 🎯 **Tool Filtering** - Deny dangerous tools based on context

## Configuration

Configure via `openclaw.plugin.json` or your agent config:

```json
{
  "enabled": true,
  "briefing": {
    "maxChars": 6000,
    "checklist": [
      "Restate the task in one sentence.",
      "List constraints and success criteria.",
      "Retrieve only the minimum relevant memory.",
      "Prefer tools over guessing when facts matter."
    ],
    "memoryFiles": ["memory/IDENTITY.md", "memory/PROJECTS.md"]
  },
  "tools": {
    "deny": ["dangerous_tool"],
    "maxToolResultChars": 12000
  },
  "afterAction": {
    "writeMemoryFile": "memory/AFTER_ACTION.md",
    "maxBullets": 8
  }
}
```

## Requirements

At least one LLM API key is required:
- OpenAI API key (for GPT-4o-mini + embeddings)
- Anthropic API key (for Claude Haiku)
- Gemini API key (for Gemini Flash)

## How it works

1. **Before Task**: Loads briefing checklist and relevant memory files
2. **During Task**: Enforces tool restrictions and monitors context size
3. **After Task**: Writes structured summary to after-action memory file

## Source

Original: https://github.com/bodii88/memory-pipeline
License: MIT
