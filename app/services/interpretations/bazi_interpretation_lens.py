"""BaZi interpretation lens — elements, hidden stems, interactions; single advice source."""

from __future__ import annotations

from typing import Any, Callable

from app.services.interpretations.bazi_five_elements import build_bazi_framework
from app.services.interpretations.bazi_hidden_stems import (
    ELEMENT_CONTROLS,
    ELEMENT_GENERATES,
    TEN_GOD_PLAIN,
    pillar_hidden_display,
    root_hidden_stem,
    ten_god_role,
)
from app.services.imprint_labels import branch_animal, stem_english

LENS_VERSION = "bazi-lens-v2"

PILLAR_ROLE_LABEL: dict[str, str] = {
    "year": "public inheritance",
    "month": "working-years season",
    "day": "daily self",
    "hour": "private engine",
}

TEN_GOD_ADVICE: dict[str, str] = {
    "companion": "peer momentum — collaborate before you compete",
    "output": "creative output — ship the refinement you usually keep private",
    "wealth": "resources and gain — name the material ask before you perform",
    "officer": "discipline and demand — structure beats speed today",
    "resource": "support and recovery — rest is part of the work",
}


def _advice_hook(visible_el: str, hidden_el: str, identity: str, role: str) -> str:
    """Plain-English behavioral hook from visible + hidden 生克."""
    if not hidden_el:
        return f"{identity} runs as written — lead with visible {visible_el or 'stem'} energy."
    if visible_el == hidden_el:
        return (
            f"{identity}: inner and outer {visible_el} align — "
            f"trust instinct on one real deliverable."
        )
    if ELEMENT_GENERATES.get(visible_el) == hidden_el:
        return (
            f"{identity}: outward {visible_el} feeds inner {hidden_el} — "
            f"act on the refinement, not just the show."
        )
    if ELEMENT_GENERATES.get(hidden_el) == visible_el:
        return (
            f"{identity}: inner {hidden_el} fuels your {visible_el} stem — "
            f"protect recovery that supplies output."
        )
    if ELEMENT_CONTROLS.get(visible_el) == hidden_el:
        return (
            f"{identity}: you regulate inner {hidden_el} through {visible_el} — "
            f"discipline private drives before they surface."
        )
    if ELEMENT_CONTROLS.get(hidden_el) == visible_el:
        return (
            f"{identity}: inner {hidden_el} checks your {visible_el} expression — "
            f"narrow scope before reacting."
        )
    return (
        f"{identity}: visible {visible_el} and hidden {hidden_el} run parallel — "
        f"let {role} timing decide which leads today."
    )


def _chart_interaction_line(
    pillar_name: str,
    visible_el: str,
    hidden_el: str,
    identity: str,
    role_label: str,
) -> str:
    hook = _advice_hook(visible_el, hidden_el, identity, PILLAR_ROLE_LABEL.get(pillar_name, pillar_name))
    prefix = f"{role_label.capitalize()} ({pillar_name} pillar)"
    if hidden_el and visible_el != hidden_el:
        if ELEMENT_GENERATES.get(visible_el) == hidden_el:
            return f"{prefix}: visible {visible_el} generates hidden {hidden_el} — {hook.split('—', 1)[-1].strip()}"
        if ELEMENT_GENERATES.get(hidden_el) == visible_el:
            return f"{prefix}: hidden {hidden_el} generates visible {visible_el} — {hook.split('—', 1)[-1].strip()}"
    return f"{prefix}: {hook}"


