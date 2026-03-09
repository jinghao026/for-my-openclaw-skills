# Memory System Configuration

## Overview
Simple file-based memory system for OpenClaw agent.

## How It Works
1. Store user info in `memory/USER.md`
2. Store daily conversations in `memory/YYYY-MM-DD.md`
3. Agent reads these files at session start
4. New info is appended automatically

## Files
- `memory/USER.md` - User profile (email, preferences, etc.)
- `memory/HISTORY.md` - Recent conversation summaries
- `memory/TASKS.md` - Ongoing tasks and todos

## Usage
The agent will automatically:
1. Read USER.md at startup to know user preferences
2. Check HISTORY.md for recent context
3. Write new info to appropriate files
