# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Groq — LPU inference, 30 RPM free tier, OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class GroqAdapter(OpenAICompatibleAdapter):
    name = "groq"
    display_name = "Groq"
    base_url = "https://api.groq.com"
    models_endpoint = "/openai/v1/models"
    chat_endpoint = "/openai/v1/chat/completions"
    test_model = "llama-3.3-70b-versatile"
    api_key_env = "GROQ_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "Blocks datacenter IPs. 30 RPM, 14400 RPD free.",
    }
