# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Base adapter interface for FreeAPIRadar provider monitoring."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PingResult:
    """Result of a single ping test."""
    status: int  # HTTP status code
    ttfb_ms: float  # Time to first byte
    tokens_per_sec: float | None = None
    total_latency_ms: float = 0.0
    error: str | None = None


@dataclass
class ModelsResult:
    """Result of listing available models."""
    status: int
    models: list[str] = field(default_factory=list)
    models_count: int = 0
    error: str | None = None


@dataclass
class RateLimitInfo:
    """Parsed rate limit information from response headers."""
    source: str = "none"  # "headers" | "docs" | "none"
    parsed_successfully: bool = False
    rpm_range: str | None = None
    rpd_range: str | None = None
    headers_raw: dict[str, str] = field(default_factory=dict)


@dataclass
class ProviderStatus:
    """Full status report for a single provider."""
    provider: str
    display_name: str
    check_timestamp: str
    check_method: str = "ping_test"
    check_region: str = "unknown"

    status: str = "unknown"  # "stable" | "degrading" | "down" | "unknown"
    confidence: int = 50

    models_endpoint: dict[str, Any] = field(default_factory=dict)
    ping_test: dict[str, Any] = field(default_factory=dict)
    rate_limits: dict[str, Any] = field(default_factory=dict)

    free_tier_info: dict[str, Any] = field(default_factory=dict)
    changes_log: list[dict[str, Any]] = field(default_factory=list)

    health_history: dict[str, Any] = field(default_factory=dict)


class ProviderAdapter(ABC):
    """Abstract base class for provider-specific adapters.

    Each provider implements:
      - get_models(): list available models
      - ping(): send a test request, measure latency
      - parse_rate_limits(): extract rate limit info from headers

    All adapters use the same interface so monitor.py can iterate
    over them uniformly.
    """

    name: str  # e.g. "groq"
    display_name: str  # e.g. "Groq"
    base_url: str  # e.g. "https://api.groq.com"
    models_endpoint: str  # e.g. "/openai/v1/models"
    chat_endpoint: str  # e.g. "/openai/v1/chat/completions"
    test_model: str  # e.g. "llama-3.3-70b-versatile"
    api_key_env: str  # e.g. "GROQ_API_KEY"

    # Free tier metadata (static, updated manually or via community PRs)
    free_tier_info: dict[str, Any] = {
        "requires_card": False,
        "requires_phone": False,
        "requires_email": True,
        "geo_restrictions": [],
    }

    @abstractmethod
    async def get_models(self, session) -> ModelsResult:
        """Fetch list of available models from the provider."""
        ...

    @abstractmethod
    async def ping(self, session) -> PingResult:
        """Send a minimal test request and measure latency."""
        ...

    @abstractmethod
    def parse_rate_limits(self, headers: dict) -> RateLimitInfo:
        """Extract rate limit info from response headers."""
        ...

    def get_api_key(self) -> str | None:
        """Get API key from environment."""
        import os
        return os.getenv(self.api_key_env, "")

    async def check(self, session) -> ProviderStatus:
        """Run full health check: models + ping + rate limits.

        Returns a ProviderStatus with all fields populated.
        """
        from datetime import datetime, timezone

        api_key = self.get_api_key()
        if not api_key:
            return ProviderStatus(
                provider=self.name,
                display_name=self.display_name,
                check_timestamp=datetime.now(timezone.utc).isoformat(),
                status="unknown",
                confidence=0,
                ping_test={"error": f"No API key set ({self.api_key_env})"},
            )

        # 1. List models
        models_result = await self.get_models(session)

        # 2. Ping test
        ping_result = await self.ping(session)

        # 3. Determine status
        if ping_result.status == 200:
            status = "stable"
        elif ping_result.status == 429:
            status = "degrading"
        else:
            status = "down"

        return ProviderStatus(
            provider=self.name,
            display_name=self.display_name,
            check_timestamp=datetime.now(timezone.utc).isoformat(),
            check_method="ping_test",
            status=status,
            confidence=90 if status == "stable" else (50 if status == "degrading" else 10),
            models_endpoint={
                "url": self.models_endpoint,
                "status": models_result.status,
                "models_count": models_result.models_count,
                "models": models_result.models,
                "error": models_result.error,
            },
            ping_test={
                "model": self.test_model,
                "status": ping_result.status,
                "ttfb_ms": round(ping_result.ttfb_ms, 1),
                "tokens_per_sec": ping_result.tokens_per_sec,
                "total_latency_ms": round(ping_result.total_latency_ms, 1),
                "error": ping_result.error,
            },
            rate_limits={},
            free_tier_info=self.free_tier_info,
        )
