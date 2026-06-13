"""Occult-wave vocabulary — compound glyphs (Sceptre, etc.) and how they differ at the same path."""

from __future__ import annotations

from typing import Any

from app.services.compound_registry import (
    COMPOUND_DIRECTORY,
    COMPOUND_GLYPH_EXPORT,
    PATH_FINAL_DIRECTORY,
)

COMPOUND_GLYPH = COMPOUND_GLYPH_EXPORT

COMPOUND_VS_KIN: dict[int, str] = {
    c: f"{c}/{d['final']} — {d['glyph']}: {d['kin_tag']}"
    for c, d in COMPOUND_DIRECTORY.items()
    if c != d["final"]
}

PATH_FINAL_GLYPH: dict[int, str] = {f: d["glyph"] for f, d in PATH_FINAL_DIRECTORY.items()}


def compound_wave_paragraph(facts: dict[str, Any]) -> str:
    """Legacy one-paragraph wave; threshold overview uses compound_occult.build_compound_depth_reading."""
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    final_glyph = PATH_FINAL_GLYPH.get(f, f"path {f}")

    if c == f:
        glyph = final_glyph
        return (
            f"Your Occult Forge seal shows one gate: {disp} — {glyph}. "
            f"No split between what you perform and what you came to finish. "
            f"The false matrix offers you masks; this number asks you to drop one mask per season until only the gate remains."
        )

    glyph = COMPOUND_GLYPH.get(c, f"the {c} field")
    kin = COMPOUND_VS_KIN.get(
        c,
        f"{c}/{f} argues in the flesh before {f} ({final_glyph}) becomes habit — the compound is the old script; the final is the exit door.",
    )
    return (
        f"Your seal reads {disp} — in the current you carry {glyph}, initiated toward {final_glyph}. "
        f"{kin} "
        f"The matrix rewards performance of the compound (comfort, drama, rescue, hustle) and punishes you when you refuse the final. "
        f"You are not generic path-{f}; you are {c}→{f}, and that distinction is the whole game."
    )


def collect_chart_warnings(facts: dict[str, Any]) -> list[str]:
    """Warnings every system agrees on — one list, plain language."""
    from app.services.babylon_premium import BRANCH_CLASH, WESTERN_OPPOSITE

    out: list[str] = []
    lp = facts["life_path"]
    c, f = lp["compound"], lp["value"]
    yz = facts["year_zodiac"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    moon = facts["moon"]
    dm = facts["day_master"]

    if c != f:
        from app.services.compound_occult import get_compound_entry

        lib = get_compound_entry(c, f, lp["display"])
        glyph = lib["glyph"]
        out.append(
            f"Numbers: {glyph} ({c}) vs life path {f} — under stress you revert to compound habits while preaching the final. "
            f"Watch spending, quitting, and rescue fantasies when tired."
        )

    if yz["animal"] != day_an:
        clash = BRANCH_CLASH.get(yz["animal"], "")
        out.append(
            f"BaZi: year {yz['animal']} vs day {day_an} — you are cast for the year animal in public; "
            f"your body runs the day animal. Wrong roles exhaust you. "
            + (f"Clash animal: {clash} — high-friction people/years." if clash else "")
        )

    if asc != sun:
        out.append(
            f"Western: rising {asc} meets the room before Sun {sun} — first impressions mislead bosses and partners. "
            f"Lead with {sun} choices after the door opens, not only {asc} charm."
        )

    if moon["sidereal_sign"] != moon["western_sign"]:
        out.append(
            f"Vedic/tropical Moon split: private hunger is {moon['sidereal_sign']} ({moon.get('nakshatra', '')}); "
            f"you tell a {moon['western_sign']} story — feed the sidereal need or mood lies."
        )

    if facts["ascendant"]["vedic_lagna"] != asc:
        out.append(
            f"Lagna {facts['ascendant']['vedic_lagna']} is the body; Ascendant {asc} is the costume — "
            f"health and work must honor lagna, not only the mask."
        )

    sun_opp = WESTERN_OPPOSITE.get(sun, "")
    if sun_opp:
        out.append(
            f"Sun {sun} axis warns: people and seasons of {sun_opp} mirror/enemy your will — not forbidden, but costly if you pretend they are neutral."
        )

    month = (facts.get("pillars") or {}).get("month") or {}
    if month.get("stem_element") and month["stem_element"] != dm["element"]:
        out.append(
            f"Month pillar {month.get('stem_element', '')} seasons your career decade; day {dm['element']} is your daily mode — "
            f"misaligned work feels like pushing a boulder uphill."
        )

    houses = facts.get("vedic_houses") or []
    h8 = next((h for h in houses if h.get("house") == 8), None)
    if h8 and h8.get("planets"):
        out.append(
            f"8th house activated ({h8.get('sign', '')}) — shared money, inheritance, and psychological depth are not optional themes; "
            f"avoid sloppy joint finances."
        )

    if not out:
        out.append(
            "Systems align more than average — main risk is drifting from your day element and life path out of boredom, not chaos."
        )
    return out