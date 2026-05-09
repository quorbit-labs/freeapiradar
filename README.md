# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**8/12 providers responding** · Last checked: 2026-05-09 13:19 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 100 | 137ms | 16 |  |
| 🟢 | **Cerebras** | 100 | 220ms | 4 |  |
| 🟢 | **SambaNova** | 100 | 188ms | 9 |  |
| 🟢 | **Mistral** | 100 | 596ms | 68 |  |
| 🟢 | **Cohere** | 100 | 256ms | 20 |  |
| 🟢 | **Fireworks AI** | 100 | 270ms | 11 |  |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🟡 | **Google AI Studio** | 20 | 171ms | 33 |  |
| 🟡 | **OpenRouter** | 20 | 389ms | 367 |  |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **openrouter**: status_change — `stable` → `degrading` (2026-05-09T07:57)
- **openrouter**: model_removed — `367` → `367` (2026-05-09T02:53)
- **openrouter**: model_added — `367` → `367` (2026-05-09T02:53)
- **openrouter**: status_change — `degrading` → `stable` (2026-05-09T02:53)
- **openrouter**: model_removed — `367` → `367` (2026-05-08T19:19)
- **openrouter**: model_added — `367` → `367` (2026-05-08T19:19)
- **openrouter**: model_removed — `369` → `367` (2026-05-08T02:57)
- **openrouter**: model_removed — `368` → `369` (2026-05-07T19:43)
- **openrouter**: model_added — `368` → `369` (2026-05-07T19:43)
- **sambanova**: model_added — `0` → `9` (2026-05-07T14:11)

## What is this?

FreeAPIRadar is a **change intelligence layer** for free AI APIs. Not a catalog. Not uptime monitoring. We track what actually changed and what's working right now.

**What we show:**
- Status: 🟢 stable / 🟡 degrading / 🔴 down (not exact RPM numbers)
- Changes: "Groq: RPM increased" (not "30 RPM")
- Confidence score: 0-100, decays on failures, recovers slowly
- Trends, not absolutes (Goodhart's Law protection)

**What we don't show:**
- Exact rate limits (invites gaming)
- Leaderboards (kills #1 provider)
- Real-time data (6-24h delay)

## Monitored Providers

Groq · DeepSeek · Google AI Studio · OpenRouter · Cerebras · SambaNova · xAI Grok · Mistral · Together AI · Cohere · Fireworks AI · Cloudflare Workers AI

## How it works

1. GitHub Actions runs checks every 6 hours
2. Each provider gets: model list + ping test + rate limit headers
3. Results compared with previous run → changes detected
4. Confidence scores updated (slow recovery, fast decay)
5. README auto-generated, status.json committed

## For developers

```python
import json, urllib.request

# Get current status
url = "https://raw.githubusercontent.com/quorbit-labs/freeapiradar/main/data/status.json"
status = json.loads(urllib.request.urlopen(url).read())

# Find working providers
working = {k: v for k, v in status.items() if v["status"] == "stable"}
print(f"{len(working)} providers working right now")
```

## Part of the QUORBIT Ecosystem

FreeAPIRadar is the data layer for [QUORBIT Protocol](https://github.com/quorbit-labs/core) — a decentralized AI agent orchestration system. QUORBIT uses FreeAPIRadar data for intelligent provider routing.

## Contributing

Found a provider we're missing? Rate limits changed? Open an issue or PR.

## License

AGPL-3.0 · Copyright (c) 2026 Quorbit Labs
