"""Backfill canonical BaZi fields on sealed imprints (read-time, no re-seal)."""

from __future__ import annotations

from typing import Any

from app.calculators.bazi import year_zodiac_from_pillars
from app.services.interpretations.bazi_hidden_stems import (
    attach_hidden_stems_to_pillars,
    build_hidden_stems_framework,
)
from app.calculators.bazi_luck import luck_pillars_legacy_list, refresh_luck_bundle
from app.services.interpretations.bazi_interpretation_lens import build_bazi_interpretation_lens
from app.services.interpretations.bazi_luck_pillar_lens import build_luck_pillar_lens
from app.services.imprint_labels import build_display_bundle
from app.services.interpretations.vedic_house_sign_engine import build_vedic_interpretation_lens
from app.services.interpretations.numerology_seal_labels import build_numerology_seal_labels
from app.services.interpretations.seal_houses import build_seal_houses
from app.services.interpretations.relationships_framing import build_relationships_framing
from app.services.interpretations.wealth_chart_lens import build_wealth_chart_lens


def ensure_bazi_canonical(imprint: dict[str, Any]) -> dict[str, Any]:
    bazi = imprint.get("bazi")
    if not bazi or "pillars" not in bazi:
        return imprint
    pillars = bazi["pillars"]
    attach_hidden_stems_to_pillars(pillars)
    dm_el = (bazi.get("day_master") or {}).get("element") or ""
    bazi["hidden_stems_framework"] = build_hidden_stems_framework(pillars, dm_el)
    bazi["luck"] = refresh_luck_bundle(imprint)
    bazi["luck_pillars"] = luck_pillars_legacy_list(bazi["luck"])
    imprint["bazi"] = bazi
    bazi["interpretation_lens"] = build_bazi_interpretation_lens(
        pillars, imprint=imprint, include_luck=False
    )
    luck_interp = build_luck_pillar_lens(imprint)
    bazi["luck"]["interpretation"] = luck_interp
    lens = bazi["interpretation_lens"]
    if lens:
        from app.services.interpretations.bazi_luck_pillar_lens import interpret_luck_pillar_for_registry

        lens["luck_pillar"] = luck_interp
        interpreters = list(lens.get("interpreters") or [])
        if "luck_pillar" not in interpreters:
            interpreters.append("luck_pillar")
        lens["interpreters"] = interpreters
        luck_ix, luck_dirs = interpret_luck_pillar_for_registry(
            pillars, dm_el, imprint=imprint
        )
        lens["chart_interactions"] = (luck_ix or []) + list(lens.get("chart_interactions") or [])
        seen: set[str] = set()
        merged: list[str] = []
        for d in (luck_dirs or []) + list(lens.get("advice_directives") or []):
            if d not in seen:
                seen.add(d)
                merged.append(d)
        lens["advice_directives"] = merged[:5]
    fresh = year_zodiac_from_pillars(pillars)
    existing = bazi.get("year_zodiac") or {}
    needs_yz = (
        existing.get("label") != fresh["label"]
        or existing.get("gan_zhi") != fresh["gan_zhi"]
        or existing.get("hidden_stem") != fresh.get("hidden_stem")
        or not existing
    )
    if needs_yz:
        bazi["year_zodiac"] = fresh
    imprint["wealth_chart"] = build_wealth_chart_lens(imprint)
    imprint["relationships_framing"] = build_relationships_framing(imprint)
    imprint["numerology_seal_labels"] = build_numerology_seal_labels(imprint)
    imprint["seal_houses"] = build_seal_houses(imprint)
    if imprint.get("vedic"):
        imprint["vedic_interpretation_lens"] = build_vedic_interpretation_lens(
            build_display_bundle(imprint)
        )
    imprint["bazi"] = bazi
    return imprint