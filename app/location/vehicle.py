"""Vehicle / license plate energy vs user chart."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from app.calculators.bazi import compute_bazi
from app.calculators.numerology import PYTHAGOREAN_MAP, CHALDEAN_MAP, reduce_with_trail, sum_letters
from app.location.compare import compare_entity_to_user
from app.location.entity import build_entity_imprint


def plate_numerology(plate: str) -> dict[str, Any]:
    cleaned = re.sub(r"[^A-Za-z0-9]", "", plate.upper())
    letters = re.sub(r"[^A-Z]", "", cleaned)
    digits = re.sub(r"[^0-9]", "", cleaned)
    digit_sum = sum(int(c) for c in digits) if digits else 0
    pyth = sum_letters(letters or cleaned, PYTHAGOREAN_MAP) if cleaned else reduce_with_trail(0)
    chal = sum_letters(letters or cleaned, CHALDEAN_MAP) if cleaned else reduce_with_trail(0)
    combined = reduce_with_trail((pyth["compound"] if letters else 0) + digit_sum)
    return {
        "plate_raw": plate,
        "plate_clean": cleaned,
        "pythagorean_letters": pyth,
        "chaldean_letters": chal,
        "digit_sum": reduce_with_trail(digit_sum) if digits else reduce_with_trail(0),
        "combined_plate_vibration": combined,
    }


def vehicle_imprint(
    *,
    model_year: int | None = None,
    plate: str | None = None,
    label: str = "Vehicle",
) -> dict[str, Any]:
    parts: dict[str, Any] = {"label": label, "plate_analysis": None, "model_year_chart": None}

    if plate:
        parts["plate_analysis"] = plate_numerology(plate)

    if model_year:
        record = {
            "name": f"{label} {model_year}",
            "founded": f"{model_year}-01-01",
            "timezone": "UTC",
            "entity_type": "vehicle_year",
            "model_year": model_year,
        }
        parts["model_year_chart"] = build_entity_imprint(record)

    return parts


def compare_vehicle_to_user(
    user_imprint: dict[str, Any],
    vehicle: dict[str, Any],
) -> dict[str, Any]:
    comparisons: dict[str, Any] = {}

    if vehicle.get("model_year_chart"):
        comparisons["model_year"] = compare_entity_to_user(
            user_imprint,
            vehicle["model_year_chart"],
            label=vehicle["model_year_chart"]["name"],
        )

    plate = vehicle.get("plate_analysis")
    if plate:
        user_lp = user_imprint["numerology"]["schools"]["pythagorean"]["life_path"]["value"]
        plate_v = plate["combined_plate_vibration"]["value"]
        diff = abs(user_lp - plate_v)
        resonance = "mirror" if diff == 0 else "harmonic" if diff in (1, 2) else "challenge" if diff >= 5 else "neutral"
        comparisons["license_plate"] = {
            "user_life_path": user_lp,
            "plate_vibration": plate_v,
            "resonance": resonance,
            "compound_trail": plate["combined_plate_vibration"]["steps"],
        }

    return comparisons