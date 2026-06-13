"""Multi-school numerology with compound reduction trails."""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

MASTER_NUMBERS = {11, 22, 33}

PYTHAGOREAN_MAP = {
    **{c: 1 for c in "AJS"},
    **{c: 2 for c in "BKT"},
    **{c: 3 for c in "CLU"},
    **{c: 4 for c in "DMV"},
    **{c: 5 for c in "ENW"},
    **{c: 6 for c in "FOX"},
    **{c: 7 for c in "GPY"},
    **{c: 8 for c in "HQZ"},
    **{c: 9 for c in "IR"},
}

# Chaldean: no 9 in letter map; name uses different tradition
CHALDEAN_MAP = {
    **{c: 1 for c in "AIJQY"},
    **{c: 2 for c in "BKR"},
    **{c: 3 for c in "CGLS"},
    **{c: 4 for c in "DMT"},
    **{c: 5 for c in "EHNX"},
    **{c: 6 for c in "UVW"},
    **{c: 7 for c in "OZ"},
    **{c: 8 for c in "FP"},
}


def _digits_only(value: str) -> str:
    return re.sub(r"\D", "", value)


def reduce_with_trail(
    total: int,
    *,
    preserve_master: bool = True,
) -> dict[str, Any]:
    """Reduce to single digit, preserving 11/22/33 when enabled."""
    steps = [total]
    current = total
    while current > 9:
        if preserve_master and current in MASTER_NUMBERS:
            break
        current = sum(int(d) for d in str(current))
        steps.append(current)
    return {
        "compound": total,
        "value": current,
        "steps": steps,
        "is_master": current in MASTER_NUMBERS,
    }


def sum_digits_with_trail(value: str | int) -> dict[str, Any]:
    raw = _digits_only(str(value)) if isinstance(value, str) else str(value)
    if not raw:
        return reduce_with_trail(0)
    total = sum(int(c) for c in raw)
    return reduce_with_trail(total)


def sum_letters(name: str, letter_map: dict[str, int]) -> dict[str, Any]:
    cleaned = re.sub(r"[^A-Za-z]", "", name.upper())
    total = sum(letter_map.get(c, 0) for c in cleaned)
    return reduce_with_trail(total)


def life_path_from_birth(d: date) -> dict[str, Any]:
    return sum_digits_with_trail(d.strftime("%Y%m%d"))


def universal_year(year: int) -> dict[str, Any]:
    return sum_digits_with_trail(str(year))


def universal_month(year: int, month: int) -> dict[str, Any]:
    return sum_digits_with_trail(f"{year}{month:02d}")


def universal_day(d: date) -> dict[str, Any]:
    """Life path of the calendar day — month+day+year digits summed and reduced."""
    return sum_digits_with_trail(d.strftime("%Y%m%d"))


def calendar_day_number(d: date) -> dict[str, Any]:
    """Day-of-month imprint — reduced day digit only (May 30 → 3). Not the calendar gate."""
    return sum_digits_with_trail(d.day)


def calendar_gate_number(d: date) -> dict[str, Any]:
    """Calendar gate — full-date universal day; masters 11/22/33 never reduce."""
    return universal_day(d)


def life_path_day_number(d: date) -> dict[str, Any]:
    """Universal life-path day — same full-date gate as calendar_gate_number."""
    return universal_day(d)


def personal_year(birth: date, calendar_year: int) -> dict[str, Any]:
    total = birth.month + birth.day + sum(int(c) for c in str(calendar_year))
    return reduce_with_trail(total)


def personal_month(birth: date, year: int, month: int) -> dict[str, Any]:
    py = personal_year(birth, year)["value"]
    total = py + month
    return reduce_with_trail(total)


def personal_day(birth: date, target: date) -> dict[str, Any]:
    pm = personal_month(birth, target.year, target.month)["value"]
    total = pm + target.day
    return reduce_with_trail(total)


def compute_numerology(
    display_name: str,
    birth_datetime: datetime,
) -> dict[str, Any]:
    birth_date = birth_datetime.date()
    vowels = re.sub(r"[^AEIOUYaeiouy]", "", display_name)
    consonants = re.sub(r"[^BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz]", "", display_name)

    pyth_name = sum_letters(display_name, PYTHAGOREAN_MAP)
    pyth_vowels = sum_letters(vowels or display_name, PYTHAGOREAN_MAP)
    pyth_consonants = sum_letters(consonants or display_name, PYTHAGOREAN_MAP)

    chal_name = sum_letters(display_name, CHALDEAN_MAP)
    chal_birth = sum_digits_with_trail(birth_date.day)

    return {
        "schools": {
            "pythagorean": {
                "life_path": life_path_from_birth(birth_date),
                "expression": pyth_name,
                "soul_urge": pyth_vowels,
                "personality": pyth_consonants,
                "birthday": sum_digits_with_trail(birth_date.day),
            },
            "chaldean": {
                "expression": chal_name,
                "birthday": chal_birth,
                "note": "Chaldean uses alternate letter values; 9 is not assigned to letters.",
            },
        },
        "cycles": {
            "universal_year": universal_year(birth_date.year),
            "personal_year_at_birth": personal_year(birth_date, birth_date.year),
            "reference_today": {
                "universal_year": universal_year(date.today().year),
                "universal_month": universal_month(date.today().year, date.today().month),
                "universal_day": universal_day(date.today()),
                "personal_year": personal_year(birth_date, date.today().year),
                "personal_month": personal_month(birth_date, date.today().year, date.today().month),
                "personal_day": personal_day(birth_date, date.today()),
            },
        },
    }