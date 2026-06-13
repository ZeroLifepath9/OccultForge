"""
How chart factors fit together — plain cause-and-effect from sealed facts.
"""

from __future__ import annotations

from typing import Any

from app.services.imprint_labels import combined_pillar_label
from app.services.interpretations.manifestation_voice import manifest_animal, manifest_pillar_element
from app.services.priest_overview import VEDIC_HOUSE_ROLE


def interaction_map(facts: dict[str, Any], tradition: str, imprint: dict[str, Any] | None = None) -> str:
    builders = {
        "bazi": lambda: _bazi_map(facts, imprint),
        "numerology": lambda: _numerology_map(facts),
        "vedic": lambda: _vedic_map(facts),
        "hellenistic": lambda: _hellenistic_map(facts),
        "financial": lambda: _financial_map(facts),
        "wealth": lambda: _wealth_map(facts, imprint),
        "relationships": lambda: _relationships_map(facts),
        "combination": lambda: _combination_map(facts),
    }
    return builders.get(tradition, lambda: _combination_map(facts))()


def _bazi_map(facts: dict[str, Any], imprint: dict[str, Any] | None) -> str:
    from app.services.bazi_enrich import ensure_bazi_canonical

    yz = facts["year_zodiac"]
    pillars = facts["pillars"]
    dm = facts["day_master"]
    month_el = pillars["month"].get("stem_element", "")
    hour_an = pillars["hour"].get("branch_animal", "")
    day_an = pillars["day"].get("branch_animal", "")
    lens = {}
    if imprint:
        lens = ensure_bazi_canonical(imprint).get("bazi", {}).get("interpretation_lens") or {}
    lens_pillars = lens.get("pillars") or {}

    lines = [
        f"Year {yz.get('element', '')} {yz['animal']} is the background you grew up in — family mood and first impressions.",
        f"Month {month_el or '—'} is your working-years weather — how bosses and industries respond to you.",
        f"Day {dm['yin_yang']} {dm['element']} ({dm['english']}) with {day_an} branch is your daily self — Tuesday morning, not the zodiac on your ID.",
        f"Hour {hour_an} is off-stage you — late nights, private drive, recovery pace.",
    ]
    for key in ("year", "month", "day", "hour"):
        card = lens_pillars.get(key) or {}
        if card.get("display_line") and card.get("display_line") != card.get("identity"):
            lines.append(f"{key.capitalize()} pillar layer: {card['display_line']} — {card.get('advice_hook', '')}")
    if imprint:
        year = imprint["bazi"]["pillars"]["year"]
        day = imprint["bazi"]["pillars"]["day"]
        lines.append(
            f"Year pillar {combined_pillar_label(year, year_style=True)} sets the room; "
            f"day pillar {combined_pillar_label(day)} is who walks through it."
        )
    luck = ensure_bazi_canonical(imprint).get("bazi", {}).get("luck", {}).get("interpretation") or {}
    luck_current = luck.get("current") or {}
    if luck_current.get("advice_citation"):
        lines.append(luck_current["advice_citation"])
    align = (luck.get("alignment_with_natal") or {}).get("summary", "")
    if align:
        lines.append(align)
    interaction = (lens.get("chart_interactions") or [""])[0]
    if interaction and interaction not in lines:
        lines.append(interaction)
    lines.append(
        "When year and day agree, life feels like tailwind. When they clash, you are often tired from wearing two stories — adjust pace, not identity."
    )
    return "\n".join(lines)


