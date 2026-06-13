"""Numerology flowing insight — compound-first, life path drives how."""

from __future__ import annotations

from typing import Any

from app.services.compound_registry import PATH_FINAL_DIRECTORY
from app.services.interpretations.flow_voice import FlowReading, weave_flow
from app.services.interpretations.manifestation_voice import manifest_compound, plain_flesh
from app.services.numerology_depth import PATH_ALIGNED, PATH_MISALIGNED
from app.services.overview_lore import COMPOUND_PRESSURE, LIFE_PATH_TRIAL

_FRAMING_SPLIT = [
    (
        "You need to know what energy you walk—not every {v} shares your road; "
        "compound {c} is why generic advice names the finish but skips the story of how to get there."
    ),
    (
        "Generic numerology tells you where the path ends; it rarely tells you how to walk it. "
        "Two people with life path {v} can live different stories when compound {c} is not the same."
    ),
    (
        "The hidden secret: same final number, different road. "
        "Compound {c} is the energy you walk; without it, advice names the destination and skips how to get there."
    ),
]

_FRAMING_SINGLE = [
    (
        "You need to know what energy you walk—a single gate {c}, body and vow aligned—"
        "but not every {v} shares your road; generic advice names the destination without your story of how to get there."
    ),
    (
        "Generic numerology tells you the finish line; it rarely tells you the pace. "
        "Even with one gate {c}, two life path {v} charts can walk different stories elsewhere in the field."
    ),
]

_TOTAL_ROLE = {
    "expression": "what the world titles you",
    "soul_urge": "private appetite after the door shuts",
    "personality": "trust in the first five minutes",
    "birthday_number": "monthly rhythm in the body",
}


def _name(imprint: dict[str, Any]) -> str:
    birth = imprint.get("birth") or {}
    alias = (birth.get("commonly_known_as") or "").strip()
    return alias or birth.get("name") or birth.get("display_name") or "you"


def _final_plain(value: int) -> str:
    row = PATH_FINAL_DIRECTORY.get(value, {})
    return plain_flesh(row.get("plain", row.get("integration", f"life path {value} rhythm")))


def _final_integration(value: int) -> str:
    row = PATH_FINAL_DIRECTORY.get(value, {})
    return plain_flesh(row.get("integration", PATH_ALIGNED.get(value, f"walk life path {value} in order")))


def _compound_intro(c: int, f: int, disp: str) -> str:
    pressure = plain_flesh(COMPOUND_PRESSURE.get(c, ""))
    if c == f:
        note = pressure or "one field, no split between flesh and vow"
        return f"life path {disp} is a single gate—body and vow share {c}; {note}"
    flesh = plain_flesh(manifest_compound(c, f, disp))
    lead = (
        f"compound {c} is the unreduced birth-date field, the energy you walk before the vow settles to {f}"
    )
    tail = pressure or flesh
    return f"{lead}; {tail}"


def _framing_line(c: int, f: int) -> str:
    pool = _FRAMING_SINGLE if c == f else _FRAMING_SPLIT
    return pool[(c + f) % len(pool)].format(c=c, v=f)


def _secondary_weave(
    facts: dict[str, Any], lp: dict[str, Any]
) -> tuple[list[str], str | None]:
    """Return up to two p2 clauses and an optional p3 leak from secondary totals."""
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    pers = facts.get("personality") or {}
    clauses: list[str] = []
    leak: str | None = None

    ev = expr.get("value")
    sv = soul.get("value")
    pv = pers.get("value")
    lv = lp.get("value")

    if ev and sv and ev != sv:
        expr_mean = _final_plain(ev)
        soul_mean = _final_plain(sv)
        clauses.append(
            f"Expression {expr.get('display', '')} is {_TOTAL_ROLE['expression']}—{expr_mean}"
        )
        clauses.append(
            f"soul urge {soul.get('display', '')} is {_TOTAL_ROLE['soul_urge']}—{soul_mean}"
        )
        leak = (
            f"booking the {expr.get('display', '')} calendar while {soul.get('display', '')} appetite simmers"
        )
    elif ev == lv and sv and sv != lv:
        clauses.append(
            f"Soul urge {soul.get('display', '')} is {_TOTAL_ROLE['soul_urge']}—{_final_plain(sv)}"
        )
    elif ev and sv and ev == sv and pv and pv != ev and pv != lv:
        clauses.append(
            f"Personality {pers.get('display', '')} is {_TOTAL_ROLE['personality']}—{_final_plain(pv)}"
        )

    if len(clauses) > 2:
        clauses = clauses[:2]

    return clauses, leak


def build_numerology_flow(facts: dict[str, Any], imprint: dict[str, Any]) -> FlowReading:
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    who = _name(imprint)
    bd = facts.get("birth_day", "—")
    integration = _final_integration(f).rstrip(".")
    aligned = plain_flesh(PATH_ALIGNED.get(f, integration)).rstrip(".")
    trial = plain_flesh(LIFE_PATH_TRIAL.get(f, PATH_MISALIGNED.get(f, "order drift")))

    intro = _compound_intro(c, f, disp)
    framing = _framing_line(c, f)
    p1 = f"{who}, you are life path {disp} — {intro}. {framing}"

    pace = ""
    if c != f:
        pace = (
            f" on a {c}-then-{f} schedule—body earns what compound {c} pleads before the {f} vow collects"
        )

    secondaries, secondary_leak = _secondary_weave(facts, lp)
    method = f"your {disp} method is still finish-first, voice second"
    if secondaries:
        method_tail = f"; {secondaries[0]}, but {method}"
        if len(secondaries) > 1:
            method_tail = f"; {secondaries[0]}, and {secondaries[1]}, but {method}"
    else:
        method_tail = f"; {method}"

    p2_core = (
        f"You're strongest when you walk life path {f} in order{pace}—{integration}. "
        f"{aligned.capitalize()}{method_tail}. "
        f"On day {bd} each month, run one maintenance pass before the next big yes."
    )

    mindful = f"Stay mindful when {trial}—that is life path {f} drift"
    if c != f and secondaries:
        expr = facts.get("expression") or {}
        ev = expr.get("value")
        if ev and ev != f:
            mindful = (
                f"Stay mindful when you perform the {ev} handshake while compound {c} still pleads unfinished"
                f"—that is order drift, not a bad number"
            )
    elif c != f:
        mindful = (
            f"Stay mindful when you spend or schedule like compound {c} landed while only final {f} is paid for"
            f"—that is order drift, not a bad number"
        )
    else:
        mindful = f"{mindful}, not fate"

    p2 = f"{p2_core} {mindful}."

    leaks: list[str] = []
    if secondary_leak:
        leaks.append(f"{secondary_leak} — Sunday signatures you call fate")
    if c != f:
        leaks.append(
            f"spending like compound {c} landed when only final {f} is paid for"
        )
    if not leaks:
        leaks.append(
            plain_flesh(PATH_MISALIGNED.get(f, f"marketing a {disp} finish the body has not earned"))
        )

    p3 = (
        f"What costs you: {leaks[0]}. "
        f"The leak is wrong order—mask or marketing before the life path {f} finish lands."
    )

    return FlowReading(body=weave_flow([p1, p2, p3]))