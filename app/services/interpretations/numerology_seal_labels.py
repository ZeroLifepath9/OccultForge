"""Compact numerology titles for the seal name block — glyphs only."""

from __future__ import annotations

from typing import Any

from app.services.compound_occult import (
    PATH_FINAL,
    build_compound_framework_reading,
    get_compound_entry,
)
from app.services.imprint_labels import numerology_display
from app.services.interpretations.manifestation_voice import plain_flesh


def _brief_sentence(text: str, max_words: int = 18) -> str:
    cleaned = plain_flesh(text).strip()
    if not cleaned:
        return ""
    lead = cleaned.split(".")[0].strip()
    words = lead.split()
    if len(words) > max_words:
        lead = " ".join(words[:max_words]).rstrip(",;") + "."
    elif not lead.endswith("."):
        lead += "."
    return lead


def _build_seal_life_path_insight(c: int, f: int, disp: str, lib: dict[str, Any]) -> str:
    """General compound→final line for the seal numerology box — not daily."""
    final_plain = PATH_FINAL.get(f, {}).get("plain", "")
    final_lead = _brief_sentence(final_plain, max_words=14)
    flesh = plain_flesh(lib.get("flesh", ""))
    compound_lead = _brief_sentence(flesh, max_words=14) if flesh else ""

    if c == f:
        core = compound_lead or final_lead or f"Single gate {f} — body and vow share one finish."
        return f"{core} Final {f} is the fixed direction."

    body = compound_lead or f"Compound {c} runs the body before the vow settles."
    direction = final_lead or f"walk life path {f} in order."
    return f"{body} Ultimate direction — {f}: {direction.rstrip('.')}."


def _glyph_for_total(row: dict[str, Any] | None) -> str:
    if not row:
        return "—"
    c, f, disp = row.get("compound"), row.get("value"), row.get("display", "—")
    if c is None or f is None:
        return "—"
    return get_compound_entry(c, f, disp).get("glyph", "—")


def build_numerology_seal_labels(imprint: dict[str, Any]) -> dict[str, Any]:
    py = imprint.get("numerology", {}).get("schools", {}).get("pythagorean") or {}
    lp = py.get("life_path") or {}
    soul = py.get("soul_urge") or {}
    born_expr = py.get("expression") or {}

    final_val = lp.get("value")
    final_title = PATH_FINAL.get(final_val, {}).get("glyph", f"path {final_val}") if final_val else "—"
    compound_val = lp.get("compound")
    lp_display = numerology_display(lp) if lp else "—"
    lib = (
        get_compound_entry(compound_val, final_val, lp_display)
        if compound_val is not None and final_val is not None
        else {}
    )
    seal_insight = (
        _build_seal_life_path_insight(compound_val, final_val, lp_display, lib)
        if compound_val is not None and final_val is not None
        else "—"
    )

    aka = imprint.get("numerology", {}).get("commonly_known_as") or {}
    aka_expr = aka.get("expression") if aka else None
    daily_walk: dict[str, str] | None = None
    daily_walk_compound_read: dict[str, Any] | None = None
    if aka_expr:
        daily_walk = {
            "display": numerology_display(aka_expr),
            "title": _glyph_for_total(aka_expr),
        }
        ac, af = aka_expr.get("compound"), aka_expr.get("value")
        if ac is not None and af is not None:
            daily_walk_compound_read = build_compound_framework_reading(
                ac,
                af,
                daily_walk["display"],
                placement="Expression compound (daily walk name-field)",
            )

    life_path_compound_read = (
        build_compound_framework_reading(
            compound_val,
            final_val,
            lp_display,
            placement="Life path compound",
        )
        if compound_val is not None and final_val is not None
        else None
    )

    born_display = numerology_display(born_expr) if born_expr else "—"
    born_compound_read = None
    if born_expr:
        bc, bf = born_expr.get("compound"), born_expr.get("value")
        if bc is not None and bf is not None:
            born_compound_read = build_compound_framework_reading(
                bc,
                bf,
                born_display,
                placement="Birth expression compound",
            )

    return {
        "life_path_display": lp_display,
        "compound_title": _glyph_for_total(lp),
        "final_title": final_title,
        "final_value": final_val,
        "seal_insight": seal_insight,
        "soul_contract_title": _glyph_for_total(soul),
        "life_path_compound_read": life_path_compound_read,
        "daily_walk_compound_read": daily_walk_compound_read,
        "born_expression_compound_read": born_compound_read,
        "born_expression": {
            "display": born_display,
            "title": _glyph_for_total(born_expr),
        },
        "daily_walk": daily_walk,
    }