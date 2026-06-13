"""
Life-domain counsel from the sealed chart — career (incl. ownership), relationship, daily.
Astrology + numerology synthesized once per domain; no repeated blocks from the numerology sections.
"""

from __future__ import annotations

from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.name_field_occult import work_lane_for_seal

# Lean chart keys — full sentences live here, not in numerology blocks
_SUN_ROLE: dict[str, str] = {
    "Aries": "lead offers",
    "Taurus": "asset-backed offers",
    "Gemini": "information products",
    "Cancer": "care and shelter offers",
    "Leo": "visible brand",
    "Virgo": "systems and QA",
    "Libra": "design and fair deals",
    "Scorpio": "transformation and leverage",
    "Sagittarius": "teaching and travel",
    "Capricorn": "institutions",
    "Aquarius": "tech and networks",
    "Pisces": "art and healing with contracts",
}

_OWNERSHIP_STRONG_FINALS = {1, 8, 5, 22}
_OWNERSHIP_COMPOUNDS = {1, 8, 10, 19, 22, 27, 35, 44}
_EMPLOYMENT_STRONG_FINALS = {2, 4, 6, 7}
_DAY_EL_BUSINESS: dict[str, str] = {
    "Wood": "agency, coaching, or growth studio",
    "Fire": "brand, media, or sales-led venture",
    "Earth": "operations, property, food, or care business",
    "Metal": "consulting, law, finance, or precision trade shop",
    "Water": "research, logistics, or advisory practice",
}

_COMPOUND_OWNERSHIP: dict[int, str] = {
    27: "Yes — own a standards-based practice (ops, care, food, shelter, closure consulting). Invoice cycles; do not nonprofit-martyr.",
    1: "Strong yes — named-credit venture; you wither as permanent #2.",
    8: "Strong yes — executive shop, holding company, or institution you command.",
    22: "Yes at scale — phased build; partners and brick before blueprint fantasy.",
    10: "Yes after one earned win — wheel turns against empty promotion.",
    19: "Yes with solar brand — visibility must follow substance.",
    13: "Yes through reinvention businesses — expect periodic rebirth of the offer.",
    4: "Build inside, then own — franchise, trade, or ops firm after apprenticeship.",
    2: "Partnership-first — co-founder or boutique duo; solo headline drains you.",
    6: "Hearth business — design, wellness, food, family brand; boundaries in the contract.",
    7: "Specialist practice — research, analyst, therapist lane; not mass-market hustle.",
}


