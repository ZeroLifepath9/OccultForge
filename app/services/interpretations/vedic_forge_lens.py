"""
Vedic / Jyotish forge lens — interpreter voice, coffee-table plain.
Sidereal imprint only. No chart callouts; lived meaning, actionable advice.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.services.interpretations.eastern_rising_lens import _NAKSHATRA_FORGE
from app.services.interpretations.matrix_decoder_voice import format_matrix_reading
from app.services.phoenix_insight import SIGN_MEANS
from app.services.interpretations.vedic_house_sign_engine import HOUSE_LENS, interpret_house_sign, interpret_lagna

_LIFE_OPEN: dict[int, str] = {
    2: "Money and what you say about it",
    4: "Home, roots, and private peace",
    5: "Romance, risk, and what you create",
    6: "Daily work, health, and service",
    7: "Partnership, contracts, and open rivalry",
    8: "Shared money, crisis, and deep change",
    10: "Career, reputation, and how you are remembered",
}

_SEASON_ACTION: dict[str, str] = {
    "Sun": "visibility is hot — lead with proof, not performance.",
    "Moon": "belonging and body cost rule — finance comfort like payroll.",
    "Mars": "fight season — make clean cuts, skip performative battles.",
    "Mercury": "messages and deals rule — follow up on paper, not vibes.",
    "Jupiter": "growth season — teach and expand with receipts.",
    "Venus": "bond and money season — charm needs written math.",
    "Saturn": "limits season — structure beats shortcuts.",
    "Rahu": "hunger is loud — verify mission before you chase the itch.",
    "Ketu": "release season — strip dead weight before you add new weight.",
}

_SEASON_NOW: dict[str, str] = {
    "Sun": "Life right now spotlights your name and pride — visibility is not optional, but ego spends fast if the body is empty.",
    "Moon": "Life right now spotlights belonging and body cost — home, food, and nervous system are part of the budget, not background.",
    "Mars": "Life right now spotlights fight and honest cuts — soft avoidance costs more than one clean conflict.",
    "Mercury": "Life right now spotlights messages, deals, and mental pace — paperwork and follow-up are destiny work.",
    "Jupiter": "Life right now spotlights growth and teaching — measured risk has tailwind when it is honest, not inflated.",
    "Venus": "Life right now spotlights love, beauty, and money — charm still needs math and written terms.",
    "Saturn": "Life right now spotlights limits and contracts — shortcuts bill compound interest; backbone is the move.",
    "Rahu": "Life right now spotlights hunger and disruption — appetite feels loud, but appetite is not the same as mission.",
    "Ketu": "Life right now spotlights release — strip noise, finish what died, and let less be the power move.",
}

_FORCE_VOICE: dict[str, str] = {
    "Sun": "Your visible will and pride",
    "Moon": "Your emotional weather",
    "Mars": "Your fight and courage",
    "Mercury": "Your speech and deals",
    "Jupiter": "Your faith and expansion",
    "Venus": "Your taste in love and money",
    "Saturn": "Your slow weight and earned limits",
    "Rahu": "Your hunger for the foreign and forbidden",
    "Ketu": "What you are meant to release",
}

_KEY_HOUSES = (2, 4, 6, 7, 8, 10)
_GRAHA_ORDER = ("Saturn", "Jupiter", "Mars", "Rahu", "Ketu", "Venus", "Mercury")
_ANGULAR = frozenset({1, 4, 7, 10})


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


def _sign_voice(sign: str) -> str:
    raw = SIGN_MEANS.get(sign, "")
    if not raw:
        return ""
    parts = [p.strip().rstrip(".") for p in raw.split(". ") if p.strip()]
    return ". ".join(parts[:2]) + "." if parts else raw


def _clean_dont(text: str) -> str:
    t = (text or "").strip()
    t = t.replace("do not ", "skip ").replace("Do not ", "Skip ")
    return t


def _life_insight(house_num: int, sign: str) -> str:
    if not sign or sign == "—":
        return ""
    opener = _LIFE_OPEN.get(house_num, "This part of life")
    interp = interpret_house_sign(house_num, sign)
    do = interp.get("do", "").strip()
    dont = _clean_dont(interp.get("dont", ""))
    if do and "runs through" not in do.lower():
        line = f"{opener}: {do}."
    else:
        focus = HOUSE_LENS.get(house_num, {}).get("focus", opener.lower())
        temp = interp.get("temperament", "distinct")
        line = (
            f"{opener}: {focus} — you handle this with {temp} pacing. "
            "Forced speed or vague terms here cost more than patience."
        )
    if dont and "forcing the lane" not in dont.lower():
        line += f" The leak: {dont}."
    return line


def _planet_house(imprint: dict[str, Any], planet: str) -> int | None:
    for row in imprint.get("vedic", {}).get("houses", []):
        if planet in (row.get("planets") or []):
            h = int(row.get("house", 0) or 0)
            return h or None
    return None


def _force_insight(planet: str, sign: str, house_num: int | None) -> str:
    if not sign:
        return ""
    voice = _FORCE_VOICE.get(planet, "This force")
    sign_bit = _sign_voice(sign)
    if house_num:
        area = _LIFE_OPEN.get(house_num, _LIFE_OPEN.get(7, "daily life")).lower()
        return f"{voice} hits hardest around {area} — {sign_bit}"
    return f"{voice}: {sign_bit}"


def _moon_read(nak: str, sid_moon: str) -> str:
    parts: list[str] = []
    if nak:
        tip = _NAKSHATRA_FORGE.get(nak, "name what you need before bodies negotiate.")
        parts.append(f"Under every bond, emotional hunger shows up as {nak} — {tip}")
    if sid_moon:
        parts.append(
            f"Moods behind the face: {_sign_voice(sid_moon)} "
            "Feed that weather in partnership or it spends you before logic arrives."
        )
    return " ".join(parts)


def build_vedic_forge_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    who = _who(imprint)
    spoken = _spoken_birth(facts)
    place = _birth_place(facts)
    place_bit = f", {place}" if place else ""

    vedic = imprint["vedic"]
    lagna = vedic["lagna"]["sign"]
    moon = facts.get("moon") or {}
    nak = moon.get("nakshatra", "")
    sid_moon = moon.get("sidereal_sign", "")
    dasha = facts.get("mahadasha") or vedic["dasha"]["active_mahadasha"]
    lord = (dasha.get("lord") or "").strip()
    planets = vedic.get("planets") or {}
    sun_sign = planets.get("Sun", {}).get("sign", "")

    h2 = (facts.get("vedic_house_2") or {}).get("sign", "")
    h7 = (facts.get("vedic_house_7") or {}).get("sign", "")
    h10 = (facts.get("vedic_house_10") or {}).get("sign", "")

    body_bit = interpret_lagna(lagna)
    season_bit = _SEASON_NOW.get(lord, "Read the body before the headline — season and stamina must agree.")
    moon_bit = _moon_read(nak, sid_moon)

    direct_parts = [
        f"{who}, born {spoken}{place_bit} — talking straight about how your life actually runs.",
        f"You enter rooms with {lagna} energy in the body: {body_bit}",
    ]
    if moon_bit:
        direct_parts.append(moon_bit)
    direct_parts.append(season_bit)
    if sun_sign and sun_sign != lagna and sun_sign != sid_moon:
        direct_parts.append(f"What you push for publicly: {_sign_voice(sun_sign)}")
    direct_parts.append(
        "Body, mood, and season are one conversation — fighting all three at once is how power leaks."
    )
    direct = " ".join(p.strip() + ("" if p.strip().endswith(".") else ".") for p in direct_parts)

    influence_lines: list[str] = [
        f"How you enter life and hold stamina: {body_bit}",
    ]
    if moon_bit:
        influence_lines.append(moon_bit)
    if lord:
        influence_lines.append(season_bit)

    for house_num in _KEY_HOUSES:
        row = facts.get(f"vedic_house_{house_num}") or next(
            (h for h in facts.get("vedic_houses", []) if h.get("house") == house_num),
            {},
        )
        line = _life_insight(house_num, row.get("sign", ""))
        if line:
            influence_lines.append(line)

    ranked_forces: list[tuple[int, str, str, int | None]] = []
    for planet in _GRAHA_ORDER:
        body = planets.get(planet) or {}
        sign = body.get("sign", "")
        if not sign:
            continue
        house_num = _planet_house(imprint, planet)
        rank = 0 if house_num in _ANGULAR else 1
        ranked_forces.append((rank, planet, sign, house_num))
    ranked_forces.sort(key=lambda x: x[0])
    for _, planet, sign, house_num in ranked_forces[:4]:
        line = _force_insight(planet, sign, house_num)
        if line:
            influence_lines.append(line)

    decoded = "\n".join(influence_lines)

    h2_i = interpret_house_sign(2, h2) if h2 else {}
    h7_i = interpret_house_sign(7, h7) if h7 else {}
    h10_i = interpret_house_sign(10, h10) if h10 else {}

    steps = [
        (
            f"Honor the body first — {body_bit.rstrip('.')}. "
            "Eat, sleep, and walk into rooms on your terms before you perform health you have not lived."
        ),
        _NAKSHATRA_FORGE.get(
            nak,
            "Before the next bond talk, say what you need emotionally — unspoken hunger becomes the whole argument.",
        ),
        (
            f"Match big moves to this season — {_SEASON_ACTION.get(lord, 'read the body before the headline').rstrip('.')}. "
            "Last year's costume will not pass for homework here."
        ),
        (
            f"In partnership: {h7_i.get('do', 'write fairness before bodies negotiate')}."
            + (
                f" Watch the leak: {_clean_dont(h7_i.get('dont', ''))}."
                if h7_i.get("dont")
                else ""
            )
        ),
        (
            f"On career and legacy: {h10_i.get('do', 'one finished public brick at a time')}. "
            "Reputation follows proof, not louder self-story."
        ),
        (
            f"On money and voice: {h2_i.get('do', 'name what you value aloud')}. "
            "Keep love conversations and invoice conversations in separate rooms."
        ),
        (
            "Once a month, write three lines: what peaked, what drained, and what your body said before your mouth took over."
        ),
    ]

    avoids = [
        f"Running on empty while your {lagna} body asks for balance — fatigue lands before the drama every time.",
        f"Launching on ego timing while this {lord or 'season'} asks for different homework — the flesh gets the bill first.",
        "Letting love and money share one argument when they need separate sentences — the fight feels personal but it is bookkeeping.",
        "Performing wellness you never practice — the body keeps score even when the room applauds the mask.",
        f"Leaving emotional hunger unspoken ({nak or 'your bond appetite'}) — every contract talk turns into a feeding fight.",
    ]

    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:7], 1))
    avoid_lines = "\n".join(f"- {a}" for a in avoids[:5])
    action = f"Forge now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"

    return format_matrix_reading(direct, decoded, action)