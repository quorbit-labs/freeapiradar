# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Cohere — free for personal use, best for embeddings/RAG."""

from __future__ import annotations

import time
from .base import ProviderAdapter, PingResult, ModelsResult, RateLimitInfo


class CohereAdapter(ProviderAdapter):
    name = "cohere"
    display_name = "Cohere"
    base_url = "https://api.cohere.com"
    models_endpoint = "/v2/models"
    chat_endpoint = "/v2/chat"
    test_model = "command-r-08-2024"
    api_key_env = "COHERE_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "Free for personal/trial. 20 RPM, 1000 RPM for embeddings.",
    }

    async def get_models(self, session) -> ModelsResult:
        api_key = self.get_api_key()
        try:
            resp = await session.get(
                f"{self.base_url}{self.models_endpoint}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=15,
            )
            if resp.status_code != 200:
                return ModelsResult(status=resp.status_code, error=resp.text[:200])
            data = resp.json()
            models = [m.get("name", "") for m in data.get("models", [])]
            return ModelsResult(status=200, models=models, models_count=len(models))
        except Exception as e:
            return ModelsResult(status=0, error=str(e)[:200])

    async def ping(self, session) -> PingResult:
        api_key = self.get_api_key()
        payload = {
            "model": self.test_model,
            "messages": [{"role": "user", "content": "Say hi"}],
            "max_tokens": 10,
        }
        t0 = time.monotonic()
        try:
            resp = await session.post(
                f"{self.base_url}{self.chat_endpoint}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=30,
            )
            ttfb = (time.monotonic() - t0) * 1000
            if resp.status_code != 200:
                return PingResult(status=resp.status_code, ttfb_ms=ttfb, total_latency_ms=ttfb, error=resp.text[:200])
            return PingResult(status=200, ttfb_ms=ttfb, total_latency_ms=ttfb)
        except Exception as e:
            elapsed = (time.monotonic() - t0) * 1000
            return PingResult(status=0, ttfb_ms=elapsed, total_latency_ms=elapsed, error=str(e)[:200])

    def parse_rate_limits(self, headers: dict) -> RateLimitInfo:
        return RateLimitInfo(source="none")
