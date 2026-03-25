# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""SambaNova — free tier, fast inference, OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class SambanovaAdapter(OpenAICompatibleAdapter):
    name = "sambanova"
    display_name = "SambaNova"
    base_url = "https://api.sambanova.ai"
    models_endpoint = "/v1/models"
    chat_endpoint = "/v1/chat/completions"
    test_model = "Meta-Llama-3.3-70B-Instruct"
    api_key_env = "SAMBANOVA_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "Free tier, no card required. Models: Llama, DeepSeek-R1.",
    }
