# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""DeepSeek — cheap frontier model, OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class DeepSeekAdapter(OpenAICompatibleAdapter):
    name = "deepseek"
    display_name = "DeepSeek"
    base_url = "https://api.deepseek.com"
    models_endpoint = "/v1/models"
    chat_endpoint = "/v1/chat/completions"
    test_model = "deepseek-chat"
    api_key_env = "DEEPSEEK_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "5M free tokens on signup, then pay-as-you-go. ~$0.14/M input.",
    }
