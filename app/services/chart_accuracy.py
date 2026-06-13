"""Verifiable chart anchors — day master vs year animal, stem truth, audit checks."""

from __future__ import annotations

from typing import Any

from app.services.imprint_labels import branch_animal, pillar_english, stem_english

STEM_META: dict[str, dict[str, str]] = {
    "甲": {"english": "Jia", "yin_yang": "Yang", "element": "Wood", "note": "yang wood — upward thrust"},
    "乙": {"english": "Yi", "yin_yang": "Yin", "element": "Wood", "note": "yin wood — vine, bend, persuade"},
    "丙": {"english": "Bing", "yin_yang": "Yang", "element": "Fire", "note": "yang fire — sun, broadcast"},
    "丁": {"english": "Ding", "yin_yang": "Yin", "element": "Fire", "note": "yin fire — candle, focus"},
    "戊": {"english": "Wu", "yin_yang": "Yang", "element": "Earth", "note": "yang earth — mountain, hold"},
    "己": {"english": "Ji", "yin_yang": "Yin", "element": "Earth", "note": "yin earth — soil, receive"},
    "庚": {
        "english": "Geng",
        "yin_yang": "Yang",
        "element": "Metal",
        "note": "yang metal — blade, axe, cut outward; NOT the same soul as Ji metal",
    },
    "辛": {"english": "Xin", "yin_yang": "Yin", "element": "Metal", "note": "yin metal — jewel, refine, inward edge"},
    "壬": {"english": "Ren", "yin_yang": "Yang", "element": "Water", "note": "yang water — river, flood"},
    "癸": {"english": "Gui", "yin_yang": "Yin", "element": "Water", "note": "yin water — rain, seep"},
}


def _pillar_anchor(pillar: dict[str, Any]) -> dict[str, Any]:
    pe = pillar_english(pillar)
    stem = pillar.get("stem", "")
    meta = STEM_META.get(stem, {})
    return {
        "gan_zhi": pe["gan_zhi"],
        "stem_hanzi": stem,
        "branch_hanzi": pillar.get("branch", ""),
        "stem_english": pe["stem_english"],
        "branch_animal": pe["branch_animal"],
        "stem_element": pe["stem_element"],
        "yin_yang": meta.get("yin_yang", ""),
        "stem_note": meta.get("note", ""),
    }


def verify_imprint_bazi(imprint: dict[str, Any]) -> list[dict[str, Any]]:
    """Machine checks so overview lore cannot drift from computed pillars."""
    bazi = imprint["bazi"]
    pillars = bazi["pillars"]
    dm = bazi["day_master"]
    checks: list[dict[str, Any]] = []

    def add(rule: str, passed: bool, detail: str) -> None:
        checks.append({"rule": rule, "pass": passed, "detail": detail})

    add(
        "day_master_is_day_stem",
        dm["stem"] == pillars["day"]["stem"],
        f"day_master {dm['stem']} vs day pillar stem {pillars['day']['stem']}",
    )
    add(
        "day_master_element_matches_stem_table",
        dm["element"] == STEM_META.get(dm["stem"], {}).get("element", dm["element"]),
        f"element {dm['element']}",
    )
    for key in ("year", "month", "day", "hour"):
        p = pillars[key]
        add(
            f"pillar_{key}_gan_zhi_consistent",
            p.get("gan_zhi") == f"{p.get('stem')}{p.get('branch')}",
            p.get("gan_zhi", ""),
        )
    year = pillars["year"]
    year_animal = branch_animal(year["branch"])
    year_el = STEM_META.get(year["stem"], {}).get("element", year.get("stem_element"))
    add(
        "year_stem_element_table",
        year.get("stem_element") == year_el,
        f"stem {year['stem']} -> {year.get('stem_element')} (expected {year_el})",
    )
    yz = bazi.get("year_zodiac") or {}
    expected_label = f"{year.get('stem_element')} {year_animal}"
    add(
        "year_zodiac_label",
        yz.get("label") == expected_label,
        f"label {yz.get('label')} vs {expected_label}",
    )
    add(
        "year_zodiac_not_day_master",
        yz.get("stem_element") == year.get("stem_element"),
        "year zodiac element must be year stem, not day master",
    )
    return checks


def build_chart_anchor(imprint: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    """Canonical labels + confusion notes (e.g. Rooster year vs Goat day)."""
    bazi = imprint["bazi"]
    pillars = bazi["pillars"]
    day = _pillar_anchor(pillars["day"])
    year = _pillar_anchor(pillars["year"])
    dm_stem = bazi["day_master"]["stem"]
    meta = STEM_META.get(dm_stem, {})
    year_animal = facts["year_zodiac"]["animal"]
    day_animal = day["branch_animal"]
    year_el = year.get("stem_element") or facts["year_zodiac"].get("element", "")

    environment_note = (
        f"Year environment: {year_el} {year_animal} ({year['gan_zhi']}). "
        f"Day storm: {meta.get('yin_yang', '')} {meta.get('element', '')} {meta.get('english', '')} stem "
        f"with {day_animal} branch ({day['gan_zhi']}). Environment sets the field; day stem and branch are the force."
    )
    if year_animal != day_animal:
        environment_note += (
            f" Year and day animals differ ({year_animal} environment, {day_animal} storm) — "
            "read both; the year is the room, the day pillar is how you move through it."
        )
    if dm_stem == "庚":
        environment_note += (
            " Geng 庚 is Yang Metal — blade outward. Ji 己 is Yin Metal — refine inward. Same family, opposite polarity."
        )
    elif dm_stem == "己":
        environment_note += (
            " Ji 己 is Yin Metal — refine inward. Geng 庚 is Yang Metal — blade outward. Same family, opposite polarity."
        )

    checks = verify_imprint_bazi(imprint)
    all_pass = all(c["pass"] for c in checks)

    return {
        "verified": all_pass,
        "engine": "lunar_python.EightChar",
        "birth_local": imprint["birth"].get("datetime_local"),
        "timezone": imprint["birth"].get("timezone"),
        "accuracy_note": (
            "Charts are computed from sealed birth date, time, and place timezone. "
            "Wrong birth time shifts hour pillar and can shift day pillar near midnight."
        ),
        "day_master": {
            "hanzi": dm_stem,
            "english": meta.get("english", stem_english(dm_stem)),
            "yin_yang": meta.get("yin_yang", ""),
            "element": meta.get("element", bazi["day_master"]["element"]),
            "polarity": meta.get("note", ""),
        },
        "day_pillar": day,
        "year_pillar": year,
        "year_zodiac_popular": year_animal,
        "day_branch_animal": day_animal,
        "environment_note": environment_note.strip(),
        "confusion_clarification": environment_note.strip(),
        "checks": checks,
    }