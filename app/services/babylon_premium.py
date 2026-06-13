"""Premium-depth layers — numerology, road, career, enemies (full occult flush)."""

from __future__ import annotations

from typing import Any

from app.services.babylon_lore import CHALDEAN_DIGIT, SIGN_CHALDEAN_BRIDGE, SIGN_NUMBER
from app.services.imprint_labels import numerology_display
from app.services.numerology_depth import (
    COMPOUND_STAR_ANGEL,
    PATH_ALIGNED,
    PATH_ALLIES,
    PATH_CONS,
    PATH_MISALIGNED,
    PATH_PROS,
    build_vow_chapter,
    compound_star_angel_lore,
)
from app.services.overview_lore import (
    COMPOUND_PRESSURE,
    DAY_MASTER_WEALTH,
    EXPRESSION_OCCULT,
    HOUSE_2_WALK,
    HOUSE_10_WALK,
    LIFE_PATH_MEANING,
    LIFE_PATH_TRIAL,
    LIFE_PATH_TRIUMPH,
    WESTERN_SIGN_ELEMENT,
    build_compound_reflects,
)

# Chinese branch clash (六冲) — enemy animal gates
BRANCH_CLASH: dict[str, str] = {
    "Rat": "Horse",
    "Horse": "Rat",
    "Ox": "Goat",
    "Goat": "Ox",
    "Tiger": "Monkey",
    "Monkey": "Tiger",
    "Rabbit": "Rooster",
    "Rooster": "Rabbit",
    "Dragon": "Dog",
    "Dog": "Dragon",
    "Snake": "Pig",
    "Pig": "Snake",
}

WESTERN_OPPOSITE: dict[str, str] = {
    "Aries": "Libra",
    "Taurus": "Scorpio",
    "Gemini": "Sagittarius",
    "Cancer": "Capricorn",
    "Leo": "Aquarius",
    "Virgo": "Pisces",
    "Libra": "Aries",
    "Scorpio": "Taurus",
    "Sagittarius": "Gemini",
    "Capricorn": "Cancer",
    "Aquarius": "Leo",
    "Pisces": "Virgo",
}

CAREER_BY_PATH: dict[int, str] = {
    1: "founder, commander, inventor, any field requiring a head that will not bow — failure when you hire yourself out forever",
    2: "mediator, therapist, diplomat, co-founder — failure when you decide alone out of fear",
    3: "orator, artist, media, sales through language — failure when you hide the gift",
    4: "builder, engineer, accountant, operations — failure when you chase flash over foundation",
    5: "trader, pilot, journalist, consultant at crossroads — failure when you sign without truth",
    6: "designer, healer, teacher of home, aesthetic authority — failure when care becomes control",
    7: "researcher, occultist, analyst, monk-capitalist — failure when you never publish the finding",
    8: "executive, banker, developer, magistrate of resources — failure when conscience exits",
    9: "closer, philanthropist, hospice industries, legacy arts — failure when you rescue instead of release",
    11: "prophet-product, inventor, nervous-system industries — failure when ungrounded",
    22: "infrastructure, civilization-scale builds — failure when the body is not trained for scale",
    33: "master teacher, healer-priest — failure when boundaries dissolve",
}

DASHA_CAREER: dict[str, str] = {
    "Ketu": "strip careers built only on ornament — spiritual tech, audit, reduction industries rise",
    "Venus": "beauty, treaty, luxury, diplomacy, design — purse opens through charm rightly used",
    "Sun": "visibility trades — leadership, government-facing brands, father-themes in office",
    "Moon": "public feeling — food, shelter, mothers, crowds, tidal markets",
    "Mars": "strike industries — surgery, sport, war-room roles, courage monetized",
    "Rahu": "foreign systems — tech disruption, scandal recovery, obsession monetized",
    "Jupiter": "law, teaching, expansion capital — counsel others pay for",
    "Saturn": "institution, bone, delay-as-strategy — mastery late, respected long",
    "Mercury": "trade, speech, data — wit as survival, brokerage, writing",
}


