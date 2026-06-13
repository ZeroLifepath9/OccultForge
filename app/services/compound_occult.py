"""
Compound occult engine — registry-backed glyphs, citations, kin, and chart modulation for every user.
"""

from __future__ import annotations

from typing import Any

from app.services.compound_registry import (
    BRANCH_MODULATION,
    COMPOUND_DIRECTORY,
    COMPOUND_ELEMENT_HINT,
    COMPOUND_GLYPH_EXPORT,
    ELEMENT_MODULATION,
    KINS_BY_FINAL,
    PATH_FINAL_DIRECTORY,
    SUN_MODULATION,
)

# Flat library shape used across overview
COMPOUND_LIBRARY: dict[int, dict[str, Any]] = {
    c: {
        "glyph": d["glyph"],
        "equation": d["equation"],
        "citations": d["citations"],
        "flesh": d["flesh"],
        "kin": d["kin_tag"],
        "final": d["final"],
    }
    for c, d in COMPOUND_DIRECTORY.items()
}

PATH_FINAL: dict[int, dict[str, str]] = {
    f: {
        "glyph": d["glyph"],
        "plain": d["plain"],
        "insight": d["insight"],
        "citations": d["citations"],
    }
    for f, d in PATH_FINAL_DIRECTORY.items()
}

PATH_INTEGRATION_PLAIN: dict[int, str] = {
    f: d["integration"] for f, d in PATH_FINAL_DIRECTORY.items()
}

KINS_AT_9 = KINS_BY_FINAL.get(9, "")


def get_compound_entry(compound: int, final: int, display: str) -> dict[str, Any]:
    """Resolve compound row; synthesize only if outside known directory."""
    if compound in COMPOUND_LIBRARY:
        lib = dict(COMPOUND_LIBRARY[compound])
        lib["kin"] = _kin_paragraph(compound, final, lib["glyph"], lib.get("kin", ""))
        return lib
    return _fallback_compound(compound, final, display)


def _kin_paragraph(compound: int, final: int, glyph: str, kin_tag: str) -> str:
    directory = KINS_BY_FINAL.get(final, "")
    if final == compound:
        return f"Single gate {compound} — {glyph}. {kin_tag}."
    return f"{kin_tag}. {directory}"


def _fallback_compound(c: int, f: int, disp: str) -> dict[str, Any]:
    from app.services.numerology_depth import COMPOUND_STAR_ANGEL
    from app.services.overview_lore import COMPOUND_PRESSURE

    return {
        "glyph": f"the {c} Field",
        "equation": f"{c} → {f} ({disp})",
        "citations": [
            f"Pythagorean compound pressure: {COMPOUND_PRESSURE.get(c, 'unreduced birth weight')}.",
            f"Star/angel thread: {COMPOUND_STAR_ANGEL.get(c, 'study compound ' + str(c) + ' numerology')}.",
            f"Look up: '{c}/{f} life path compound' vs 'life path {f} only' — different initiations.",
        ],
        "flesh": f"The body still runs {c} habits under stress while the soul is sworn to {f}.",
        "kin": _kin_paragraph(c, f, f"the {c} Field", f"signature compound {c} at final {f}"),
        "final": f,
    }


def _compound_chart_hooks(facts: dict[str, Any], c: int, glyph: str) -> list[str]:
    """Chart-specific lines from this seal — same engine for every user."""
    dm = facts["day_master"]
    el = dm["element"]
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "") or ""

    hooks: list[str] = []
    if el in ELEMENT_MODULATION:
        hooks.append(ELEMENT_MODULATION[el])
    hints = COMPOUND_ELEMENT_HINT.get(c, {})
    if el in hints:
        hooks.append(hints[el])
    if sun in SUN_MODULATION:
        hooks.append(SUN_MODULATION[sun])
    if day_an in BRANCH_MODULATION:
        hooks.append(f"{day_an} day branch: {BRANCH_MODULATION[day_an]}")
    if asc in ("Libra", "Scorpio") and c != facts["life_path"]["value"]:
        hooks.append(
            f"Rising {asc}: the room reads your compound before you do — perform {glyph} with integrity or it becomes gossip."
        )
    return hooks


def _chart_modulation(facts: dict[str, Any], c: int, glyph: str) -> str:
    dm = facts["day_master"]
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    expr = facts.get("expression", {}).get("value")
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    moon_n = facts["moon"].get("nakshatra", "")
    f = facts["life_path"]["value"]

    lines = [
        f"On your Occult Forge seal, {glyph} runs through {dm['yin_yang']} {dm['element']} ({dm['english']}) "
        f"on the {day_an or '—'} day — the final gate {f} must show in how you earn, cut, and serve.",
        f"Sun {sun} + rising {asc}: the compound performs you if closure is not verifiable to others.",
    ]
    lines.extend(_compound_chart_hooks(facts, c, glyph))
    if yz != day_an:
        lines.append(
            f"Year {yz} cast vs day {day_an} body: matrix wants {yz}; {glyph} wants {day_an} precision — "
            f"honor the day animal in work and love."
        )
    if expr and expr != f:
        lines.append(
            f"Name-field {facts['expression']['display']} vs birth {facts['life_path']['display']}: "
            f"reconcile brand and body before you sign."
        )
    if moon_n:
        lines.append(
            f"Moon nakshatra {moon_n}: emotional appetite colors {glyph} — look up {moon_n} + compound {c} together."
        )
    return " ".join(lines)


