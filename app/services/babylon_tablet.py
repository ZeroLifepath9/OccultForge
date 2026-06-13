"""Babylon tablet — premium threshold reading (full occult depth)."""

from __future__ import annotations

from typing import Any

from app.services.babylon_lore import (
    CHALDEAN_DIGIT,
    DASHA_SEASON,
    NAKSHATRA_SCRIPT,
    SIGN_CHALDEAN_BRIDGE,
    SIGN_NUMBER,
)
from app.services.babylon_premium import (
    build_career_premium,
    build_enemies_premium,
    build_numerology_premium,
    build_road_premium,
)
from app.services.imprint_labels import numerology_display
from app.services.overview_lore import (
    ANIMAL_INHERITANCE,
    HOUSE_2_WALK,
    HOUSE_10_WALK,
    LIFE_PATH_MEANING,
    WESTERN_SIGN_ELEMENT,
)

SEAL_MARKER = "walk this path"
OVERVIEW_FORMAT = "babylon-premium"

HOUSE_1_WALK: dict[str, str] = {
    "Aries": "the body arrives as campaign — life opens with rupture",
    "Taurus": "the flesh is bank — stamina, appetite, value in the skin",
    "Gemini": "breath as twin — mind and hand share the gate",
    "Cancer": "shell first — belonging before ambition",
    "Leo": "heart on display — vitality as public fact",
    "Virgo": "service in the marrow — health as ritual",
    "Libra": "balance in the bone — others define you until you choose",
    "Scorpio": "depth in the blood — survival through transformation",
    "Sagittarius": "road in the feet — pilgrimage as posture",
    "Capricorn": "bone as institution — age before youth",
    "Aquarius": "difference in the frame — outsider body",
    "Pisces": "porous skin — spirit leaks into matter",
}

HOUSE_7_WALK: dict[str, str] = {
    "Aries": "partners arrive as sparks — union through conflict",
    "Taurus": "marriage as estate — loyalty measured in matter",
    "Gemini": "contracts of words — duets, duplicates, indecision",
    "Cancer": "union as nest — family law in the mirror",
    "Leo": "throne shared — pride in love, drama as bond",
    "Virgo": "service in partnership — critique as intimacy",
    "Libra": "mirror of justice — beauty as treaty",
    "Scorpio": "oath in shadow — possession, renewal, test",
    "Sagittarius": "beloved as pilgrim — truth in foreign beds",
    "Capricorn": "status as spouse — delay, duty, endurance",
    "Aquarius": "friend as mate — odd contracts of the heart",
    "Pisces": "dissolution in union — mercy, confusion, sacrifice",
}


def build_greeting(name: str) -> str:
    return (
        f"{name}, the tablet is opened. What follows is the full inscription — "
        f"the kind reserved for kings who paid priests to hide nothing. "
        f"Chaldean number, birth-date field, name-field, four pillars, sidereal court, western wheel, "
        f"career, enemies, and the road you are commanded to walk. Read as fact."
    )


