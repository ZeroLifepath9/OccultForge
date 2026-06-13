"""
Deterministic episode casts — anime/TV archetypes keyed to sealed chart signatures.
"""

from __future__ import annotations

from typing import Any

from app.services.imprint_labels import combined_pillar_label


def episode_scene(tradition: str, facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    builders = {
        "bazi": _bazi_scene,
        "numerology": _numerology_scene,
        "vedic": _vedic_scene,
        "hellenistic": _hellenistic_scene,
        "financial": _financial_scene,
        "wealth": _wealth_scene,
        "relationships": _relationships_scene,
    }
    return builders.get(tradition, _wealth_scene)(facts, imprint)


def _bazi_scene(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    dm = facts["day_master"]
    yz = facts["year_zodiac"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    day_combined = ""
    if imprint:
        day_combined = combined_pillar_label(imprint["bazi"]["pillars"]["day"])
    casts = {
        ("Metal", "Rooster"): "the audit-obsessed fixer from a slow-burn crime drama — sharp eyes, faster pen",
        ("Metal", "Ox"): "the stonemason character who outlasts everyone — quiet, immovable, done when it's done",
        ("Wood", "Tiger"): "the hot-headed protagonist who charges when the plan finally clicks",
        ("Fire", "Horse"): "the racer who lives for momentum — restless until the lap is finished",
        ("Water", "Rat"): "the strategist who reads the room three moves ahead",
        ("Earth", "Dragon"): "the builder who needs the ending to look finished from the street",
    }
    cast = casts.get(
        (dm["element"], day_an),
        f"someone who runs on {dm['element']} daily energy with {day_an} pacing",
    )
    year = f"{yz.get('element', '')} {yz['animal']}".strip()
    day_label = day_combined or f"{dm['english']} {dm['element']} {day_an}"
    return (
        f"Cold open: you enter like {cast}. "
        f"ENVIRONMENT — your {year} year is the family noise and first impression you were born into; "
        f"DAY PILLAR — {day_label} with "
        f"{dm['yin_yang']} {dm['element']} stem and {day_an} branch is who you are once the door shuts."
    )


def _numerology_scene(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    lp = facts["life_path"]
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    name = imprint["birth"]["name"] if imprint else "you"
    casts = {
        27: "the priestess-type lead who finishes other people's cycles — Sailor Saturn energy, closure as craft",
        9: "the wanderer who keeps giving the last chapter away — Avatar's Iroh in a younger body",
        1: "the first-episode protagonist who names the mission before the team agrees",
        6: "the hearth-holder everyone leans on until boundaries blur — Pam from The Office with mystic weight",
        8: "the empire-builder montage — Walter White before the lie, all competence",
        30: "the voice-before-throne arc — publicity arrives before the root is earned",
    }
    key = lp["compound"]
    cast = casts.get(key, casts.get(lp["value"], f"someone walking life path {lp['display']}"))
    mask = ""
    if expr.get("display") and expr["value"] != lp["value"]:
        mask = f" Public field {expr['display']} markets a different tempo than birth path {lp['display']}."
    if soul.get("display") and soul.get("value") != lp["value"]:
        mask += f" Private {soul['display']} runs hotter than what {name} shows at the door."
    return f"Episode cast for {name}: {cast}. Birth math centers on {lp['display']}.{mask}"


def _vedic_scene(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    lagna = facts["ascendant"].get("vedic_lagna") or facts["ascendant"]["western_sign"]
    moon = facts["moon"]
    nak = moon.get("nakshatra", "")
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    casts = {
        "Virgo": "the healer who fixes systems before feelings — Dr. House without the cruelty",
        "Libra": "the diplomat in a courtroom anime — every exit must look fair",
        "Scorpio": "the undercover agent — intensity dialed down in public, vault in private",
        "Leo": "the captain whose body language fills the frame before dialogue",
        "Pisces": "the dreamer who absorbs the room — Stevie from Schitt's Creek with tidal memory",
    }
    cast = casts.get(lagna, f"someone whose body runs on {lagna} lagna rhythm")
    return (
        f"Scene one: lagna {lagna} — {cast}. "
        f"Moon in {nak} ({moon.get('sidereal_sign', '')}) is the hunger under the script. "
        f"This life chapter runs under {dasha} mahadasha — the season title above every major plot turn."
    )


def _hellenistic_scene(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    asc = facts["ascendant"]["western_sign"]
    sun = facts["sun_sign"]
    mc = (facts.get("western_angles") or {}).get("midheaven", {}).get("sign", "")
    pairs = {
        ("Scorpio", "Libra"): "the charming investigator — surface grace, basement intensity",
        ("Leo", "Leo"): "the main-character lighting — same face at the door and the podium",
        ("Virgo", "Capricorn"): "the competent junior executive who becomes indispensable",
        ("Gemini", "Sagittarius"): "the talker who sells the road trip before packing",
    }
    cast = pairs.get((asc, sun), f"{asc} rising selling one story, {sun} Sun pushing another")
    mc_bit = f" Midheaven {mc} is what the credits say about you later." if mc else ""
    return f"Opening shot: {cast}.{mc_bit} Ascendant {asc} opens doors; Sun in {sun} decides what you keep fighting for."


def _financial_scene(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    wp = facts.get("western_planets") or {}
    jup = wp.get("Jupiter", {}).get("sign", "")
    sat = wp.get("Saturn", {}).get("sign", "")
    return (
        f"Money episode: Jupiter in {jup} is the montage where spending feels smart; "
        f"Saturn in {sat} is the paperwork episode that follows. "
        f"Think Breaking Bad's boom-and-audit rhythm — hype leg, consequences leg — personal, not global news."
    )


def _wealth_scene(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    dm = facts["day_master"]
    h2 = facts["vedic_house_2"]["sign"]
    lp = facts["life_path"]
    return (
        f"Paycheck episode: {dm['yin_yang']} {dm['element']} day master ({dm['english']}) is the vehicle; "
        f"2nd house {h2} is the toll booth; life path {lp['display']} is the destination that still matters "
        f"when the deposit lands."
    )


def _relationships_scene(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    h7 = facts["vedic_house_7"]["sign"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    moon = facts["moon"]
    return (
        f"Bond episode: 7th house {h7} is the kitchen-table contract scene. "
        f"Moon {moon.get('nakshatra', '')} is what you need when the door closes. "
        f"Year {yz} is who people think they met; day {day_an} is who shows up on month three."
    )