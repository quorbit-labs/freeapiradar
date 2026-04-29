# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**8/12 providers responding** · Last checked: 2026-04-29 13:59 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 100 | 93ms | 16 |  |
| 🟢 | **Cerebras** | 100 | 233ms | 4 |  |
| 🟢 | **SambaNova** | 100 | 600ms | 8 |  |
| 🟢 | **Mistral** | 100 | 379ms | 64 |  |
| 🟢 | **Cohere** | 100 | 2724ms | 20 |  |
| 🟢 | **Fireworks AI** | 100 | 3802ms | 11 |  |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🟡 | **Google AI Studio** | 20 | 94ms | 38 |  |
| 🟡 | **OpenRouter** | 20 | 342ms | 369 |  |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **mistral**: models_count_changed — `62` → `64` (2026-04-29T08:20)
- **openrouter**: model_removed — `371` → `369` (2026-04-29T02:57)
- **openrouter**: model_added — `367` → `371` (2026-04-28T19:42)
- **openrouter**: model_added — `360` → `367` (2026-04-28T03:20)
- **fireworks**: model_added — `9` → `11` (2026-04-27T19:24)
- **openrouter**: status_change — `down` → `degrading` (2026-04-27T19:24)
- **cohere**: status_change — `down` → `stable` (2026-04-27T13:56)
- **openrouter**: status_change — `degrading` → `down` (2026-04-27T13:56)
- **cohere**: status_change — `stable` → `down` (2026-04-27T08:28)
- **openrouter**: model_added — `356` → `360` (2026-04-27T08:28)

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
