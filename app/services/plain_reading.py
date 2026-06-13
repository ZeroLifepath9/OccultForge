"""Threshold reading — delegates to deep inline occult engine."""

from typing import Any

from app.services.interpretations.zero_overview import (
    READING_ENGINE,
    SEAL_CLOSE,
    ZERO_OVERVIEW_MARKER,
    build_zero_overview,
)

INTERPRETATION_MARKER = ZERO_OVERVIEW_MARKER

__all__ = [
    "INTERPRETATION_MARKER",
    "SEAL_CLOSE",
    "READING_ENGINE",
    "build_plain_reading",
]


def build_plain_reading(facts: dict[str, Any], name: str) -> str:
    return build_zero_overview(facts, name)