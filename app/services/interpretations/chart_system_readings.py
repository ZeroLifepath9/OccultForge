"""
Per-tradition chart readings for Occult Forge chart boxes.
Each system reads only its own language — combination/wealth/relationships blend.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.bazi_forge_lens import build_bazi_forge_reading
from app.services.interpretations.chart_reading_verify import assert_chart_reading
from app.services.interpretations.financial_deep_reading import build_financial_deep_reading
from app.services.interpretations.hellenistic_deep_reading import build_hellenistic_deep_reading
from app.services.imprint_labels import build_display_bundle
from app.services.interpretations.numerology_panels import assemble_numerology_narrative, build_numerology_panels
from app.services.interpretations.relationships_deep_reading import build_relationships_deep_reading
from app.services.interpretations.vedic_deep_reading import build_vedic_deep_reading
from app.services.interpretations.wealth_deep_reading import build_wealth_deep_reading
from app.services.interpretations.zero_overview import build_zero_overview

READING_ENGINE = "chart-system-v8.27-forge-lens"

VALID_SYSTEMS = frozenset(
    {
        "numerology",
        "bazi",
        "vedic",
        "hellenistic",
        "financial",
        "combination",
        "wealth",
        "relationships",
    }
)

SYSTEM_TITLES = {
    "numerology": "Occult Numerology",
    "bazi": "BaZi Pillars",
    "vedic": "Vedic / Jyotish (Sidereal)",
    "hellenistic": "Hellenistic Astrology",
    "financial": "Financial / Mundane & Modern Hybrids",
    "combination": "Master Combination — Light in the Meat Suit",
    "wealth": "Wealth Chart",
    "relationships": "Relationships — Intimate to Professional",
}


def _display_name(imprint: dict[str, Any]) -> str:
    birth = imprint.get("birth") or {}
    alias = (birth.get("commonly_known_as") or "").strip()
    return alias or birth.get("name") or birth.get("display_name") or "Seeker"


def build_numerology_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    panels = build_numerology_panels(facts, imprint)
    return assemble_numerology_narrative(panels, imprint)


def build_bazi_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    return build_bazi_forge_reading(facts, imprint)


def build_vedic_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    return build_vedic_deep_reading(facts, imprint)


def build_hellenistic_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    return build_hellenistic_deep_reading(facts, imprint)


def build_financial_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    return build_financial_deep_reading(facts, imprint)


def build_combination_reading(facts: dict[str, Any], name: str) -> str:
    return build_zero_overview(facts, name)


def build_wealth_reading(facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    return build_wealth_deep_reading(facts, imprint)


def build_relationships_reading(facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    return build_relationships_deep_reading(facts, imprint)


def build_system_reading(
    system: str,
    imprint: dict[str, Any],
    *,
    name: str | None = None,
) -> dict[str, Any]:
    if system not in VALID_SYSTEMS:
        raise ValueError(f"Unknown chart system: {system}")

    facts = build_display_bundle(imprint)
    display = name or _display_name(imprint)

    builders = {
        "numerology": lambda: build_numerology_reading(facts, imprint),
        "bazi": lambda: build_bazi_reading(facts, imprint),
        "vedic": lambda: build_vedic_reading(facts, imprint),
        "hellenistic": lambda: build_hellenistic_reading(facts, imprint),
        "financial": lambda: build_financial_reading(facts, imprint),
        "combination": lambda: build_combination_reading(facts, display),
        "wealth": lambda: build_wealth_reading(facts, imprint),
        "relationships": lambda: build_relationships_reading(facts, imprint),
    }
    panels: dict[str, Any] | None = None
    if system == "numerology":
        panels = build_numerology_panels(facts, imprint)
    narrative = assert_chart_reading(
        system, builders[system], facts, imprint, panels=panels
    )
    out: dict[str, Any] = {
        "system": system,
        "title": SYSTEM_TITLES[system],
        "narrative": narrative,
        "verified": True,
        "reading_engine": READING_ENGINE,
    }
    if panels is not None:
        out["panels"] = panels
    return out