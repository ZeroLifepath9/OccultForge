"""
Occult Forge threshold seal — sealed chart record + plain occult-wave reading.
"""

from __future__ import annotations

from typing import Any

from app.services.overview_lore import WESTERN_SIGN_ELEMENT
from app.services.plain_reading import (
    INTERPRETATION_MARKER,
    SEAL_CLOSE,
    build_plain_reading,
)

OVERVIEW_FORMAT = "priest-chart"
CHART_MARKER = "OCCULT FORGE — SEALED NATAL CHART"
FORGE_FOOTER = "All daily readings and counsel read against this Occult Forge seal."

SIGN_MODALITY: dict[str, str] = {
    "Aries": "Cardinal",
    "Taurus": "Fixed",
    "Gemini": "Mutable",
    "Cancer": "Cardinal",
    "Leo": "Fixed",
    "Virgo": "Mutable",
    "Libra": "Cardinal",
    "Scorpio": "Fixed",
    "Sagittarius": "Mutable",
    "Capricorn": "Cardinal",
    "Aquarius": "Fixed",
    "Pisces": "Mutable",
}

VEDIC_HOUSE_ROLE: dict[int, str] = {
    1: "Self, body, and how you enter life",
    2: "Money, speech, and what you value",
    3: "Courage, siblings, and short journeys",
    4: "Home, roots, and private peace",
    5: "Creativity, risk, children, and romance",
    6: "Health, service, and daily work",
    7: "Partners, contracts, and open rivals",
    8: "Shared money, depth, and transformation",
    9: "Belief, teachers, and long travel",
    10: "Career, reputation, and public name",
    11: "Allies, gains, and networks",
    12: "Rest, exile, spirituality, and what you release",
}


def _ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _format_pillar_block(label: str, pillar: dict[str, Any]) -> list[str]:
    from app.services.chart_accuracy import STEM_META

    stem_hz = pillar.get("stem_hanzi") or pillar.get("stem", "—")
    branch_hz = pillar.get("branch_hanzi") or pillar.get("branch", "—")
    meta = STEM_META.get(stem_hz, {})
    yy = pillar.get("yin_yang") or meta.get("yin_yang", "")
    return [
        f"  {label}",
        f"    Heavenly stem: {stem_hz} ({pillar.get('stem_english', '—')}) · {yy} {pillar.get('stem_element', '—')}",
        f"    Branch: {branch_hz} · {pillar.get('branch_animal', '—')}",
        f"    Pillar: {pillar.get('gan_zhi', '—')}",
    ]


def _format_house_block(house: dict[str, Any]) -> list[str]:
    n = house.get("house", 0)
    sign = house.get("sign", "—")
    planets = house.get("planets") or []
    pl = ", ".join(planets) if planets else "none"
    role = VEDIC_HOUSE_ROLE.get(n, house.get("theme", ""))
    return [
        f"  {_ordinal(n)} House · {sign}",
        f"    Planets: {pl}",
        f"    Role: {role}",
        "",
    ]


