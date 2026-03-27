# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""FreeAPIRadar Telegram Bot — configuration."""

import os

# Telegram bot token (from @BotFather)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# GitHub raw URL for status.json
GITHUB_REPO = os.environ.get(
    "FREEAPIRADAR_REPO", "quorbit-labs/freeapiradar"
)
STATUS_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/data/status.json"
)
CHANGES_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/data/changes.json"
)

# Local paths (when running alongside monitor)
LOCAL_STATUS_PATH = os.environ.get("STATUS_PATH", "data/status.json")
LOCAL_CHANGES_PATH = os.environ.get("CHANGES_PATH", "data/changes.json")

# Subscriber storage
SUBSCRIBERS_PATH = os.environ.get("SUBSCRIBERS_PATH", "data/subscribers.json")

# Provider display names
PROVIDER_NAMES = {
    "groq": "Groq",
    "deepseek": "DeepSeek",
    "mistral": "Mistral",
    "google_ai": "Google AI (Gemini)",
    "together": "Together AI",
    "cerebras": "Cerebras",
    "sambanova": "SambaNova",
    "openrouter": "OpenRouter",
    "xai": "xAI (Grok)",
    "cohere": "Cohere",
    "fireworks": "Fireworks AI",
    "cloudflare": "Cloudflare Workers AI",
}

STATUS_EMOJI = {
    "stable": "🟢",
    "degraded": "🟡",
    "degrading": "🟡",
    "down": "🔴",
    "unknown": "⚪",
}
