"""Numerology episode reading — unified manifestation."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.numerology_panels import assemble_numerology_narrative, build_numerology_panels


def build_numerology_deep_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    panels = build_numerology_panels(facts, imprint)
    return assemble_numerology_narrative(panels, imprint)