def _pillar_card(
    pillar: dict[str, Any],
    *,
    pillar_name: str,
    day_master_el: str,
) -> dict[str, Any]:
    animal = branch_animal(pillar.get("branch", ""))
    display = pillar_hidden_display({**pillar, "branch_en": animal})
    visible_el = pillar.get("stem_element", "")
    hidden_el = display.get("hidden_stem_element", "")
    tg_key = ten_god_role(day_master_el, hidden_el) if hidden_el else ""
    tg_plain = TEN_GOD_PLAIN.get(tg_key, "")
    advice = _advice_hook(visible_el, hidden_el, display["label"], PILLAR_ROLE_LABEL.get(pillar_name, ""))
    if pillar_name == "day" and tg_plain:
        advice = (
            f"{display['label']}: you show {visible_el} outwardly but carry {hidden_el} inside — "
            f"let that {tg_plain} guide a choice you would normally play safe on."
        )
    return {
        "identity": display["label"],
        "display_line": display.get("display_line", display["label"]),
        "gan_zhi": pillar.get("gan_zhi", ""),
        "visible_element": visible_el,
        "branch_animal": animal,
        "hidden": {
            "stem": display.get("hidden_stem", ""),
            "stem_en": display.get("hidden_stem_en", ""),
            "element": hidden_el,
            "role_label": display.get("hidden_role_label", ""),
        },
        "synergy_note": display.get("synergy_note", ""),
        "ten_god_vs_dm": tg_key,
        "ten_god_plain": tg_plain,
        "advice_hook": advice,
        "pillar_role": PILLAR_ROLE_LABEL.get(pillar_name, ""),
    }


def interpret_pillar_synergy(
    pillars: dict[str, Any],
    day_master_el: str,
) -> tuple[list[str], list[str]]:
    """Registry: per-pillar synergy → chart_interactions + advice_directives."""
    interactions: list[str] = []
    directives: list[str] = []
    priority = ("day", "year", "month", "hour")
    for name in priority:
        p = pillars.get(name)
        if not isinstance(p, dict):
            continue
        card = _pillar_card(p, pillar_name=name, day_master_el=day_master_el)
        if card["hidden"]["element"]:
            interactions.append(
                _chart_interaction_line(
                    name,
                    card["visible_element"],
                    card["hidden"]["element"],
                    card["identity"],
                    card["pillar_role"],
                )
            )
        if card["advice_hook"]:
            directives.append(card["advice_hook"])
    return interactions, directives


def interpret_ten_gods(
    pillars: dict[str, Any],
    day_master_el: str,
) -> tuple[list[str], list[str]]:
    """Registry: day-branch Ten God vs Day Master."""
    day = pillars.get("day") or {}
    hidden_el = (root_hidden_stem(day.get("branch", "")) or {}).get("element", "")
    if not hidden_el:
        return [], []
    tg_key = ten_god_role(day_master_el, str(hidden_el))
    tg_advice = TEN_GOD_ADVICE.get(tg_key, "")
    if not tg_advice:
        return [], []
    line = (
        f"Day branch hidden {hidden_el} maps as {tg_key} relative to {day_master_el} Day Master — {tg_advice}."
    )
    return [line], [line]


