# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Diff engine — compares current status with previous, detects changes."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import asdict


def load_previous_status(data_dir: Path) -> dict:
    """Load previous status.json, return empty dict if not found."""
    status_file = data_dir / "status.json"
    if status_file.exists():
        return json.loads(status_file.read_text())
    return {}


def detect_changes(
    previous: dict, current: dict, provider_name: str
) -> list[dict]:
    """Compare previous and current status for a provider, return list of changes.

    Tracks: status changes, model additions/removals, confidence shifts.
    """
    changes = []
    now = datetime.now(timezone.utc).isoformat()

    prev = previous.get(provider_name, {})
    curr = current

    if not prev:
        # First time seeing this provider
        return []

    # Status change
    old_status = prev.get("status", "unknown")
    new_status = curr.get("status", "unknown")
    if old_status != new_status:
        changes.append({
            "field": "status",
            "old_value": old_status,
            "new_value": new_status,
            "change_type": "status_change",
            "detected_at": now,
        })

    # Models diff
    old_models = set(prev.get("models_endpoint", {}).get("models", []))
    new_models = set(curr.get("models_endpoint", {}).get("models", []))
    added = new_models - old_models
    removed = old_models - new_models

    if added:
        changes.append({
            "field": "models",
            "old_value": len(old_models),
            "new_value": len(new_models),
            "change_type": "model_added",
            "detail": list(added),
            "detected_at": now,
        })
    if removed:
        changes.append({
            "field": "models",
            "old_value": len(old_models),
            "new_value": len(new_models),
            "change_type": "model_removed",
            "detail": list(removed),
            "detected_at": now,
        })

    # Models count change (even without knowing specifics)
    old_count = prev.get("models_endpoint", {}).get("models_count", 0)
    new_count = curr.get("models_endpoint", {}).get("models_count", 0)
    if old_count != new_count and not added and not removed:
        changes.append({
            "field": "models_count",
            "old_value": old_count,
            "new_value": new_count,
            "change_type": "models_count_changed",
            "detected_at": now,
        })

    # Significant confidence change (>15 points)
    old_conf = prev.get("confidence", 50)
    new_conf = curr.get("confidence", 50)
    if abs(old_conf - new_conf) >= 15:
        changes.append({
            "field": "confidence",
            "old_value": old_conf,
            "new_value": new_conf,
            "change_type": "confidence_shift",
            "detected_at": now,
        })

    return changes


def save_status(data_dir: Path, all_statuses: dict):
    """Save current status to status.json and append to history."""
    data_dir.mkdir(parents=True, exist_ok=True)
    status_file = data_dir / "status.json"
    status_file.write_text(json.dumps(all_statuses, indent=2, default=str))

    # Append snapshot to history
    history_dir = data_dir / "history"
    history_dir.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    snapshot = history_dir / f"status-{ts}.json"
    snapshot.write_text(json.dumps(all_statuses, indent=2, default=str))


def save_changes(data_dir: Path, all_changes: list[dict]):
    """Append detected changes to changes.json."""
    changes_file = data_dir / "changes.json"
    existing = []
    if changes_file.exists():
        try:
            existing = json.loads(changes_file.read_text())
        except json.JSONDecodeError:
            existing = []

    existing.extend(all_changes)

    # Keep last 1000 changes
    existing = existing[-1000:]
    changes_file.write_text(json.dumps(existing, indent=2, default=str))
