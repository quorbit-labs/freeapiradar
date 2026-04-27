# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**8/12 providers responding** · Last checked: 2026-04-27 19:24 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 100 | 160ms | 16 |  |
| 🟢 | **Cerebras** | 100 | 179ms | 4 |  |
| 🟢 | **SambaNova** | 100 | 447ms | 8 |  |
| 🟢 | **Mistral** | 100 | 472ms | 62 |  |
| 🟢 | **Cohere** | 100 | 270ms | 20 |  |
| 🟢 | **Fireworks AI** | 100 | 816ms | 11 |  |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🟡 | **Google AI Studio** | 20 | 109ms | 38 |  |
| 🟡 | **OpenRouter** | 20 | 282ms | 360 |  |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **fireworks**: model_added — `9` → `11` (2026-04-27T19:24)
- **openrouter**: status_change — `down` → `degrading` (2026-04-27T19:24)
- **cohere**: status_change — `down` → `stable` (2026-04-27T13:56)
- **openrouter**: status_change — `degrading` → `down` (2026-04-27T13:56)
- **cohere**: status_change — `stable` → `down` (2026-04-27T08:28)
- **openrouter**: model_added — `356` → `360` (2026-04-27T08:28)
- **openrouter**: model_added — `355` → `356` (2026-04-27T02:51)
- **openrouter**: model_added — `353` → `355` (2026-04-24T18:54)
- **openrouter**: model_added — `351` → `353` (2026-04-24T08:05)
- **fireworks**: model_removed — `10` → `9` (2026-04-24T02:43)

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