def build_natal_chart_record(facts: dict[str, Any]) -> dict[str, Any]:
    dm = facts["day_master"]
    day_p = facts.get("day_pillar") or facts["pillars"]["day"]
    yz = facts["year_zodiac"]
    pillars = facts["pillars"]
    houses = facts.get("vedic_houses") or []

    return {
        "occult_forge": True,
        "astrological_layer": {
            "day_stem": day_p.get("stem_hanzi", dm.get("hanzi", "")),
            "day_stem_english": day_p.get("stem_english", dm.get("english", "")),
            "day_element": dm["element"],
            "day_yin_yang": dm["yin_yang"],
            "day_branch_animal": day_p.get("branch_animal", ""),
            "western_sun": facts["sun_sign"],
            "western_sun_element": WESTERN_SIGN_ELEMENT.get(facts["sun_sign"], ""),
            "western_asc": facts["ascendant"]["western_sign"],
            "western_asc_element": WESTERN_SIGN_ELEMENT.get(facts["ascendant"]["western_sign"], ""),
            "western_moon": facts["moon"]["western_sign"],
            "western_moon_element": WESTERN_SIGN_ELEMENT.get(facts["moon"]["western_sign"], ""),
            "eastern_year": f"{yz.get('element', '')} {yz['animal']}".strip(),
            "eastern_year_pillar": yz.get("gan_zhi") or "",
            "vedic_lagna": facts["ascendant"]["vedic_lagna"],
            "sidereal_moon": facts["moon"]["sidereal_sign"],
            "nakshatra": facts["moon"].get("nakshatra"),
            "mahadasha": (facts.get("mahadasha") or {}).get("lord"),
        },
        "bazi_pillars": pillars,
        "vedic_houses": {h["house"]: h for h in houses if h},
        "numerology": {
            "life_path": facts["life_path"]["display"],
            "expression": facts.get("expression", {}).get("display"),
            "birthday": facts.get("birthday_number", {}).get("display"),
        },
        "western_planets": facts.get("western_planets") or {},
    }


def format_chart_reference(record: dict[str, Any]) -> str:
    al = record["astrological_layer"]
    lines = [
        CHART_MARKER,
        "",
        "ASTROLOGICAL LAYER",
        "  Day Master (your core gate)",
        f"    Sign / branch: {al['day_branch_animal']}",
        f"    Heavenly stem: {al['day_stem']} ({al['day_stem_english']}) · {al['day_yin_yang']} {al['day_element']}",
        "  Western sky",
        f"    Sun sign: {al['western_sun']} · {SIGN_MODALITY.get(al['western_sun'], '')} {al['western_sun_element']}",
        f"    Ascendant: {al['western_asc']} · {al['western_asc_element']}",
        f"    Moon: {al['western_moon']} · {al['western_moon_element']}",
        "  Eastern lineage (year)",
        f"    Zodiac: {al['eastern_year']}",
        f"    Year pillar: {al['eastern_year_pillar']}",
        "  Vedic reference",
        f"    Lagna: {al['vedic_lagna']} · Sidereal Moon: {al['sidereal_moon']} · {al['nakshatra']}",
        f"    Maha dasha: {al['mahadasha'] or '—'}",
        "",
        "BAZI PILLARS",
    ]
    p = record["bazi_pillars"]
    for label, key in (
        ("Hour Pillar", "hour"),
        ("Day Pillar", "day"),
        ("Month Pillar", "month"),
        ("Year Pillar", "year"),
    ):
        lines.extend(_format_pillar_block(label, p[key]))
        lines.append("")

    lines.append("VEDIC SIDEREAL HOUSES (Lahiri · whole-sign)")
    lines.append("")
    houses = record["vedic_houses"]
    for n in range(1, 13):
        h = houses.get(n, {"house": n, "sign": "—", "planets": []})
        lines.extend(_format_house_block(h))

    num = record["numerology"]
    lines.extend(
        [
            "NUMEROLOGY (sealed in Occult Forge)",
            f"  Life path: {num['life_path']}",
            f"  Expression: {num.get('expression') or '—'}",
            f"  Birth day: {num.get('birthday') or '—'}",
            "",
            FORGE_FOOTER,
        ]
    )
    return "\n".join(lines)


def build_priest_interpretation(facts: dict[str, Any], name: str) -> str:
    return build_plain_reading(facts, name)


def build_threshold_seal(facts: dict[str, Any], name: str) -> tuple[str, str, str, dict[str, Any]]:
    record = build_natal_chart_record(facts)
    chart = format_chart_reference(record)
    interpretation = build_priest_interpretation(facts, name)
    full = f"{chart}\n\n---\n\n{interpretation}"
    return chart, interpretation, full, record


def build_zero_seal(facts: dict[str, Any], name: str, **kwargs: Any) -> str:
    _, _, full, _ = build_threshold_seal(facts, name)
    return full