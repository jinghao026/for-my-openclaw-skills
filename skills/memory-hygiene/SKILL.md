---
name: memory-hygiene
description: |
  Memory hygiene tools for OpenClaw.
  Helps clean up and maintain healthy memory stores.
  Identifies and removes duplicate, outdated, or low-quality memories.
---

# Memory Hygiene

Keep your OpenClaw memory clean and efficient.

## Purpose

Over time, memory systems can accumulate:
- Duplicate entries
- Outdated information
- Low-quality captures
- Noise from auto-capture

This skill helps maintain memory hygiene through periodic cleaning.

## Configuration

The main source of junk is `autoCapture: true`. Disable it:

```json
{
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "config": {
          "autoCapture": false,
          "autoRecall": true
        }
      }
    }
  }
}
```

Use `gateway action=config.patch` to apply.

## Best Practices

1. **Periodic Review**: Schedule weekly memory audits
2. **Deduplication**: Remove duplicate or similar entries
3. **Expiration**: Set TTL for temporary memories
4. **Quality Control**: Review auto-captured memories regularly

## Cleaning Tasks

- Remove exact duplicates
- Merge similar memories
- Delete outdated information
- Compact memory storage

## Source

Original: https://github.com/dylanbaker24/memory-hygiene
License: MIT
