"""Ensure daily payload BaZi fields are English (incl. cached rows)."""

from __future__ import annotations

from datetime import date
from typing import Any

from app.overlay.daily import BLEND_RULE, build_daily_reflection_payload
from app.services.imprint_labels import branch_animal, gan_zhi_english, stem_english


def _needs_refresh(payload: dict[str, Any]) -> bool:
    bazi = payload.get("bazi") or {}
    saturn = payload.get("saturn_karma") or {}
    scores = payload.get("scores") or {}
    numerology = payload.get("numerology") or {}
    return not (
        bazi.get("sky_pillars")
        and saturn.get("insight")
        and scores.get("tier")
        and bazi.get("favorability_tier")
        and numerology.get("compat")
        and numerology.get("insight")
        and bazi.get("astrology_layer")
        and (bazi.get("astrology_layer") or {}).get("framework")
        and (bazi.get("astrology_layer") or {}).get("natal", {}).get("day", {}).get("hidden_stem")
        and (bazi.get("astrology_layer") or {}).get("framework", {}).get("hidden_stems", {}).get("formula")
        and (bazi.get("astrology_layer") or {}).get("interpretation_lens", {}).get("version")
        == "bazi-lens-v2"
        and (bazi.get("astrology_layer") or {}).get("luck_pillar", {}).get("current")
        and payload.get("daily_framing")
        and scores.get("blend_rule") == BLEND_RULE
    )


def enrich_daily_bazi_english(payload: dict[str, Any], imprint: dict[str, Any]) -> dict[str, Any]:
    target = None
    if payload.get("date"):
        try:
            target = date.fromisoformat(str(payload["date"]))
        except ValueError:
            target = None

    if _needs_refresh(payload):
        fresh = build_daily_reflection_payload(imprint, target)
        for key in ("numerology", "bazi", "saturn_karma", "scores", "daily_framing", "payload_hash"):
            if key in fresh:
                payload[key] = fresh[key]
        payload["date"] = fresh.get("date", payload.get("date"))

    bazi = dict(payload.get("bazi") or {})
    natal = imprint["bazi"]["pillars"]["day"]
    bazi["natal_day_pillar_en"] = (
        f"{stem_english(natal['stem'])} {branch_animal(natal['branch'])}"
    )
    current_gz = bazi.get("current_day_pillar") or ""
    bazi["current_day_pillar_en"] = gan_zhi_english(current_gz)
    bazi["day_master_en"] = stem_english(imprint["bazi"]["day_master"]["stem"])
    payload["bazi"] = bazi
    return payload