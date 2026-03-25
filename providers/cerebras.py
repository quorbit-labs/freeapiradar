# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Cerebras — wafer-scale engine, 1M tokens/day free, ultra-fast."""

from .openai_compat import OpenAICompatibleAdapter


class CerebrasAdapter(OpenAICompatibleAdapter):
    name = "cerebras"
    display_name = "Cerebras"
    base_url = "https://api.cerebras.ai"
    models_endpoint = "/v1/models"
    chat_endpoint = "/v1/chat/completions"
    test_model = "llama3.1-8b"
    api_key_env = "CEREBRAS_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "1M tokens/day free, 30 RPM. Models: llama3.1-8b, gpt-oss-120b.",
    }