def build_compound_depth_reading(
    facts: dict[str, Any],
    *,
    include_chart: bool = True,
    field_label: str = "Birth current (life path)",
) -> tuple[str, dict[str, Any]]:
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    lib = get_compound_entry(c, f, disp)
    glyph = lib["glyph"]
    final = PATH_FINAL.get(f, {"glyph": f"path {f}", "citations": [], "plain": "", "insight": ""})
    final_glyph = final.get("glyph", f"path {f}")

    chart_block = _chart_modulation(facts, c, glyph) if include_chart else ""

    if c == f:
        cite_lines = "\n".join(f"  • {x}" for x in lib.get("citations", []) + final.get("citations", []))
        parts = [
            f"{field_label}: one gate {disp} — {glyph}.",
            lib.get("flesh", ""),
            f"Gate insight: {final.get('insight', final.get('plain', ''))}",
            "Occult seeds:",
            cite_lines,
        ]
        if chart_block:
            parts.extend(["On your chart:", chart_block])
        parts.append(f"Integration: {PATH_INTEGRATION_PLAIN.get(f, 'Walk the gate daily.')}")
        body = "\n".join(parts)
        return body, {"compound": c, "final": f, "glyph": glyph, "single_gate": True}

    cite_block = "\n".join(f"  • {cite}" for cite in lib["citations"])
    if f in KINS_BY_FINAL and "not one life" in KINS_BY_FINAL[f]:
        cite_block += f"\n  • {KINS_BY_FINAL[f]}"
    integration = PATH_INTEGRATION_PLAIN.get(f, f"Walk final {f} daily — starve compound {c} when it drives.")

    parts = [
        f"{field_label}: {disp} — {glyph} → {final_glyph}. Not interchangeable with generic path-{f} advice.",
        f"Equation: {lib['equation']}.",
        "Occult seeds:",
        cite_block,
        f"In the flesh: {lib['flesh']}",
        f"At this final: {lib.get('kin', '')}",
    ]
    if chart_block:
        parts.extend(["On your chart:", chart_block])
    parts.extend(
        [
            f"Final vow ({final_glyph}): {final.get('plain', '')}",
            f"Integration: {integration} Starve {c} when '{glyph}' signs or rescues for you.",
        ]
    )
    body = "\n".join(parts)

    meta = {
        "compound": c,
        "final": f,
        "display": disp,
        "glyph": glyph,
        "citations": lib["citations"],
        "lookup_terms": [glyph, f"compound {c}", f"{c}/{f} numerology", lib["equation"]],
    }
    return body, meta


def build_compound_framework_reading(
    c: int,
    f: int,
    display: str,
    *,
    placement: str = "Compound field",
) -> dict[str, Any]:
    """Generic occult compound read — chart framework only, not applied to a seeker."""
    lib = get_compound_entry(c, f, display)
    glyph = lib["glyph"]
    final = PATH_FINAL.get(f, {"glyph": f"path {f}", "plain": "", "insight": "", "citations": []})
    final_glyph = final.get("glyph", f"path {f}")

    lines: list[str] = [
        f"{placement}: {display} — {glyph}.",
        (
            "Framework: compound body, life-path final, and soul contract are separate gates — "
            "never collapse expression into path or contract into compound."
        ),
    ]
    if c == f:
        lines.append(f"Single gate {c}: compound and final share one finish ({final_glyph}).")
        if lib.get("flesh"):
            lines.append(lib["flesh"])
    else:
        lines.append(
            f"Equation {lib['equation']}: unreduced {c} runs habit and appetite; "
            f"final {f} ({final_glyph}) sets chart direction."
        )
        if lib.get("flesh"):
            lines.append(lib["flesh"])
        if lib.get("kin"):
            lines.append(lib["kin"])
    cites = lib.get("citations") or []
    if cites:
        lines.append("Occult seeds:")
        lines.extend(f"• {cite}" for cite in cites[:5])
    if final.get("plain"):
        lines.append(f"Final vow ({final_glyph}): {final['plain']}")
    integration = PATH_INTEGRATION_PLAIN.get(f, "")
    if integration:
        lines.append(f"Placement in chart work: {integration}")

    body = "\n\n".join(line for line in lines if line and line.strip())
    return {
        "compound": c,
        "final": f,
        "display": display,
        "glyph": glyph,
        "placement": placement,
        "body": body,
    }


def build_compound_seal_section(facts: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    body, meta = build_compound_depth_reading(facts)
    lp = facts["life_path"]
    header = [
        f"COMPOUND {lp['compound']} → final {lp['value']} ({lp['display']})",
        f"Occult name: {meta['glyph']}",
        "",
        body,
    ]
    return "\n".join(header), meta


def build_prophetic_opening(facts: dict[str, Any], name: str) -> str:
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    lib = get_compound_entry(c, f, disp)
    final_glyph = PATH_FINAL.get(f, {}).get("glyph", f"path {f}")
    if c == f:
        return (
            f"{name}, you carry one gate on the seal: {disp} — {lib['glyph']}. "
            f"Generic path-{f} horoscopes do not apply; this directory is keyed to your compound-field."
        )
    return (
        f"{name}, you are {disp}: {lib['glyph']} initiated toward {final_glyph}. "
        f"The unreduced field {c} is your primary occult name; path-{f} advice is secondary."
    )


# Re-export for occult_wave
COMPOUND_GLYPH = COMPOUND_GLYPH_EXPORT