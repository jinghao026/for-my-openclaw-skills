---
name: openclaw-persistent-memory
description: |
  Persistent memory system for OpenClaw with automatic context capture and
  semantic search. Uses SQLite + FTS5 for fast full-text search.
  
  Features:
  - Auto-capture: Important observations saved automatically
  - Auto-recall: Relevant memories injected before each prompt
  - Tools: memory_search, memory_get, memory_store, memory_delete
---

# OpenClaw Persistent Memory

Give your AI agent long-term memory with automatic context capture and recall.

## Features

- 🧠 **Auto-capture** - Important observations saved automatically
- 🔍 **Auto-recall** - Relevant memories injected before each prompt
- 💾 **SQLite + FTS5** - Fast full-text search
- 🛠️ **Tools** - `memory_search`, `memory_get`, `memory_store`, `memory_delete`

## Installation

### Via ClawHub (Recommended)
```bash
clawhub install openclaw-persistent-memory
```

### Via npm
```bash
npm install -g openclaw-persistent-memory
```

## Usage

The skill provides these tools:

| Tool | Description |
|------|-------------|
| `memory_search` | Search memories by query |
| `memory_get` | Get specific memory by ID |
| `memory_store` | Store new memory |
| `memory_delete` | Delete memory by ID |

## How it works

1. **Auto-Capture**: After every AI turn, important observations are extracted and stored
2. **Auto-Recall**: Before each prompt, relevant memories are retrieved and injected as context
3. **Semantic Search**: Uses embeddings to find conceptually similar memories
4. **Full-Text Search**: SQLite FTS5 enables fast keyword search

## Storage

- Local SQLite database
- No cloud dependency
- Fast local queries

## Source

Original: https://github.com/webdevtodayjason/openclaw-persistent-memory
Author: Jason Brashear / Titanium Computing
License: AGPL-3.0
Stars: 779★
