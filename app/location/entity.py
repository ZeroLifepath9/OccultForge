"""Build mini-chart for a place, state, company, or vehicle from founding data."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.calculators.bazi import compute_bazi
from app.calculators.numerology import (
    PYTHAGOREAN_MAP,
    life_path_from_birth,
    reduce_with_trail,
    sum_digits_with_trail,
    sum_letters,
)


def _parse_founded(founded: str) -> datetime:
    """founded: YYYY-MM-DD"""
    y, m, d = founded.split("-")
    return datetime(int(y), int(m), int(d), 12, 0, 0)


def build_entity_imprint(record: dict[str, Any]) -> dict[str, Any]:
    """
    Entity imprint at local noon on founding/admission date.
    Hour pillar omitted when birth time unknown — noted in metadata.
    """
    founded = record["founded"]
    dt = _parse_founded(founded)
    name = record.get("name", record.get("code", "Entity"))
    bazi = compute_bazi(dt)

    birth_date = dt.date()
    lp = life_path_from_birth(birth_date)
    expression = sum_letters(name, PYTHAGOREAN_MAP)
    founded_num = sum_digits_with_trail(founded.replace("-", ""))

    return {
        "entity_type": record.get("entity_type", "entity"),
        "name": name,
        "founded": founded,
        "timezone": record.get("timezone", "UTC"),
        "metadata": {
            "hour_pillar_estimated": False,
            "note": "BaZi month/day/year from founding date at noon; hour pillar excluded.",
        },
        "bazi": {
            "pillars": {
                k: bazi["pillars"][k]
                for k in ("year", "month", "day")
            },
            "day_master": bazi["day_master"],
            "element_balance": bazi["element_balance"],
        },
        "numerology": {
            "life_path": lp,
            "expression": expression,
            "founded_date_number": founded_num,
        },
        "extra": {k: v for k, v in record.items() if k not in ("founded", "timezone", "entity_type", "name")},
    }