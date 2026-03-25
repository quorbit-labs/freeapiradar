# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""OpenRouter — model aggregator, some free models, OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class OpenRouterAdapter(OpenAICompatibleAdapter):
    name = "openrouter"
    display_name = "OpenRouter"
    base_url = "https://openrouter.ai"
    models_endpoint = "/api/v1/models"
    chat_endpoint = "/api/v1/chat/completions"
    test_model = "deepseek/deepseek-chat-v3-0324:free"
    api_key_env = "OPENROUTER_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "Free models available (community-sponsored). Lower rate limits on free tier.",
    }