def _glyph(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    return get_compound_entry(lp["compound"], lp["value"], lp["display"])["glyph"]


def _ownership_score(facts: dict[str, Any]) -> tuple[int, list[str], list[str]]:
    lp = facts["life_path"]
    expr = facts.get("expression", {})
    soul = facts.get("soul_urge", {})
    h10 = facts["vedic_house_10"]["sign"]
    el = facts["day_master"]["element"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    score = 0
    own: list[str] = []
    emp: list[str] = []

    if lp["value"] in _OWNERSHIP_STRONG_FINALS:
        score += 2
        own.append(f"life path final {lp['value']} wants command")
    if lp["compound"] in _OWNERSHIP_COMPOUNDS:
        score += 2
        own.append(f"birth compound {lp['compound']} ({_glyph(facts)}) builds authority")
    if expr.get("value") in _OWNERSHIP_STRONG_FINALS:
        score += 1
        own.append(f"expression {expr.get('display')} markets leadership")
    if soul.get("value") in _EMPLOYMENT_STRONG_FINALS:
        score -= 1
        emp.append(f"soul {soul.get('display')} craves dyad or hearth, not solo throne")
    if h10 in ("Leo", "Aries", "Capricorn", "Scorpio"):
        score += 1
        own.append(f"10th in {h10} — public name tied to command or transformation")
    if h10 in ("Virgo", "Pisces", "Cancer"):
        emp.append(f"10th in {h10} — excel as expert, healer, or protector inside a structure first")
    if el in ("Earth", "Metal"):
        score += 1
        own.append(f"{el} day master compounds tangible systems ({_DAY_EL_BUSINESS[el]})")
    if day_an in ("Rooster", "Ox", "Dragon"):
        score += 1
        own.append(f"{day_an} day — precision or endurance suits owning the standard")
    if day_an in ("Rabbit", "Goat"):
        emp.append(f"{day_an} day — partnership or aesthetic studio often beats solo grind")

    return score, own, emp


def build_career_section(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    glyph = _glyph(facts)
    expr = facts.get("expression", {})
    soul = facts.get("soul_urge", {})
    bday = facts.get("birthday_number", {})
    dm = facts["day_master"]
    el = dm["element"]
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    h2 = facts["vedic_house_2"]["sign"]
    h10 = facts["seal_house_10"]["sign"]
    score, own_r, emp_r = _ownership_score(facts)

    if score >= 4:
        verdict = "Chart favors OWNING — employment should be a bridge, not the destination."
    elif score <= 1:
        verdict = "Chart favors MASTERING inside strong structures — own later, or as a side entity."
    else:
        verdict = "Hybrid — build expertise on payroll, then spin a bounded practice when the offer is yours."

    own_line = _COMPOUND_OWNERSHIP.get(lp["compound"]) or _COMPOUND_OWNERSHIP.get(
        lp["value"], "Follow compound + 10th house, not generic path copy."
    )

    fields: list[str] = []
    lane = work_lane_for_seal(facts)
    fields.append(lane)
    fields.append(f"Sun {sun}: {_SUN_ROLE.get(sun, 'aligned offers')}.")
    fields.append(f"10th house {h10}: reputation as {({'Libra': 'diplomat/designer', 'Scorpio': 'power broker/transformer', 'Virgo': 'expert fixer', 'Cancer': 'protector', 'Leo': 'visible lead', 'Capricorn': 'institution builder', 'Gemini': 'messenger/writer', 'Taurus': 'luxury/builder', 'Aries': 'pioneer', 'Sagittarius': 'teacher-explorer', 'Aquarius': 'innovator', 'Pisces': 'artist-healer'}).get(h10, h10)}.")
    fields.append(f"Vedic 2nd ({h2}): income through {({'Scorpio': 'leverage and clean crisis skill', 'Libra': 'partners and design decisions', 'Virgo': 'skill at scale', 'Taurus': 'tangible slow builds', 'Gemini': 'multiple streams — pick one', 'Cancer': 'home/food/care', 'Leo': 'visibility', 'Capricorn': 'late solidity', 'Aquarius': 'networks/tech', 'Pisces': 'art/healing with boundaries', 'Aries': 'leading the offer', 'Sagittarius': 'teaching/travel with proof'}).get(h2, h2)}.")
    if expr.get("display") and expr["compound"] != lp["compound"]:
        e = get_compound_entry(expr["compound"], expr["value"], expr["display"])
        fields.append(f"Brand math {expr['display']} ({e['glyph']}): public face must match how you sell — not the birth compound alone.")
    if soul.get("display"):
        s = get_compound_entry(soul["compound"], soul["value"], soul["display"])
        fields.append(f"Private hunger {soul['display']} ({s['glyph']}): choose partners and schedules that feed this or you quit.")
    if bday.get("display"):
        b = get_compound_entry(bday["compound"], bday["value"], bday["display"])
        fields.append(f"Birth-day {bday['display']} ({b['glyph']}): monthly skill refresh on day {facts.get('birth_day', '—')} — use for craft, not identity drift.")

    avoid = {
        27: "rescuing clients without contracts, unpaid cycle-closing, ugly exits that stain Libra fairness",
        9: "generic helper roles with no closure authority",
        1: "permanent assistant roles",
        6: "fixing adults as a business model",
    }.get(lp["compound"], f"roles that contradict {el} day work and {h10} reputation")

    lines = [
        f"Birth current {lp['display']} ({glyph}) + {dm['english']} {el} + rising {asc}.",
        f"Ownership: {verdict}",
        own_line,
    ]
    if own_r:
        lines.append("Signals for owning: " + "; ".join(own_r) + ".")
    if emp_r:
        lines.append("Signals for employment first: " + "; ".join(emp_r) + ".")
    lines.append("Fields to excel in (synthesized): " + " · ".join(fields[:5]))
    lines.append(f"Avoid: {avoid}.")
    dasha = (facts.get("mahadasha") or {}).get("lord")
    if dasha:
        from app.services.babylon_lore import DASHA_SEASON

        lines.append(
            f"Mahadasha season of {dasha}: {DASHA_SEASON.get(dasha, 'this lord colors timing and consequence')}. "
            f"Career moves now must respect that weather — not only {glyph}."
        )
    return "\n".join(lines)


def build_relationship_section(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    glyph = _glyph(facts)
    soul = facts.get("soul_urge", {})
    expr = facts.get("expression", {})
    moon = facts["moon"]
    h7 = facts["vedic_house_7"]["sign"]
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")

    bond_style = {
        "Aries": "direct fire — games collapse trust",
        "Libra": "equals and documented fairness",
        "Scorpio": "depth and financial honesty",
        "Virgo": "acts of service — critique must stay kind",
        "Taurus": "loyalty shown in matter",
        "Gemini": "mental spark — boredom is the exit",
        "Cancer": "emotional safety and nest",
        "Leo": "mutual admiration",
        "Capricorn": "respect for ambition and time",
        "Aquarius": "friendship and mental space",
        "Pisces": "clarity — confusion is the enemy",
        "Sagittarius": "freedom with honest promises",
    }.get(h7, h7)

    moon_need = {
        "Virgo": "order, sleep, and repair after conflict",
        "Scorpio": "one vault of full truth",
        "Libra": "fast repair — silence rots",
        "Cancer": "belonging, not performance",
        "Gemini": "private journal before public talk",
        "Leo": "felt value daily",
        "Pisces": "alone time after absorbing others",
    }.get(moon["western_sign"], "steady rhythm")

    lines = [
        f"7th house {h7}: partnership style — {bond_style}.",
        f"Moon {moon['western_sign']} ({moon.get('nakshatra', '')}): needs {moon_need}.",
        f"Sun {sun} + rising {asc}: you enter bonds with {({'Libra': 'charm that must decide', 'Scorpio': 'intensity that must soften after trust', 'Virgo': 'helpfulness that must not fix', 'Leo': 'pride that must share stage', 'Gemini': 'talk that must listen', 'Cancer': 'warmth with boundaries', 'Aries': 'speed with a pause', 'Taurus': 'calm with honest push', 'Sagittarius': 'hope with follow-through', 'Capricorn': 'professional mask with chosen heart', 'Aquarius': 'difference with emotional reach', 'Pisces': 'gentleness with clear no'}).get(asc, asc)}.",
    ]
    if soul.get("display"):
        s = get_compound_entry(soul["compound"], soul["value"], soul["display"])
        lines.append(
            f"Soul {soul['display']} ({s['glyph']}): private appetite in love — "
            f"partners must not force you to perform only {lp['display']} in the bedroom of the soul."
        )
    if expr.get("display") and expr.get("value") != soul.get("value"):
        lines.append(f"Public name {expr['display']} vs soul {soul.get('display', '—')}: what you advertise and what you need must be negotiated early.")
    if yz != day_an:
        lines.append(
            f"Year {yz} vs day {day_an}: you attract {yz} types publicly but run {day_an} in daily intimacy — choose partners who honor the day animal."
        )
    if lp["compound"] == 27:
        lines.append(
            f"{glyph}: do not romance rescue — love is fair closure and standards, not carrying someone's unfinished book."
        )
    elif lp["compound"] == 18:
        lines.append(f"{glyph}: grief and mood cycles need witness, not fixers.")
    moon = facts["moon"]
    if moon.get("nakshatra"):
        from app.services.interpretations.occult_insight_corpus import teach_nakshatra

        lines.append(
            f"Sidereal Moon / {moon['nakshatra']}: {teach_nakshatra(moon['nakshatra'], moon.get('nakshatra_pada'))}"
        )
    return "\n".join(lines)


def build_daily_section(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    glyph = _glyph(facts)
    dm = facts["day_master"]
    el = dm["element"]
    daily = {
        "Wood": ("one growth task with a deadline", "tools/education", "cut one dead project"),
        "Fire": ("one visible pitch or publish", "marketing only with ROI", "rest after heat"),
        "Earth": ("one ops brick — invoice, meal prep, property tick", "save before spend", "sleep/meals on time"),
        "Metal": ("one contract or cut", "quality once", "declutter one drawer"),
        "Water": ("one research block before deciding", "reserves untouched", "walk before reply"),
    }.get(el, ("one concrete task", "pause spends", "single focus block"))
    bday = facts.get("birthday_number", {})
    uy = facts.get("universal_year", {}).get("value")
    py = facts.get("personal_year", {}).get("value")

    lines = [
        f"Daily spine: {dm['english']} {el} day — {glyph} ({lp['display']}) is the authority, not mood.",
        f"This week: {daily[0]}.",
        f"Money rhythm: {daily[1]}.",
        f"Energy: {daily[2]}.",
    ]
    if bday.get("display"):
        lines.append(
            f"On the {facts.get('birth_day', '—')} of each month (birth-day {bday['display']}): reset one habit tied to hearth or craft — details in name-field section."
        )
    if uy:
        from app.services.overview_lore import UNIVERSAL_YEAR_MEANING

        lines.append(
            f"Universal year {uy}: {UNIVERSAL_YEAR_MEANING.get(uy, 'world-year tone presses all seals')}"
        )
    if py:
        from app.services.overview_lore import LIFE_PATH_MEANING

        lines.append(
            f"Personal year {py}: private calendar — {LIFE_PATH_MEANING.get(py, 'one chapter for the year')}"
        )
    lines.append("Paid daily layer compares today's sky to this seal — use it for timing, not to replace the birth compound.")
    return "\n".join(lines)


def build_domain_actions(facts: dict[str, Any]) -> list[str]:
    lp = facts["life_path"]
    glyph = _glyph(facts)
    el = facts["day_master"]["element"]
    score, _, _ = _ownership_score(facts)
    lines = []

    if score >= 4:
        lines.append("Career: draft one offer only you can sign — price, deliverable, deadline — even if you still have a job.")
    else:
        lines.append("Career: ship one visible win inside your current structure before debating ownership.")
    lines.append(f"Relationship: one boundary sentence using 7th-house {facts['vedic_house_7']['sign']} fairness — say it, do not imply.")
    lines.append(f"Daily: one {el} brick — {({'Earth': 'invoice or standard', 'Metal': 'contract line', 'Fire': 'pitch', 'Water': 'research hour', 'Wood': 'growth metric'}).get(el, 'task')}.")
    if lp["compound"] != lp["value"]:
        lines.append(f"When tired: pause before {glyph} signs, spends, or rescues.")
    return lines