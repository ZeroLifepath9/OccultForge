"""Hellenistic episode reading — unified manifestation."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.episode_manifestation import build_hellenistic_episode


def build_hellenistic_deep_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    return build_hellenistic_episode(facts, imprint).build()