"""Build verified chart readings bundle for imprint payload."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.chart_system_readings import VALID_SYSTEMS, build_system_reading


def build_all_chart_readings(imprint: dict[str, Any]) -> dict[str, Any]:
    """All tradition readings — deterministic, self-verified."""
    return {system: build_system_reading(system, imprint) for system in sorted(VALID_SYSTEMS)}