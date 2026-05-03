# lossless-claw Config Guide

## Config (openclaw.json)

plugins.entries.lossless-claw.config:
- **contextThreshold** 0.6 — compress when context > 60% of 200k window
- **freshTailCount** 16 — keep last 16 messages uncompressed
- **incrementalMaxDepth** 5 — max 5 compression passes
- **dbPath** — SQLite DB for LCM storage

agents.defaults.heartbeat.lightContext: true — heartbeat uses light context mode

## What it does
- Monitors context window size
- Auto-compacts old messages into semantic summaries
- Preserves recent conversation at full fidelity
- LCM tools: lcm_grep, lcm_expand, lcm_describe for memory recall

## Caveman + lossless-claw
Layer 1 (SOUL.md): Output style — ~75% fewer output tokens
Layer 2 (lossless-claw): Context management — ~60% fewer input tokens
Combined: dramatically extended effective token budget
