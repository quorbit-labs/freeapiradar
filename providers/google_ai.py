# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Google AI Studio (Gemini) — custom API format, generous free tier."""

from __future__ import annotations

import time
from .base import ProviderAdapter, PingResult, ModelsResult, RateLimitInfo


class GoogleAIAdapter(ProviderAdapter):
    name = "google_ai"
    display_name = "Google AI Studio"
    base_url = "https://generativelanguage.googleapis.com"
    models_endpoint = "/v1beta/models"
    chat_endpoint = "/v1beta/models/{model}:generateContent"
    test_model = "gemini-2.0-flash"
    api_key_env = "GEMINI_API_KEY"

    free_tier_info = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
        "notes": "5-15 RPM depending on model, 100-1000 RPD. 1M context window.",
    }

    async def get_models(self, session) -> ModelsResult:
        api_key = self.get_api_key()
        url = f"{self.base_url}{self.models_endpoint}?key={api_key}"
        try:
            resp = await session.get(url, timeout=15)
            if resp.status_code != 200:
                return ModelsResult(status=resp.status_code, error=resp.text[:200])
            data = resp.json()
            models = [
                m.get("name", "").replace("models/", "")
                for m in data.get("models", [])
                if "generateContent" in str(m.get("supportedGenerationMethods", []))
            ]
            return ModelsResult(status=200, models=models, models_count=len(models))
        except Exception as e:
            return ModelsResult(status=0, error=str(e)[:200])

    async def ping(self, session) -> PingResult:
        api_key = self.get_api_key()
        url = (
            f"{self.base_url}/v1beta/models/{self.test_model}"
            f":generateContent?key={api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": "Say hi"}]}],
            "generationConfig": {"maxOutputTokens": 10},
        }
        t0 = time.monotonic()
        try:
            resp = await session.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )
            ttfb = (time.monotonic() - t0) * 1000
            if resp.status_code != 200:
                return PingResult(
                    status=resp.status_code,
                    ttfb_ms=ttfb,
                    total_latency_ms=ttfb,
                    error=resp.text[:200],
                )
            self._last_headers = dict(resp.headers)
            return PingResult(status=200, ttfb_ms=ttfb, total_latency_ms=ttfb)
        except Exception as e:
            elapsed = (time.monotonic() - t0) * 1000
            return PingResult(status=0, ttfb_ms=elapsed, total_latency_ms=elapsed, error=str(e)[:200])

    def parse_rate_limits(self, headers: dict) -> RateLimitInfo:
        return RateLimitInfo(source="none")