def _numerology_map(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    bday = facts.get("birthday_number") or {}
    pers = facts.get("personality") or {}

    roles: list[str] = [f"life path {lp['display']} is the main road"]
    if expr.get("value"):
        if expr["compound"] == lp["compound"]:
            roles.append("expression doubles that same current in public")
        elif expr["value"] == lp["value"]:
            roles.append(f"expression shares final {lp['value']} with a different color")
        else:
            roles.append(f"expression {expr['display']} markets differently than birth {lp['display']}")
    if soul.get("value") and soul["value"] != lp["value"]:
        roles.append(f"soul urge {soul['display']} wants what birth {lp['display']} earns slowly")
    if pers.get("value") and pers["compound"] != lp["compound"]:
        roles.append(f"personality {pers['display']} is the armor strangers meet first")
    if bday.get("value"):
        roles.append(f"birth-day {bday['display']} returns monthly on day {facts.get('birth_day', '—')}")

    tension = ""
    if expr.get("value") and soul.get("value") and expr["value"] != soul["value"]:
        tension = f" Public {expr['display']} and private {soul['display']} share one calendar — that is where resentment usually starts."
    return "; ".join(roles).capitalize() + "." + tension


def _vedic_map(facts: dict[str, Any]) -> str:
    from app.services.interpretations.vedic_house_sign_engine import build_vedic_interpretation_lens, interpret_lagna

    lagna = facts["ascendant"].get("vedic_lagna") or facts["ascendant"]["western_sign"]
    moon = facts["moon"]
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    vedic_lens = build_vedic_interpretation_lens(facts)
    lagna_body = interpret_lagna(lagna) if lagna else ""
    wealth = vedic_lens.get("wealth") or {}
    partnership = vedic_lens.get("partnership") or {}
    career = vedic_lens.get("career") or {}
    mask = vedic_lens.get("tropical_mask") or ""
    return (
        f"{lagna_body} Moon in {moon.get('nakshatra', '')} is private hunger. "
        f"Mahadasha {dasha} is the chapter you are in now. "
        f"{wealth.get('weave', '')} {partnership.get('weave', '')} {career.get('weave', '')} "
        f"{mask}"
    ).strip()


def _hellenistic_map(facts: dict[str, Any]) -> str:
    asc = facts["ascendant"]["western_sign"]
    sun = facts["sun_sign"]
    moon = facts["moon"]["western_sign"]
    mc = (facts.get("western_angles") or {}).get("midheaven", {}).get("sign", "")
    fit = (
        f"Ascendant {asc} opens the door. Sun {sun} is what you keep pushing for. Moon {moon} is what you need after."
    )
    if mc:
        fit += f" Midheaven {mc} is what people say about you later."
    if sun == asc:
        fit += " Sun and Ascendant agree — intensity is the pattern."
    else:
        fit += f" Sun in {sun} and {asc} rising tell different stories at first — first impression is not the whole plot."
    return fit


def _financial_map(facts: dict[str, Any]) -> str:
    wp = facts.get("western_planets") or {}
    jup = wp.get("Jupiter", {}).get("sign", "")
    sat = wp.get("Saturn", {}).get("sign", "")
    ven = wp.get("Venus", {}).get("sign", "")
    mar = wp.get("Mars", {}).get("sign", "")
    return (
        f"Jupiter in {jup} inflates appetite and margin. Saturn in {sat} brings paperwork and patience. "
        f"Venus in {ven} and Mars in {mar} price what you want and how hard you push. "
        f"Your personal boom-bust rhythm is mostly Jupiter talking to Saturn."
    )


def _wealth_map(facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    if imprint:
        from app.services.interpretations.wealth_chart_lens import build_wealth_chart_lens

        return build_wealth_chart_lens(imprint).get("condensed", "")
    dm = facts["day_master"]
    h2 = facts["vedic_house_2"]["sign"]
    lp = facts["life_path"]
    bday = facts.get("birthday_number") or {}
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    return (
        f"Vehicle: life path {lp['display']} + birth-day {bday.get('display', '—')} supersede timing. "
        f"Road: {dm['yin_yang']} {dm['element']} Day Master; {day_an} day pillar sets wealth cheat code. "
        f"2nd house {h2} is where money enters or stalls."
    )


def _relationships_map(facts: dict[str, Any]) -> str:
    h7 = facts["vedic_house_7"]["sign"]
    h10 = facts["vedic_house_10"]["sign"]
    h2 = facts["vedic_house_2"]["sign"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    moon = facts["moon"]
    return (
        f"7th {h7}: intimate and contract bonds. 10th {h10}: mentors, rivals, public reputation. "
        f"2nd {h2}: shared values. Moon {moon.get('western_sign', '')} / {moon.get('nakshatra', '')}: emotional hunger. "
        f"Year {yz} is first charm; day {day_an} is month-three reality — {manifest_animal(day_an).split('.')[0]}."
    )


def _combination_map(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    lp = facts["life_path"]
    yz = facts["year_zodiac"]
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    return (
        f"BaZi {yz['animal']} + {dm['element']} day master is body weather. "
        f"Western {sun} Sun + {asc} rising is will and first impression. "
        f"Numerology {lp['display']} is the finish you keep returning to. "
        f"One person, several lenses."
    )