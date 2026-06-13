"""
Zero's combined seal read — Matrix Decoder across every sealed chart.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.matrix_decoder_voice import build_zero_matrix_overview
from app.services.interpretations.zero_framework import ZERO_SEAL_CLOSE

READING_ENGINE = "zero-overview-v7-zero-framework"
SEAL_CLOSE = ZERO_SEAL_CLOSE
ZERO_OVERVIEW_MARKER = SEAL_CLOSE


def build_zero_overview(facts: dict[str, Any], name: str) -> str:
    return build_zero_matrix_overview(facts, name)