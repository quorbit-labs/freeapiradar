# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Cloudflare Workers AI — serverless, generous free tier, custom API."""

from __future__ import annotations

import time
from .base import ProviderAdapter, PingResult, ModelsResult, RateLimitInfo


class CloudflareAdapter(ProviderAdapter):
    name = "cloudflare"
    display_name = "Cloudflare Workers AI"
    base_url = "https://api.cloudflare.com/client/v4"
    models_endpoint = "/accounts/{account_id}/ai/models/search"
    chat_endpoint = "/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"
    test_model = "@cf/meta/llama-3.1-8b-instruct"
    api_key_env = "CLOUDFLARE_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "10K neurons/day free. Requires Cloudflare account + account_id.",
    }

    async def get_models(self, session) -> ModelsResult:
        # Cloudflare requires account_id in URL — skip models list for now
        return ModelsResult(
            status=0,
            error="Cloudflare requires CLOUDFLARE_ACCOUNT_ID (not implemented in MVP)",
        )

    async def ping(self, session) -> PingResult:
        # Requires account_id — stub for MVP
        return PingResult(
            status=0, ttfb_ms=0, total_latency_ms=0,
            error="Cloudflare requires CLOUDFLARE_ACCOUNT_ID (not implemented in MVP)",
        )

    def parse_rate_limits(self, headers: dict) -> RateLimitInfo:
        return RateLimitInfo(source="none")
