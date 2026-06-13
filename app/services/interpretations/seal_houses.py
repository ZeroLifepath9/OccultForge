"""Frozen whole-sign house signs for the seal — tropical ascendant, set once at imprint."""

from __future__ import annotations

from typing import Any

from app.calculators.western import SIGNS


def whole_sign_house(ascendant_sign: str, house_num: int) -> str:
    if not ascendant_sign or ascendant_sign not in SIGNS or house_num < 1 or house_num > 12:
        return "—"
    start = SIGNS.index(ascendant_sign)
    return SIGNS[(start + house_num - 1) % 12]


def build_seal_houses(imprint: dict[str, Any]) -> dict[str, Any]:
    asc = (imprint.get("western") or {}).get("angles", {}).get("ascendant", {}).get("sign", "")
    return {
        "system": "western_whole_sign",
        "ascendant": asc or "—",
        "house_2": whole_sign_house(asc, 2),
        "house_7": whole_sign_house(asc, 7),
        "house_10": whole_sign_house(asc, 10),
    }


def seal_house_line(imprint: dict[str, Any], house_num: int) -> dict[str, Any]:
    from app.services.imprint_labels import HOUSE_THEMES

    seal = imprint.get("seal_houses") or build_seal_houses(imprint)
    key = f"house_{house_num}"
    sign = seal.get(key, "—")
    return {
        "house": house_num,
        "theme": HOUSE_THEMES.get(house_num, f"House {house_num}"),
        "sign": sign,
        "system": seal.get("system", "western_whole_sign"),
        "planets": [],
    }