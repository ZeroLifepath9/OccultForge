"""
Everyday scenario vignettes — chart-anchored, deterministic, example-driven.
"""

from __future__ import annotations

from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.imprint_labels import combined_pillar_label
from app.services.interpretations.manifestation_voice import manifest_animal, manifest_compound, manifest_pillar_element


def everyday_scenarios(facts: dict[str, Any], tradition: str) -> list[str]:
    builders = {
        "bazi": _bazi_everyday,
        "numerology": _numerology_everyday,
        "vedic": _vedic_everyday,
        "hellenistic": _hellenistic_everyday,
        "financial": _financial_everyday,
        "wealth": _wealth_everyday,
        "relationships": _relationships_everyday,
        "combination": _combination_everyday,
    }
    return builders.get(tradition, _combination_everyday)(facts)


def pillar_like_this(pillar_key: str, facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    pillar = imprint["bazi"]["pillars"][pillar_key]
    pe_animal = facts["pillars"][pillar_key].get("branch_animal", "")
    el = facts["pillars"][pillar_key].get("stem_element", "")
    combined = combined_pillar_label(pillar, year_style=(pillar_key == "year"))

    scenes = {
        "year": (
            f"At a family dinner, people still describe you the way {pe_animal} years are talked about — "
            f"the tone of the room you grew up in. Your chart's year pillar is {combined}; "
            f"that is the background you walk into, not the whole story of who you are Tuesday morning."
        ),
        "month": (
            f"In your career years, bosses and clients respond to your {el} month season — "
            f"like a workplace that rewards {manifest_pillar_element(el).split('—')[0].strip().lower()}. "
            f"Month pillar {combined} is the working weather you navigate as an adult."
        ),
        "day": (
            f"On a random Tuesday, you are your day pillar {combined}: "
            f"{manifest_pillar_element(el)} "
            f"Like someone who {manifest_animal(pe_animal).split('—')[0].strip().lower()} — "
            f"that is your real daily self, more than the zodiac year on your ID."
        ),
        "hour": (
            f"Late at night, when nobody is watching, the {pe_animal} hour side shows up — "
            f"private projects, recovery pace, and what you do after the performance ends. "
            f"Hour pillar {combined} is your off-stage rhythm."
        ),
    }
    return scenes.get(pillar_key, f"Your {pillar_key} pillar {combined} shows up in daily habits.")


def _bazi_everyday(facts: dict[str, Any]) -> list[str]:
    dm = facts["day_master"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    yz = facts["year_zodiac"]["animal"]
    return [
        (
            f"Like a coworker who finishes the slow job everyone else abandoned — "
            f"your {dm['element']} stem and {day_an} branch show up as steady output, not loud promises."
        ),
        (
            f"At a reunion, old friends still cast you as the {yz} type; "
            f"at work this week you ran as the {day_an} type. Both are real — the year is the room, the day is you in it."
        ),
        (
            f"You might notice energy returning after one finished task and one clean boundary — "
            f"that is {dm['yin_yang']} {dm['element']} day rhythm, not willpower theater."
        ),
    ]


def _numerology_everyday(facts: dict[str, Any]) -> list[str]:
    lp = facts["life_path"]
    glyph = get_compound_entry(lp["compound"], lp["value"], lp["display"])["glyph"]
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    bday = facts.get("birthday_number") or {}
    lines = [
        (
            f"Like someone whose calendar keeps circling back to the same kind of project — "
            f"life path {lp['display']} ({glyph}) is the pattern you keep finishing or avoiding."
        ),
    ]
    if expr.get("display") and expr["value"] != lp["value"]:
        lines.append(
            f"On LinkedIn you market {expr['display']}; on Sunday night your body wants {lp['display']} work — "
            f"both numbers are on your chart, and the gap shows up in price, partner, and schedule."
        )
    if soul.get("display") and soul.get("value") != lp["value"]:
        lines.append(
            f"In private you crave what {soul['display']} describes; in public you carry {lp['display']} — "
            f"like enjoying quiet research while your job title says sales."
        )
    if bday.get("display"):
        lines.append(
            f"Every month on day {facts.get('birth_day', '—')}, the same kind of reset returns — "
            f"birth-day {bday['display']} is a maintenance rhythm, like paying a bill you actually benefit from."
        )
    return lines


def _vedic_everyday(facts: dict[str, Any]) -> list[str]:
    lagna = facts["ascendant"].get("vedic_lagna") or facts["ascendant"]["western_sign"]
    moon = facts["moon"]
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    h2 = facts["vedic_house_2"]["sign"]
    h7 = facts["vedic_house_7"]["sign"]
    return [
        (
            f"Like someone whose body complains when sleep and meals slip — "
            f"lagna {lagna} is the physical pattern you cannot fake for long."
        ),
        (
            f"Your Moon in {moon.get('nakshatra', '')} shows up as what you need after conflict — "
            f"not the story you post, the recovery you actually require."
        ),
        (
            f"This stretch of life runs under {dasha} mahadasha — "
            f"like a chapter title where major moves either match that season or feel oddly expensive."
        ),
        (
            f"Money habits echo {h2}; partnership fights echo {h7} — "
            f"same person, two rooms in the house."
        ),
    ]


def _hellenistic_everyday(facts: dict[str, Any]) -> list[str]:
    asc = facts["ascendant"]["western_sign"]
    sun = facts["sun_sign"]
    mc = (facts.get("western_angles") or {}).get("midheaven", {}).get("sign", "")
    return [
        (
            f"At a first meeting, people meet your {asc} rising first — "
            f"like the handshake before the real conversation starts."
        ),
        (
            f"What you push for when tired is your {sun} Sun — "
            f"the goal you keep returning to even when the mask is off."
        ),
        (
            f"Reputation works like midheaven in {mc or 'your chart'} — "
            f"what people say about you after the project ends, not during the performance."
        ),
    ]


def _financial_everyday(facts: dict[str, Any]) -> list[str]:
    wp = facts.get("western_planets") or {}
    jup = wp.get("Jupiter", {}).get("sign", "")
    sat = wp.get("Saturn", {}).get("sign", "")
    return [
        (
            f"Like a household that spends freely when Jupiter in {jup} is loud — "
            f"then gets serious about spreadsheets when Saturn in {sat} shows up."
        ),
        (
            f"You might notice boom-and-bust is not random mood — "
            f"it is the dialogue between expansion ({jup}) and patience ({sat}) on your birth chart."
        ),
        (
            f"For example, a 'great opportunity' that skips the paperwork "
            f"often lands during Jupiter weather and bills you during Saturn weather."
        ),
    ]


def _wealth_everyday(facts: dict[str, Any]) -> list[str]:
    dm = facts["day_master"]
    h2 = facts["vedic_house_2"]["sign"]
    lp = facts["life_path"]
    bday = facts.get("birthday_number") or {}
    glyph = get_compound_entry(lp["compound"], lp["value"], lp["display"])["glyph"]
    return [
        (
            f"Payday feels right when {dm['element']} craft meets {h2} values — "
            f"like getting paid for work that actually fits how you operate daily."
        ),
        (
            f"Birth-day {bday.get('display', '—')} on day {facts.get('birth_day', '—')} each month "
            f"is like a recurring tune-up that funds life path {lp['display']} ({glyph})."
        ),
        (
            f"Imagine a job that pays well but never lets you finish anything — "
            f"your chart still starves on that, even with a big deposit."
        ),
    ]


def _relationships_everyday(facts: dict[str, Any]) -> list[str]:
    h7 = facts["vedic_house_7"]["sign"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    soul = facts.get("soul_urge") or {}
    return [
        (
            f"Partnership friction often sounds like {h7} fairness — "
            f"who does the dishes, who signs the lease, who gets the credit."
        ),
        (
            f"You might attract {yz} charm at the door and need {day_an} rhythm by month three — "
            f"like dating the life of the party and living with the early riser."
        ),
        (
            f"In private, soul urge {soul.get('display', '—')} is what you need from the table — "
            f"not the version of you that small talk expects."
        ),
    ]


def _combination_everyday(facts: dict[str, Any]) -> list[str]:
    dm = facts["day_master"]
    lp = facts["life_path"]
    return [
        (
            f"Like one person carrying a work style ({dm['element']} day), a birth pattern ({lp['display']}), "
            f"and a public story at the same time — the charts are lenses on the same life."
        ),
    ]