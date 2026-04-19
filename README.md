# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**8/12 providers responding** · Last checked: 2026-04-19 13:04 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 100 | 89ms | 16 |  |
| 🟢 | **Cerebras** | 100 | 135ms | 4 |  |
| 🟢 | **SambaNova** | 100 | 356ms | 8 |  |
| 🟢 | **Mistral** | 100 | 600ms | 62 |  |
| 🟢 | **Cohere** | 100 | 373ms | 20 |  |
| 🟢 | **Fireworks AI** | 100 | 277ms | 12 |  |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🟡 | **Google AI Studio** | 20 | 81ms | 36 |  |
| 🟡 | **OpenRouter** | 20 | 209ms | 342 |  |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **openrouter**: model_removed — `343` → `342` (2026-04-19T02:46)
- **openrouter**: model_removed — `345` → `343` (2026-04-18T02:30)
- **fireworks**: model_removed — `13` → `12` (2026-04-17T19:02)
- **openrouter**: model_removed — `346` → `345` (2026-04-17T02:39)
- **sambanova**: model_removed — `9` → `8` (2026-04-16T19:16)
- **openrouter**: model_added — `345` → `346` (2026-04-16T19:16)
- **groq**: model_removed — `18` → `16` (2026-04-16T07:48)
- **sambanova**: model_removed — `10` → `9` (2026-04-16T02:44)
- **openrouter**: model_added — `344` → `345` (2026-04-15T19:20)
- **google_ai**: model_added — `35` → `36` (2026-04-15T19:20)

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
