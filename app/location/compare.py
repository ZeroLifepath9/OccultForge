"""Compare user natal imprint to location/company entity charts."""

from __future__ import annotations

from typing import Any

from app.overlay.clashes import branch_clashes, branch_harmony

NUMEROLOGY_COMPLEMENTS = {
    1: [5, 7], 2: [6, 8], 3: [5, 9], 4: [6, 8],
    5: [1, 3], 6: [2, 4], 7: [1, 5], 8: [2, 4],
    9: [3, 6], 11: [2, 4], 22: [4, 6], 33: [6, 9],
}


def _branch_harmony(a: str, b: str) -> str | None:
    return branch_harmony(a, b)


def _numerology_resonance(user_val: int, entity_val: int) -> dict[str, Any]:
    diff = abs(user_val - entity_val)
    label = "neutral"
    if user_val == entity_val:
        label = "mirror"
    elif entity_val in NUMEROLOGY_COMPLEMENTS.get(user_val, []):
        label = "complement"
    elif diff <= 2:
        label = "harmonic"
    elif diff >= 5:
        label = "challenge"
    return {
        "user": user_val,
        "entity": entity_val,
        "difference": diff,
        "resonance": label,
    }


def compare_entity_to_user(
    user_imprint: dict[str, Any],
    entity: dict[str, Any],
    *,
    label: str | None = None,
) -> dict[str, Any]:
    user_bazi = user_imprint["bazi"]["pillars"]
    ent_bazi = entity["bazi"]["pillars"]
    user_py = user_imprint["numerology"]["schools"]["pythagorean"]

    pillar_compare = {}
    for level in ("year", "month", "day"):
        ub = user_bazi[level]["branch"]
        eb = ent_bazi[level]["branch"]
        pillar_compare[level] = {
            "user": user_bazi[level]["gan_zhi"],
            "entity": ent_bazi[level]["gan_zhi"],
            "branch_relation": _branch_harmony(ub, eb),
            "stem_elements": {
                "user": user_bazi[level]["stem_element"],
                "entity": ent_bazi[level]["stem_element"],
            },
        }

    day_clash = branch_clashes(user_bazi["day"]["branch"], ent_bazi["day"]["branch"])
    year_harmony = _branch_harmony(user_bazi["year"]["branch"], ent_bazi["year"]["branch"])

    num = {
        "life_path": _numerology_resonance(
            user_py["life_path"]["value"],
            entity["numerology"]["life_path"]["value"],
        ),
        "expression_vs_user_soul": _numerology_resonance(
            user_py["soul_urge"]["value"],
            entity["numerology"]["expression"]["value"],
        ),
    }

    score = 0.5
    if day_clash:
        score -= 0.25
    if year_harmony in ("san_he_三合", "liu_he_六合", "same_branch"):
        score += 0.15
    if num["life_path"]["resonance"] in ("mirror", "complement", "harmonic"):
        score += 0.15
    if num["life_path"]["resonance"] == "challenge":
        score -= 0.1
    score = max(0.0, min(1.0, round(score, 2)))

    affinity = "ally" if score >= 0.65 else "flow" if score >= 0.45 else "caution" if score >= 0.3 else "challenge"

    return {
        "label": label or entity.get("name"),
        "entity_type": entity.get("entity_type"),
        "pillar_comparison": pillar_compare,
        "day_pillar_clashes": day_clash,
        "year_branch_relation": year_harmony,
        "numerology": num,
        "affinity_score": score,
        "relationship_label": affinity,
        "insight_summary": _summary(pillar_compare, day_clash, year_harmony, num, affinity),
    }


def _summary(pillars, day_clash, year_harmony, num, affinity) -> str:
    parts = [f"Overall affinity: {affinity}."]
    if day_clash:
        parts.append(f"Day branches clash: {', '.join(day_clash)}.")
    if year_harmony:
        parts.append(f"Year branches: {year_harmony}.")
    parts.append(
        f"Life path resonance: {num['life_path']['resonance']} "
        f"(you {num['life_path']['user']}, place {num['life_path']['entity']})."
    )
    day_rel = pillars.get("day", {}).get("branch_relation")
    if day_rel:
        parts.append(f"Day pillar relation: {day_rel}.")
    return " ".join(parts)