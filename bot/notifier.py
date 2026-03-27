# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""FreeAPIRadar — Push notification sender.

Usage (from GitHub Actions or CLI):
    python -m bot.notifier

Reads changes.json + status.json, sends alerts to subscribers.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from telegram import Bot

from . import config
from .storage import SubscriberStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def load_changes() -> list:
    """Load changes.json from local path."""
    path = Path(config.LOCAL_CHANGES_PATH)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def load_status() -> dict:
    """Load status.json as {provider: status_dict}."""
    path = Path(config.LOCAL_STATUS_PATH)
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        return {p["provider"]: p for p in data} if isinstance(data, list) else {}
    except (json.JSONDecodeError, IOError):
        return {}


def format_change_alert(change: dict, current_status: dict) -> str:
    """Format a single change into a Telegram message."""
    provider_id = change.get("provider", "unknown")
    display = config.PROVIDER_NAMES.get(provider_id, provider_id)
    change_type = change.get("change_type", change.get("field", "unknown"))
    detail = change.get("detail", "")
    old = change.get("old_value", "")
    new = change.get("new_value", "")
    ts = change.get("detected_at", "")

    # Current status emoji
    prov_data = current_status.get(provider_id, {})
    status = prov_data.get("status", "unknown")
    emoji = config.STATUS_EMOJI.get(status, "⚪")

    lines = [f"📡 **{display}** {emoji}"]

    if change_type == "status_change":
        old_emoji = config.STATUS_EMOJI.get(str(old), "⚪")
        new_emoji = config.STATUS_EMOJI.get(str(new), "⚪")
        lines.append(f"Status: {old_emoji} {old} → {new_emoji} {new}")
    elif change_type == "model_added":
        lines.append(f"➕ New model: `{detail}`")
    elif change_type == "model_removed":
        lines.append(f"➖ Model removed: `{detail}`")
    elif change_type == "confidence_change":
        direction = "📈" if (new or 0) > (old or 0) else "📉"
        lines.append(f"{direction} Confidence: {old} → {new}")
    else:
        lines.append(f"Change: {change_type}")
        if detail:
            lines.append(f"Detail: {detail}")
        if old and new:
            lines.append(f"{old} → {new}")

    if ts:
        lines.append(f"🕐 {ts}")

    return "\n".join(lines)


async def send_alerts():
    """Main function: load changes, send to subscribers."""
    if not config.BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set. Skipping notifications.")
        return 0

    changes = load_changes()
    if not changes:
        logger.info("No changes detected. Nothing to notify.")
        return 0

    current_status = load_status()
    store = SubscriberStore(config.SUBSCRIBERS_PATH)

    if store.total_subscribers == 0:
        logger.info("No subscribers yet. Skipping notifications.")
        return 0

    bot = Bot(token=config.BOT_TOKEN)
    sent = 0

    # Group changes by provider
    by_provider: dict[str, list] = {}
    for change in changes:
        pid = change.get("provider", "unknown")
        by_provider.setdefault(pid, []).append(change)

    for provider_id, prov_changes in by_provider.items():
        subscribers = store.get_subscribers_for(provider_id)
        if not subscribers:
            continue

        # Build message for this provider (combine all changes)
        messages = []
        for change in prov_changes[:5]:  # max 5 changes per provider per alert
            messages.append(format_change_alert(change, current_status))

        full_message = "\n\n".join(messages)
        if len(prov_changes) > 5:
            full_message += f"\n\n... and {len(prov_changes) - 5} more changes"

        for chat_id in subscribers:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=full_message,
                    parse_mode="Markdown",
                )
                sent += 1
                logger.info("Sent alert to %s for %s", chat_id, provider_id)
            except Exception as e:
                logger.warning("Failed to send to %s: %s", chat_id, e)

    logger.info("Sent %d notifications total.", sent)
    return sent


def main():
    """Entry point for CLI / GitHub Actions."""
    count = asyncio.run(send_alerts())
    print(f"Sent {count} notifications.")
    sys.exit(0)


if __name__ == "__main__":
    main()
