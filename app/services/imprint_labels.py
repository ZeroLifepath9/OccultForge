"""English display labels for chart facts (symbols preserved where useful)."""

from __future__ import annotations

from typing import Any

STEM_PINYIN: dict[str, str] = {
    "甲": "Jia",
    "乙": "Yi",
    "丙": "Bing",
    "丁": "Ding",
    "戊": "Wu",
    "己": "Ji",
    "庚": "Geng",
    "辛": "Xin",
    "壬": "Ren",
    "癸": "Gui",
}

BRANCH_ANIMAL: dict[str, str] = {
    "子": "Rat",
    "丑": "Ox",
    "寅": "Tiger",
    "卯": "Rabbit",
    "辰": "Dragon",
    "巳": "Snake",
    "午": "Horse",
    "未": "Goat",
    "申": "Monkey",
    "酉": "Rooster",
    "戌": "Dog",
    "亥": "Pig",
}

HOUSE_THEMES: dict[int, str] = {
    1: "Self & body",
    2: "Wealth & values",
    3: "Courage & kin",
    4: "Home & root",
    5: "Creation & risk",
    6: "Service & health",
    7: "Union & open enemies",
    8: "Depth & shared resources",
    9: "Belief & long road",
    10: "Crown & vocation",
    11: "Allies & gains",
    12: "Exile & dissolution",
}


def numerology_display(num: dict[str, Any]) -> str:
    """Compound/final form e.g. 27/9."""
    compound = num.get("compound")
    value = num.get("value")
    if compound is None or value is None:
        return "—"
    if compound == value:
        return str(value)
    return f"{compound}/{value}"


def stem_english(stem: str) -> str:
    return STEM_PINYIN.get(stem, stem)


def branch_animal(branch: str) -> str:
    return BRANCH_ANIMAL.get(branch, branch)


def pillar_english(pillar: dict[str, Any]) -> dict[str, str]:
    stem = pillar.get("stem", "")
    branch = pillar.get("branch", "")
    return {
        "stem_hanzi": stem,
        "stem_english": stem_english(stem),
        "branch_hanzi": branch,
        "branch_animal": branch_animal(branch),
        "gan_zhi": pillar.get("gan_zhi", f"{stem}{branch}"),
        "stem_element": pillar.get("stem_element", ""),
        "branch_element": pillar.get("branch_element", ""),
    }


def combined_pillar_label(pillar: dict[str, Any], *, year_style: bool = False) -> str:
    """English label: Yin Metal Goat (stem polarity + element + branch animal)."""
    from app.services.chart_accuracy import STEM_META

    stem = pillar.get("stem", "")
    branch = pillar.get("branch", "")
    meta = STEM_META.get(stem, {})
    el = pillar.get("stem_element") or meta.get("element", "")
    animal = branch_animal(branch)
    if year_style:
        return f"{el} {animal}".strip()
    yy = meta.get("yin_yang", "")
    if yy and el:
        return f"{yy} {el} {animal}"
    if el:
        return f"{el} {animal}"
    return animal or "—"


def _seal_house_line(imprint: dict[str, Any], house_num: int) -> dict[str, Any]:
    from app.services.interpretations.seal_houses import seal_house_line

    return seal_house_line(imprint, house_num)


def vedic_house_line(houses: list[dict[str, Any]], house_num: int) -> dict[str, Any]:
    row = next((h for h in houses if h.get("house") == house_num), None)
    if not row:
        return {"house": house_num, "theme": HOUSE_THEMES.get(house_num, ""), "sign": "—", "planets": []}
    return {
        "house": house_num,
        "theme": HOUSE_THEMES.get(house_num, f"House {house_num}"),
        "sign": row.get("sign", "—"),
        "planets": row.get("planets") or [],
    }


def gan_zhi_english(gan_zhi: str) -> str:
    if not gan_zhi or len(gan_zhi) < 2:
        return gan_zhi or "—"
    stem, branch = gan_zhi[0], gan_zhi[-1]
    return f"{stem_english(stem)} {branch_animal(branch)}"


def _day_master_facts(dm: dict[str, Any]) -> dict[str, Any]:
    from app.services.chart_accuracy import STEM_META

    stem = dm["stem"]
    meta = STEM_META.get(stem, {})
    return {
        "hanzi": stem,
        "english": meta.get("english", stem_english(stem)),
        "element": dm["element"],
        "yin_yang": meta.get("yin_yang", ""),
        "polarity": meta.get("note", ""),
    }


