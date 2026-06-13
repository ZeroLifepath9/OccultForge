"""
Western forge lens — outer planets, houses, transits, and timing rhythm.
Battle-tested brother voice; no raw degrees or chart recitation in output.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

import swisseph as swe

from app.calculators.numerology import personal_day, personal_month, personal_year
from app.services.interpretations.matrix_decoder_voice import format_matrix_reading

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_ELEMENT = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

HOUSE_LIFE = {
    1: "identity and how you enter the room",
    2: "money, voice, and what you claim as yours",
    3: "messages, courage, and your local lane",
    4: "home, roots, and private nervous system",
    5: "creativity, risk, romance, and what you birth",
    6: "daily work, health, and service contracts",
    7: "partners, rivals, and fairness in bond",
    8: "shared money, debt, power, and deep change",
    9: "belief, teachers, and the long road",
    10: "career, reputation, and legacy on the record",
    11: "community, allies, and networks you build",
    12: "rest, dreams, exile, and what you dissolve",
}

SIGN_EDGE = {
    "Aries": "fast, blunt, first-through-the-door",
    "Taurus": "slow, sensual, built to hold",
    "Gemini": "wired, restless, many doors open",
    "Cancer": "protective, tidal, memory-heavy",
    "Leo": "visible, proud, heat-seeking",
    "Virgo": "precise, service-minded, critical eye",
    "Libra": "relational, aesthetic, balance-obsessed",
    "Scorpio": "deep, private, all-or-nothing",
    "Sagittarius": "wide, restless, truth-hungry",
    "Capricorn": "long-game, structural, reputation-first",
    "Aquarius": "future-facing, odd angle, collective pull",
    "Pisces": "porous, dreamy, mercy and fog",
}

PLANET_CORE = {
    "Pluto": "power resets — what must die so the real you can rebirth",
    "Venus": "love, money, magnetism, and what you attract or price wrong",
    "Uranus": "breaks, innovation, and where normal cannot hold anymore",
    "Neptune": "dreams, fog, glamour, and spiritual dissolve",
}

_DASHA_SEASON = {
    "Sun": "visibility and name are the headline",
    "Moon": "belonging and body finance the week",
    "Mars": "fight, cut, and honest conflict set pace",
    "Mercury": "messages, deals, and mental wiring dominate",
    "Jupiter": "expansion and measured risk have tailwind",
    "Venus": "bonds, beauty, and money want negotiation",
    "Saturn": "backbone, contracts, and limits rule",
    "Rahu": "hunger, disruption, and foreign edges activate",
    "Ketu": "release, stripping noise, spiritual subtraction",
}


def _who(imprint: dict[str, Any]) -> str:
    birth = imprint.get("birth") or {}
    alias = (birth.get("commonly_known_as") or "").strip()
    return alias or birth.get("name") or birth.get("display_name") or "Seeker"


def _spoken_birth(facts: dict[str, Any]) -> str:
    raw = (facts.get("birth") or {}).get("datetime_local") or ""
    raw = raw.replace("Z", "")
    if not raw:
        return "your sealed birth moment"
    try:
        dt = datetime.fromisoformat(raw)
        hour = dt.strftime("%I").lstrip("0") or "12"
        minute = dt.strftime("%M")
        ampm = dt.strftime("%p")
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}, {hour}:{minute} {ampm}"
    except ValueError:
        return raw[:16].replace("T", " ")


def _birth_place(facts: dict[str, Any]) -> str:
    return (facts.get("birth") or {}).get("place") or ""


def _whole_sign_house(asc: str, planet_sign: str) -> int:
    if asc not in SIGNS or planet_sign not in SIGNS:
        return 1
    return (SIGNS.index(planet_sign) - SIGNS.index(asc)) % 12 + 1


def _planet_slots(imprint: dict[str, Any]) -> dict[str, dict[str, Any]]:
    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    planets = imprint["western"]["planets"]
    out: dict[str, dict[str, Any]] = {}
    for name in ("Pluto", "Venus", "Uranus", "Neptune"):
        row = planets.get(name) or {}
        sign = row.get("sign", "")
        house = _whole_sign_house(asc, sign) if sign else 0
        out[name] = {
            "sign": sign,
            "house": house,
            "life": HOUSE_LIFE.get(house, "life themes"),
            "edge": SIGN_EDGE.get(sign, "distinct"),
        }
    return out


def _distill_planet(name: str, slot: dict[str, Any]) -> str:
    core = PLANET_CORE[name]
    life = slot["life"]
    edge = slot["edge"]
    if name == "Pluto":
        return (
            f"Pluto — {core}. For you this hits {life} with a {edge} undertow. "
            f"Transformation is not optional there; control games rot the mission."
        )
    if name == "Venus":
        return (
            f"Venus — {core}. Yours runs through {life} with a {edge} flavor. "
            f"Relationships and money rhyme here — cheap charm without substance drains sovereignty."
        )
    if name == "Uranus":
        return (
            f"Uranus — {core}. It wakes up {life} with a {edge} jolt. "
            f"Sudden exits and sudden openings both belong to this lane — rigidity snaps."
        )
    return (
        f"Neptune — {core}. It softens {life} with a {edge} haze. "
        f"Dreams inspire here; fog and addiction pose as destiny if you skip proof."
    )


def _outer_rhythm_big_picture(slots: dict[str, dict[str, Any]], facts: dict[str, Any]) -> str:
    pluto_life = slots["Pluto"]["life"]
    venus_life = slots["Venus"]["life"]
    ura_life = slots["Uranus"]["life"]
    nep_life = slots["Neptune"]["life"]
    sun = facts.get("sun_sign", "")
    asc = facts.get("ascendant", {}).get("western_sign", "")
    return (
        f"Your deep wiring runs on four outer drums. Power resets pull at {pluto_life}. "
        f"Love and money breathe through {venus_life}. Breakthroughs and shocks hit {ura_life}. "
        f"Dreams and dissolve wash {nep_life}. "
        f"That quartet colors how your {sun} will and {asc} door move through Western, Vedic, and Hermetic timing — "
        f"one pulse, not four separate scripts."
    )


def _outer_action_steps(facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    dm = facts["day_master"]["element"]
    h7 = facts["seal_house_7"]["sign"]
    lp = facts["life_path"]["display"]
    brick = {
        "Earth": "Land one money or meal-prep brick before the next pitch.",
        "Metal": "Write one boundary or contract line in plain language today.",
        "Fire": "Ship one proof-backed move before you argue vision.",
        "Water": "Take one quiet research hour before the group chat decides for you.",
        "Wood": "Prune one dead branch so the living project gets oxygen.",
    }.get(dm, "Finish one concrete task before the next big swing.")
    return [
        brick,
        f"Stack one action on life path {lp} — finish line work, not mask work.",
        f"Name one fairness line in partnership tone ({h7} field) before bodies negotiate.",
        "Track power, love, shock, and fog as four separate weather systems — keep ledgers separate.",
        "Build community and legacy in public steps — one visible brick per week.",
        "Protect recovery like payroll — outer-planet seasons bill the body before the spreadsheet.",
    ]


def _outer_watch_outs(slots: dict[str, dict[str, Any]]) -> list[str]:
    return [
        "Skip signing, merging, or rebranding in Neptune fog without a paper trail.",
        "Uranus adrenaline is not a finished mission — pace the forge stroke.",
        f"Pluto power games in {slots['Pluto']['life']} will eat your name on the record if you perform control.",
        f"Venus charm in {slots['Venus']['life']} without math drains sovereignty fast.",
    ]


def _transit_outer_signs(ref: date) -> dict[str, str]:
    jd = swe.julday(ref.year, ref.month, ref.day, 12.0)
    flags = swe.FLG_SWIEPH
    out: dict[str, str] = {}
    for name, pid in (("Pluto", swe.PLUTO), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE)):
        xx, _ = swe.calc_ut(jd, pid, flags)
        out[name] = SIGNS[int(xx[0] // 30) % 12]
    return out


def _transit_pulse(natal: str, transit: str, planet: str) -> str:
    if natal == transit:
        return "same sign as your birth chart — old homework is loud again, deeper reps not a new test"
    ne, te = SIGN_ELEMENT.get(natal, ""), SIGN_ELEMENT.get(transit, "")
    if ne == te:
        return "sky weather matches your natal lane — easier to move without breaking your base"
    if {ne, te} <= {"Fire", "Air"} or {ne, te} <= {"Earth", "Water"}:
        return "pushes growth with friction — move, keep receipts"
    return "corrective pressure — narrow the field, skip heroics"


def _timing_pulse_line(planet: str, life: str, pulse: str) -> str:
    if planet == "Pluto":
        lead = "Power resets hit"
    elif planet == "Uranus":
        lead = "Breaks and shocks wake up"
    elif planet == "Neptune":
        lead = "Dreams and fog soften"
    else:
        lead = "Love and money breathe through"
    return f"{planet} — {lead} {life}. Right now: {pulse}."


def _cycle_pulse_line(label: str, display: str, plain: str) -> str:
    return f"{label} {display} — {plain}"


_PERSONAL_YEAR_PLAIN = {
    1: "start the engine, name the direction, skip waiting for permission",
    2: "patience and partnership — slow bonds beat loud launches",
    3: "voice, visibility, creative output — ship the story",
    4: "brick work, schedules, foundations — boring wins",
    5: "movement, risk, novelty — finish loops before you chase the next door",
    6: "home, duty, care contracts — fairness is the price of peace",
    7: "inward finish, research, quiet power — skip noisy rebrands",
    8: "money, authority, harvest — invoice what you built",
    9: "release, closure, legacy handoff — cut what already died",
    11: "high-wire calling — one mission, not twelve side quests",
    22: "big-build season — structure the vision or the vision owns you",
    33: "service and teaching — lead with mercy, keep boundaries",
}

_PERSONAL_MONTH_PLAIN = {
    1: "this month wants a fresh push — pick one lane and move",
    2: "this month wants patience — negotiate, listen, pair up",
    3: "this month wants expression — talk, publish, perform with proof",
    4: "this month wants structure — calendars, budgets, brick by brick",
    5: "this month wants change — travel, pivot, test, but close open tabs first",
    6: "this month wants duty — family, home, fair contracts",
    7: "this month wants quiet depth — research beats hype",
    8: "this month wants harvest — money, power, receipts",
    9: "this month wants endings — clear the dead weight",
}

_PERSONAL_DAY_PLAIN = {
    1: "today is a starter day — lead one move, skip committee votes",
    2: "today is a pair day — listen before you fix",
    3: "today is a voice day — say it, write it, show it",
    4: "today is a work day — one task list, one finish line",
    5: "today is a shift day — movement yes, chaos no",
    6: "today is a care day — home, health, fair give-and-take",
    7: "today is a quiet day — research, rest, inner audit",
    8: "today is a power day — money talk, authority move, keep it clean",
    9: "today is a close day — finish, forgive, release",
}

_SKY_MONTH_PLAIN = {
    "Wood": "growth pressure in the room — plant what fits, prune what doesn't",
    "Fire": "heat in the room — ship while honest, skip performative brightness",
    "Earth": "stability pressure — slow builds beat flashy shortcuts",
    "Metal": "cut-and-hold pressure — standards protect the mission",
    "Water": "depth pressure — read the room, move once with proof",
}


def build_hellenistic_forge_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    who = _who(imprint)
    spoken = _spoken_birth(facts)
    place = _birth_place(facts)
    place_bit = f", {place}" if place else ""
    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    sun = facts.get("sun_sign") or imprint["western"]["planets"]["Sun"]["sign"]
    slots = _planet_slots(imprint)

    direct = (
        f"{who}, born {spoken}{place_bit} — I'm reading your Western seal with no fluff. "
        f"{_outer_rhythm_big_picture(slots, facts)} "
        f"Your {asc} rising and {sun} Sun set the handshake and the plot; the outer four set the weather underneath."
    )
    decoded = " ".join(
        [
            _distill_planet("Pluto", slots["Pluto"]),
            _distill_planet("Venus", slots["Venus"]),
            _distill_planet("Uranus", slots["Uranus"]),
            _distill_planet("Neptune", slots["Neptune"]),
        ]
    )
    steps = _outer_action_steps(facts, imprint)
    avoids = _outer_watch_outs(slots)
    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:6], 1))
    avoid_lines = "\n".join(f"• {a}" for a in avoids[:4])
    action = f"Do this now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"
    return format_matrix_reading(direct, decoded, action)


def build_vedic_forge_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    who = _who(imprint)
    spoken = _spoken_birth(facts)
    place = _birth_place(facts)
    place_bit = f", {place}" if place else ""
    lagna = imprint["vedic"]["lagna"]["sign"]
    moon = facts.get("moon") or {}
    nak = moon.get("nakshatra", "")
    sid = moon.get("sidereal_sign", "")
    dasha = facts.get("mahadasha") or imprint["vedic"]["dasha"]["active_mahadasha"]
    lord = (dasha.get("lord") or "").strip()
    slots = _planet_slots(imprint)
    sun = facts.get("sun_sign", "")

    direct = (
        f"{who}, born {spoken}{place_bit} — body-truth first. "
        f"You carry {lagna} lagna; Moon {nak} ({sid}) is hunger under every bond. "
        f"{_DASHA_SEASON.get(lord, 'This dasha season sets the drum')}. "
        f"Western outer planets still hit the same meat suit: {_outer_rhythm_big_picture(slots, facts)} "
        f"Vedic timing and {sun} will must agree in the body, not only in theory."
    )
    decoded = " ".join(
        [
            _distill_planet("Pluto", slots["Pluto"]),
            _distill_planet("Venus", slots["Venus"]),
            _distill_planet("Uranus", slots["Uranus"]),
            _distill_planet("Neptune", slots["Neptune"]),
            f"Nakshatra {nak} adds appetite under the bond — feed that before you renegotiate terms.",
        ]
    )
    steps = _outer_action_steps(facts, imprint)
    steps.insert(0, "Honor lagna body-truth before performing for strangers.")
    avoids = _outer_watch_outs(slots)
    avoids.insert(0, "Overriding body signal with performance bills the flesh before the spreadsheet.")
    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:6], 1))
    avoid_lines = "\n".join(f"• {a}" for a in avoids[:4])
    action = f"Do this now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"
    return format_matrix_reading(direct, decoded, action)


def build_western_setting_reading(
    facts: dict[str, Any],
    imprint: dict[str, Any],
    *,
    reference: date | None = None,
) -> str:
    from app.services.interpretations.western_setting_lens import build_western_setting_reading as _natal_read

    return _natal_read(facts, imprint)