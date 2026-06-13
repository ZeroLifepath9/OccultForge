"""Vedic episode reading — unified manifestation."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.episode_manifestation import build_vedic_episode


def build_vedic_deep_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    return build_vedic_episode(facts, imprint).build()