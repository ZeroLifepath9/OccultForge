"""Financial episode reading — unified manifestation."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.episode_manifestation import build_financial_episode


def build_financial_deep_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    return build_financial_episode(facts, imprint).build()