# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Together AI — $5 credit on signup, 200+ models, OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class TogetherAdapter(OpenAICompatibleAdapter):
    name = "together"
    display_name = "Together AI"
    base_url = "https://api.together.xyz"
    models_endpoint = "/v1/models"
    chat_endpoint = "/v1/chat/completions"
    test_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    api_key_env = "TOGETHER_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "$5 credit on signup. No permanent free tier.",
    }
