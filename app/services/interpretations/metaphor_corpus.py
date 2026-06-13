"""
Everyday picture scenes — chart-anchored, plain English, no occult allegory.
"""

from __future__ import annotations

from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.imprint_labels import combined_pillar_label


def picture_this(facts: dict[str, Any], tradition: str) -> str:
    builders = {
        "bazi": _bazi_picture,
        "numerology": _numerology_picture,
        "vedic": _vedic_picture,
        "hellenistic": _hellenistic_picture,
        "financial": _financial_picture,
        "wealth": _wealth_picture,
        "relationships": _relationships_picture,
        "combination": _combination_picture,
    }
    return builders.get(tradition, _combination_picture)(facts)


def friction_allegory(facts: dict[str, Any], tradition: str) -> str:
    builders = {
        "bazi": _bazi_friction,
        "numerology": _numerology_friction,
        "vedic": _vedic_friction,
        "hellenistic": _hellenistic_friction,
        "financial": _financial_friction,
        "wealth": _wealth_friction,
        "relationships": _relationships_friction,
        "combination": _combination_friction,
    }
    return builders.get(tradition, _combination_friction)(facts)


def _bazi_picture(facts: dict[str, Any]) -> str:
    yz = facts["year_zodiac"]
    day = facts.get("day_pillar") or facts["pillars"]["day"]
    dm = facts["day_master"]
    day_combined = combined_pillar_label(day) if day.get("stem") else f"{dm['yin_yang']} {dm['element']}"
    return (
        f"Imagine your childhood home had a certain mood — {yz.get('element', '')} {yz['animal']} year energy. "
        f"That is the room you walked into. Your daily self is {day_combined} with {dm['english']} {dm['element']} "
        f"and {day.get('branch_animal', '')} branch — the person who shows up at work, in love, and on a Tuesday. "
        f"The year is the house; the day pillar is who lives in it."
    )


