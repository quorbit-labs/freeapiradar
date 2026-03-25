# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""xAI Grok — $25 free credits on signup, OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class XaiAdapter(OpenAICompatibleAdapter):
    name = "xai"
    display_name = "xAI Grok"
    base_url = "https://api.x.ai"
    models_endpoint = "/v1/models"
    chat_endpoint = "/v1/chat/completions"
    test_model = "grok-2-latest"
    api_key_env = "GROK_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "$25 free credits on signup. $175/month free for developers.",
    }
