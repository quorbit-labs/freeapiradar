# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Provider registry — all 12 adapters."""

from .groq import GroqAdapter
from .deepseek import DeepSeekAdapter
from .google_ai import GoogleAIAdapter
from .openrouter import OpenRouterAdapter
from .cerebras import CerebrasAdapter
from .sambanova import SambanovaAdapter
from .xai import XaiAdapter
from .mistral import MistralAdapter
from .together import TogetherAdapter
from .cohere import CohereAdapter
from .fireworks import FireworksAdapter
from .cloudflare import CloudflareAdapter


ALL_ADAPTERS = [
    GroqAdapter(),
    DeepSeekAdapter(),
    GoogleAIAdapter(),
    OpenRouterAdapter(),
    CerebrasAdapter(),
    SambanovaAdapter(),
    XaiAdapter(),
    MistralAdapter(),
    TogetherAdapter(),
    CohereAdapter(),
    FireworksAdapter(),
    CloudflareAdapter(),
]


def get_adapter(name: str):
    """Get adapter by provider name."""
    for a in ALL_ADAPTERS:
        if a.name == name:
            return a
    return None
