"""
Deep threshold reading — full inline occult teaching (no 'look up' deferrals).
"""

from __future__ import annotations

from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.interpretations.occult_insight_corpus import (
    teach_compound,
    teach_day_master,
    teach_final,
    teach_name_field,
    teach_nakshatra,
    teach_number_weave,
    teach_sky_weave,
)
from app.services.occult_wave import collect_chart_warnings
from app.services.seal_domains import (
    build_career_section,
    build_daily_section,
    build_domain_actions,
    build_relationship_section,
)

INTERPRETATION_MARKER = "YOUR READING"
SEAL_CLOSE = "walk this path"
READING_ENGINE = "deep-corpus-v1"


def _opening(name: str, facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    lib = get_compound_entry(lp["compound"], lp["value"], lp["display"])
    glyph, final_g = lib["glyph"], teach_final(lp["value"]).split(":")[0]
    if lp["compound"] == lp["value"]:
        return (
            f"{name}, this seal is one gate: {lp['display']} — {glyph}. "
            f"What follows is not a horoscope; it is the occult math of your birth date and name, "
            f"read through BaZi, Vedic, and Western sky together."
        )
    return (
        f"{name}, you are {lp['display']}: {glyph} moving toward {final_g}. "
        f"The unreduced compound is your primary initiation; the final number is the vow you must live. "
        f"Generic path-{lp['value']} copy will misread you — the compound is the body, the final is the exit."
    )


def _taught_warnings(facts: dict[str, Any], glyph: str) -> str:
    raw = collect_chart_warnings(facts)
    taught: list[str] = []
    for w in raw:
        if "look up" in w.lower():
            continue
        taught.append(w)
    lp = facts["life_path"]
    if lp["compound"] == 27 and not any("Sceptre" in t for t in taught):
        taught.insert(
            0,
            f"{glyph}: under fatigue you sign, spend, or rescue from compound 27 while preaching nine — "
            f"the matrix rewards that split; your seal does not.",
        )
    return "\n".join(f"• {t}" for t in taught) if taught else "• Systems align — main risk is drifting from day element when bored."


def build_deep_seal_reading(facts: dict[str, Any], name: str) -> str:
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    lib = get_compound_entry(c, f, disp)
    glyph = lib["glyph"]

    initiation = teach_compound(c, f, disp)
    if c != f:
        initiation += f"\n\n{teach_final(f)}"
    initiation += f"\n\n{teach_day_master(facts)}"

    name_blocks = [
        teach_name_field(k, facts)
        for k in ("expression", "soul_urge", "birthday_number", "personality")
    ]
    name_section = "\n\n".join(b for b in name_blocks if b)

    sections = [
        INTERPRETATION_MARKER,
        "",
        _opening(name, facts),
        "",
        "THE INITIATION — birth current",
        initiation,
        "",
        "HOW YOUR NUMBERS BEND THE INITIATION",
        teach_number_weave(facts),
        "",
        "THE SKY PRESSED ON YOUR SEAL",
        teach_sky_weave(facts, glyph),
    ]
    if name_section:
        sections.extend(["", "THE NAME ON YOUR BROW", name_section])
    sections.extend(
        [
            "",
            "CAREER & BUSINESS",
            build_career_section(facts),
            "",
            "RELATIONSHIP",
            build_relationship_section(facts),
            "",
            "DAILY RHYTHM",
            build_daily_section(facts),
            "",
            "CROSSWINDS — where systems agree you drift",
            _taught_warnings(facts, glyph),
            "",
            "THIS WEEK — body before story",
            "\n".join(f"{i + 1}. {a}" for i, a in enumerate(build_domain_actions(facts))),
            "",
            f"This is your Occult Forge threshold seal — depth meant to be lived, not collected. "
            f"Daily overlays compare today's sky to this record. {SEAL_CLOSE}.",
        ]
    )
    return "\n".join(sections)