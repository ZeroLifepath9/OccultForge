"""Deterministic daily overlay — no LLM."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo

from lunar_python import Solar

from app.calculators.bazi import BRANCH_ELEMENTS, STEM_ELEMENTS
from app.calculators.numerology import personal_month, personal_year, universal_day, universal_year
from app.overlay.clashes import branch_clashes
from app.services.imprint_labels import branch_animal, stem_english
from app.services.interpretations.bazi_daily_astrology import (
    bazi_favorability_score,
    build_bazi_astrology_layer,
    build_bazi_daily_framing,
    build_sky_element_friction,
)
from app.services.interpretations.numerology_daily_compat import (
    build_daily_number_framing,
    build_daily_numerology_overlay,
    build_day_field_assessment,
)
from app.services.interpretations.saturn_karma_insight import build_saturn_karma_insight
from app.services.interpretations.wealth_chart_lens import build_wealth_chart_lens


def _pillar_bundle(ec: Any, gan_fn: str, zhi_fn: str) -> dict[str, str]:
    stem = getattr(ec, gan_fn)()
    branch = getattr(ec, zhi_fn)()
    return {
        "stem": stem,
        "branch": branch,
        "gan_zhi": f"{stem}{branch}",
        "stem_en": stem_english(stem),
        "branch_en": branch_animal(branch),
        "stem_element": STEM_ELEMENTS.get(stem, ""),
        "branch_element": BRANCH_ELEMENTS.get(branch, ""),
    }


def _tier_from_score(score: float) -> str:
    if score >= 0.82:
        return "very-good"
    if score >= 0.62:
        return "good"
    if score >= 0.45:
        return "neutral"
    if score >= 0.28:
        return "bad"
    return "terrible"


BLEND_RULE = "num45_bazi55_v1"


def _merge_daily_framing(
    num_framing: dict[str, list[str]],
    bazi_framing: dict[str, list[str]],
) -> dict[str, list[str]]:
    promote: list[str] = []
    avoid: list[str] = []
    for src in (num_framing, bazi_framing):
        for item in src.get("promote") or []:
            if item and item not in promote:
                promote.append(item)
        for item in src.get("avoid") or []:
            if item and item not in avoid:
                avoid.append(item)
    return {"promote": promote[:3], "avoid": avoid[:3]}


def _merge_favorability(
    num_score: float,
    num_tier: str,
    num_hint: str,
    astrology_layer: dict[str, Any],
) -> tuple[float, str, str]:
    """45% numerology compat + 55% BaZi day tone; severe clash caps the blend."""
    bazi_score = bazi_favorability_score(astrology_layer)
    score = max(0.08, min(0.96, 0.45 * num_score + 0.55 * bazi_score))
    if astrology_layer.get("severe_clash") and score >= 0.45:
        score = max(0.28, score - 0.08)
    tier = _tier_from_score(score)
    if tier in ("terrible", "bad") or astrology_layer.get("severe_clash"):
        hint = "caution"
    elif tier == "very-good":
        hint = "tailwind"
    elif tier == "good":
        hint = "flow"
    else:
        hint = "ordinary"
    return round(score, 3), tier, hint


def _current_bazi_pillars(local_dt: datetime) -> dict[str, dict[str, str]]:
    solar = Solar.fromYmdHms(
        local_dt.year, local_dt.month, local_dt.day, 12, 0, 0
    )
    ec = solar.getLunar().getEightChar()
    return {
        "year": _pillar_bundle(ec, "getYearGan", "getYearZhi"),
        "month": _pillar_bundle(ec, "getMonthGan", "getMonthZhi"),
        "day": _pillar_bundle(ec, "getDayGan", "getDayZhi"),
    }


def build_daily_reflection_payload(
    imprint: dict[str, Any],
    target_date: date | None = None,
) -> dict[str, Any]:
    birth = imprint["birth"]
    tz = ZoneInfo(birth["timezone"])
    local_now = datetime.now(tz)
    target = target_date or local_now.date()

    birth_dt = datetime.fromisoformat(birth["datetime_local"].replace("Z", ""))
    if birth_dt.tzinfo is None:
        birth_dt = birth_dt.replace(tzinfo=tz)
    birth_date = birth_dt.date()

    pillars = imprint["bazi"]["pillars"]
    natal_day = pillars["day"]
    local_noon = datetime(target.year, target.month, target.day, 12, 0, tzinfo=tz)
    sky = _current_bazi_pillars(local_noon)
    current_day = sky["day"]
    clashes = branch_clashes(natal_day["branch"], current_day["branch"])
    astrology_layer = build_bazi_astrology_layer(pillars, sky, imprint=imprint)
    sky_friction = build_sky_element_friction(pillars, sky, astrology_layer, imprint=imprint)
    ud_num = universal_day(target)
    num_overlay = build_daily_numerology_overlay(imprint, target)
    fav_score, fav_tier, fav_hint = _merge_favorability(
        num_overlay["favorability_score"],
        num_overlay["favorability_tier"],
        num_overlay["favorability_hint"],
        astrology_layer,
    )
    num_framing = build_daily_number_framing(
        num_overlay["compat"],
        num_overlay["month_skew"],
    )
    bazi_framing = build_bazi_daily_framing(astrology_layer)
    daily_framing = _merge_daily_framing(num_framing, bazi_framing)
    day_field = build_day_field_assessment(num_overlay, astrology_layer)

    natal_pillars_en = {
        k: f"{stem_english(pillars[k]['stem'])} {branch_animal(pillars[k]['branch'])}"
        for k in ("year", "month", "day")
    }

    lp_raw = num_overlay.get("user_life_path")
    lp_val = lp_raw if isinstance(lp_raw, int) else (lp_raw.get("value") if isinstance(lp_raw, dict) else None)
    saturn_karma = build_saturn_karma_insight(imprint, user_life_path=lp_val)
    from app.services.bazi_enrich import ensure_bazi_canonical

    enriched = ensure_bazi_canonical(imprint)
    wealth_chart = build_wealth_chart_lens(enriched, reference=target)
    from app.services.imprint_labels import build_display_bundle
    from app.services.interpretations.interaction_maps import interaction_map

    daily_facts = build_display_bundle(enriched)
    relationships_chart = {
        "condensed": interaction_map(daily_facts, "relationships", enriched),
    }

    payload = {
        "date": target.isoformat(),
        "timezone": birth["timezone"],
        "numerology": {
            "universal_year": universal_year(target.year),
            "universal_day": ud_num,
            "personal_year": personal_year(birth_date, target.year),
            "personal_month": personal_month(birth_date, target.year, target.month),
            "personal_day": num_overlay["personal_day"],
            "calendar_day": num_overlay["calendar_day"],
            "life_path_day": num_overlay["life_path_day"],
            "user_life_path": num_overlay["user_life_path"],
            "user_birthday_number": num_overlay["user_birthday_number"],
            "compat": num_overlay["compat"],
            "month_skew": num_overlay["month_skew"],
            "insight": num_overlay["insight"],
            "gate_relation": num_overlay["gate_relation"],
            "gate_line": num_overlay["gate_line"],
        },
        "bazi": {
            "natal_day_pillar": natal_day["gan_zhi"],
            "current_day_pillar": current_day["gan_zhi"],
            "natal_day_pillar_en": natal_pillars_en["day"],
            "current_day_pillar_en": (
                f"{current_day['stem_en']} {current_day['branch_en']}"
            ),
            "natal_pillars_en": natal_pillars_en,
            "sky_pillars": sky,
            "day_master": imprint["bazi"]["day_master"]["stem"],
            "day_master_en": stem_english(imprint["bazi"]["day_master"]["stem"]),
            "clashes": clashes,
            "natal_pillars": {
                "year": pillars["year"],
                "day": pillars["day"],
            },
            "astrology_layer": astrology_layer,
            "sky_friction": sky_friction,
            "favorability_hint": fav_hint,
            "favorability_tier": fav_tier,
        },
        "saturn_karma": saturn_karma,
        "wealth_chart": {
            "condensed": wealth_chart.get("condensed", ""),
            "primary_insight": wealth_chart.get("primary_insight", ""),
            "day_pillar_narrative": wealth_chart.get("day_pillar_narrative", ""),
            "element_climate_insight": wealth_chart.get("element_climate_insight", ""),
            "mission_sentence": wealth_chart.get("mission_sentence", ""),
            "support": wealth_chart.get("support", ""),
            "end": wealth_chart.get("end", ""),
            "shadow": wealth_chart.get("shadow", ""),
            "cheat_code": (wealth_chart.get("day_pillar_animal") or {}).get("cheat_code", ""),
            "animal": (wealth_chart.get("day_pillar_animal") or {}).get("animal", ""),
            "day_master": wealth_chart.get("day_master") or {},
            "day_pillar_profile": wealth_chart.get("day_pillar_profile") or {},
            "income_crown_synthesis": wealth_chart.get("income_crown_synthesis", ""),
            "vedic_wealth_weave": wealth_chart.get("vedic_wealth_weave", ""),
            "vedic_career_weave": wealth_chart.get("vedic_career_weave", ""),
            "year_climate": wealth_chart.get("year_climate") or {},
        },
        "relationships_chart": relationships_chart,
        "western": {
            "natal_sun": imprint["western"]["planets"]["Sun"]["sign"],
            "natal_moon": imprint["western"]["planets"]["Moon"]["sign"],
        },
        "daily_framing": daily_framing,
        "day_field": day_field,
        "scores": {
            "favorability": fav_score,
            "tier": fav_tier,
            "blend_rule": BLEND_RULE,
            "bazi_component": bazi_favorability_score(astrology_layer),
            "numerology_component": num_overlay["favorability_score"],
        },
    }

    # Western daily planets (tropical) for lens toggle — planets signs/degrees for "planets, timing" framing.
    # Reuse compute_western (planets are location-independent; houses/angles use birth lat/lon + target noon).
    # Guard so Eastern path + all prior daily callers are 100% unaffected.
    try:
        from datetime import timezone as _tz
        from app.calculators.western import compute_western as _cw
        target_noon_local = datetime(target.year, target.month, target.day, 12, 0, tzinfo=tz)
        target_utc = target_noon_local.astimezone(_tz.utc).replace(tzinfo=None)
        w_today = _cw(target_utc, birth["latitude"], birth["longitude"])
        w_planets = w_today.get("planets") or {}
        payload["western"]["planets_today"] = {
            k: {"sign": v.get("sign"), "degree": v.get("degree")} for k, v in w_planets.items()
        }
    except Exception:
        # Never fail daily payload construction for the toggle feature
        payload["western"].setdefault("planets_today", {})

    payload["payload_hash"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]
    return payload