"""
Self-check chart readings against sealed imprint facts before display.
"""

from __future__ import annotations

import re
from typing import Any, Callable

from app.services.chart_accuracy import verify_imprint_bazi
from app.services.interpretations.flow_voice import (
    FORBIDDEN_FRAMING,
    FORBIDDEN_GLOSSARY,
    FORBIDDEN_SECTIONS,
    MAX_WORDS_BAZI,
    MAX_WORDS_BOX,
    MAX_WORDS_WESTERN_SETTING,
    MAX_WORDS_EASTERN,
    MAX_WORDS_VEDIC,
    MAX_WORDS_ZERO,
    MIN_WORDS_BOX,
    MIN_WORDS_ZERO,
)
from app.services.imprint_labels import combined_pillar_label
from app.services.interpretations.matrix_decoder_voice import is_matrix_reading

from app.services.interpretations.manifestation_voice import FORBIDDEN_PHRASES


class ChartReadingVerificationError(Exception):
    def __init__(self, system: str, errors: list[str]) -> None:
        self.system = system
        self.errors = errors
        super().__init__(f"{system} reading failed verification: {'; '.join(errors)}")


def _require_in(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle and needle not in text:
        errors.append(f"missing:{label}:{needle}")


def _forbid_in(text: str, phrase: str, errors: list[str]) -> None:
    if phrase.lower() in text.lower():
        errors.append(f"forbidden_framing:{phrase}")


def verify_bazi_reading(narrative: str, facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for check in verify_imprint_bazi(imprint):
        if not check["pass"]:
            errors.append(f"imprint:{check['rule']}:{check['detail']}")

    pillars = imprint["bazi"]["pillars"]
    _require_in(narrative, combined_pillar_label(pillars["year"], year_style=True), "year_pillar", errors)
    _require_in(narrative, combined_pillar_label(pillars["day"]), "day_pillar", errors)

    dm = facts["day_master"]
    day_p = facts.get("day_pillar") or {}
    day_an = day_p.get("branch_animal", "")
    yz = facts["year_zodiac"]

    _require_in(narrative, dm.get("english", ""), "day_master_stem", errors)
    _require_in(narrative, dm.get("yin_yang", ""), "day_master_polarity", errors)
    _require_in(narrative, dm.get("element", ""), "day_master_element", errors)
    _require_in(narrative, day_an, "day_branch_animal", errors)
    _require_in(narrative, yz.get("animal", ""), "year_zodiac_animal", errors)
    _require_in(narrative, "stem", "day_stem_cited", errors)
    _require_in(narrative, "branch", "day_branch_cited", errors)
    _require_in(narrative, "Day Master", "day_master_label", errors)

    low = narrative.lower()
    for forbidden in (
        "nakshatra",
        "jyotish",
        "vedic chapter",
        "sidereal",
        "rising body",
        "mahadasha",
        "life path",
    ):
        if forbidden in low:
            errors.append(f"bazi:overlay:{forbidden.replace(' ', '_')}")

    for phrase in (
        "do not let it override",
        "let the year animal be backdrop",
        "not only your birth year",
        "performing a costume",
        "you are not ",
        "misread when people treat you as only",
    ):
        _forbid_in(narrative, phrase, errors)

    return errors


_NUMEROLOGY_FRAMING = re.compile(
    r"(energy you walk|same (road|final|life path|number)|generic (advice|numerology)|how to get there|story of how|how to walk)",
    re.I,
)


def verify_numerology_panels(panels: dict[str, Any], facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not panels.get("birth_date") or panels["birth_date"] == "—":
        errors.append("missing:birth_date")

    lp = panels.get("life_path") or {}
    facts_lp = facts.get("life_path") or {}
    _require_in(str(lp.get("display", "")), facts_lp.get("display", ""), "panels_life_path", errors)
    if not panels.get("birth_digit_sum") or panels["birth_digit_sum"] == "—":
        errors.append("missing:birth_digit_sum")
    friends = panels.get("friend_numbers") or []
    enemies = panels.get("enemy_numbers") or []
    if not friends:
        errors.append("missing:friend_numbers")
    if not enemies:
        errors.append("missing:enemy_numbers")

    if not panels.get("compound_title"):
        errors.append("missing:compound_title")
    if not panels.get("compound_subtitle"):
        errors.append("missing:compound_subtitle")
    for forbidden in ("compound_definition", "compound_insight", "compound_scale", "chart_archetype"):
        if panels.get(forbidden):
            errors.append(f"forbidden:{forbidden}")

    pi = panels.get("path_insight") or {}
    if pi.get("walk") or pi.get("calling") or pi.get("framing") or pi.get("weaknesses"):
        errors.append("forbidden:path_insight_extra")
    if not pi.get("avatar"):
        errors.append("missing:path_insight:avatar")
    avatar = (pi.get("avatar") or "").lower()
    subtitle = (panels.get("compound_subtitle") or "").lower()
    for token in ("triple 9", "3×3×3", "one hand", "look up", "angel ", "tarot"):
        if token in avatar or token in subtitle:
            errors.append(f"numerology:forbidden_token:{token.strip()}")
    for token in ("unreduced", "vow", "expression triple", "compound first", "strong looks like"):
        if token in avatar:
            errors.append(f"numerology:occult_token_in_avatar:{token}")
    if len(pi.get("avatar") or "") < 80:
        errors.append("numerology:avatar_too_short")

    totals = panels.get("other_totals") or []
    if len(totals) != 4:
        errors.append(f"numerology:other_totals_count:{len(totals)}")
    for row in totals:
        if not row.get("display") or not row.get("advice") or not row.get("path"):
            errors.append(f"missing:other_total:{row.get('key', '?')}")
        if row.get("role") or row.get("meaning") or row.get("shapes_path"):
            errors.append(f"forbidden:other_total_extra:{row.get('key', '?')}")

    return errors


def verify_numerology_reading(narrative: str, facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    lp = facts.get("life_path") or {}
    c = lp.get("compound")
    f = lp.get("value")
    disp = lp.get("display", "")
    _require_in(narrative, disp, "life_path", errors)
    who = (imprint["birth"].get("commonly_known_as") or "").strip() or imprint["birth"]["name"]
    _require_in(narrative, who, "display_name", errors)

    if c is not None and f is not None:
        if c == f:
            if "single gate" not in narrative.lower() and str(c) not in narrative:
                errors.append("missing:compound:single_gate")
        else:
            _require_in(narrative, str(c), "compound_value", errors)

    low = narrative.lower()
    if "your avatar" not in low and not _NUMEROLOGY_FRAMING.search(narrative):
        errors.append("missing:numerology_framing")
    if "friend" not in low or "enem" not in low:
        errors.append("missing:numerology_allies")

    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    pers = facts.get("personality") or {}
    displays = {disp}
    for row in (expr, soul, pers, facts.get("birthday_number") or {}):
        d = row.get("display", "")
        if d and d in narrative:
            displays.add(d)
    if len(displays) > 6:
        errors.append(f"numerology:too_many_displays:{len(displays)}")

    ev = expr.get("value")
    sv = soul.get("value")
    if not (ev and sv and ev != sv):
        while_clauses = len(re.findall(r"\bwhile\b", narrative, re.I))
        if while_clauses > 1:
            errors.append("numerology:gratuitous_cross_compare")

    return errors


def verify_flow_structure(narrative: str, *, combination: bool = False) -> list[str]:
    errors: list[str] = []
    low = narrative.lower()

    for label in FORBIDDEN_SECTIONS:
        for line in narrative.splitlines():
            if line.strip().upper() == label:
                errors.append(f"forbidden_framing:{label}")
                break
    for phrase in FORBIDDEN_FRAMING:
        _forbid_in(narrative, phrase, errors)
    if "·" in narrative:
        errors.append("flow:no_bullets")

    if is_matrix_reading(narrative):
        for section in ("**Direct Answer**", "**Decoded Insight**", "**Action**"):
            _require_in(narrative, section, "matrix_section", errors)
        if combination:
            if "take the blade" not in narrative.lower():
                errors.append("missing:seal_close:take the blade")
        return errors

    if "you are" not in low and "you're" not in low:
        errors.append("flow:missing_declarative_identity")
    if "you're strongest" not in low and "you are strongest" not in low:
        errors.append("flow:missing_strength")
    if "stay mindful" not in low:
        errors.append("flow:missing_mindful")
    if "what costs you" not in low and "what conflicts you" not in low:
        errors.append("flow:missing_conflict")

    if low.count(" is the ") > 4:
        errors.append("flow:too_recitative")

    if combination:
        if "take the blade" not in narrative.lower():
            errors.append("missing:seal_close:take the blade")
    return errors


def verify_flow_voice(
    narrative: str,
    *,
    combination: bool = False,
    eastern_rising: bool = False,
    bazi_forge: bool = False,
    western_setting: bool = False,
    vedic_forge: bool = False,
) -> list[str]:
    errors: list[str] = []
    for phrase in FORBIDDEN_PHRASES + FORBIDDEN_GLOSSARY:
        _forbid_in(narrative, phrase, errors)
    wc = len(narrative.split())
    if bazi_forge:
        min_w, max_w = MIN_WORDS_BOX, MAX_WORDS_BAZI
    elif western_setting:
        min_w, max_w = MIN_WORDS_BOX, MAX_WORDS_WESTERN_SETTING
    elif eastern_rising:
        min_w, max_w = MIN_WORDS_BOX, MAX_WORDS_EASTERN
    elif vedic_forge:
        min_w, max_w = MIN_WORDS_BOX, MAX_WORDS_VEDIC
    elif combination:
        min_w, max_w = MIN_WORDS_ZERO, MAX_WORDS_ZERO
    else:
        min_w, max_w = MIN_WORDS_BOX, MAX_WORDS_BOX
    if wc < min_w:
        errors.append("narrative_too_short")
    if wc > max_w:
        errors.append(f"narrative_too_long:{wc}")
    return errors


def verify_vedic_reading(narrative: str, facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    lagna = imprint["vedic"]["lagna"]["sign"]
    moon = facts.get("moon") or {}
    _require_in(narrative, lagna, "lagna", errors)
    if moon.get("nakshatra"):
        _require_in(narrative, moon["nakshatra"], "nakshatra", errors)
    low = narrative.lower()
    for forbidden in ("pluto", "uranus", "neptune", "life path", "day master", "luck pillar", "ba zi", "bazi"):
        if forbidden in low:
            errors.append(f"vedic:overlay:{forbidden.replace(' ', '_')}")
    if "outer planet" in low or "western" in low and "sidereal" not in low:
        if "outer planet" in low:
            errors.append("vedic:western_overlay")
    return errors


def verify_eastern_rising_reading(narrative: str, facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    dm = facts.get("day_master") or {}
    _require_in(narrative, dm.get("element", ""), "day_master_element", errors)
    _require_in(narrative, "Day Master", "day_master_label", errors)
    moon = facts.get("moon") or {}
    if moon.get("nakshatra"):
        _require_in(narrative, moon["nakshatra"], "nakshatra", errors)
    low = narrative.lower()
    if "gate" not in low and "luck pillar" not in low:
        errors.append("eastern_rising:missing_bazi_framing")
    if "life path" in low:
        errors.append("eastern_rising:numerology_overlay")
    return errors


def verify_western_setting_reading(narrative: str, facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    sun = facts.get("sun_sign") or imprint["western"]["planets"]["Sun"]["sign"]
    moon = facts.get("moon", {}).get("western_sign") or imprint["western"]["planets"]["Moon"]["sign"]
    _require_in(narrative, asc, "ascendant", errors)
    _require_in(narrative, sun, "sun_sign", errors)
    _require_in(narrative, moon, "moon_sign", errors)
    low = narrative.lower()
    for forbidden in (
        "life path",
        "personal year",
        "personal month",
        "personal day",
        "universal year",
        "dasha",
        "mahadasha",
        "nakshatra",
        "jyotish",
        "ba zi",
        "bazi",
        "sky month",
        "luck pillar",
        "day master",
    ):
        if forbidden in low:
            errors.append(f"western_setting:overlay:{forbidden.replace(' ', '_')}")
    return errors


def verify_hellenistic_reading(narrative: str, facts: dict[str, Any], imprint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    _require_in(narrative, asc, "ascendant", errors)
    sun = facts.get("sun_sign") or imprint["western"]["planets"]["Sun"]["sign"]
    _require_in(narrative, sun, "sun_sign", errors)
    return errors


def verify_generic_reading(narrative: str) -> list[str]:
    errors: list[str] = []
    if "look up" in narrative.lower() or "investigate" in narrative.lower():
        errors.append("deferral_language")
    return errors


def verify_chart_reading(
    system: str,
    narrative: str,
    facts: dict[str, Any],
    imprint: dict[str, Any],
    *,
    panels: dict[str, Any] | None = None,
) -> list[str]:
    errors = verify_generic_reading(narrative)
    if system in (
        "numerology",
        "bazi",
        "vedic",
        "hellenistic",
        "financial",
        "wealth",
        "relationships",
        "western_setting",
        "eastern_rising",
    ):
        if system != "numerology":
            errors.extend(verify_flow_structure(narrative))
            if system == "bazi":
                errors.extend(verify_flow_voice(narrative, bazi_forge=True))
            elif system == "western_setting":
                errors.extend(verify_flow_voice(narrative, western_setting=True))
            elif system == "eastern_rising":
                errors.extend(verify_flow_voice(narrative, eastern_rising=True))
            elif system == "vedic":
                errors.extend(verify_flow_voice(narrative, vedic_forge=True))
            else:
                errors.extend(verify_flow_voice(narrative))
    elif system == "combination":
        errors.extend(verify_flow_structure(narrative, combination=True))
        errors.extend(verify_flow_voice(narrative, combination=True))
    if system == "bazi":
        errors.extend(verify_bazi_reading(narrative, facts, imprint))
    elif system == "numerology":
        if panels:
            errors.extend(verify_numerology_panels(panels, facts, imprint))
        errors.extend(verify_numerology_reading(narrative, facts, imprint))
    elif system == "vedic":
        errors.extend(verify_vedic_reading(narrative, facts, imprint))
    elif system == "hellenistic":
        errors.extend(verify_hellenistic_reading(narrative, facts, imprint))
    elif system == "western_setting":
        errors.extend(verify_western_setting_reading(narrative, facts, imprint))
    elif system == "eastern_rising":
        errors.extend(verify_eastern_rising_reading(narrative, facts, imprint))
    return errors


# Back-compat alias for tests
verify_episode_structure = verify_flow_structure


def assert_chart_reading(
    system: str,
    builder: Callable[[], str],
    facts: dict[str, Any],
    imprint: dict[str, Any],
    *,
    panels: dict[str, Any] | None = None,
) -> str:
    first = builder()
    second = builder()
    if first != second:
        raise ChartReadingVerificationError(system, ["non_deterministic:build_mismatch"])

    errors = verify_chart_reading(system, first, facts, imprint, panels=panels)
    if errors:
        raise ChartReadingVerificationError(system, errors)
    return first