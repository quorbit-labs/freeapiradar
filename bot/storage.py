# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""Subscriber storage — JSON file persistence."""

import json
import os
from pathlib import Path
from typing import Dict, List, Set


class SubscriberStore:
    """Stores subscriber data: {chat_id: [provider1, provider2, ...]}."""

    def __init__(self, path: str):
        self.path = Path(path)
        self._data: Dict[str, List[str]] = {}
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                # Normalize: keys as strings, values as lists
                self._data = {str(k): list(v) for k, v in raw.items()}
            except (json.JSONDecodeError, IOError):
                self._data = {}
        else:
            self._data = {}

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def subscribe(self, chat_id: int, provider: str) -> bool:
        """Subscribe chat to provider alerts. Returns True if new."""
        key = str(chat_id)
        if key not in self._data:
            self._data[key] = []
        if provider in self._data[key]:
            return False
        self._data[key].append(provider)
        self._save()
        return True

    def unsubscribe(self, chat_id: int, provider: str) -> bool:
        """Unsubscribe chat from provider. Returns True if was subscribed."""
        key = str(chat_id)
        if key not in self._data or provider not in self._data[key]:
            return False
        self._data[key].remove(provider)
        if not self._data[key]:
            del self._data[key]
        self._save()
        return True

    def subscribe_all(self, chat_id: int, providers: List[str]) -> int:
        """Subscribe to all providers. Returns count of new subscriptions."""
        key = str(chat_id)
        if key not in self._data:
            self._data[key] = []
        count = 0
        for p in providers:
            if p not in self._data[key]:
                self._data[key].append(p)
                count += 1
        if count:
            self._save()
        return count

    def get_subscriptions(self, chat_id: int) -> List[str]:
        """Get list of providers a chat is subscribed to."""
        return self._data.get(str(chat_id), [])

    def get_subscribers_for(self, provider: str) -> List[int]:
        """Get all chat_ids subscribed to a provider."""
        return [
            int(cid)
            for cid, providers in self._data.items()
            if provider in providers
        ]

    def get_all_subscribers(self) -> Set[int]:
        """Get all unique chat_ids."""
        return {int(cid) for cid in self._data.keys()}

    @property
    def total_subscribers(self) -> int:
        return len(self._data)
