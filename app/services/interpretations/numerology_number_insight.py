"""Brief lived examples, card arcs, and ally-field flow for numerology reads."""

from __future__ import annotations

import re
from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.interpretations.manifestation_voice import plain_flesh
from app.services.interpretations.numerology_daily_compat import numerology_relation
from app.services.numerology_depth import PATH_ENEMY_NUMBERS, PATH_FRIEND_NUMBERS

FINAL_ESSENCE: dict[int, str] = {
    1: "leadership and independence — beginnings, nerve, standing first without a committee",
    2: "partnership and sensitivity — cooperation, mirror, emotional tide in the room",
    3: "creativity and expression — joy, voice, and charisma when the draft is real",
    4: "stability and practicality — structure, repetition, and foundations that outlast hype",
    5: "change and freedom — adaptability, travel, and honest motion before escape",
    6: "responsibility and nurturing — home, care, and service without controlling the table",
    7: "introspection and study — analysis, solitude, and counsel earned in the cave",
    8: "power and ambition — material command when accounts and conscience agree",
    9: "compassion and completion — release, mercy, and endings that teach the room",
    11: "intuition and inspiration — voltage that must land as product, not prophecy",
    22: "master builder — practical idealism poured in phases, not fantasy pace",
    33: "christic labor — teaching love with fees, limits, and a schedule",
}

FINAL_WORLD_EXAMPLE: dict[int, str] = {
    1: "like the person who opens the meeting with a decision instead of a fifth round of opinions",
    2: "like the friend both sides call when the argument needs a fair referee, not a referee who disappears",
    3: "like the creator who ships one finished piece while others perform three empty intros",
    4: "like the contractor with the same crew, hour, and checklist every Tuesday — trust is repetition",
    5: "like someone who says why they are leaving before they book the ticket",
    6: "like the host who fixes the kitchen schedule without lecturing the guests",
    7: "like the coworker who will not quote the answer until the brief has been read alone",
    8: "like the manager who audits the books before signing the bonus",
    9: "like the mentor who writes the exit letter, hands off the files, and actually walks out",
    11: "like the inventor who builds the prototype before pitching the vision",
    22: "like the builder who pours one foundation this quarter instead of selling the whole skyline",
    33: "like the teacher who sets office hours and a fee — help with a spine",
}

_COMPOUND_WORLD_EXAMPLE: dict[int, str] = {
    10: "like promoting to director before the team has seen you run one hard quarter alone",
    12: "like making art only after you gave up the safer path that paid the rent",
    13: "like renaming the company after you outgrew the first logo — same spine, new chapter",
    17: "like rebuilding client trust from delivery logs, not from a rebrand deck",
    18: "like grieving the job loss on Sunday and telling the truth on Tuesday, not performing fine on Monday",
    19: "like expecting the award to certify skill — burnout when applause replaces craft",
    21: "like speaking for two departments in one email and forgetting which side you lead",
    27: "like closing the client file fairly, documenting it, and leaving when the room wants rescue theater",
    28: "like co-founding before you take the solo CEO title the contract never supported",
    30: "like running four social channels when one essay is still in the drawer",
    36: "like needing witnesses at the retirement party because private finish alone feels like failure",
}

_TOTAL_ROLE_EXAMPLE: dict[str, str] = {
    "expression": "how the room titles you before it has seen the private draft",
    "soul_urge": "what you hunger for when the calendar is empty and no one is watching",
    "personality": "the ease people read in the first five minutes — charm before proof",
    "birthday_number": "the monthly rhythm that repeats on your birth day — upkeep, not mood",
}


def extract_card_arc(citations: list[str]) -> str:
    """Card arc from registry citations — never returns the word 'tarot' (verifier)."""
    for cite in citations or []:
        raw = plain_flesh(cite)
        if "tarot" not in raw.lower():
            continue
        arc = re.sub(r"(?i)tarot\s*", "", raw)
        arc = re.sub(r"(?i)look up:.*", "", arc)
        arc = arc.split("—")[0].split("–")[0].strip(" .")
        if arc and len(arc) > 8:
            return arc[:120].rstrip(".,;")
    return ""