def _numerology_picture(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    if lp["compound"] == lp["value"]:
        return (
            f"Your birth numbers read like one label on a moving box: {lp['display']}. "
            f"What you carry and the road you walk use the same name — public life and private life rhyme."
        )
    return (
        f"Your birth numbers read like a heavy box ({lp['compound']}) on a road marked {lp['value']}. "
        f"You feel the weight of the compound in your body; the final {lp['value']} is the exit you keep walking toward."
    )


def _vedic_picture(facts: dict[str, Any]) -> str:
    asc = facts["ascendant"]["vedic_lagna"] or facts["ascendant"]["western_sign"]
    moon = facts["moon"]
    nak = moon.get("nakshatra", "")
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    return (
        f"Your body walks into rooms as {asc} lagna — the physical pattern people eventually notice. "
        f"Your feelings eat at the {nak} table (Moon in {moon.get('sidereal_sign', '')}). "
        f"Right now life is in a {dasha} chapter — like a season of a long book you are already inside."
    )


def _hellenistic_picture(facts: dict[str, Any]) -> str:
    asc = facts["ascendant"]["western_sign"]
    sun = facts["sun_sign"]
    mc = facts.get("western_angles", {}).get("midheaven", {}).get("sign", "")
    return (
        f"At a party, people meet your {asc} rising first — the first impression. "
        f"Your {sun} Sun is what you keep pushing for once the small talk ends. "
        f"Midheaven in {mc or 'your chart'} is what gets written on your professional reputation later."
    )


def _financial_picture(facts: dict[str, Any]) -> str:
    wp = facts.get("western_planets") or {}
    jup = wp.get("Jupiter", {}).get("sign", "")
    sat = wp.get("Saturn", {}).get("sign", "")
    ven = wp.get("Venus", {}).get("sign", "")
    return (
        f"Jupiter in {jup} is the month the budget loosens and optimism feels smart. "
        f"Saturn in {sat} is the month the bills and deadlines get real. "
        f"Venus in {ven} prices what you enjoy — your personal boom-and-bust rhythm lives between those two."
    )


def _wealth_picture(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    bday = facts.get("birthday_number") or {}
    dm = facts["day_master"]
    h2 = facts["vedic_house_2"]["sign"]
    return (
        f"Your money story is three lanes: {dm['element']} day master is how you earn daily, "
        f"birth-day {bday.get('display', '—')} is the monthly tune-up, life path {lp['display']} is the destination, "
        f"and 2nd house {h2} is where income actually enters or stalls."
    )


def _relationships_picture(facts: dict[str, Any]) -> str:
    h7 = facts["vedic_house_7"]["sign"]
    h10 = facts["vedic_house_10"]["sign"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    soul = facts.get("soul_urge") or {}
    return (
        f"Love and contracts test in {h7} — fairness at the kitchen table. "
        f"Work relationships test in {h10} — mentors, rivals, and reputation. "
        f"Your day animal {day_an} is how you show up daily; soul urge {soul.get('display', '—')} "
        f"is what you need when the door closes."
    )


def _combination_picture(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    lp = facts["life_path"]
    yz = facts["year_zodiac"]
    sun = facts["sun_sign"]
    return (
        f"Picture one person at the kitchen table: {yz['animal']} year is the family mood you grew up in, "
        f"{sun} Sun is what you keep fighting for, {dm['yin_yang']} {dm['element']} day master is how you work, "
        f"and life path {lp['display']} is the kind of finish you keep circling back to. "
        f"Every chart box is a different angle on the same person."
    )


def _bazi_friction(facts: dict[str, Any]) -> str:
    yz = facts["year_zodiac"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    month_el = facts["pillars"]["month"].get("stem_element", "")
    if yz["animal"] == day_an:
        return (
            f"Year and day both run {day_an} — family cast and daily self agree. "
            f"The rub is pace: month {month_el} season can push faster than your {facts['day_master']['element']} "
            f"stem can sustain without rest."
        )
    return (
        f"At reunions you are still the {yz['animal']} story; on Tuesday you run as {day_an}. "
        f"Like being cast in the family play while living a different role at work — both true, "
        f"and the tired feeling is often two stories asking for two costumes at once."
    )


def _numerology_friction(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    parts = []
    if lp["compound"] != lp["value"]:
        parts.append(f"you feel compound {lp['compound']} in your body while walking final {lp['value']} on paper")
    if expr.get("value") and expr["value"] != lp["value"]:
        parts.append(f"public {expr.get('display')} markets a different current than birth {lp['display']}")
    if soul.get("value") and soul["value"] != lp["value"]:
        parts.append(f"private {soul.get('display')} wants what {lp['display']} has to earn slowly")
    if not parts:
        return (
            "Your numbers rhyme — the risk is drifting, not war. "
            "Like having one playlist for work and home; boredom replaces conflict."
        )
    return (
        "Your chart holds number tension: " + "; ".join(parts) + ". "
        "Like two roommates with one calendar — price, partner, and schedule need talking before resentment moves in."
    )


def _vedic_friction(facts: dict[str, Any]) -> str:
    asc = facts["ascendant"]["vedic_lagna"]
    trop = facts["ascendant"]["western_sign"]
    if asc and trop and asc != trop:
        return (
            f"Sidereal lagna {asc} is what your body runs on; tropical Ascendant {trop} is the first impression. "
            f"Like eating for the Instagram version of health while your body asks for something simpler — "
            f"the bill arrives as fatigue, not drama."
        )
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    h7 = facts["vedic_house_7"]["sign"]
    return (
        f"Mahadasha lord {dasha} colors this whole chapter — big moves feel expensive when they ignore that season. "
        f"If 7th house {h7} fairness and money values diverge, love and invoices share one fight."
    )


def _hellenistic_friction(facts: dict[str, Any]) -> str:
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    if sun == asc:
        return (
            f"Sun and Ascendant both in {sun} — will and first impression match. "
            f"Like being 'on' all the time: intensity is the gift and burnout is the price."
        )
    return (
        f"Sun in {sun} wants one plot; {asc} rising sells another at the door. "
        f"Like getting hired for charm and promoted for strategy — winning rooms you did not mean to keep."
    )


def _financial_friction(facts: dict[str, Any]) -> str:
    wp = facts.get("western_planets") or {}
    jup = wp.get("Jupiter", {}).get("sign", "")
    sat = wp.get("Saturn", {}).get("sign", "")
    nep = wp.get("Neptune", {}).get("sign", "")
    if jup == sat:
        return (
            f"Jupiter and Saturn share {jup} — expansion and caution wear the same coat. "
            f"Boom and austerity arrive as one weather pattern; tracking dates beats tracking mood."
        )
    return (
        f"Jupiter in {jup} says 'more'; Saturn in {sat} says 'show me the paperwork.' "
        f"Neptune in {nep} adds fog — like a deal that looks generous until the fine print week."
    )


def _wealth_friction(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    h2 = facts["vedic_house_2"]["sign"]
    lp = facts["life_path"]
    return (
        f"Earning as {dm['element']} while income runs on {h2} rhythm can feel like "
        f"speaking one language at work and another at the bank. "
        f"Life path {lp['display']} still wants completion — a paycheck alone can leave you hungry."
    )


def _relationships_friction(facts: dict[str, Any]) -> str:
    h7 = facts["vedic_house_7"]["sign"]
    h2 = facts["vedic_house_2"]["sign"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    return (
        f"When 7th house {h7} fairness fights 2nd house {h2} values, love and money share one argument. "
        f"Year cast {yz} explains first charm; day {day_an} explains month three — "
        f"like falling for the party version and living with the weekday version."
    )


def _combination_friction(facts: dict[str, Any]) -> str:
    expr = facts.get("expression") or {}
    lp = facts["life_path"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    bits = []
    if expr.get("value") and expr["value"] != lp["value"]:
        bits.append(f"public name {expr['display']} and birth path {lp['display']} pull different ways")
    if yz != day_an:
        bits.append(f"you are seen as {yz} in public but run {day_an} in private")
    if not bits:
        return "Your charts mostly rhyme — the risk is boredom and drift, not open war."
    return "When life gets messy: " + "; ".join(bits) + ". Like wearing shoes that fit in the store but pinch by evening."