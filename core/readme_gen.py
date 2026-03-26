# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Generate README.md with live status table from status.json."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


STATUS_ICONS = {
    "stable": "🟢",
    "degrading": "🟡",
    "down": "🔴",
    "unknown": "⚪",
}


def generate_readme(data_dir: Path, statuses: dict):
    """Generate README.md with provider status table."""
    project_root = data_dir.parent
    readme_path = project_root / "README.md"

    # Count working providers
    working = sum(
        1 for s in statuses.values()
        if s.get("status") in ("stable", "degrading")
    )
    total = len(statuses)

    # Load recent changes
    changes_file = data_dir / "changes.json"
    recent_changes = []
    if changes_file.exists():
        try:
            all_changes = json.loads(changes_file.read_text())
            recent_changes = all_changes[-10:]  # last 10
        except (json.JSONDecodeError, TypeError):
            pass

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Build status table
    table_rows = []
    for name, s in sorted(statuses.items(), key=lambda x: x[1].get("confidence", 0), reverse=True):
        icon = STATUS_ICONS.get(s.get("status", "unknown"), "⚪")
        display = s.get("display_name", name)
        conf = s.get("confidence", "?")
        ping_ms = s.get("ping_test", {}).get("ttfb_ms")
        ping_str = f"{ping_ms:.0f}ms" if isinstance(ping_ms, (int, float)) and ping_ms > 0 else "—"
        models = s.get("models_endpoint", {}).get("models_count", "—")
        error = s.get("ping_test", {}).get("error", "")
        note = ""
        if error and s.get("status") == "down":
            # Truncate error for table
            note = error[:50] + "..." if len(error) > 50 else error

        table_rows.append(
            f"| {icon} | **{display}** | {conf} | {ping_str} | {models} | {note} |"
        )

    status_table = "\n".join(table_rows)

    # Build changes section
    changes_section = ""
    if recent_changes:
        changes_lines = []
        for c in reversed(recent_changes):
            provider = c.get("provider", "?")
            change_type = c.get("change_type", "?")
            old_val = c.get("old_value", "")
            new_val = c.get("new_value", "")
            detected = c.get("detected_at", "")[:16]
            changes_lines.append(
                f"- **{provider}**: {change_type} — `{old_val}` → `{new_val}` ({detected})"
            )
        changes_section = "\n".join(changes_lines)
    else:
        changes_section = "_No changes detected yet._"

    readme_content = f"""# FreeAPIRadar

> Don't guess. Know which free AI APIs work — right now.

**{working}/{total} providers responding** · Last checked: {now}

## Current Status

| Status | Provider | Confidence | Latency | Models | Notes |
|--------|----------|------------|---------|--------|-------|
{status_table}

**Legend:** 🟢 stable · 🟡 degrading · 🔴 down · ⚪ unknown

## Recent Changes

{changes_section}

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
working = {{k: v for k, v in status.items() if v["status"] == "stable"}}
print(f"{{len(working)}} providers working right now")
```

## Part of the QUORBIT Ecosystem

FreeAPIRadar is the data layer for [QUORBIT Protocol](https://github.com/quorbit-labs/core) — a decentralized AI agent orchestration system. QUORBIT uses FreeAPIRadar data for intelligent provider routing.

## Contributing

Found a provider we're missing? Rate limits changed? Open an issue or PR.

## License

AGPL-3.0 · Copyright (c) 2026 Quorbit Labs
"""

    readme_path.write_text(readme_content, encoding="utf-8")
