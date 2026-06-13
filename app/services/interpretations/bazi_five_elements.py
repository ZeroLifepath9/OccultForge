"""BaZi 八字 — Five Elements framing for all BaZi narration."""

from __future__ import annotations

from typing import Any

from app.services.interpretations.bazi_hidden_stems import (
    build_hidden_stems_framework,
    count_surface_elements,
    count_weighted_element_balance,
    root_hidden_stem,
)

ELEMENT_TRAITS: dict[str, str] = {
    "Wood": "growth and flexibility",
    "Fire": "warmth and drive",
    "Earth": "stability and nurture",
    "Metal": "structure and clarity",
    "Water": "wisdom and adaptability",
}

PILLAR_ROLE: dict[str, str] = {
    "year": "ancestry and social climate — what you inherited from family and field",
    "month": "seasonal pillar — adulthood, career weather, and how strong your Day Master sits",
    "day": "self — Day Master stem plus branch; core personality and inner constitution",
    "hour": "later life, children, and private projects — where talent matures late",
}

# When an element runs hot, what tends to balance it (controlling/generating logic, plain tongue).
ELEMENT_NEED: dict[str, str] = {
    "Wood": "Metal to prune excess or Water to feed without scatter",
    "Fire": "Water to cool flux or Earth to ground the burn",
    "Earth": "Wood to move stagnation or Metal to give shape",
    "Metal": "Fire to soften rigidity or Water to flex the edge",
    "Water": "Earth to anchor or Wood to give direction",
}

SKY_PILLAR_ROLE: dict[str, str] = {
    "year": "universal year climate — public ancestral tone",
    "month": "seasonal sky — the month pillar sets weekly weather",
    "day": "today's sky pillar — the day stem and branch in the open",
}


def count_elements(pillars: dict[str, Any], *, weighted_hidden: bool = True) -> dict[str, float]:
    """Element balance: visible stems + weighted 藏干 (classical qi hierarchy)."""
    if weighted_hidden:
        return count_weighted_element_balance(pillars)
    surface = count_surface_elements(pillars)
    return {k: float(v) for k, v in surface.items()}


def _strong_weak(counts: dict[str, float]) -> tuple[list[str], list[str]]:
    if not counts:
        return [], []
    avg = sum(counts.values()) / len(counts)
    strong = [el for el, n in counts.items() if n >= max(2.0, avg + 0.5)]
    weak = [el for el in ELEMENT_TRAITS if counts.get(el, 0) == 0]
    return strong, weak


def balance_insight(
    counts: dict[str, float],
    day_master: str,
    *,
    latent_note: str = "",
) -> str:
    strong, weak = _strong_weak(counts)
    parts: list[str] = []
    if strong:
        traits = ", ".join(f"{el} ({ELEMENT_TRAITS[el]})" for el in strong[:2])
        parts.append(f"Chart runs strong on {traits} (stems + weighted 藏干)")
    if weak:
        parts.append(f"light on {', '.join(weak[:2])} — room to cultivate {ELEMENT_TRAITS.get(weak[0], 'balance')}")
    if latent_note:
        parts.append(latent_note)
    if day_master:
        need = ELEMENT_NEED.get(day_master, "balance across the cycles")
        parts.append(f"Day Master {day_master} is the center — everything else feeds or presses it; watch for {need}")
    return ". ".join(parts) + "." if parts else ""


def cycle_name(el_rel: str) -> str:
    if el_rel in ("generates", "generated_by"):
        return "generating (生 Sheng)"
    if el_rel in ("controls", "controlled_by"):
        return "controlling (克 Ke)"
    if el_rel == "same":
        return "resonance"
    return "neutral"


def compare_framing(level: str, day_master: str) -> str:
    """Which pillar role is being compared — Day Master centric."""
    if level == "day_vs_sky_day":
        return f"Day Master {day_master} versus today's sky day pillar"
    if level == "day_vs_sky_month":
        return f"Day Master {day_master} versus the seasonal month pillar"
    if level == "day_vs_sky_year":
        return f"Day Master {day_master} versus the universal year climate"
    if level == "year_vs_sky_year":
        return "birth year pillar versus sky year — ancestry and public environment"
    return "pillar compare"


def build_bazi_framework(imprint: dict[str, Any]) -> dict[str, Any]:
    """Natal eight-characters snapshot for BaZi narration."""
    bazi = imprint.get("bazi") or {}
    pillars = bazi.get("pillars") or {}
    dm_el = (bazi.get("day_master") or {}).get("element") or ""
    hidden_fw = build_hidden_stems_framework(pillars, dm_el)
    counts = count_elements(pillars)
    strong, weak = _strong_weak(counts)

    pillar_cards = {}
    for name in ("year", "month", "day", "hour"):
        p = pillars.get(name) or {}
        root = root_hidden_stem(p.get("branch", ""))
        pillar_cards[name] = {
            "gan_zhi": p.get("gan_zhi", ""),
            "stem_element": p.get("stem_element", ""),
            "branch_element": p.get("branch_element", ""),
            "hidden_stem": (root or {}).get("stem", ""),
            "hidden_stem_element": (root or {}).get("element", ""),
            "role": PILLAR_ROLE.get(name, ""),
        }

    return {
        "primer": (
            "BaZi is four pillars — year, month, day, hour — each a heavenly stem over an earthly branch. "
            "Eight characters total; branches carry Cáng Gān (藏干) hidden stems in root, center, and remnant qi. "
            "Wood, Fire, Earth, Metal, Water interact through generating (生) and controlling (克) cycles. "
            "Day Master is the day stem — the reference point; visible stems show outward expression, "
            "hidden stems reveal latent structure, Ten Gods, and true elemental weight."
        ),
        "day_master_element": dm_el,
        "element_balance": counts,
        "surface_balance": hidden_fw.get("surface_balance", {}),
        "strong_elements": strong,
        "weak_elements": weak,
        "balance_insight": balance_insight(
            counts,
            dm_el,
            latent_note=hidden_fw.get("latent_insight", ""),
        ),
        "hidden_stems": hidden_fw,
        "pillars": pillar_cards,
        "cycles": {
            "generating": "Wood → Fire → Earth → Metal → Water → Wood",
            "controlling": "Wood → Earth → Water → Fire → Metal → Wood",
        },
        "pillar_roles": PILLAR_ROLE,
        "sky_pillar_roles": SKY_PILLAR_ROLE,
    }