"""BaZi (Four Pillars) via lunar_python."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from lunar_python import Solar

STEM_ELEMENTS = {
    "甲": "Wood", "乙": "Wood",
    "丙": "Fire", "丁": "Fire",
    "戊": "Earth", "己": "Earth",
    "庚": "Metal", "辛": "Metal",
    "壬": "Water", "癸": "Water",
}

BRANCH_ELEMENTS = {
    "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood",
    "辰": "Earth", "巳": "Fire", "午": "Fire", "未": "Earth",
    "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water",
}

BRANCH_ANIMAL = {
    "子": "Rat", "丑": "Ox", "寅": "Tiger", "卯": "Rabbit",
    "辰": "Dragon", "巳": "Snake", "午": "Horse", "未": "Goat",
    "申": "Monkey", "酉": "Rooster", "戌": "Dog", "亥": "Pig",
}

STEM_PINYIN = {
    "甲": "Jia", "乙": "Yi", "丙": "Bing", "丁": "Ding",
    "戊": "Wu", "己": "Ji", "庚": "Geng", "辛": "Xin",
    "壬": "Ren", "癸": "Gui",
}


def year_zodiac_from_pillars(pillars: dict[str, Any]) -> dict[str, Any]:
    """Birth-year Chinese zodiac: visible stem element + branch animal; 藏干 root for display."""
    from app.services.interpretations.bazi_hidden_stems import root_hidden_stem

    y = pillars["year"]
    stem = y["stem"]
    branch = y["branch"]
    element = y["stem_element"]
    animal = BRANCH_ANIMAL.get(branch, "")
    root = root_hidden_stem(branch) or {}
    hidden_el = root.get("element", "")
    hidden_en = root.get("stem_en", "")
    hidden_stem = root.get("stem", "")
    identity_label = f"{element} {animal}"
    branch_hidden_label = f"{hidden_el} {animal}".strip() if hidden_el else ""
    return {
        "gan_zhi": y["gan_zhi"],
        "stem": stem,
        "branch": branch,
        "stem_element": element,
        "animal": animal,
        "label": identity_label,
        "hidden_stem": hidden_stem,
        "hidden_stem_en": hidden_en,
        "hidden_stem_element": hidden_el,
        "branch_hidden_label": branch_hidden_label,
        "hidden_label": branch_hidden_label,
        "stem_english": STEM_PINYIN.get(stem, stem),
        "rule": "year_heavenly_stem_element_plus_year_earthly_branch_animal",
    }


def _pillar(stem: str, branch: str) -> dict[str, Any]:
    from app.services.interpretations.bazi_hidden_stems import attach_hidden_stems_to_pillar

    return attach_hidden_stems_to_pillar({
        "stem": stem,
        "branch": branch,
        "gan_zhi": f"{stem}{branch}",
        "stem_element": STEM_ELEMENTS.get(stem, ""),
        "branch_element": BRANCH_ELEMENTS.get(branch, ""),
    })


def compute_bazi(
    birth_local: datetime,
    *,
    gender: str = "male",
) -> dict[str, Any]:
    solar = Solar.fromYmdHms(
        birth_local.year,
        birth_local.month,
        birth_local.day,
        birth_local.hour,
        birth_local.minute,
        birth_local.second,
    )
    lunar = solar.getLunar()
    ec = lunar.getEightChar()

    pillars = {
        "year": _pillar(ec.getYearGan(), ec.getYearZhi()),
        "month": _pillar(ec.getMonthGan(), ec.getMonthZhi()),
        "day": _pillar(ec.getDayGan(), ec.getDayZhi()),
        "hour": _pillar(ec.getTimeGan(), ec.getTimeZhi()),
    }

    day_master = pillars["day"]["stem"]
    elements: dict[str, int] = {}
    for p in pillars.values():
        for key in ("stem_element", "branch_element"):
            el = p[key]
            if el:
                elements[el] = elements.get(el, 0) + 1

    from app.calculators.bazi_luck import build_luck_timeline, luck_pillars_legacy_list, resolve_luck_for_date
    from datetime import date

    g = "female" if gender == "female" else "male"
    luck = build_luck_timeline(ec, gender=g)  # type: ignore[arg-type]
    luck = resolve_luck_for_date(luck, birth_local.year, date.today())
    da_yun = luck_pillars_legacy_list(luck)

    return {
        "pillars": pillars,
        "year_zodiac": year_zodiac_from_pillars(pillars),
        "day_master": {
            "stem": day_master,
            "element": STEM_ELEMENTS.get(day_master, ""),
        },
        "element_balance": elements,
        "luck": luck,
        "luck_pillars": da_yun,
        "solar_reference": solar.toYmdHms(),
    }