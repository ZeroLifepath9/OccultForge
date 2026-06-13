"""Relationships episode reading — unified manifestation."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.episode_manifestation import build_relationships_episode


def build_relationships_deep_reading(facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    return build_relationships_episode(facts, imprint or {}).build()