# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**4/12 providers responding** · Last checked: 2026-03-27 02:29 UTC

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
| 🟢 | **Groq** | 63 | 253ms | 18 |  |
| 🟢 | **Cerebras** | 63 | 106ms | 2 |  |
| 🟢 | **SambaNova** | 63 | 215ms | 17 |  |
| ⚪ | **DeepSeek** | 50 | — | — |  |
| ⚪ | **xAI Grok** | 50 | — | — |  |
| ⚪ | **Mistral** | 50 | — | — |  |
| ⚪ | **Together AI** | 50 | — | — |  |
| ⚪ | **Cohere** | 50 | — | — |  |
| ⚪ | **Fireworks AI** | 50 | — | — |  |
| ⚪ | **Cloudflare Workers AI** | 50 | — | — |  |
| 🟡 | **Google AI Studio** | 40 | 291ms | 33 |  |
| 🔴 | **OpenRouter** | 30 | 127ms | 346 | {"error":{"message":"No endpoints found for deepse... |

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

- **sambanova**: model_added — `16` → `17` (2026-03-27T02:29)
- **openrouter**: model_removed — `347` → `346` (2026-03-27T02:29)
- **sambanova**: model_added — `0` → `16` (2026-03-25T21:11)
- **sambanova**: status_change — `unknown` → `stable` (2026-03-25T21:11)
- **cerebras**: model_added — `0` → `2` (2026-03-25T21:11)
- **cerebras**: status_change — `unknown` → `stable` (2026-03-25T21:11)
- **openrouter**: model_added — `0` → `347` (2026-03-25T21:11)
- **openrouter**: status_change — `unknown` → `down` (2026-03-25T21:11)
- **google_ai**: model_added — `0` → `33` (2026-03-25T21:11)
- **google_ai**: status_change — `unknown` → `degrading` (2026-03-25T21:11)

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
