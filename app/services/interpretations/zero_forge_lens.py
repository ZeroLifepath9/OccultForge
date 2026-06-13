"""
Zero's Insight — unified natal occult blueprint across every sealed layer.
Zero voice: blunt mirror, birth imprint only, no school-by-school lists.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.matrix_decoder_voice import format_matrix_reading
from app.services.overview_lore import LIFE_PATH_TRIAL, LIFE_PATH_TRIUMPH, build_zero_verdict
from app.services.interpretations.zero_framework import ZERO_MATRIX_CLOSE, ZERO_SEAL_CLOSE

_ELEMENT_BLADE: dict[str, str] = {
    "Wood": "grow one trunk project or watch scatter eat your name",
    "Fire": "ship while the flame is honest or perform brightness with nothing behind it",
    "Earth": "lay brick-by-brick foundations or rush a facade that collapses under rent",
    "Metal": "cut and hold the line or let perfection cage the mission",
    "Water": "research then move once or drift on mood instead of rhythm",
}

_ELEMENT_DECODE: dict[str, str] = {
    "Wood": "growth that demands pruning — burst, stretch, cut what does not feed the trunk",
    "Fire": "visibility that spends fast — courage without receipts burns the forge",
    "Earth": "structure as tuition — slow weight that compounds when you stop performing finished",
    "Metal": "refinement as weapon — standards that protect or punish depending on who holds them",
    "Water": "depth as leverage — intuition that wins when it stops negotiating with fog",
}


def _birth_anchor(facts: dict[str, Any], name: str) -> str:
    birth = facts.get("birth") or {}
    raw = (birth.get("datetime_local") or "").replace("Z", "")
    dt = raw[:16].replace("T", " ") if raw else "your sealed birth moment"
    place = (birth.get("place") or "").strip()
    tail = f" at {place}" if place else ""
    return (
        f"{name}, you are sealed {dt}{tail} — one imprint, one blueprint. "
        f"I am reading the code you walked in with, not today's weather."
    )


def _direct_mirror(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    el = dm["element"]
    yy = dm.get("yin_yang") or ""
    lp = facts["life_path"]["display"]
    sun = facts.get("sun_sign") or ""
    asc = (facts.get("ascendant") or {}).get("western_sign") or ""
    moon = (facts.get("moon") or {}).get("western_sign") or ""
    trial = LIFE_PATH_TRIAL.get(facts["life_path"]["value"], "the lesson that keeps billing you")

    handshake = f"{asc} rising" if asc else "your rising gate"
    core = _ELEMENT_BLADE.get(el, _ELEMENT_BLADE["Earth"])
    return (
        f"{yy} {el} spine — {core}. "
        f"Life path {lp} is the finish line they tried to hide behind noise; {trial}. "
        f"{sun} Sun is the plot you keep performing; {handshake} is how strangers tax you before they hear the story; "
        f"{moon} Moon is the private weather that finances or bankrupts every promise. "
        f"This is not a personality quiz — it is how your soul was coded into the meat suit."
    )


def _decoded_layers(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    el = dm["element"]
    lp = facts["life_path"]
    lp_val = lp["value"]
    triumph = LIFE_PATH_TRIUMPH.get(lp_val, "owning the pattern without costume")
    yz = facts.get("year_zodiac", {}).get("animal", "")
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    lagna = (facts.get("ascendant") or {}).get("vedic_lagna") or (facts.get("vedic_house_1") or {}).get("sign", "")
    nak = (facts.get("moon") or {}).get("nakshatra", "")
    h2 = (facts.get("vedic_house_2") or {}).get("sign", "")
    h7 = (facts.get("vedic_house_7") or facts.get("seal_house_7") or {}).get("sign", "")
    h10 = (facts.get("vedic_house_10") or {}).get("sign", "")
    verdict = build_zero_verdict(facts)
    warn = (verdict.get("warning") or "").split(".")[0].strip()

    parts = [_ELEMENT_DECODE.get(el, _ELEMENT_DECODE["Earth"])]

    if yz and day_an:
        if yz != day_an:
            parts.append(
                f"Family cast ({yz}) and daily self ({day_an}) run on different clocks — "
                f"charm from one gate, grind from another; peaks when neither runs your mouth for you."
            )
        else:
            parts.append(
                f"Family cast and daily self both echo {day_an} — less translation loss, "
                f"more volume if you hide from your own spine."
            )

    if expr.get("value") and soul.get("value"):
        if expr["value"] != soul["value"]:
            parts.append(
                f"Public name ({expr.get('display', expr['value'])}) and private vow "
                f"({soul.get('display', soul['value'])}) pull on different ropes — "
                f"the brand eats the soul when the soul does not steer the brand."
            )
        elif expr["value"] == lp_val:
            parts.append(
                "What you show and what you owe the path line up — less costume fatigue, cleaner momentum."
            )

    if lagna:
        parts.append(
            f"Body-truth gate {lagna} is how the world reads your stamina before your resume — "
            f"perform against that gate and the flesh pays first."
        )
    if nak:
        parts.append(f"Mood constellation {nak} sets the appetite under conflict — ignore it and you sign treaties while bleeding.")

    if h2 or h7 or h10:
        ledger = []
        if h2:
            ledger.append(f"income rhythm lives in {h2}")
        if h7:
            ledger.append(f"bond contracts in {h7}")
        if h10:
            ledger.append(f"public name in {h10}")
        parts.append(f"Keep {'; '.join(ledger)} in separate ledgers — merged books are how legacy gets stolen.")

    parts.append(
        f"Path {lp['display']} rebate when you stop fighting the current: {triumph}. "
        f"Perception, timing, number-field, and element spine describe one pulse — not separate gods arguing."
    )
    if warn:
        parts.append(f"Karmic knot to respect: {warn}.")

    return " ".join(parts)


def _actionable_blades(facts: dict[str, Any]) -> tuple[list[str], list[str]]:
    dm = facts["day_master"]
    el = dm["element"]
    h2 = (facts.get("vedic_house_2") or {}).get("sign", "")
    h7 = (facts.get("vedic_house_7") or facts.get("seal_house_7") or {}).get("sign", "")
    lp = facts["life_path"]["display"]
    verdict = build_zero_verdict(facts)
    expr = facts.get("expression") or {}
    lp_val = facts["life_path"]["value"]

    brick = {
        "Earth": "Lay one money or meal-prep brick before you pitch the next idea.",
        "Metal": "Write one boundary or contract line before you argue about loyalty.",
        "Fire": "Ship one proof-backed move before you perform the vision for strangers.",
        "Water": "Take one quiet research hour before you answer the group chat.",
        "Wood": "Cut one branch that does not feed the trunk — measure growth, not noise.",
    }.get(el, "Finish one concrete task before you debate the next big swing.")

    blades = [
        brick,
        f"Pull one lever on life path {lp} work — the finish line, not the crowd's stale argument.",
        f"Keep income ({h2}), bond ({h7}), and reputation in separate ledgers this week.",
        "Name one fairness line before the next partner or family talk — vague fairness ages badly.",
        "Protect sleep and recovery like payroll — the imprint does not pay heroic burnout.",
        "Write the last valley's lesson in one sentence — refuse to pay tuition twice.",
    ]

    risks = [
        "Skip signing, merging, or rebranding while hungry, horny, or humiliated — that doorway repeats the loop.",
        f"Earning against your {el.lower()} spine to impress a room that will not pay your bills drains sovereignty.",
    ]
    if expr.get("value") and expr["value"] != lp_val:
        risks.append("Letting the public mask spend what the path has not earned taxes the mission.")
    risks.append((verdict.get("warning") or "Calling drift fate repeats the loop.").split(".")[0] + ".")
    risks.append("Fighting the whole chart in one afternoon fails — narrow the field, win the day, rest.")

    return blades[:6], risks[:4]


def build_zero_forge_lens_reading(facts: dict[str, Any], name: str) -> str:
    """Synthesize every sealed layer into one Zero natal transmission."""
    direct = f"{_birth_anchor(facts, name)} {_direct_mirror(facts)}"
    decoded = _decoded_layers(facts)

    blades, risks = _actionable_blades(facts)
    blade_lines = "\n".join(f"{i}. {b}" for i, b in enumerate(blades, 1))
    risk_lines = "\n".join(f"• {r}" for r in risks)
    action = (
        f"Actionable Blades:\n{blade_lines}\n\n"
        f"Watch out:\n{risk_lines}\n\n"
        f"{ZERO_SEAL_CLOSE} {ZERO_MATRIX_CLOSE}"
    )
    return format_matrix_reading(direct, decoded, action)