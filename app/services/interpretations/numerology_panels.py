"""Structured numerology panels — compound-first, plain English."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.interpretations.numerology_compound_voice import build_avatar_text, build_compound_subtitle

from app.services.numerology_depth import PATH_ENEMY_NUMBERS, PATH_FRIEND_NUMBERS
from app.services.interpretations.numerology_lived_voice import build_total_advice, build_total_path

_TOTAL_SPECS = (
    ("expression", "Expression"),
    ("soul_urge", "Soul urge"),
    ("personality", "Personality"),
    ("birthday_number", "Birth day"),
)


def _format_birth_date(facts: dict[str, Any]) -> str:
    raw = (facts.get("birth") or {}).get("datetime_local", "")
    if not raw:
        return "—"
    dt = datetime.fromisoformat(raw.replace("Z", ""))
    return dt.strftime("%B %d, %Y")


def _build_birth_digit_sum(facts: dict[str, Any]) -> str:
    raw = (facts.get("birth") or {}).get("datetime_local", "")
    if not raw:
        return "—"
    dt = datetime.fromisoformat(raw.replace("Z", ""))
    ymd = dt.strftime("%Y%m%d")
    return "+".join(ymd)


def _other_totals(facts: dict[str, Any], lp: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for key, label in _TOTAL_SPECS:
        row = facts.get(key) or {}
        total = {
            "compound": row.get("compound"),
            "value": row.get("value"),
            "display": row.get("display", "—"),
        }
        rows.append(
            {
                "key": key,
                "label": label,
                "display": total["display"],
                "advice": build_total_advice(key, facts, lp),
                "path": build_total_path(lp, total, key),
            }
        )
    return rows


def build_numerology_panels(facts: dict[str, Any], imprint: dict[str, Any]) -> dict[str, Any]:
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    lib = get_compound_entry(c, f, disp)
    compound_title = lib["glyph"]

    return {
        "birth_date": _format_birth_date(facts),
        "birth_digit_sum": _build_birth_digit_sum(facts),
        "friend_numbers": PATH_FRIEND_NUMBERS.get(f, []),
        "enemy_numbers": PATH_ENEMY_NUMBERS.get(f, []),
        "life_path": {
            "compound": c,
            "value": f,
            "display": disp,
        },
        "compound_title": compound_title,
        "compound_subtitle": build_compound_subtitle(c, f, lib),
        "path_insight": {
            "avatar": build_avatar_text(c, f, facts, lib),
        },
        "other_totals": _other_totals(facts, lp),
    }


def assemble_numerology_narrative(panels: dict[str, Any], imprint: dict[str, Any]) -> str:
    from app.services.imprint_labels import build_display_bundle
    from app.services.interpretations.matrix_decoder_voice import build_numerology_matrix

    facts = build_display_bundle(imprint)
    return build_numerology_matrix(facts, imprint, panels=panels)