"""Assemble grounded context for Zero conversations."""

from __future__ import annotations

from typing import Any

from app.overlay.hourly import build_hourly_advice_payload
from app.services.interpretations.zero_framework import zero_framework_context
from app.zero.rituals import ritual_candidates_for_payload


def imprint_summary(imprint: dict[str, Any]) -> dict[str, Any]:
    """Compact natal facts for LLM context (immutable imprint)."""
    from app.services.bazi_enrich import ensure_bazi_canonical
    from app.services.interpretations.bazi_interpretation_lens import compact_bazi_interpretation

    imprint = ensure_bazi_canonical(imprint)
    bazi = imprint["bazi"]
    py = imprint["numerology"]["schools"]["pythagorean"]
    lens = bazi.get("interpretation_lens") or {}
    return {
        "name": imprint["birth"]["display_name"],
        "bazi_pillars": {
            k: bazi["pillars"][k]["gan_zhi"] for k in ("year", "month", "day", "hour")
        },
        "day_master": bazi["day_master"],
        "element_balance": bazi["element_balance"],
        "bazi_interpretation": compact_bazi_interpretation(lens) if lens else {},
        "vedic_lagna": imprint["vedic"]["lagna"]["sign"],
        "moon_nakshatra": imprint["vedic"]["moon_nakshatra"],
        "active_mahadasha": imprint["vedic"]["dasha"]["active_mahadasha"],
        "western_sun_moon_rising": {
            "sun": imprint["western"]["planets"]["Sun"]["sign"],
            "moon": imprint["western"]["planets"]["Moon"]["sign"],
            "ascendant": imprint["western"]["angles"]["ascendant"]["sign"],
        },
        "numerology_pythagorean": {
            "life_path": py["life_path"],
            "expression": py["expression"],
            "soul_urge": py["soul_urge"],
        },
    }


def build_zero_context(imprint: dict[str, Any]) -> dict[str, Any]:
    hourly = build_hourly_advice_payload(imprint)
    rituals = ritual_candidates_for_payload(hourly)
    return {
        "natal_imprint_summary": imprint_summary(imprint),
        "current_hour_overlay": hourly,
        "ritual_candidates": rituals,
        "zero_framework": zero_framework_context(),
    }