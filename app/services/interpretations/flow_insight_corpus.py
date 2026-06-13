"""
Flowing occult insight — Matrix Decoder 3-part framework per tradition.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.flow_voice import FlowReading
from app.services.interpretations.matrix_decoder_voice import (
    build_bazi_matrix,
    build_financial_matrix,
    build_hellenistic_matrix,
    build_numerology_matrix,
    build_relationships_matrix,
    build_vedic_matrix,
    build_wealth_matrix,
)


def build_bazi_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    return FlowReading(body=build_bazi_matrix(facts, imprint))


def build_numerology_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    return FlowReading(body=build_numerology_matrix(facts, imprint))


def build_vedic_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    return FlowReading(body=build_vedic_matrix(facts, imprint))


def build_hellenistic_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    return FlowReading(body=build_hellenistic_matrix(facts, imprint))


def build_financial_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    return FlowReading(body=build_financial_matrix(facts, imprint))


def build_wealth_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    return FlowReading(body=build_wealth_matrix(facts, imprint))


def build_relationships_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    return FlowReading(body=build_relationships_matrix(facts, imprint))