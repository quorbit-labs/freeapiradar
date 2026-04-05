#!/usr/bin/env python3
# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""FreeAPIRadar — main monitoring script.

Runs health checks on all configured providers, detects changes,
updates status.json, and generates README.
"""

from __future__ import annotations

import asyncio
import io
import json
import sys
from dataclasses import asdict
from pathlib import Path

# Ensure stdout can handle Unicode (emoji) on Windows CP1251 terminals
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx

# Resolve project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

sys.path.insert(0, str(PROJECT_ROOT))

from providers import ALL_ADAPTERS
from core.diff_engine import load_previous_status, detect_changes, save_status, save_changes
from core.confidence import ConfidenceState, update_confidence


async def check_provider(adapter, session) -> dict:
    """Run full check on a single provider."""
    try:
        status = await adapter.check(session)
        return asdict(status)
    except Exception as e:
        from datetime import datetime, timezone
        return {
            "provider": adapter.name,
            "display_name": adapter.display_name,
            "check_timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "down",
            "confidence": 0,
            "ping_test": {"error": str(e)[:200]},
            "models_endpoint": {},
            "rate_limits": {},
            "free_tier_info": adapter.free_tier_info,
            "changes_log": [],
            "health_history": {},
        }


async def run_all_checks():
    """Run health checks on all providers in parallel."""
    previous = load_previous_status(DATA_DIR)

    # Load confidence states from previous run
    conf_states: dict[str, ConfidenceState] = {}
    for name, prev in previous.items():
        conf_states[name] = ConfidenceState(
            confidence=prev.get("confidence", 50),
            consecutive_failures=prev.get("_consecutive_failures", 0),
            last_status=prev.get("status", "unknown"),
        )

    async with httpx.AsyncClient() as session:
        tasks = [check_provider(adapter, session) for adapter in ALL_ADAPTERS]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_statuses = {}
    all_changes = []

    for result in results:
        if isinstance(result, Exception):
            continue

        name = result["provider"]

        # Update confidence with decay/recovery
        state = conf_states.get(name, ConfidenceState())
        state = update_confidence(state, result["status"])
        result["confidence"] = state.confidence
        result["_consecutive_failures"] = state.consecutive_failures

        # Detect changes vs previous
        changes = detect_changes(previous, result, name)
        result["changes_log"] = changes
        for c in changes:
            c["provider"] = name
        all_changes.extend(changes)

        all_statuses[name] = result

    # Save results
    save_status(DATA_DIR, all_statuses)
    if all_changes:
        save_changes(DATA_DIR, all_changes)

    # Print summary
    print(f"\n{'='*60}")
    print(f"FreeAPIRadar — Status Update")
    print(f"{'='*60}")

    working = 0
    total = 0
    for name, s in sorted(all_statuses.items()):
        total += 1
        status_icon = {"stable": "🟢", "degrading": "🟡", "down": "🔴"}.get(
            s["status"], "⚪"
        )
        is_working = s["status"] in ("stable", "degrading")
        if is_working:
            working += 1

        ping_ms = s.get("ping_test", {}).get("ttfb_ms", "—")
        conf = s.get("confidence", "?")
        print(f"  {status_icon} {s['display_name']:25s}  conf={conf:3}  ping={ping_ms}ms")

    print(f"\n  {working}/{total} providers responding")

    if all_changes:
        print(f"\n  📋 {len(all_changes)} change(s) detected:")
        for c in all_changes:
            print(f"     • {c['provider']}: {c['change_type']} — {c.get('old_value')} → {c.get('new_value')}")

    print(f"{'='*60}\n")

    return all_statuses, all_changes


def main():
    statuses, changes = asyncio.run(run_all_checks())

    # Generate README
    from core.readme_gen import generate_readme
    generate_readme(DATA_DIR, statuses)

    print(f"✅ Status saved to {DATA_DIR / 'status.json'}")
    print(f"✅ README updated")


if __name__ == "__main__":
    main()
