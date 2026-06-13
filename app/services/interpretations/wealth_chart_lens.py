"""Wealth Chart — BaZi day pillar led: day master, hidden root, animal corpus, Vedic synthesis."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo

from lunar_python import Solar

from app.calculators.bazi import BRANCH_ELEMENTS, STEM_ELEMENTS
from app.services.interpretations.bazi_hidden_stems import ELEMENT_CONTROLS, ELEMENT_GENERATES, pillar_hidden_display
from app.services.imprint_labels import branch_animal, stem_english
from app.services.interpretations.numerology_mission_engine import (
    birthday_execution_clause,
    life_path_mission_sentence,
)
from app.services.interpretations.vedic_house_sign_engine import (
    interpret_house_sign,
    interpret_lagna,
    tropical_ascendant_overlay,
)
from app.services.interpretations.wealth_day_pillar_corpus import DAY_PILLAR_WEALTH

YEAR_ELEMENT_ALLIES: dict[str, list[str]] = {
    "Fire": ["Fire", "Water"],
    "Water": ["Water", "Wood"],
    "Wood": ["Wood", "Metal"],
    "Metal": ["Metal", "Fire"],
    "Earth": ["Earth", "Wood"],
}


def _sky_year_pillar(reference: date, timezone: str) -> dict[str, str]:
    tz = ZoneInfo(timezone)
    local_noon = datetime(reference.year, reference.month, reference.day, 12, 0, tzinfo=tz)
    solar = Solar.fromYmdHms(local_noon.year, local_noon.month, local_noon.day, 12, 0, 0)
    ec = solar.getLunar().getEightChar()
    stem = ec.getYearGan()
    branch = ec.getYearZhi()
    return {
        "stem": stem,
        "branch": branch,
        "gan_zhi": f"{stem}{branch}",
        "stem_en": stem_english(stem),
        "branch_en": branch_animal(branch),
        "stem_element": STEM_ELEMENTS.get(stem, ""),
        "branch_element": BRANCH_ELEMENTS.get(branch, ""),
    }


def _climate_insight_prose(dm_element: str, year_element: str, relation: str, aligned: bool) -> str:
    """Element-first money weather — no comparison citations."""
    if not dm_element or not year_element:
        return "Element and modality steer money seasons more than branch animal story alone."
    if relation == "same":
        return (
            f"When sky climate shares your {dm_element} element, branch friction is secondary — "
            f"seasons land on element fit first; ride maintenance and visible craft."
        )
    if relation == "defeats":
        return (
            f"Your {dm_element} defeats hostile sky element this season — obstacles still arrive, "
            f"but even clashing branch years bend easier when element wins the argument. "
            f"Structure beats panic."
        )
    if relation == "pressed":
        return (
            f"Sky element presses your {dm_element} now — slow leverage, protect cash, "
            f"and build before spectacle. Element weather is the headline, not zodiac noise."
        )
    if relation == "output":
        return (
            f"You feed the season through output — ship visible {dm_element} work and let the year consume what you produce."
        )
    if relation == "resource":
        return (
            f"The season feeds your {dm_element} — learning, backing, and maintenance favor inflow; receive before you push alone."
        )
    if aligned:
        return (
            f"Element allies favor your {dm_element} this season — tailwind for money moves that honor your day-master nature."
        )
    return (
        f"Read element before animal — how {dm_element} meets this season's charge decides whether branch story helps or hinders."
    )


def _element_year_climate(dm_element: str, year_element: str) -> dict[str, Any]:
    allies = YEAR_ELEMENT_ALLIES.get(year_element, [year_element])
    aligned = dm_element in allies
    relation = "neutral"
    headline = ""
    if dm_element == year_element:
        relation = "same"
        headline = (
            f"{year_element} year meets your {dm_element} Day Master — element matches climate; "
            f"zodiac friction matters less than element fit."
        )
    elif ELEMENT_CONTROLS.get(dm_element) == year_element:
        relation = "defeats"
        headline = (
            f"Your {dm_element} defeats the year's {year_element} — obstacles still show, "
            f"but even enemy-branch years are easier to beat when element wins."
        )
    elif ELEMENT_CONTROLS.get(year_element) == dm_element:
        relation = "pressed"
        headline = (
            f"The year's {year_element} presses your {dm_element} Day Master — "
            f"build structure, slow leverage, and protect cash before spectacle."
        )
    elif ELEMENT_GENERATES.get(dm_element) == year_element:
        relation = "output"
        headline = (
            f"You feed the {year_element} year through output — earn by shipping visible {dm_element} craft."
        )
    elif ELEMENT_GENERATES.get(year_element) == dm_element:
        relation = "resource"
        headline = (
            f"The {year_element} year feeds your {dm_element} — learning seasons and backing favor maintenance."
        )
    else:
        headline = (
            f"Element is the primary money weather — read {dm_element} against {year_element} before animal story."
        )
    climate_insight = _climate_insight_prose(dm_element, year_element, relation, aligned)
    return {
        "year_element": year_element,
        "day_master_element": dm_element,
        "relation": relation,
        "aligned": aligned,
        "headline": headline,
        "climate_insight": climate_insight,
        "branch_enemy_muted_when_defeats": relation == "defeats",
        "allies_this_year": allies,
    }


def _wealth_root_clause(hidden: dict[str, Any], dm_element: str) -> str:
    hidden_el = hidden.get("hidden_stem_element") or ""
    hidden_en = hidden.get("hidden_stem_en") or ""
    visible_el = hidden.get("stem_element") or ""
    if not hidden_el:
        return ""
    synergy = hidden.get("synergy_note") or ""
    if visible_el == hidden_el:
        return (
            f"Beneath your visible {visible_el} stem, branch root echoes the same charge — "
            f"latent talent and inflow align without translation loss."
        )
    if ELEMENT_GENERATES.get(hidden_el) == visible_el:
        return (
            f"Beneath your {visible_el} day stem, hidden {hidden_en} {hidden_el} feeds the stem — "
            f"quiet reservoir powers public money moves."
        )
    if ELEMENT_GENERATES.get(visible_el) == hidden_el:
        return (
            f"Your {visible_el} stem generates hidden {hidden_el} in the branch — "
            f"outward deals fertilize inner reserves that fund the next season."
        )
    if synergy and "parallel" in synergy.lower():
        return (
            f"Visible {visible_el} and hidden {hidden_el} run parallel tracks — "
            f"activate the root when timing asks for depth beneath the deal."
        )
    return (
        f"Branch root holds {hidden_en} {hidden_el} beneath your {visible_el} stem — "
        f"wealth deepens when you honor what the root supplies, not only the visible stem."
    )


def build_day_pillar_wealth_profile(
    day_pillar: dict[str, str],
    day_master: dict[str, Any],
) -> dict[str, Any]:
    hidden = pillar_hidden_display(day_pillar)
    dm_el = day_master.get("element") or day_pillar.get("stem_element") or ""
    dm_yy = day_master.get("yin_yang") or ""
    return {
        "gan_zhi": day_pillar.get("gan_zhi", ""),
        "stem_en": stem_english(day_pillar.get("stem", "")),
        "stem_element": hidden.get("stem_element") or dm_el,
        "branch_en": hidden.get("branch_en") or branch_animal(day_pillar.get("branch", "")),
        "yin_yang": dm_yy,
        "hidden_stem": hidden.get("hidden_stem", ""),
        "hidden_stem_en": hidden.get("hidden_stem_en", ""),
        "hidden_stem_element": hidden.get("hidden_stem_element", ""),
        "hidden_role_label": hidden.get("hidden_role_label", ""),
        "display_line": hidden.get("display_line", ""),
        "root_clause": _wealth_root_clause(hidden, dm_el),
    }


def synthesize_income_crown(
    vedic_wealth: dict[str, Any],
    vedic_career: dict[str, Any],
    *,
    animal: str,
    spotlight: bool,
) -> str:
    """Weave income and crown lanes without sign or house labels."""
    w_focus = vedic_wealth.get("focus", "what you earn and value")
    c_focus = vedic_career.get("focus", "how you are remembered publicly")
    w_temp = vedic_wealth.get("temperament", "distinct income temperament")
    c_temp = vedic_career.get("temperament", "distinct public temperament")
    w_do = vedic_wealth.get("do", "name what feeds you honestly")
    c_do = vedic_career.get("do", "name how you want to be remembered")
    w_dont = vedic_wealth.get("dont", "")
    c_dont = vedic_career.get("dont", "")

    aligned = w_temp == c_temp or w_temp.split()[-1] == c_temp.split()[-1]
    if spotlight:
        lead = (
            f"Public presence leads — {c_focus} with {c_temp} tone should headline; "
            f"let {w_focus} follow the attention you already command."
        )
    else:
        lead = (
            f"Private architecture leads — build {w_focus} with {w_temp} discipline first; "
            f"let {c_focus} ride the machine you run from center."
        )

    if aligned:
        body = (
            f"Income and crown pull the same direction — {w_do.lower() if w_do else 'honest naming'} "
            f"and {c_do.lower() if c_do else 'public clarity'} compound without splitting your calendar."
        )
    else:
        body = (
            f"Income and crown temperaments differ — earn in the lane that honors {w_temp} rhythm, "
            f"crown in the lane that honors {c_temp} authority; sequence them, never collapse both into one rushed brand."
        )

    guard = ""
    if w_dont or c_dont:
        guard = (
            f" Guard against forcing one lane when the other resists — "
            f"{w_dont or c_dont or 'split focus leaks margin'}."
        )
    return f"{lead} {body}{guard}"


def _modality_note(yin_yang: str) -> str:
    if yin_yang == "Yang":
        return (
            "Yang modality pushes wealth through outward deal-making, visible bids, and direct initiative."
        )
    if yin_yang == "Yin":
        return (
            "Yin modality accumulates through timing, networks, and receptive positioning — "
            "less noise, more negotiated inflow."
        )
    return "Modality sets how seasons of money land across the years."


def _primary_insight(
    *,
    dm_yy: str,
    dm_el: str,
    animal: str,
    animal_profile: dict[str, Any],
    climate_insight: str,
    root_clause: str,
    income_crown: str,
) -> str:
    narrative = animal_profile.get("narrative", "")[:280]
    close = animal_profile.get("close", "")
    parts = [
        f"{dm_yy} {dm_el} Day Master — element steers the season.",
        climate_insight,
        narrative,
        root_clause,
        income_crown[:200] if income_crown else "",
        close,
    ]
    return " ".join(p for p in parts if p).strip()


def _numerology_overlay(imprint: dict[str, Any]) -> dict[str, str]:
    py = imprint["numerology"]["schools"]["pythagorean"]
    lp = py["life_path"]
    bday = py["birthday"]
    compound = lp.get("compound", lp["value"])
    final = lp["value"]
    bday_final = bday["value"]
    return {
        "mission_sentence": life_path_mission_sentence(compound, final),
        "birthday_execution": birthday_execution_clause(bday_final),
    }


def build_wealth_chart_lens(
    imprint: dict[str, Any],
    *,
    reference: date | None = None,
) -> dict[str, Any]:
    """Structured wealth lens: day master + day pillar root + animal narrative + Vedic synthesis."""
    ref = reference or date.today()
    birth = imprint.get("birth") or {}
    tz = birth.get("timezone") or "UTC"
    bazi = imprint.get("bazi") or {}
    pillars = bazi.get("pillars") or {}
    day = pillars.get("day") or {}
    dm = bazi.get("day_master") or {}
    branch = day.get("branch", "")
    animal = day.get("branch_en") or branch_animal(branch)
    dm_el = dm.get("element") or day.get("stem_element") or ""
    dm_yy = dm.get("yin_yang") or ""
    dm_stem = dm.get("english") or stem_english(day.get("stem", ""))

    sky_year = _sky_year_pillar(ref, tz)
    year_el = sky_year.get("stem_element") or ""
    climate = _element_year_climate(dm_el, year_el)
    animal_profile = DAY_PILLAR_WEALTH.get(animal, {})
    day_profile = build_day_pillar_wealth_profile(day, dm)

    numerology = _numerology_overlay(imprint)
    luck = (bazi.get("interpretation_lens") or {}).get("luck_pillar") or {}
    luck_current = luck.get("current") or {}

    from app.services.imprint_labels import build_display_bundle

    facts = build_display_bundle(imprint)
    asc = facts.get("ascendant") or {}
    lagna = asc.get("vedic_lagna") or imprint.get("vedic", {}).get("lagna", {}).get("sign", "")
    tropical = asc.get("western_sign") or ""
    h2_sign = (facts.get("vedic_house_2") or {}).get("sign", "")
    h10_sign = (facts.get("seal_house_10") or {}).get("sign", "")
    vedic_wealth = interpret_house_sign(2, h2_sign) if h2_sign else {}
    vedic_career = interpret_house_sign(10, h10_sign) if h10_sign else {}
    lagna_body = interpret_lagna(lagna) if lagna else ""
    tropical_mask = tropical_ascendant_overlay(lagna, tropical)

    spotlight = bool(animal_profile.get("spotlight", True))
    income_crown = synthesize_income_crown(
        vedic_wealth, vedic_career, animal=animal, spotlight=spotlight
    )
    day_narrative = animal_profile.get("narrative", "")
    primary = _primary_insight(
        dm_yy=dm_yy,
        dm_el=dm_el,
        animal=animal,
        animal_profile=animal_profile,
        climate_insight=climate.get("climate_insight", ""),
        root_clause=day_profile.get("root_clause", ""),
        income_crown=income_crown,
    )

    examples = animal_profile.get("examples") or []
    example_line = examples[0] if examples else animal_profile.get("example")

    return {
        "reference_date": ref.isoformat(),
        "mission_sentence": numerology["mission_sentence"],
        "birthday_execution": numerology["birthday_execution"],
        "day_master": {
            "yin_yang": dm_yy,
            "element": dm_el,
            "stem_en": dm_stem,
            "modality_note": _modality_note(dm_yy),
        },
        "day_pillar_profile": day_profile,
        "element_climate_insight": climate.get("climate_insight", ""),
        "day_pillar_narrative": day_narrative,
        "income_crown_synthesis": income_crown,
        "primary_insight": primary,
        "year_climate": {**climate, "sky_year": sky_year},
        "day_pillar_animal": {
            "animal": animal,
            "gan_zhi": day.get("gan_zhi", ""),
            "example": example_line,
            "examples": examples,
            **animal_profile,
        },
        "luck_citation": luck_current.get("advice_citation", ""),
        "vedic_wealth_lens": vedic_wealth,
        "vedic_career_lens": vedic_career,
        "vedic_wealth_weave": vedic_wealth.get("weave", ""),
        "vedic_career_weave": vedic_career.get("weave", ""),
        "lagna_body": lagna_body,
        "tropical_mask": tropical_mask,
        "condensed": primary[:320],
        "support": animal_profile.get("support", ""),
        "end": animal_profile.get("end", ""),
        "shadow": animal_profile.get("shadow", ""),
    }


def wealth_flow_paragraphs(
    lens: dict[str, Any],
    facts: dict[str, Any],
    imprint: dict[str, Any],
) -> tuple[str, str, str]:
    """Three flow paragraphs — day master + element climate + animal narrative; verify-safe."""
    who = (imprint.get("birth") or {}).get("commonly_known_as") or (imprint.get("birth") or {}).get("name") or "you"
    if isinstance(who, str):
        who = who.strip() or "you"

    dm = lens["day_master"]
    climate = lens["year_climate"]
    animal = lens["day_pillar_animal"]
    mission = lens.get("mission_sentence", "")
    birthday_exec = lens.get("birthday_execution", "")
    root_clause = (lens.get("day_pillar_profile") or {}).get("root_clause", "")
    narrative = lens.get("day_pillar_narrative") or animal.get("narrative", "")
    income_crown = lens.get("income_crown_synthesis", "")
    climate_insight = lens.get("element_climate_insight") or climate.get("climate_insight", "")
    close = animal.get("close", "")
    examples = animal.get("examples") or []
    ex_clause = f" {examples[0]}." if examples else (
        f" {animal['example']}." if animal.get("example") else ""
    )
    vedic_w = lens.get("vedic_wealth_lens") or {}
    vedic_c = lens.get("vedic_career_lens") or {}
    wealth_dont = vedic_w.get("dont", "")
    career_dont = vedic_c.get("dont", "")
    shadow = lens.get("shadow") or animal.get("shadow", "")
    end = lens.get("end") or animal.get("end", "")

    p1 = (
        f"{who}, you are {dm['yin_yang']} {dm['element']} — modality and element steer how money seasons land "
        f"more than branch animal alone. {dm['modality_note']} "
        f"{climate_insight} "
        f"Element beats animal when sky weather turns — that is the best advice on money, career, and success."
    )

    p2 = (
        f"You're strongest when you honor your {animal.get('animal', '')} day pillar architecture. "
        f"{narrative}{ex_clause} "
        f"{root_clause} "
        f"{income_crown} "
        f"{birthday_exec} "
        f"Stay mindful when you split income and crown lanes or chase spectacle before structure."
    )

    p3 = (
        f"What costs you: {shadow}; {wealth_dont}; {career_dont}; {end} "
        f"Chasing lanes your mission never finishes drains the cheat code. "
        f"{mission} "
        f"{close}"
    )
    return p1, p2, p3