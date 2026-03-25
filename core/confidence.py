# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Confidence score decay and recovery logic.

Based on DeepSeek's confidence decay model from action document:
- Slow recovery on success after failure
- Accelerating decay on consecutive failures
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConfidenceState:
    confidence: int = 50
    consecutive_failures: int = 0
    last_status: str = "unknown"


def update_confidence(state: ConfidenceState, new_status: str) -> ConfidenceState:
    """Update confidence score based on new check result.

    Args:
        state: Current confidence state
        new_status: "stable" | "degrading" | "down"

    Returns:
        Updated ConfidenceState
    """
    if new_status == "stable":
        state.consecutive_failures = 0
        if state.last_status in ("down", "unknown"):
            # Slow recovery after outage
            state.confidence = min(state.confidence + 10, 100)
        elif state.last_status == "degrading":
            state.confidence = min(state.confidence + 5, 100)
        else:
            state.confidence = min(state.confidence + 3, 100)

    elif new_status == "degrading":
        state.consecutive_failures = 0
        state.confidence = max(state.confidence - 5, 20)

    elif new_status == "down":
        state.consecutive_failures += 1
        if state.consecutive_failures >= 5:
            state.confidence = max(state.confidence - 30, 0)
        elif state.consecutive_failures >= 3:
            state.confidence = max(state.confidence - 15, 0)
        else:
            state.confidence = max(state.confidence - 10, 0)

    state.last_status = new_status
    return state
