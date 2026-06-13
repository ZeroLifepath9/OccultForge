"""
Name-field numerology — expression, soul urge, birthday, personality.
Same compound directory as life path; field-specific occult role (no generic path-9 repetition).
"""

from __future__ import annotations

from typing import Any

from app.services.compound_occult import get_compound_entry

# Occult role of each field on the seal (not interchangeable with life path)
FIELD_META: dict[str, dict[str, str]] = {
    "expression": {
        "title": "Expression (public name-field)",
        "role": "How the world contracts your name — brand, title, first impression of competence.",
        "lookup": "Pythagorean expression number; compare to birth compound.",
    },
    "soul_urge": {
        "title": "Soul urge (vowels of the name)",
        "role": "What you crave when alone — private appetite behind the mask.",
        "lookup": "Soul urge numerology; vowel sum before reduction.",
    },
    "birthday_number": {
        "title": "Birth day number",
        "role": "Gift and wound of the day you were born — repeats every month as a tide.",
        "lookup": "Birthday number numerology; day-of-month field, not full birth sum.",
    },
    "personality": {
        "title": "Personality (consonants of the name)",
        "role": "Armor at the door — how strangers read you before trust.",
        "lookup": "Personality number; consonant sum in Pythagorean name math.",
    },
}

COMPOUND_WORK_LANE: dict[int, str] = {
    27: "cycle-closer, standards officer, ops in care/food/shelter, editor of endings — not generic nonprofit casting",
    18: "grief-worker, therapist, archivist, estate/emotional closure roles",
    36: "public legacy roles, stage-facing completion, executive release",
    13: "rebuilder, phoenix trades, systems that die and respawn",
    11: "channel product, grounded coach, pattern analyst — invoice the nerve",
    29: "sensitive liaison, translator, diplomat of hard news",
    10: "spokesperson, pivot leader, turnaround face — earn the wheel before spin",
    19: "solar brand lead, visibility with reinvention discipline",
    1: "founder lane, named credit, solo offer — no waiting for permission",
    6: "hearth professions: design, wellness, food, family systems — beauty with boundaries",
}


def _num_dict(facts: dict[str, Any], key: str) -> dict[str, Any]:
    return facts.get(key) or {}


def build_field_compound_block(
    facts: dict[str, Any],
    field_key: str,
    *,
    documented_compounds: set[int],
) -> str:
    """Occult depth for one name-field; skips repeated citations when compound already opened."""
    meta = FIELD_META[field_key]
    num = _num_dict(facts, field_key)
    if not num.get("value"):
        return ""

    c, v, disp = num["compound"], num["value"], num["display"]
    lib = get_compound_entry(c, v, disp)
    glyph = lib["glyph"]

    if c in documented_compounds:
        return "\n".join(
            [
                meta["title"],
                meta["role"],
                f"  {disp} — {glyph} (same compound as above). This field {meta['lookup'].split(';')[0].lower()}; "
                f"do not read it as a second life path — it colors how the birth current shows in this layer.",
                f"  Field tint: {lib['flesh']}",
            ]
        )

    documented_compounds.add(c)
    cites = lib["citations"][:3]
    cite_lines = "\n".join(f"    • {x}" for x in cites)
    gate_note = (
        f"Single gate {disp} — {glyph}; flesh and vow align in this field."
        if c == v
        else f"{disp}: {glyph} → final {v}; compound performs before the vow settles."
    )

    return "\n".join(
        [
            meta["title"],
            meta["role"],
            gate_note,
            f"  Occult name: {glyph} · {lib['equation']}",
            f"  In this field: {lib['flesh']}",
            f"  Lookup: {meta['lookup']}",
            "  Seeds:",
            cite_lines,
        ]
    )


def build_name_fields_section(facts: dict[str, Any]) -> str:
    documented: set[int] = {facts["life_path"]["compound"]}
    blocks = []
    for key in ("expression", "soul_urge", "birthday_number", "personality"):
        block = build_field_compound_block(facts, key, documented_compounds=documented)
        if block:
            blocks.append(block)
    if not blocks:
        return ""
    return "\n\n".join(blocks)


