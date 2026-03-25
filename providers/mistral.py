# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Mistral — 2 RPM free tier (Experiment), OpenAI-compatible."""

from .openai_compat import OpenAICompatibleAdapter


class MistralAdapter(OpenAICompatibleAdapter):
    name = "mistral"
    display_name = "Mistral"
    base_url = "https://api.mistral.ai"
    models_endpoint = "/v1/models"
    chat_endpoint = "/v1/chat/completions"
    test_model = "mistral-small-latest"
    api_key_env = "MISTRAL_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "Experiment tier: 2 RPM, 500K TPM, 1B tokens/month.",
    }
