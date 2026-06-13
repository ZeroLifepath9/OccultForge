"""Assemble full location insight bundle for paid tier."""

from __future__ import annotations

from typing import Any

from app.kb.loaders import (
    city_by_name,
    companies_for_city,
    companies_for_state,
    state_by_code,
)
from app.location.compare import compare_entity_to_user
from app.location.entity import build_entity_imprint
from app.location.vehicle import compare_vehicle_to_user, vehicle_imprint


def _nearest_state_code(state_code: str | None, latitude: float, longitude: float) -> str | None:
    if state_code:
        return state_code.upper()
    return None


def build_location_insight(
    user_imprint: dict[str, Any],
    *,
    state_code: str | None = None,
    city_name: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    include_companies: bool = True,
    vehicle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state_code = _nearest_state_code(state_code, latitude or 0, longitude or 0)
    result: dict[str, Any] = {
        "coordinates": {"latitude": latitude, "longitude": longitude},
        "state": None,
        "city": None,
        "companies": [],
        "vehicle": None,
    }

    if state_code:
        rec = state_by_code(state_code)
        if rec:
            ent = build_entity_imprint(rec)
            result["state"] = {
                "record": rec,
                "entity_imprint": ent,
                "comparison": compare_entity_to_user(user_imprint, ent, label=rec["name"]),
            }

    if city_name:
        crec = city_by_name(city_name)
        if crec:
            ent = build_entity_imprint(crec)
            result["city"] = {
                "record": crec,
                "entity_imprint": ent,
                "comparison": compare_entity_to_user(user_imprint, ent, label=crec["name"]),
            }
            if include_companies:
                for comp in companies_for_city(city_name):
                    cent = build_entity_imprint(comp)
                    result["companies"].append({
                        "record": comp,
                        "entity_imprint": cent,
                        "comparison": compare_entity_to_user(user_imprint, cent, label=comp["name"]),
                    })

    if include_companies and state_code and not city_name:
        for comp in companies_for_state(state_code):
            cent = build_entity_imprint(comp)
            result["companies"].append({
                "record": comp,
                "entity_imprint": cent,
                "comparison": compare_entity_to_user(user_imprint, cent, label=comp["name"]),
            })

    if vehicle:
        vimp = vehicle_imprint(
            model_year=vehicle.get("model_year"),
            plate=vehicle.get("plate"),
            label=vehicle.get("label", "Vehicle"),
        )
        result["vehicle"] = {
            "imprint": vimp,
            "comparison": compare_vehicle_to_user(user_imprint, vimp),
        }

    scores = []
    if result["state"]:
        scores.append(result["state"]["comparison"]["affinity_score"])
    if result["city"]:
        scores.append(result["city"]["comparison"]["affinity_score"])
    for c in result["companies"]:
        scores.append(c["comparison"]["affinity_score"])

    result["aggregate"] = {
        "mean_affinity": round(sum(scores) / len(scores), 2) if scores else None,
        "entity_count": len(scores),
        "top_ally": _top_match(result, "ally"),
        "top_challenge": _top_match(result, "challenge"),
    }
    return result


def _top_match(result: dict, label: str) -> str | None:
    candidates = []
    for key in ("state", "city"):
        block = result.get(key)
        if block and block["comparison"]["relationship_label"] == label:
            candidates.append((block["comparison"]["affinity_score"], block["comparison"]["label"]))
    for c in result.get("companies", []):
        if c["comparison"]["relationship_label"] == label:
            candidates.append((c["comparison"]["affinity_score"], c["comparison"]["label"]))
    if not candidates:
        return None
    candidates.sort(reverse=(label == "ally"))
    return candidates[0][1]