"""
Western Setting — pure tropical natal Western astrology at birth.
Conversational forge read; no numerology, Vedic, or BaZi overlay.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.matrix_decoder_voice import format_matrix_reading
from app.services.interpretations.hellenistic_forge_lens import _smooth_influence
from app.services.interpretations.western_forge_lens import (
    HOUSE_LIFE,
    SIGN_EDGE,
    _birth_place,
    _planet_slots,
    _spoken_birth,
    _whole_sign_house,
    _who,
)


def _natal_slot(imprint: dict[str, Any], name: str) -> dict[str, Any]:
    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    row = imprint["western"]["planets"].get(name) or {}
    sign = row.get("sign", "")
    house = _whole_sign_house(asc, sign) if sign else 0
    return {
        "sign": sign,
        "house": house,
        "life": HOUSE_LIFE.get(house, "life themes"),
        "edge": SIGN_EDGE.get(sign, "distinct"),
    }


def _luminary_line(label: str, sign: str, life: str, edge: str, voice: str) -> str:
    return (
        f"{label} in {sign} — colors {life} with a {edge} undertone. "
        f"{voice}"
    )


_LUMINARY_VOICE = {
    "Sun": "This is the plot you keep performing; honor it without letting it spend the whole chart.",
    "Moon": "This is private weather — moods, appetite, and repair run here before logic wins.",
    "Ascendant": "This is the door you walk through; strangers read this before they read your resume.",
}

_PERSONAL_VOICE = {
    "Mercury": "Messages, deals, and mental pace — how you talk is how you steer the week.",
    "Mars": "Fight, courage, and push — where you spend anger becomes where you spend power.",
    "Jupiter": "Growth, faith, and expansion — optimism needs receipts in this lane.",
    "Saturn": "Limits, contracts, and slow weight — structure is not punishment here, it is tuition.",
}


def _personal_line(name: str, slot: dict[str, Any]) -> str:
    sign = slot["sign"]
    life = slot["life"]
    edge = slot["edge"]
    voice = _PERSONAL_VOICE.get(name, "distinct rhythm in daily outcomes")
    return f"{name} in {sign} — runs through {life} ({edge}). {voice}"


def _western_setting_steps(asc: str, sun: str, moon: str, slots: dict[str, Any]) -> list[str]:
    return [
        f"Enter rooms like {asc} rising — one honest entrance before you perform the {sun} story.",
        f"Check {moon} Moon weather before big promises — body and mood finance the deal.",
        "Track Pluto, Venus, Uranus, and Neptune as four weather systems — separate ledgers, separate moves.",
        "Say one Mercury-clear sentence before mental scatter wins the room.",
        "Batch visible moves on proof weeks; let Neptune weeks stay research-only.",
        "Protect sleep like payroll — tired kings sign treaties the chart did not order.",
    ]


def _western_setting_watch(slots: dict[str, Any]) -> list[str]:
    pluto = slots["Pluto"]["life"]
    venus = slots["Venus"]["life"]
    return [
        "Neptune fog plus urgency breeds mirage launches — keep paper, skip destiny cosplay.",
        "Uranus jolt is not a finished mission — pace the forge stroke.",
        f"Pluto power plays around {pluto} eat your name if you perform control.",
        f"Venus charm around {venus} without math drains sovereignty fast.",
    ]


def build_western_setting_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    who = _who(imprint)
    spoken = _spoken_birth(facts)
    place = _birth_place(facts)
    place_bit = f", {place}" if place else ""

    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    sun = facts.get("sun_sign") or imprint["western"]["planets"]["Sun"]["sign"]
    moon = facts.get("moon", {}).get("western_sign") or imprint["western"]["planets"]["Moon"]["sign"]
    sun_slot = _natal_slot(imprint, "Sun")
    moon_slot = _natal_slot(imprint, "Moon")
    outer = _planet_slots(imprint)

    mercury = _natal_slot(imprint, "Mercury")
    mars = _natal_slot(imprint, "Mars")
    jupiter = _natal_slot(imprint, "Jupiter")
    saturn = _natal_slot(imprint, "Saturn")

    direct = (
        f"{who}, born {spoken}{place_bit} — Western seal only, plain talk. "
        f"{asc} rising is how you enter; {sun} Sun is the story; {moon} Moon is the private weather. "
        f"Four outer planets set the long drum under that — power, love, shock, and fog — "
        f"one tropical chart at birth, not mixed schools."
    )

    influence_lines = [
        _luminary_line(
            "Ascendant",
            asc,
            HOUSE_LIFE.get(1, "identity"),
            SIGN_EDGE.get(asc, "distinct"),
            _LUMINARY_VOICE["Ascendant"],
        ),
        _luminary_line("Sun", sun, sun_slot["life"], sun_slot["edge"], _LUMINARY_VOICE["Sun"]),
        _luminary_line("Moon", moon, moon_slot["life"], moon_slot["edge"], _LUMINARY_VOICE["Moon"]),
        _personal_line("Mercury", mercury),
        _personal_line("Mars", mars),
        _personal_line("Jupiter", jupiter),
        _personal_line("Saturn", saturn),
        _smooth_influence("Pluto", outer["Pluto"]),
        _smooth_influence("Venus", outer["Venus"]),
        _smooth_influence("Uranus", outer["Uranus"]),
        _smooth_influence("Neptune", outer["Neptune"]),
        (
            f"Whole-sign houses from {asc} — planets land in life areas, not headlines. "
            f"Read the handshake ({asc}), the plot ({sun}), and the mood ({moon}); let the rest color pace."
        ),
    ]
    decoded = "\n".join(influence_lines)

    steps = _western_setting_steps(asc, sun, moon, {"Mercury": mercury, **outer})
    avoids = _western_setting_watch(outer)
    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:6], 1))
    avoid_lines = "\n".join(f"- {a}" for a in avoids[:4])
    action = f"Forge now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"

    return format_matrix_reading(direct, decoded, action)