def build_number_weave(facts: dict[str, Any]) -> str:
    """
    What the numbers mean together — once, specific to this seal.
    Avoids repeating generic final-path copy (e.g. path-9 humanitarian platitudes).
    """
    lp = facts["life_path"]
    expr = _num_dict(facts, "expression")
    soul = _num_dict(facts, "soul_urge")
    bday = _num_dict(facts, "birthday_number")
    pers = _num_dict(facts, "personality")

    lp_e = get_compound_entry(lp["compound"], lp["value"], lp["display"])
    lp_glyph = lp_e["glyph"]
    final_glyph = lp_e.get("final", lp["value"])

    lines = [
        f"Birth current (primary): {lp['display']} — {lp_glyph}. "
        f"This is the initiation, not a horoscope paragraph about path-{lp['value']}.",
    ]

    fields = [
        ("expression", expr, "the world reads"),
        ("soul_urge", soul, "you privately want"),
        ("birthday_number", bday, "the day itself repeats"),
        ("personality", pers, "strangers meet"),
    ]
    glyphs_seen: dict[str, list[str]] = {}

    for key, num, lens in fields:
        if not num.get("value"):
            continue
        lib = get_compound_entry(num["compound"], num["value"], num["display"])
        g = lib["glyph"]
        glyphs_seen.setdefault(g, []).append(key)
        if num["compound"] == lp["compound"]:
            lines.append(
                f"{FIELD_META[key]['title']}: {num['display']} — {g} (same compound as birth). "
                f"{lens.capitalize()} the birth current in this layer only — details under Birth current, not a second path."
            )
        elif num["value"] == lp["value"]:
            lines.append(
                f"{FIELD_META[key]['title']}: {num['display']} shares final {lp['value']} ({final_glyph}) but compound {num['compound']} differs — "
                f"{lens} {g}, not the same road as {lp_glyph}."
            )
        else:
            lines.append(
                f"{FIELD_META[key]['title']}: {num['display']} ({g}) — {lens} a different current than birth {lp['display']}; "
                f"reconcile before you brand or hire."
            )

    # Tension / harmony synthesis (one paragraph)
    expr_v, soul_v, bday_v = expr.get("value"), soul.get("value"), bday.get("value")
    tensions: list[str] = []
    if expr_v and expr_v != lp["value"]:
        tensions.append(f"public {expr['display']} vs birth {lp['display']}")
    if soul_v and soul_v != lp["value"]:
        tensions.append(f"private soul {soul['display']} vs birth {lp['display']}")
    if expr_v and soul_v and expr_v != soul_v:
        tensions.append(f"mask {expr['display']} vs appetite {soul['display']}")

    if tensions:
        lines.append(
            "Friction to manage: " + "; ".join(tensions) + ". "
            "The matrix wants you to perform the loudest mask; the birth compound decides what must close."
        )
    elif lp["compound"] == 27:
        lines.append(
            "Name-fields and birth rhyme or stay in the same voltage — the work is Sceptre discipline in public, "
            "not scattering into generic completion language."
        )
    else:
        lines.append("Number-fields point one direction — execute the birth compound daily; masks are amplifiers, not replacements.")

    if bday_v:
        b_lib = get_compound_entry(bday["compound"], bday["value"], bday["display"])
        lines.append(
            f"Monthly tide: birthday {bday['display']} ({b_lib['glyph']}) revisits each month on the {facts.get('birth_day', 'birth')} day — "
            f"use it for {b_lib['flesh'].split('—')[0].strip().lower() or 'maintenance'}, not life-path re-explaining."
        )

    dup = [g for g, keys in glyphs_seen.items() if len(keys) > 1]
    if dup:
        lines.append(
            f"Repeated glyph {dup[0]} across fields — the chart doubles down; say it once, live it daily."
        )

    return "\n".join(lines)


def work_lane_for_seal(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    return COMPOUND_WORK_LANE.get(lp["compound"]) or COMPOUND_WORK_LANE.get(
        lp["value"],
        "roles that match your day element and house signs below",
    )