def build_display_bundle(imprint: dict[str, Any]) -> dict[str, Any]:
    from datetime import datetime

    from app.services.chart_accuracy import build_chart_anchor
    from app.services.overview_lore import add_calendar_numerology

    bazi = imprint["bazi"]
    year_p = pillar_english(bazi["pillars"]["year"])
    day_p = pillar_english(bazi["pillars"]["day"])
    dm = bazi["day_master"]
    western = imprint["western"]
    vedic = imprint["vedic"]
    py = imprint["numerology"]["schools"]["pythagorean"]
    ch = imprint["numerology"]["schools"]["chaldean"]
    from app.services.babylon_lore import SIGN_NUMBER

    birth_dt = datetime.fromisoformat(
        imprint["birth"]["datetime_local"].replace("Z", "")
    )
    pillars = bazi["pillars"]
    facts = {
        "pillars": {
            k: pillar_english(pillars[k]) for k in ("year", "month", "day", "hour")
        },
        "element_balance": bazi.get("element_balance") or {},
        "day_master": _day_master_facts(dm),
        "year_zodiac": {
            "animal": year_p["branch_animal"],
            "branch_hanzi": year_p["branch_hanzi"],
            "element": year_p["stem_element"],
            "pillar_english": f"{year_p['stem_english']} {year_p['branch_animal']}",
            "gan_zhi": year_p["gan_zhi"],
        },
        "day_pillar": day_p,
        "moon": {
            "western_sign": western["planets"]["Moon"]["sign"],
            "sidereal_sign": vedic["planets"]["Moon"]["sign"],
            "nakshatra": vedic["moon_nakshatra"]["name"],
            "nakshatra_pada": vedic["moon_nakshatra"]["pada"],
        },
        "ascendant": {
            "western_sign": western["angles"]["ascendant"]["sign"],
            "vedic_lagna": vedic["lagna"]["sign"],
        },
        "sun_sign": western["planets"]["Sun"]["sign"],
        "vedic_houses": [vedic_house_line(vedic["houses"], n) for n in range(1, 13)],
        "vedic_house_1": vedic_house_line(vedic["houses"], 1),
        "vedic_house_2": vedic_house_line(vedic["houses"], 2),
        "vedic_house_7": vedic_house_line(vedic["houses"], 7),
        "vedic_house_10": vedic_house_line(vedic["houses"], 10),
        "seal_house_2": _seal_house_line(imprint, 2),
        "seal_house_7": _seal_house_line(imprint, 7),
        "seal_house_10": _seal_house_line(imprint, 10),
        "vedic_planets": {
            k: {"sign": v["sign"], "degree": v.get("degree")}
            for k, v in vedic["planets"].items()
        },
        "mahadasha": vedic["dasha"]["active_mahadasha"],
        "chaldean": {
            "expression": {
                "compound": ch["expression"]["compound"],
                "value": ch["expression"]["value"],
                "display": numerology_display(ch["expression"]),
            },
            "birthday": {
                "compound": ch["birthday"]["compound"],
                "value": ch["birthday"]["value"],
                "display": numerology_display(ch["birthday"]),
            },
            "life_path": {
                "compound": py["life_path"]["compound"],
                "value": py["life_path"]["value"],
                "display": numerology_display(py["life_path"]),
                "note": "Birth-date field; Chaldean and Pythagorean share the day sum.",
            },
        },
        "sun_sign_number": SIGN_NUMBER.get(western["planets"]["Sun"]["sign"], 0),
        "ascendant_sign_number": SIGN_NUMBER.get(western["angles"]["ascendant"]["sign"], 0),
        "life_path": {
            "compound": py["life_path"]["compound"],
            "value": py["life_path"]["value"],
            "display": numerology_display(py["life_path"]),
            "is_master": py["life_path"].get("is_master", False),
        },
        "expression": {
            "compound": py["expression"]["compound"],
            "value": py["expression"]["value"],
            "display": numerology_display(py["expression"]),
        },
        "soul_urge": {
            "compound": py["soul_urge"]["compound"],
            "value": py["soul_urge"]["value"],
            "display": numerology_display(py["soul_urge"]),
        },
        "personality": {
            "compound": py["personality"]["compound"],
            "value": py["personality"]["value"],
            "display": numerology_display(py["personality"]),
        },
        "birthday_number": {
            "compound": py["birthday"]["compound"],
            "value": py["birthday"]["value"],
            "display": numerology_display(py["birthday"]),
        },
    }
    facts["birth_day"] = birth_dt.day
    add_calendar_numerology(facts, birth_dt.date())
    facts["western_planets"] = {
        k: {
            "sign": v["sign"],
            "degree": v.get("degree"),
            "longitude": v.get("longitude"),
        }
        for k, v in western["planets"].items()
    }
    facts["western_angles"] = {
        "ascendant": western["angles"]["ascendant"],
        "midheaven": western["angles"]["midheaven"],
    }
    facts["birth"] = {
        "datetime_local": imprint["birth"].get("datetime_local", ""),
        "place": imprint["birth"].get("place", ""),
        "timezone": imprint["birth"].get("timezone", ""),
    }
    facts["chart_anchor"] = build_chart_anchor(imprint, facts)
    return facts