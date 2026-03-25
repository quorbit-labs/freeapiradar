# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Fireworks AI — $1 credit on signup, fast inference, OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class FireworksAdapter(OpenAICompatibleAdapter):
    name = "fireworks"
    display_name = "Fireworks AI"
    base_url = "https://api.fireworks.ai"
    models_endpoint = "/inference/v1/models"
    chat_endpoint = "/inference/v1/chat/completions"
    test_model = "accounts/fireworks/models/llama-v3p3-70b-instruct"
    api_key_env = "FIREWORKS_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "$1 credit on signup. Fast serverless inference.",
    }
