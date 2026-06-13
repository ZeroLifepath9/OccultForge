"""Wealth episode reading — unified manifestation."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.episode_manifestation import build_wealth_episode


def build_wealth_deep_reading(facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    return build_wealth_episode(facts, imprint or {}).build()