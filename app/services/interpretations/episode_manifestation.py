"""
Flowing chart insight — one prose layer per tradition.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.flow_insight_corpus import (
    build_bazi_flow,
    build_financial_flow,
    build_hellenistic_flow,
    build_numerology_flow,
    build_relationships_flow,
    build_vedic_flow,
    build_wealth_flow,
)


def build_episode_reading(tradition: str, facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    builders = {
        "bazi": build_bazi_flow,
        "numerology": build_numerology_flow,
        "vedic": build_vedic_flow,
        "hellenistic": build_hellenistic_flow,
        "financial": build_financial_flow,
        "wealth": build_wealth_flow,
        "relationships": build_relationships_flow,
    }
    return builders[tradition](facts, imprint).build()


def build_bazi_episode(facts: dict[str, Any], imprint: dict[str, Any]):
    return build_bazi_flow(facts, imprint)


def build_numerology_episode(facts: dict[str, Any], imprint: dict[str, Any]):
    return build_numerology_flow(facts, imprint)


def build_vedic_episode(facts: dict[str, Any], imprint: dict[str, Any]):
    return build_vedic_flow(facts, imprint)


def build_hellenistic_episode(facts: dict[str, Any], imprint: dict[str, Any]):
    return build_hellenistic_flow(facts, imprint)


def build_financial_episode(facts: dict[str, Any], imprint: dict[str, Any]):
    return build_financial_flow(facts, imprint)


def build_wealth_episode(facts: dict[str, Any], imprint: dict[str, Any]):
    return build_wealth_flow(facts, imprint)


def build_relationships_episode(facts: dict[str, Any], imprint: dict[str, Any]):
    return build_relationships_flow(facts, imprint)