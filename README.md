# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**8/12 providers responding** · Last checked: 2026-04-23 02:42 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 100 | 142ms | 16 |  |
| 🟢 | **Cerebras** | 100 | 131ms | 4 |  |
| 🟢 | **SambaNova** | 100 | 2096ms | 8 |  |
| 🟢 | **Mistral** | 100 | 358ms | 69 |  |
| 🟢 | **Cohere** | 100 | 285ms | 20 |  |
| 🟢 | **Fireworks AI** | 100 | 212ms | 12 |  |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🟢 | **OpenRouter** | 25 | 831ms | 348 |  |
| 🟡 | **Google AI Studio** | 20 | 68ms | 38 |  |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **fireworks**: model_added — `11` → `12` (2026-04-23T02:42)
- **openrouter**: model_removed — `349` → `348` (2026-04-23T02:42)
- **openrouter**: model_added — `349` → `348` (2026-04-23T02:42)
- **openrouter**: status_change — `degrading` → `stable` (2026-04-23T02:42)
- **openrouter**: model_added — `346` → `349` (2026-04-22T19:15)
- **cerebras**: status_change — `down` → `stable` (2026-04-22T02:39)
- **openrouter**: model_added — `344` → `346` (2026-04-22T02:39)
- **mistral**: model_removed — `63` → `67` (2026-04-21T19:14)
- **mistral**: model_added — `63` → `67` (2026-04-21T19:14)
- **cerebras**: status_change — `stable` → `down` (2026-04-21T19:14)

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
