"""Threshold seal — sealed natal chart + Babylonian Priest interpretation (no Zero/AI overview)."""

from __future__ import annotations

from typing import Any

from app.services.imprint_labels import build_display_bundle, pillar_english
from app.services.overview_lore import build_interpretive_briefs
from app.services.priest_overview import (
    CHART_MARKER,
    INTERPRETATION_MARKER,
    OVERVIEW_FORMAT,
    build_natal_chart_record,
    build_threshold_seal,
)

THRESHOLD_CTA = (
    "Chart sealed once. Daily readings compare today to this record — personalized, not generic."
)


def _deterministic_overview(
    imprint: dict[str, Any], facts: dict[str, Any], _briefs: dict[str, str]
) -> str:
    name = (
        imprint.get("birth", {}).get("display_name")
        or imprint.get("birth", {}).get("name")
        or "Seeker"
    )
    _, _, full, _ = build_threshold_seal(facts, name)
    return full


async def build_imprint_overview(
    imprint: dict[str, Any],
    *,
    use_ai: bool = False,
) -> dict[str, Any]:
    """Overview is priest template only — Zero is not invoked here."""
    facts = build_display_bundle(imprint)
    facts["ascendant"]["glyph"] = _sign_glyph(facts["ascendant"]["western_sign"])

    pillars = imprint["bazi"]["pillars"]
    facts["pillars_english"] = {
        k: pillar_english(pillars[k]) for k in ("year", "month", "day", "hour")
    }

    name = (
        imprint.get("birth", {}).get("display_name")
        or imprint.get("birth", {}).get("name")
        or "Seeker"
    )
    briefs = build_interpretive_briefs(facts)
    chart_ref, interpretation, narrative, chart_record = build_threshold_seal(facts, name)
    briefs["threshold_reading"] = interpretation
    briefs["chart_reference"] = chart_ref
    facts["interpretive_briefs"] = briefs
    facts["natal_chart_record"] = chart_record

    from app.config import settings as cfg

    from app.services.interpretations.zero_overview import READING_ENGINE

    return {
        "facts": facts,
        "reading_engine": READING_ENGINE,
        "narrative": narrative,
        "chart_reference": chart_ref,
        "interpretation": interpretation,
        "deterministic_fallback": narrative,
        "natal_chart_record": chart_record,
        "ai_used": False,
        "model": None,
        "ai_error": None,
        "zero_teaser": THRESHOLD_CTA,
        "chart_verified": bool(facts.get("chart_anchor", {}).get("verified")),
        "reading_kind": "threshold_seal",
        "overview_format": OVERVIEW_FORMAT,
        "template_signature": cfg.overview_template_signature,
        "chart_marker": CHART_MARKER,
        "interpretation_marker": INTERPRETATION_MARKER,
    }


def _sign_glyph(sign: str) -> str:
    glyphs = {
        "Aries": "♈",
        "Taurus": "♉",
        "Gemini": "♊",
        "Cancer": "♋",
        "Leo": "♌",
        "Virgo": "♍",
        "Libra": "♎",
        "Scorpio": "♏",
        "Sagittarius": "♐",
        "Capricorn": "♑",
        "Aquarius": "♒",
        "Pisces": "♓",
    }
    return glyphs.get(sign, "")