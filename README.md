# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**7/12 providers responding** · Last checked: 2026-04-13 19:15 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 100 | 228ms | 18 |  |
| 🟢 | **Cerebras** | 100 | 192ms | 4 |  |
| 🟢 | **SambaNova** | 100 | 361ms | 12 |  |
| 🟢 | **Mistral** | 100 | 755ms | 62 |  |
| 🟢 | **Fireworks AI** | 100 | 345ms | 12 |  |
| 🔴 | **Cohere** | 90 | 47ms | 0 | {"id":"51aeebd1-f934-41d1-bb2e-224ce47447c2","mess... |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🟡 | **Google AI Studio** | 20 | 75ms | 34 |  |
| 🟡 | **OpenRouter** | 20 | 233ms | 350 |  |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **cohere**: model_removed — `20` → `0` (2026-04-13T19:15)
- **cohere**: status_change — `stable` → `down` (2026-04-13T19:15)
- **openrouter**: model_added — `349` → `350` (2026-04-13T19:15)
- **openrouter**: model_removed — `350` → `349` (2026-04-13T02:46)
- **openrouter**: status_change — `stable` → `degrading` (2026-04-11T07:02)
- **openrouter**: status_change — `degrading` → `stable` (2026-04-11T02:23)
- **fireworks**: model_removed — `13` → `12` (2026-04-10T07:43)
- **mistral**: model_removed — `65` → `60` (2026-04-10T07:43)
- **openrouter**: model_removed — `351` → `350` (2026-04-10T02:39)
- **mistral**: model_added — `60` → `65` (2026-04-09T19:08)

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
