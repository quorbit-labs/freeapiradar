# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Base class for OpenAI-compatible providers (Groq, Cerebras, SambaNova, etc.)."""

from __future__ import annotations

import time
from .base import ProviderAdapter, PingResult, ModelsResult, RateLimitInfo


class OpenAICompatibleAdapter(ProviderAdapter):
    """Base for providers with OpenAI-compatible /v1/chat/completions API.

    Subclasses only need to set class attributes (name, base_url, etc.)
    and optionally override parse_rate_limits() for provider-specific headers.
    """

    async def get_models(self, session) -> ModelsResult:
        api_key = self.get_api_key()
        url = f"{self.base_url}{self.models_endpoint}"
        try:
            resp = await session.get(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                timeout=15,
            )
            if resp.status_code != 200:
                return ModelsResult(
                    status=resp.status_code,
                    error=resp.text[:200],
                )
            data = resp.json()
            models = [m.get("id", "") for m in data.get("data", [])]
            return ModelsResult(
                status=200,
                models=models,
                models_count=len(models),
            )
        except Exception as e:
            return ModelsResult(status=0, error=str(e)[:200])

    async def ping(self, session) -> PingResult:
        api_key = self.get_api_key()
        url = f"{self.base_url}{self.chat_endpoint}"
        payload = {
            "model": self.test_model,
            "messages": [{"role": "user", "content": "Say hi"}],
            "max_tokens": 10,
            "stream": False,
        }
        t0 = time.monotonic()
        try:
            resp = await session.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=30,
            )
            ttfb = (time.monotonic() - t0) * 1000
            total = ttfb  # non-streaming, so ttfb ≈ total

            if resp.status_code != 200:
                return PingResult(
                    status=resp.status_code,
                    ttfb_ms=ttfb,
                    total_latency_ms=total,
                    error=resp.text[:200],
                )

            data = resp.json()
            # Try to extract token speed from usage
            usage = data.get("usage", {})
            completion_tokens = usage.get("completion_tokens", 0)
            tps = round(completion_tokens / (total / 1000), 1) if total > 0 and completion_tokens > 0 else None

            # Parse rate limits from headers
            self._last_headers = dict(resp.headers)

            return PingResult(
                status=200,
                ttfb_ms=ttfb,
                tokens_per_sec=tps,
                total_latency_ms=total,
            )
        except Exception as e:
            elapsed = (time.monotonic() - t0) * 1000
            return PingResult(
                status=0,
                ttfb_ms=elapsed,
                total_latency_ms=elapsed,
                error=str(e)[:200],
            )

    def parse_rate_limits(self, headers: dict) -> RateLimitInfo:
        """Default parser for OpenAI-style rate limit headers."""
        rl_headers = {
            k: v for k, v in headers.items()
            if "ratelimit" in k.lower() or "rate-limit" in k.lower()
        }
        if not rl_headers:
            return RateLimitInfo(source="none")

        rpm = rl_headers.get("x-ratelimit-limit-requests", "")
        rpd = rl_headers.get("x-ratelimit-limit-tokens", "")

        return RateLimitInfo(
            source="headers",
            parsed_successfully=bool(rpm or rpd),
            rpm_range=rpm if rpm else None,
            rpd_range=rpd if rpd else None,
            headers_raw=rl_headers,
        )
