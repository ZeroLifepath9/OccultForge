"""
Hellenistic forge lens — smooth brother voice, list-formatted insight.
Western whole-sign outer planets; conversational, not chart recitation.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.matrix_decoder_voice import format_matrix_reading
from app.services.interpretations.western_forge_lens import (
    _birth_place,
    _outer_action_steps,
    _outer_watch_outs,
    _planet_slots,
    _spoken_birth,
    _who,
)


def _smooth_influence(name: str, slot: dict[str, Any]) -> str:
    life = slot["life"]
    edge = slot["edge"]
    if name == "Pluto":
        return (
            f"Power and rebirth — hits hardest around {life}. "
            f"Something in you runs {edge}; when a chapter must end, end it clean or control rots the mission."
        )
    if name == "Venus":
        return (
            f"Love and money — breathe through {life} with a {edge} flavor. "
            f"Charm and comfort rhyme here; price both or sovereignty leaks."
        )
    if name == "Uranus":
        return (
            f"Breaks and jolts — wake up {life}. "
            f"You need room to move {edge}; rigidity snaps, but adrenaline is not a finished plan."
        )
    return (
        f"Dreams and fog — soften {life} with a {edge} undertow. "
        f"Inspiration lives here; mirages pose as destiny when proof is skipped."
    )


def _smooth_direct(who: str, spoken: str, place_bit: str, asc: str, sun: str, slots: dict[str, Any]) -> str:
    return (
        f"{who}, born {spoken}{place_bit} — Hellenistic read, plain talk. "
        f"{asc} rising is how you enter the room; {sun} Sun is the plot you keep performing. "
        f"Under that, four slow planets set the weather — power in {slots['Pluto']['life']}, "
        f"love and money in {slots['Venus']['life']}, shocks in {slots['Uranus']['life']}, "
        f"dreams in {slots['Neptune']['life']}. One body, one pulse — not four separate scripts."
    )


def build_hellenistic_forge_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    who = _who(imprint)
    spoken = _spoken_birth(facts)
    place = _birth_place(facts)
    place_bit = f", {place}" if place else ""
    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    sun = facts.get("sun_sign") or imprint["western"]["planets"]["Sun"]["sign"]
    slots = _planet_slots(imprint)

    direct = _smooth_direct(who, spoken, place_bit, asc, sun, slots)
    influence_lines = [
        _smooth_influence("Pluto", slots["Pluto"]),
        _smooth_influence("Venus", slots["Venus"]),
        _smooth_influence("Uranus", slots["Uranus"]),
        _smooth_influence("Neptune", slots["Neptune"]),
        (
            f"Whole-sign lens — outer planets land in life areas, not headlines. "
            f"Read {asc} door and {sun} will as the handshake; let the four drums color timing, not identity."
        ),
    ]
    decoded = "\n".join(influence_lines)

    steps = _outer_action_steps(facts, imprint)
    avoids = _outer_watch_outs(slots)
    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:6], 1))
    avoid_lines = "\n".join(f"- {a}" for a in avoids[:4])
    action = f"Forge now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"

    return format_matrix_reading(direct, decoded, action)