def interpret_latent_balance(framework: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Registry: weighted 藏干 balance vs surface."""
    latent = (framework.get("hidden_stems") or {}).get("latent_insight", "")
    balance = framework.get("balance_insight", "")
    interactions: list[str] = []
    directives: list[str] = []
    if latent:
        interactions.append(f"Latent element weight: {latent}")
        if "inside" in latent.lower() or "hidden" in latent.lower():
            directives.append(
                "Precision lives inside the chart — schedule proof before you pitch."
            )
    if balance and balance not in interactions:
        interactions.append(balance)
    return interactions, directives


def _sky_activation(
    natal_day: dict[str, str],
    sky_day: dict[str, str],
    *,
    day_master_el: str,
    branch_relation: str | None = None,
) -> dict[str, Any]:
    from app.services.interpretations.bazi_daily_astrology import element_relation

    natal_inner = root_hidden_stem(natal_day.get("branch", ""))
    sky_inner = root_hidden_stem(sky_day.get("branch", ""))
    natal_hidden_el = str((natal_inner or {}).get("element", ""))
    sky_hidden_el = str((sky_inner or {}).get("element", ""))
    el_rel = element_relation(
        natal_day.get("stem_element", ""),
        sky_day.get("stem_element", ""),
    )
    hidden_match = bool(natal_hidden_el and sky_hidden_el and natal_hidden_el == sky_hidden_el)
    activation_note = ""
    if hidden_match:
        activation_note = (
            f"Today's sky stirs your inner {natal_hidden_el.lower()} — "
            f"act on instinct you usually keep private."
        )
    elif branch_relation == "chong_冲":
        activation_note = (
            "A sign clash is active — keep your pace steady and skip fresh arguments."
        )
    elif natal_hidden_el and sky_hidden_el:
        activation_note = (
            f"Sky hides {sky_hidden_el}; track whether today feeds or checks your inner {natal_hidden_el}."
        )
    return {
        "element_relation": el_rel,
        "branch_relation": branch_relation or "",
        "natal_hidden_element": natal_hidden_el,
        "sky_hidden_element": sky_hidden_el,
        "hidden_match": hidden_match,
        "activation_note": activation_note,
    }


# Extensible interpreter registry — append future layers without rewriting consumers.
INTERPRETERS: list[tuple[str, Callable[..., tuple[list[str], list[str]]]]] = [
    ("pillar_synergy", interpret_pillar_synergy),
    ("ten_gods", interpret_ten_gods),
    ("latent_balance", interpret_latent_balance),
    ("luck_pillar", None),  # wired below — needs imprint
]


def build_bazi_interpretation_lens(
    pillars: dict[str, Any],
    *,
    imprint: dict[str, Any] | None = None,
    sky_pillars: dict[str, dict[str, str]] | None = None,
    compares: dict[str, Any] | None = None,
    include_luck: bool = True,
) -> dict[str, Any]:
    """Structured interpretation lens for natal (+ optional sky) BaZi."""
    framework = build_bazi_framework(imprint) if imprint else {}
    dm_el = framework.get("day_master_element") or (pillars.get("day") or {}).get("stem_element", "")
    dm_stem = (pillars.get("day") or {}).get("stem", "")
    dm_facts = (imprint or {}).get("bazi", {}).get("day_master") or {}
    from app.services.chart_accuracy import STEM_META

    dm_meta = STEM_META.get(dm_stem, {})

    pillar_cards = {
        name: _pillar_card(pillars[name], pillar_name=name, day_master_el=dm_el)
        for name in ("year", "month", "day", "hour")
        if isinstance(pillars.get(name), dict)
    }

    chart_interactions: list[str] = []
    advice_directives: list[str] = []
    interpreter_ran: list[str] = []

    from app.services.interpretations.bazi_luck_pillar_lens import interpret_luck_pillar_for_registry

    for key, fn in INTERPRETERS:
        if key == "luck_pillar" and not include_luck:
            continue
        if key == "latent_balance":
            interactions, directives = fn(framework)
        elif key == "luck_pillar":
            interactions, directives = interpret_luck_pillar_for_registry(
                pillars, dm_el, imprint=imprint
            )
        else:
            interactions, directives = fn(pillars, dm_el)
        chart_interactions.extend(interactions)
        if key == "luck_pillar":
            advice_directives = directives + advice_directives
        else:
            advice_directives.extend(directives)
        interpreter_ran.append(key)

    # Deduplicate directives while preserving order
    seen: set[str] = set()
    unique_directives: list[str] = []
    for d in advice_directives:
        if d not in seen:
            seen.add(d)
            unique_directives.append(d)
    advice_directives = unique_directives[:5]

    sky_activation: dict[str, Any] = {}
    if sky_pillars and compares:
        day_cmp = compares.get("day_vs_sky_day") or {}
        sky_activation = {
            "day_vs_natal": _sky_activation(
                pillars.get("day") or {},
                sky_pillars.get("day") or {},
                day_master_el=dm_el,
                branch_relation=day_cmp.get("branch_relation"),
            )
        }
        note = sky_activation["day_vs_natal"].get("activation_note", "")
        if note and note not in advice_directives:
            advice_directives.insert(0, note)
            advice_directives = advice_directives[:4]

    hidden_fw = framework.get("hidden_stems") or {}
    return {
        "version": LENS_VERSION,
        "interpreters": interpreter_ran,
        "day_master": {
            "element": dm_el,
            "stem_en": stem_english(dm_stem),
            "yin_yang": dm_meta.get("yin_yang") or dm_facts.get("yin_yang", ""),
        },
        "balance": {
            "weighted": framework.get("element_balance") or {},
            "surface": hidden_fw.get("surface_balance") or {},
            "strong": framework.get("strong_elements") or [],
            "weak": framework.get("weak_elements") or [],
            "balance_insight": framework.get("balance_insight", ""),
            "latent_insight": hidden_fw.get("latent_insight", ""),
        },
        "pillars": pillar_cards,
        "chart_interactions": chart_interactions[:6],
        "sky_activation": sky_activation,
        "advice_directives": advice_directives,
    }


def compact_bazi_interpretation(lens: dict[str, Any]) -> dict[str, Any]:
    """Compact slice for AI imprint_summary — no Hanzi dump."""
    pillars_compact = {
        name: {
            "identity": card.get("identity"),
            "advice_hook": card.get("advice_hook"),
            "display_line": card.get("display_line"),
        }
        for name, card in (lens.get("pillars") or {}).items()
    }
    return {
        "version": lens.get("version"),
        "day_master_element": (lens.get("day_master") or {}).get("element"),
        "balance_insight": (lens.get("balance") or {}).get("balance_insight"),
        "latent_insight": (lens.get("balance") or {}).get("latent_insight"),
        "pillars": pillars_compact,
        "chart_interactions": (lens.get("chart_interactions") or [])[:3],
        "advice_directives": (lens.get("advice_directives") or [])[:3],
        "current_luck_pillar": _compact_luck(lens.get("luck_pillar")),
    }


def _compact_luck(luck: dict[str, Any] | None) -> dict[str, Any]:
    if not luck:
        return {}
    current = luck.get("current") or {}
    return {
        "identity": current.get("identity"),
        "gan_zhi": current.get("gan_zhi"),
        "advice_citation": current.get("advice_citation"),
        "phase_label": current.get("phase_label"),
        "alignment_summary": (luck.get("alignment_with_natal") or {}).get("summary"),
    }


def distill_daily_bazi_advice(
    lens: dict[str, Any],
    *,
    primary_sky_advice: str,
) -> str:
    """Daily card: 1–2 plain English sentences from lens + sky tone."""
    directives = list(lens.get("advice_directives") or [])
    luck_pillar = lens.get("luck_pillar") or {}
    luck_citation = (luck_pillar.get("current") or {}).get("advice_citation", "")

    luck_line = ""
    for d in directives:
        if d.startswith("Your current luck pillar suggests"):
            luck_line = d
            break
    if not luck_line and luck_citation:
        luck_line = luck_citation

    day_card = (lens.get("pillars") or {}).get("day") or {}
    day_hook = day_card.get("advice_hook", "")
    hidden_line = ""
    for d in directives:
        if "outwardly" in d or "inside" in d or "inner" in d.lower():
            hidden_line = d
            break
    if not hidden_line and day_hook:
        hidden_line = day_hook

    parts: list[str] = []
    if luck_line:
        parts.append(luck_line.rstrip("."))
    elif primary_sky_advice:
        parts.append(primary_sky_advice.rstrip("."))
    if hidden_line and hidden_line not in parts:
        parts.append(hidden_line.rstrip("."))

    if not parts:
        return primary_sky_advice
    if len(parts) == 1:
        return parts[0] + "."
    return ". ".join(parts[:2]) + "."