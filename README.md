# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**7/12 providers responding** · Last checked: 2026-04-05 16:44 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 75 | 256ms | 18 |  |
| 🟢 | **Cerebras** | 75 | 110ms | 4 |  |
| 🟢 | **SambaNova** | 75 | 225ms | 17 |  |
| 🟢 | **Mistral** | 60 | 399ms | 61 |  |
| 🟢 | **Fireworks AI** | 60 | 288ms | 12 |  |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🔴 | **Cohere** | 40 | 75ms | 20 | {"id":"c0a00e70-a37e-4c89-9ca4-20452d7ae7e2","mess... |
| 🟡 | **Google AI Studio** | 20 | 94ms | 34 |  |
| 🟡 | **OpenRouter** | 20 | 300ms | 349 |  |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **fireworks**: model_added — `0` → `12` (2026-04-05T16:44)
- **fireworks**: status_change — `unknown` → `stable` (2026-04-05T16:44)
- **cohere**: model_added — `0` → `20` (2026-04-05T16:44)
- **cohere**: status_change — `unknown` → `down` (2026-04-05T16:44)
- **mistral**: model_added — `0` → `59` (2026-04-05T16:44)
- **mistral**: status_change — `unknown` → `stable` (2026-04-05T16:44)
- **cerebras**: model_added — `2` → `4` (2026-04-05T16:44)
- **openrouter**: confidence_shift — `0` → `20` (2026-04-05T16:44)
- **openrouter**: model_removed — `346` → `349` (2026-04-05T16:44)
- **openrouter**: model_added — `346` → `349` (2026-04-05T16:44)

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