def build_bazi_layer(facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    p = facts["pillars"]
    y, m, d, h = p["year"], p["month"], p["day"], p["hour"]
    dm = facts["day_master"]
    yz = facts["year_zodiac"]
    inherit = ANIMAL_INHERITANCE.get(yz["animal"], "ancestral weather presses from behind")
    bal_note = ""
    if imprint:
        from app.services.bazi_enrich import ensure_bazi_canonical

        lens = ensure_bazi_canonical(imprint).get("bazi", {}).get("interpretation_lens") or {}
        balance = (lens.get("balance") or {}).get("balance_insight", "")
        latent = (lens.get("balance") or {}).get("latent_insight", "")
        if balance:
            bal_note = f" {balance}"
        if latent:
            bal_note += f" {latent}"
    else:
        bal = facts.get("element_balance") or {}
        if bal:
            top = max(bal.items(), key=lambda x: x[1])[0]
            bal_note = f" Elemental weight in the pillars runs hot on {top} — compensate or the road buckles."

    return (
        f"THE FOUR GATES (BaZi).\n"
        f"Gate of blood — {y['stem_element']} {y['branch_animal']} ({y['stem_english']} {y['gan_zhi']}): {inherit} "
        f"Prologue only; not the protagonist. "
        f"Gate of season — {m['stem_element']} {m['branch_animal']}: the corridor of your working years; "
        f"promotion and collapse follow {m['stem_element']} law. "
        f"Gate of sovereign day — {d['stem_english']} {d['branch_animal']} ({d['gan_zhi']}): "
        f"{dm['yin_yang']} {dm['element']} ({dm['english']}) is the blade that cuts fate; "
        f"every accurate eastern reading judges this gate first. "
        f"Gate of hidden hour — {h['stem_english']} {h['branch_animal']}: the private engine; "
        f"what you do when the audience leaves explains nights you cannot justify by daylight.{bal_note} "
        f"Year element {yz['element']} colors the myth; day element {dm['element']} colors the body — "
        f"performing only the {yz['animal']} while walking the {d['branch_animal']} day is why others misread you."
    )


def build_vedic_layer(facts: dict[str, Any]) -> str:
    asc = facts["ascendant"]["vedic_lagna"]
    moon = facts["moon"]
    h1 = facts["vedic_house_1"]
    h2 = facts["vedic_house_2"]
    h7 = facts["vedic_house_7"]
    h10 = facts["vedic_house_10"]
    dasha = facts.get("mahadasha") or {}
    lord = dasha.get("lord", "")
    planets = facts.get("vedic_planets") or {}

    nak_line = NAKSHATRA_SCRIPT.get(moon["nakshatra"], "a lunar mansion fixing hunger older than speech")
    p2 = ", ".join(h2["planets"]) if h2.get("planets") else "no graha in the mouth of wealth"
    p10 = ", ".join(h10["planets"]) if h10.get("planets") else "no graha on the public crown"

    align_parts = [
        f"{pname} in {planets[pname]['sign']}"
        for pname in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
        if pname in planets
    ]
    alignment = "; ".join(align_parts)

    return (
        f"THE SIDEREAL COURT (Vedic, Lahiri).\n"
        f"Lagna {asc} — {HOUSE_1_WALK.get(asc, 'body-law')}; the flesh arrives under this sign's verdict. "
        f"Moon {moon['sidereal_sign']} / {moon['nakshatra']} pada {moon.get('nakshatra_pada', '—')}: {nak_line} "
        f"Tropical Moon may narrate {moon['western_sign']}; initiates feed the sidereal hunger. "
        f"2nd house {h2['sign']} — {HOUSE_2_WALK.get(h2['sign'], '')}; grahas: {p2}. "
        f"7th house {h7['sign']} — {HOUSE_7_WALK.get(h7['sign'], '')}; the mirror of contract and enemy-ally in flesh. "
        f"10th house {h10['sign']} — {HOUSE_10_WALK.get(h10['sign'], '')}; grahas: {p10}. "
        f"Maha season {lord} — {DASHA_SEASON.get(lord, 'planetary reign')}. "
        f"Planetary alignment at birth: {alignment}. "
        f"Heaven distributes emphasis: body (1st), purse (2nd), spouse-field (7th), name (10th)."
    )


def build_west_east_layer(facts: dict[str, Any]) -> str:
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    moon_w = facts["moon"]["western_sign"]
    yz = facts["year_zodiac"]
    dm = facts["day_master"]
    sun_el = WESTERN_SIGN_ELEMENT.get(sun, "")
    asc_el = WESTERN_SIGN_ELEMENT.get(asc, "")
    moon_el = WESTERN_SIGN_ELEMENT.get(moon_w, "")

    mask = ""
    if asc != sun:
        mask = (
            f" The room meets {asc} ({asc_el}) before {sun} ({sun_el}); "
            f"you are judged at the gate, crowned by the Sun only after the first room."
        )

    return (
        f"THE WHEELS.\n"
        f"West — Sun {sun} ({sun_el}) will; Ascendant {asc} ({asc_el}) costume; "
        f"Moon {moon_w} ({moon_el}) private myth.{mask} "
        f"East — year {yz['element']} {yz['animal']}; day {dm['yin_yang']} {dm['element']} blade. "
        f"Elements must negotiate or the person tears their own script."
    )


def build_script_layer(facts: dict[str, Any]) -> str:
    f = facts["life_path"]["value"]
    dm = facts["day_master"]
    raw = LIFE_PATH_MEANING.get(f, "initiatory road")
    if "—" in raw:
        raw = raw.split("—", 1)[-1].strip()

    return (
        f"THE PERSON THIS TABLET WRITES.\n"
        f"One protagonist: {dm['yin_yang']} {dm['element']} ({dm['english']}) under vow {facts['life_path']['display']}. "
        f"Curriculum: {raw} "
        f"This is the role cast — not a suggestion. The chart reports; you execute or repeat the same room with new faces."
    )


def build_manifestation_layer(facts: dict[str, Any]) -> str:
    h2 = facts["vedic_house_2"]
    h7 = facts["vedic_house_7"]
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    sun = facts["sun_sign"]
    lp = facts["life_path"]["display"]
    f = facts["life_path"]["value"]

    lines = [
        f"Money obeys the 2nd-house rhythm in {h2['sign']} — not your wish-list.",
        f"Union and open enemies concentrate in the 7th — {h7['sign']} — contracts look like love, war, or treaty accordingly.",
        f"Offers in this decade wear {dasha}'s mask even if you stay still.",
        f"Speech and brand obey name-number and Sun in {sun} — path {lp} funds or punishes every sentence.",
    ]
    if yz != day_an:
        lines.append(
            f"You will be cast for {yz} roles while your constitution is {day_an} — exhaustion in three cycles if you accept."
        )
    lines.append(
        f"When enemy-field numbers or clash animals dominate a partnership, the tablet records breakages — not curses, physics."
    )

    return "MANIFESTATIONS — HOW THE INSCRIPTION SHOWS IN MATTER:\n" + " ".join(lines)


def build_close(name: str) -> str:
    return (
        f"{name}, the premium tablet is sealed at this threshold. "
        f"What you were not taught to ask for is now written: compound war, vow, career, enemies, road. "
        f"Seeker opens the hour-by-hour court where Zero steels each day against this script — "
        f"walk this path knowing the inscription precedes you."
    )


def build_babylon_tablet(facts: dict[str, Any], name: str) -> str:
    blocks = [
        build_greeting(name),
        build_numerology_premium(facts),
        build_road_premium(facts),
        build_career_premium(facts),
        build_enemies_premium(facts),
        build_bazi_layer(facts),
        build_vedic_layer(facts),
        build_west_east_layer(facts),
        build_script_layer(facts),
        build_manifestation_layer(facts),
        build_close(name),
    ]
    return "\n\n".join(blocks)


def build_zero_seal(facts: dict[str, Any], name: str) -> str:
    return build_babylon_tablet(facts, name)


# Legacy layer aliases for briefs
def build_chaldean_layer(facts: dict[str, Any]) -> str:
    return build_numerology_premium(facts)


def build_vow_master(facts: dict[str, Any]) -> str:
    return build_numerology_premium(facts)