"""
Plain-life manifestation language — what chart factors mean in everyday terms.
"""

from __future__ import annotations

from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.compound_registry import PATH_FINAL_DIRECTORY, COMPOUND_DIRECTORY
from app.services.imprint_labels import combined_pillar_label, pillar_english

FORBIDDEN_PHRASES = (
    "occult depth",
    "leverage this",
    "leverage for",
    "you must",
    "do not ",
    "don't ",
    "look up",
    "investigate",
    "high priestess",
    "major arcana",
    "tarot",
    "kabbalah",
    "mantra",
    "gem and",
    "remedial",
    "divisional chart",
    "cosmobiology",
    "harmonic:",
    "uranian",
)

EXAMPLE_LEADS = ("Like this:", "Like ", "You might notice", "For example", "Imagine ")


def has_example_signal(text: str) -> bool:
    low = text.lower()
    return any(lead.lower() in low for lead in EXAMPLE_LEADS)


def plain_flesh(text: str) -> str:
    """Rewrite registry flesh into observational plain English."""
    out = text
    replacements = (
        ("do not wait for permission", "waiting for permission slowly costs you momentum"),
        ("do not ", "skipping "),
        ("Do not ", "Skipping "),
        ("you must ", "the pattern asks you to "),
        ("look up:", ""),
        ("Look up:", ""),
    )
    for old, new in replacements:
        out = out.replace(old, new)
    return " ".join(out.split())


def manifest_compound(c: int, f: int, disp: str) -> str:
    lib = get_compound_entry(c, f, disp)
    flesh = plain_flesh(lib.get("flesh", ""))
    fin = PATH_FINAL_DIRECTORY.get(f, {}).get("plain", "")
    parts = []
    if flesh:
        parts.append(flesh)
    if c != f and fin:
        parts.append(f"The daily rhythm settles toward: {plain_flesh(fin)}")
    elif fin and not flesh:
        parts.append(plain_flesh(fin))
    if not parts:
        row = COMPOUND_DIRECTORY.get(c, {})
        parts.append(plain_flesh(row.get("flesh", f"Life path {disp} shapes how you finish what you start.")))
    return plain_flesh(" ".join(parts))


def manifest_nakshatra(name: str, pada: int | None = None) -> str:
    from app.services.babylon_lore import NAKSHATRA_SCRIPT

    script = NAKSHATRA_SCRIPT.get(name, "a private emotional need that runs under your public story")
    base = (
        f"With Moon in {name}, your feelings lean toward {script.lower()}. "
        "This is the hunger underneath mood — what you need when nobody is performing."
    )
    pada_note = {
        1: "You feel better when you act first and explain later.",
        2: "You feel better when something becomes tangible — a meal, a payment, a finished task.",
        3: "You feel better when you name it out loud or write it down.",
        4: "You feel better when an ending is felt and rested, not rushed.",
    }.get(pada or 0, "")
    return f"{base} {pada_note}".strip()


def manifest_pillar_element(element: str) -> str:
    return {
        "Wood": "You grow by starting things and learning on the move — new projects feel like oxygen.",
        "Fire": "You come alive when the work is visible — hiding your effort drains your energy.",
        "Earth": "You build trust by being reliable — schedules, meals, and follow-through matter.",
        "Metal": "You think in clean lines — decisions, boundaries, and finished work feel right.",
        "Water": "You read timing and people — rushing when the room isn't ready costs you twice.",
    }.get(element, f"Your {element} day energy shapes how you work and recover.")


def manifest_animal(animal: str) -> str:
    return {
        "Rat": "You size up the room before you commit — timing beats speed.",
        "Ox": "You outlast problems others walk away from — slow and steady is your real speed.",
        "Tiger": "You move when the plan is clear — bold starts, not endless debate.",
        "Rabbit": "You handle tension with tact — a soft exit can still be a real decision.",
        "Dragon": "You want endings that feel complete — half-finished chapters nag at you.",
        "Snake": "You research first, act once — one clean move beats noisy repetition.",
        "Horse": "You recover through movement — sitting still too long makes everything worse.",
        "Goat": "Peace and beauty matter — ugly environments wear you down faster than hard work.",
        "Monkey": "You improvise under pressure — chaos becomes a workable plan in your hands.",
        "Rooster": "You catch details others miss — half-done loops keep you up at night.",
        "Dog": "You show up for people and causes you believe in — loyalty is your default.",
        "Pig": "You enjoy life fully — generosity is real until boundaries get too loose.",
    }.get(animal, f"Your {animal} side colors your daily pace and style.")


def manifest_house(house_num: int, sign: str, role: str) -> str:
    return (
        f"Your {house_num}th house in {sign} points to {role.lower()}. "
        f"In plain life, {sign} flavors how that theme shows up — not as a label, but as a recurring pattern."
    )


def manifest_planet(name: str, sign: str) -> str:
    roles = {
        "Jupiter": f"expansion, optimism, and where luck tends to swell in {sign}",
        "Saturn": f"limits, patience, and what takes time to prove in {sign}",
        "Sun": f"what you push for and where your will is strongest in {sign}",
        "Moon": f"what soothes you and what you need after a hard day in {sign}",
        "Venus": f"what you value, enjoy, and price in relationships and money in {sign}",
        "Mars": f"how you fight for what you want and where friction heats up in {sign}",
        "Mercury": f"how you think, talk, and solve problems in {sign}",
        "Uranus": f"sudden changes, surprises, and breaks from routine in {sign}",
        "Neptune": f"confusion, glamour, and what looks better than it is in {sign}",
        "Pluto": f"power, debt, and deep transformation in {sign}",
    }
    return f"{name} in {sign} colors {roles.get(name, f'life themes in {sign}')}."


def manifest_day_master(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    el = dm["element"]
    stem = dm.get("english", "")
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    return (
        f"Your day master is {stem} ({dm.get('yin_yang', '')} {el}) with a {day_an} branch. "
        f"{manifest_pillar_element(el)} {manifest_animal(day_an)}"
    )


def manifest_bazi_pillar(pillar: dict[str, Any], role: str) -> str:
    pe = pillar_english(pillar)
    combined = combined_pillar_label(pillar)
    return (
        f"{combined} ({pe['gan_zhi']}) — {role}. "
        f"{manifest_pillar_element(pe['stem_element'])} {manifest_animal(pe['branch_animal'])}"
    )


def strip_forbidden(text: str) -> str:
    """Light sanitizer — builders should avoid forbidden phrases at source."""
    out = text
    for phrase in FORBIDDEN_PHRASES:
        while phrase.lower() in out.lower():
            idx = out.lower().find(phrase.lower())
            end = idx + len(phrase)
            out = (out[:idx] + out[end:]).strip()
    return out