def _ally_scheduling_brief(final_gate: int) -> str:
    friends = PATH_FRIEND_NUMBERS.get(final_gate, [])
    enemies = PATH_ENEMY_NUMBERS.get(final_gate, [])
    f_str = ", ".join(str(n) for n in friends) or "—"
    e_str = ", ".join(str(n) for n in enemies) or "—"
    return (
        f"Daily imprint: stack care and contracts on friendly-field days ({f_str}); "
        f"enemy-field gates ({e_str}) cost twice — finish your part, document, step light."
    )


def _relation_flow(user_gate: int, other_gate: int) -> str:
    rel = numerology_relation(user_gate, other_gate, context="path")
    if rel == "friend":
        return "this gate compounds your birth walk — schedule the yes here"
    if rel == "enemy":
        return "this gate drags your birth walk — proof before you sign, or step out clean"
    return "neutral field — your habit sets the tone more than the number"


def build_compound_insight_layer(c: int, f: int, lib: dict[str, Any] | None = None) -> str:
    if lib is None:
        lib = get_compound_entry(c, f, f"{c}/{f}" if c != f else str(c))
    parts: list[str] = []

    arc = extract_card_arc(lib.get("citations") or [])
    if arc:
        parts.append(f"Card arc: {arc}.")

    if c != f:
        lived = _COMPOUND_WORLD_EXAMPLE.get(c)
        if not lived:
            flesh = plain_flesh(lib.get("flesh", "")).split(".")[0].strip()
            if flesh and len(flesh) > 20:
                lived = f"like {flesh[0].lower() + flesh[1:]}"
        if lived:
            parts.append(f"In life {lived}.")

    essence = FINAL_ESSENCE.get(f, "")
    example = FINAL_WORLD_EXAMPLE.get(f, "")
    if essence:
        parts.append(f"Final {f} — {essence}.")
    if example:
        parts.append(f"Where it lands {example}.")

    parts.append(_ally_scheduling_brief(f))
    return " ".join(parts)


def build_total_insight(
    key: str,
    total_row: dict[str, Any],
    lp: dict[str, Any],
) -> tuple[str, str]:
    """Return (advice, path) — brief lived insight + ally flow for chart totals."""
    tc = total_row.get("compound") or 0
    tv = total_row.get("value") or 0
    lf = lp.get("value") or 0
    role = _TOTAL_ROLE_EXAMPLE.get(key, "this name-field")
    rel_line = _relation_flow(lf, tv)

    lib_entry: dict[str, Any] = {}
    if tc and tv:
        lib_entry = get_compound_entry(tc, tv, total_row.get("display", f"{tc}/{tv}"))

    arc = extract_card_arc(lib_entry.get("citations") or []) if lib_entry else ""
    arc_bit = f"Card arc: {arc}. " if arc else ""

    compound_lived = _COMPOUND_WORLD_EXAMPLE.get(tc, "")
    compound_bit = f"In life {compound_lived}. " if compound_lived and tc != tv else ""

    essence = FINAL_ESSENCE.get(tv, "")
    example = FINAL_WORLD_EXAMPLE.get(tv, "")
    meaning = f"{essence.rstrip('.')}. " if essence else ""
    example_bit = f"Like {example.lstrip('like ')}. " if example else ""

    advice = (
        f"{role.capitalize()} — {meaning}"
        f"{arc_bit}"
        f"Measure this total against your birth walk: {rel_line}."
    ).strip()

    path = (
        f"{compound_bit}"
        f"{meaning}"
        f"{example_bit}"
        f"Use your birth walk here: {rel_line}. "
        f"{_ally_scheduling_brief(lf)}"
    ).strip()

    words = path.split()
    if len(words) > 55:
        path = " ".join(words[:55]) + "."
    return advice, path