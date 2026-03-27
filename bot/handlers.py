# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""FreeAPIRadar Telegram Bot — command handlers."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

from . import config
from .storage import SubscriberStore

logger = logging.getLogger(__name__)

store = SubscriberStore(config.SUBSCRIBERS_PATH)


# ─── Helpers ────────────────────────────────────────────────

async def _fetch_status() -> list | None:
    """Fetch status.json — local file first, then GitHub."""
    local = Path(config.LOCAL_STATUS_PATH)
    if local.exists():
        try:
            with open(local, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return list(raw.values()) if isinstance(raw, dict) else raw
        except (json.JSONDecodeError, IOError):
            pass

    # Fallback: fetch from GitHub
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(config.STATUS_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    raw = await resp.json()
                    return list(raw.values()) if isinstance(raw, dict) else raw
    except Exception as e:
        logger.error("Failed to fetch status from GitHub: %s", e)
    return None


def _format_provider_status(provider: dict) -> str:
    """Format one provider line for /status output."""
    name = provider.get("provider", "?")
    display = config.PROVIDER_NAMES.get(name, name)
    status = provider.get("status", "unknown")
    emoji = config.STATUS_EMOJI.get(status, "⚪")
    conf = provider.get("confidence", 0)

    ping = provider.get("ping_test", {})
    latency = ping.get("ttfb_ms")
    lat_str = f"{latency}ms" if latency else "—"

    models = provider.get("models_endpoint", {})
    model_count = models.get("models_count")
    mod_str = f"{model_count} models" if model_count else ""

    return f"{emoji} **{display}** — conf:{conf}  ping:{lat_str}  {mod_str}"


def _format_timestamp(ts_str: str | None) -> str:
    """Format ISO timestamp to human-readable."""
    if not ts_str:
        return "unknown"
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt
        hours = int(delta.total_seconds() // 3600)
        mins = int((delta.total_seconds() % 3600) // 60)
        if hours > 0:
            return f"{hours}h {mins}m ago"
        return f"{mins}m ago"
    except (ValueError, TypeError):
        return ts_str


# ─── Commands ───────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        "📡 **FreeAPIRadar Bot**\n\n"
        "Real-time status of free AI APIs.\n\n"
        "Commands:\n"
        "/status — current status of all providers\n"
        "/subscribe <provider> — get alerts when status changes\n"
        "/subscribe all — subscribe to everything\n"
        "/unsubscribe <provider> — stop alerts\n"
        "/mysubs — your current subscriptions\n"
        "/providers — list available provider IDs\n"
        "/help — this message\n\n"
        "GitHub: github.com/quorbit-labs/freeapiradar",
        parse_mode="Markdown",
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await cmd_start(update, context)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status — show current status of all providers."""
    data = await _fetch_status()
    if not data:
        await update.message.reply_text(
            "⚠️ Could not fetch status data. Try again later."
        )
        return

    lines = ["📡 **FreeAPIRadar — Current Status**\n"]

    # Group by status: green first, then yellow, then red, then unknown
    order = {"stable": 0, "degraded": 1, "degrading": 1, "down": 2, "unknown": 3}
    sorted_data = sorted(data, key=lambda p: order.get(p.get("status", "unknown"), 9))

    for provider in sorted_data:
        lines.append(_format_provider_status(provider))

    # Find latest check timestamp
    timestamps = [p.get("check_timestamp") for p in data if p.get("check_timestamp")]
    if timestamps:
        latest = max(timestamps)
        lines.append(f"\n🕐 Last check: {_format_timestamp(latest)}")

    working = sum(1 for p in data if p.get("status") == "stable")
    total = len(data)
    lines.append(f"✅ {working}/{total} providers working")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /subscribe <provider> or /subscribe all."""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/subscribe groq` or `/subscribe all`\n"
            "See `/providers` for available IDs.",
            parse_mode="Markdown",
        )
        return

    provider = context.args[0].lower().strip()
    chat_id = update.effective_chat.id

    if provider == "all":
        count = store.subscribe_all(chat_id, list(config.PROVIDER_NAMES.keys()))
        await update.message.reply_text(
            f"✅ Subscribed to all {count} providers!\n"
            "You'll get alerts when any status changes."
        )
        return

    if provider not in config.PROVIDER_NAMES:
        await update.message.reply_text(
            f"❌ Unknown provider: `{provider}`\n"
            "Use `/providers` to see available IDs.",
            parse_mode="Markdown",
        )
        return

    if store.subscribe(chat_id, provider):
        display = config.PROVIDER_NAMES[provider]
        await update.message.reply_text(
            f"✅ Subscribed to **{display}** alerts!",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("You're already subscribed to this provider.")


async def cmd_unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unsubscribe <provider>."""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/unsubscribe groq`",
            parse_mode="Markdown",
        )
        return

    provider = context.args[0].lower().strip()
    chat_id = update.effective_chat.id

    if provider == "all":
        subs = store.get_subscriptions(chat_id)
        for p in list(subs):
            store.unsubscribe(chat_id, p)
        await update.message.reply_text("✅ Unsubscribed from all providers.")
        return

    if store.unsubscribe(chat_id, provider):
        await update.message.reply_text(f"✅ Unsubscribed from {provider}.")
    else:
        await update.message.reply_text("You weren't subscribed to this provider.")


async def cmd_mysubs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mysubs — show current subscriptions."""
    chat_id = update.effective_chat.id
    subs = store.get_subscriptions(chat_id)

    if not subs:
        await update.message.reply_text(
            "You have no subscriptions.\n"
            "Use `/subscribe groq` to get started!",
            parse_mode="Markdown",
        )
        return

    lines = ["📋 **Your subscriptions:**\n"]
    for p in subs:
        display = config.PROVIDER_NAMES.get(p, p)
        lines.append(f"  • {display}")
    lines.append(f"\nTotal: {len(subs)} provider(s)")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_providers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /providers — list available provider IDs."""
    lines = ["📋 **Available providers:**\n"]
    for pid, name in sorted(config.PROVIDER_NAMES.items()):
        lines.append(f"  `{pid}` — {name}")
    lines.append("\nUse: `/subscribe <id>`")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