def build_numerology_premium(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    ch = facts["chaldean"]
    py_bday = facts["birthday_number"]
    soul = facts.get("soul_urge", {})
    pers = facts.get("personality", {})
    expr = facts["expression"]
    sun_n = facts["sun_sign_number"]

    star = compound_star_angel_lore(c, f)
    c_press = COMPOUND_PRESSURE.get(c, "raw birth-date weight before the god-number settles")
    f_mean = LIFE_PATH_MEANING.get(f, "initiatory road")

    weave = build_compound_reflects(facts)
    vow = build_vow_chapter(facts)

    if c == f:
        compound_deep = (
            f"COMPOUND AND PATH ARE ONE — {disp}. {star} "
            f"Occult pressure on the flesh: {c_press} "
            f"There is no separate 'argument' between body and vow — only discipline. "
            f"When you drift, you are not fighting a compound; you are refusing the single gate."
        )
    else:
        compound_deep = (
            f"COMPOUND {c} BEFORE PATH {disp}. This is the central war of your numerology. "
            f"{star} "
            f"Compound occult law: {c_press} "
            f"The compound is the unreduced birth-date field — hungers, debts, and performances written "
            f"before the soul's final reduction to {f}. You will feel {c} in crisis: how you spend, seduce, "
            f"quit, or rage when unmonitored. The path {f} is the priest's assignment: {f_mean} "
            f"You are not allowed to preach {f} while funding {c} forever — the tablet calls fraud on that life."
        )

    ch_path = ch["life_path"]
    ch_expr = ch["expression"]
    ch_bday = ch["birthday"]

    chaldean_block = (
        f"CHALDEAN TABLET (nine absent from letters — name math differs from day math). "
        f"Birth-date field {numerology_display(ch_path)}: {CHALDEAN_DIGIT.get(f, 'guarded digit')}. "
        f"Name-field {numerology_display(ch_expr)} ({ch_expr['value']}): "
        f"{CHALDEAN_DIGIT.get(ch_expr['value'], 'guarded digit')}. "
        f"Day-of-month {numerology_display(ch_bday)}: "
        f"{CHALDEAN_DIGIT.get(ch_bday['value'], 'guarded digit')} — the daily pulse under the life vow. "
        f"When Chaldean name and Pythagorean expression diverge, you live two public truths; markets read the name, "
        f"temples read the day."
    )

    pyth_block = ""
    if soul.get("display"):
        pyth_block += (
            f" Soul-urge {soul['display']} — private appetite when alone; what you chase without audience. "
        )
    if pers.get("display"):
        pyth_block += (
            f" Personality {pers['display']} — how strangers contract you before intimacy. "
        )
    if py_bday.get("display"):
        pyth_block += (
            f" Pythagorean birthday {py_bday['display']} — gift and wound of the birth-day itself, "
            f"not the full path sum. "
        )
    if expr.get("display"):
        pyth_block += (
            f" Expression {expr['display']}: {EXPRESSION_OCCULT.get(expr['value'], 'name as public fate')}. "
        )

    sign_block = (
        f"Solar sign-number {sun_n}: {SIGN_CHALDEAN_BRIDGE.get(sun_n, 'zodiac seal on the will')}. "
        f"The sign-number must agree with path {f} or every promotion feels like theft."
    )

    gift_price = (
        f"GIFT WHEN THE VOW IS OWNED: {PATH_PROS.get(f, '')} "
        f"PRICE WHEN REFUSED: {PATH_CONS.get(f, '')} "
        f"TRIAL ON THE ROAD: {LIFE_PATH_TRIAL.get(f, '')} "
        f"TRIUMPH WHEN INTEGRATED: {LIFE_PATH_TRIUMPH.get(f, '')}"
    )

    allies = PATH_ALLIES.get(f, "friendly and enemy number-fields guarded")

    return (
        f"THE VOW — NUMEROLOGY WITHOUT VEIL.\n"
        f"{compound_deep}\n"
        f"{weave}\n"
        f"{vow}\n"
        f"{chaldean_block}{pyth_block}{sign_block}\n"
        f"{gift_price}\n"
        f"NUMBER FIELD (allies and enemies): {allies}"
    )


def build_road_premium(facts: dict[str, Any]) -> str:
    f = facts["life_path"]["value"]
    disp = facts["life_path"]["display"]
    c = facts["life_path"]["compound"]
    dm = facts["day_master"]

    steps = [
        f"1) Breathe the final {f} daily — not the compound {c} — until the body stops performing the old argument.",
        f"2) Earn and cut as {dm['yin_yang']} {dm['element']} — refuse careers that make you perform another element's myth.",
        f"3) {PATH_ALIGNED.get(f, 'Walk aligned with your path')}",
        f"4) Guard against: {PATH_MISALIGNED.get(f, 'the drift your path warns')}",
        f"5) Partner and schedule with your friendly numbers; treat enemy-field numbers as high-risk contracts.",
    ]
    if c != f:
        steps.insert(
            1,
            f"1b) Starve compound {c} behaviors explicitly — name them when they rise; the tablet says they are not you, only residue.",
        )

    return (
        f"THE ROAD CALLED — path {disp}.\n"
        f"The priests do not suggest this; they command it for ascent: "
        + " ".join(steps)
        + f" Integration looks like: {LIFE_PATH_TRIUMPH.get(f, 'the vow owned')}. "
        f"Refusal looks like: {LIFE_PATH_TRIAL.get(f, 'the vow resisted')} — you already know which rooms repeat."
    )


def build_career_premium(facts: dict[str, Any]) -> str:
    f = facts["life_path"]["value"]
    dm = facts["day_master"]
    m = facts["pillars"]["month"]
    h2 = facts["vedic_house_2"]
    h10 = facts["vedic_house_10"]
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    expr = facts.get("expression", {})

    p2 = ", ".join(h2["planets"]) if h2.get("planets") else "silent"
    p10 = ", ".join(h10["planets"]) if h10.get("planets") else "silent"

    return (
        f"CAREER AND CROWN — explicit.\n"
        f"Life-path vocation: {CAREER_BY_PATH.get(f, 'walk your path in any trade that obeys it')}. "
        f"Day master {dm['english']} {dm['yin_yang']} {dm['element']}: {DAY_MASTER_WEALTH.get(dm['element'], '')} "
        f"Month {m['stem_element']} {m['branch_animal']} seasons the decade — work rises when you honor "
        f"{m['stem_element']} corridors even if the world demands another pace. "
        f"Vedic sustenance (2nd in {h2['sign']}): {HOUSE_2_WALK.get(h2['sign'], '')}; grahas: {p2}. "
        f"Public crown (10th in {h10['sign']}): {HOUSE_10_WALK.get(h10['sign'], '')}; grahas: {p10}. "
        f"Running Maha {dasha}: {DASHA_CAREER.get(dasha, 'the planetary season tints every offer')}. "
        f"Name-field {expr.get('display', '—')}: {EXPRESSION_OCCULT.get(expr.get('value', 0), 'how the market titles you')}. "
        f"The tablet says: earn as {dm['element']}, bank in the rhythm of the 2nd house, "
        f"build reputation as the 10th demands — never swap them or self-sabotage follows within two cycles."
    )


def build_enemies_premium(facts: dict[str, Any]) -> str:
    f = facts["life_path"]["value"]
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    moon_s = facts["moon"]["sidereal_sign"]

    opp = WESTERN_OPPOSITE.get(sun, "the axis sign")
    asc_opp = WESTERN_OPPOSITE.get(asc, "the axis at the gate")
    year_clash = BRANCH_CLASH.get(yz, "")
    day_clash = BRANCH_CLASH.get(day_an, "")

    clash_lines = []
    if year_clash:
        clash_lines.append(
            f"Blood-year {yz} clashes {year_clash} — people and years bearing {year_clash} weather "
            f"trigger 冲 rupture unless consciously integrated."
        )
    if day_clash and day_clash != year_clash:
        clash_lines.append(
            f"Day body {day_an} clashes {day_clash} — intimate timing and partners with {day_clash} "
            f"energy fatigue the sovereign blade."
        )

    return (
        f"ENEMIES — NUMBERS, SIGNS, GATES.\n"
        f"Numerology: {PATH_ALLIES.get(f, '')} "
        f"Treat enemy-field numbers as contracts that invoice your path — not forbidden, but expensive. "
        f"Western: Sun in {sun} opposes {opp} — the will meets its mirror-enemy in people and seasons of {opp}. "
        f"Ascendant {asc} opposes {asc_opp} — the costume fights {asc_opp} gates in the room. "
        f"Sidereal Moon in {moon_s} — emotional enemies often wear {WESTERN_OPPOSITE.get(moon_s, 'opposite')} "
        f"or square-element weather. "
        f"Eastern clash: {' '.join(clash_lines) if clash_lines else 'no branch clash on record — still respect element enemies'}. "
        f"Do not confuse ally charm with vow-alignment — the friendly number can still waste your decade if the path is betrayed."
    )