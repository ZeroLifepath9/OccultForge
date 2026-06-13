"""Deep interpretive lore for natal overview — Zero voice, blunt and woven."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.calculators.numerology import personal_year, universal_year
from app.services.imprint_labels import numerology_display

LIFE_PATH_MEANING: dict[int, str] = {
    1: "the monad — you were sent to stand alone and name the direction others fear to choose",
    2: "the dyad — your fate is forged in partnership; solitude rots what you came to polish",
    3: "the triad — language is your weapon and your scandal; silence costs more than speech",
    4: "the tetrad — empire from repetition; the gods tax shortcuts with bone-deep fatigue",
    5: "the pentad — change is not adventure for you, it is oxygen; cages make you cruel",
    6: "the hexad — beauty and duty are the same rope; you hang or you heal with it",
    7: "the heptad — knowledge bought with distance; crowds drain what the inner room restores",
    8: "the octad — matter answers to you when conscience leads; gold without spine devours",
    9: "the ennead — endings are your craft; what you release returns as authority",
    11: "master voltage — nervous system of the unseen; not a casual life, a charged one",
    22: "master masonry — blueprint in the sky; the body must catch the vision or break",
    33: "master healing — love as labor; sacrifice without boundaries becomes theft",
}

LIFE_PATH_TRIAL: dict[int, str] = {
    1: "you split allies by refusing the throne; rage when mirrored",
    2: "you dissolve into moods that are not yours; kindness as camouflage",
    3: "you burn bright and leave truth behind; fame without root",
    4: "you harden until joy looks childish; resentment of slower souls",
    5: "you run before you finish; broken oaths, skin that never rests",
    6: "you carry what is not yours; love as invoice",
    7: "you isolate until paranoia feels holy; secrets that sour",
    8: "you build before you forgive; power that buys silence",
    9: "you mourn what you will not bury; savior fatigue",
    11: "you channel without grounding; prophecy that scorches the nerve",
    22: "you architect beyond the spine; collapse when scale exceeds body",
    33: "you pay for the world; martyr scripts",
}

LIFE_PATH_TRIUMPH: dict[int, str] = {
    1: "you claim center without apology — fate stops testing and starts following",
    2: "you choose one mirror and polish it — peace becomes structure",
    3: "you speak what the age needed — art converts noise to congregation",
    4: "you outlast — wealth from sacred repetition, legacy in stone",
    5: "you tell the truth and move — luck after honest risk",
    6: "you make home temple — beauty that repairs lineages",
    7: "you finish initiation — counsel from the inner room",
    8: "you command resources with justice — crown that feeds others",
    9: "you release without amnesia — wisdom offered, not imposed",
    11: "you ground the voltage — intuition that builds",
    22: "you enact the cathedral — world-touching work",
    33: "you discipline compassion — love that teaches ascent",
}

COMPOUND_PRESSURE: dict[int, str] = {
    10: "the unreduced decade — public mask louder than private vow until integrated",
    11: "twin ones before the master — nervous brilliance, fame before root",
    12: "the dozen in the flesh — sacrifice learned before reward",
    13: "death-and-rebirth digit in the body — reinvention as tax",
    14: "movement chained to matter — appetite for change, ledger for consequence",
    15: "magnetism with a shadow price — charm that binds",
    16: "tower pressure — ego stripped by collision; humility or fracture",
    17: "star-seed weight — spiritual hunger before worldly proof",
    18: "power + completion in one skin — endings fund beginnings",
    19: "sun-king compound — visibility before readiness",
    20: "judgment in the flesh — partnerships as courtroom",
    21: "crown before throne — creative force that must mature",
    22: "master number carried raw — masonry before the tools",
    24: "home + crown tension — family law vs public myth",
    27: "nine in triple — compassion as labor, genius as burden",
    29: "master 11 in flesh — voltage without insulation",
    30: "expression triple — voice as fate, scatter as trap",
}

UNIVERSAL_YEAR_MEANING: dict[int, str] = {
    1: "world-year of rupture and seed — what you start fights concrete",
    2: "world-year of delay and alliance — patience is not optional",
    3: "world-year of spectacle — your voice competes with every screen",
    4: "world-year of austerity — sweat visible, shortcuts punished",
    5: "world-year of breakage — travel, scandal, systems open",
    6: "world-year of hearth-law — family and duty renegotiated",
    7: "world-year of veil — secrets surface; research beats hustle",
    8: "world-year of contested crowns — markets judge character",
    9: "world-year of purge — close doors or they close you",
}

DAY_MASTER_WEALTH: dict[str, str] = {
    "Wood": "grow before harvest; cut dead wood quarterly or wealth rots on the vine",
    "Fire": "sell vision first; visibility is currency, impatience is bankruptcy",
    "Earth": "compound slow, own infrastructure; hoarding without rotation breeds decay",
    "Metal": "price the edge — contracts, standards, cuts; blunt force loses",
    "Water": "follow liquidity — timing, information, hidden reserves; never fight the current",
}

HOUSE_2_WALK: dict[str, str] = {
    "Aries": "money arrives when you lead the offer; bleeding when impulse spends for pride",
    "Taurus": "sustenance through what can be touched and held; famine when you rush the soil",
    "Gemini": "twin streams — words, brokerage, parallel trades; loss when you split without focus",
    "Cancer": "wealth through shelter, food, lineage repair; drain when you mother the wrong ledger",
    "Leo": "value performed in public; tax when pride outruns substance",
    "Virgo": "small perfections at scale; poverty when you nitpick instead of ship",
    "Libra": "fair exchange and design; bankruptcy when you please everyone",
    "Scorpio": "leverage, inheritance, crisis craft; ruin when you hoard poison",
    "Sagittarius": "distance, teaching, belief products; waste when you preach without product",
    "Capricorn": "institutional climb; triumph when delay is strategy not fear",
    "Aquarius": "networks, tech, odd contracts; chaos when you rebel without a vault",
    "Pisces": "art, healing, dissolution of debt; drowning when boundaries dissolve",
}

HOUSE_7_WALK: dict[str, str] = {
    "Aries": "partners arrive as sparks — union through conflict; love feels like a duel you are driven to win",
    "Taurus": "marriage as estate — loyalty measured in matter; betrayal is financial before emotional",
    "Gemini": "contracts of words — duets, duplicates, indecision; the enemy wears a charming twin face",
    "Cancer": "union as nest — family law in the mirror; you mother partners or suffocate them",
    "Leo": "throne shared — pride in love, drama as bond; you need worship, not only warmth",
    "Virgo": "service in partnership — critique as intimacy; love looks like fixing until it wounds",
    "Libra": "mirror of justice — beauty as treaty; indecision in love costs more than a wrong yes",
    "Scorpio": "oath in shadow — possession, renewal, test; intimacy is leverage or it is nothing",
    "Sagittarius": "beloved as pilgrim — truth in foreign beds; freedom and commitment war weekly",
    "Capricorn": "status as spouse — delay, duty, endurance; affection arrives late but heavy",
    "Aquarius": "friend as mate — odd contracts of the heart; distance reads as rejection to lovers",
    "Pisces": "dissolution in union — mercy, confusion, sacrifice; boundaries are the only protection",
}

HOUSE_10_WALK: dict[str, str] = {
    "Aries": "public life as campaign — you are seen when you strike, burned when you strike alone",
    "Taurus": "reputation built slow; crown of reliability, trap of stubborn image",
    "Gemini": "many faces in the square — writer, broker, messenger; scatter erodes trust",
    "Cancer": "known as protector — emotional brand; cost when mood governs office",
    "Leo": "stage as office — radiance or ridicule, no middle",
    "Virgo": "craft as name — service precision; invisible when you hide behind perfect",
    "Libra": "diplomat's crown — aesthetic judgment; fall when you avoid the hard verdict",
    "Scorpio": "power behind the title — transformation public; enemies when secrets leak",
    "Sagittarius": "teacher-pilgrim path — truth-teller brand; exile when dogma replaces sight",
    "Capricorn": "institution's spine — authority earned late, respected long",
    "Aquarius": "reformer visible — future-facing myth; isolation when tribe cannot follow",
    "Pisces": "mystic in the market — compassion as brand; erasure when you escape matter",
}

ANIMAL_INHERITANCE: dict[str, str] = {
    "Rat": "ancestral weather: strategic hunger, night mind, survival intelligence pressed into your timing",
    "Ox": "ancestral weather: slow force, loyalty as law, rage when rushed by lesser stakes",
    "Tiger": "ancestral weather: righteous charge, court drama, danger when pride outruns plan",
    "Rabbit": "ancestral weather: grace under surveillance, diplomacy as armor, fracture when cornered",
    "Dragon": "ancestral weather: scale and spectacle — you inherit appetite for magnitude",
    "Snake": "ancestral weather: venom and vision — secrets as inheritance, strike when coiled too long",
    "Horse": "ancestral weather: velocity, open road, broken fences when tamed by small rooms",
    "Goat": "ancestral weather: art, appeasement, melancholy when beauty serves fear",
    "Monkey": "ancestral weather: wit as weapon — improvisation praised, trust thin",
    "Rooster": "ancestral weather: precision, display, cut when criticism becomes vanity",
    "Dog": "ancestral weather: oath-keeper — loyalty noble, suffocation when cause is unworthy",
    "Pig": "ancestral weather: abundance and appetite — generosity that can be farmed by predators",
}

ELEMENT_SEASON: dict[str, str] = {
    "Wood": "social season pushes growth and argument — spring politics in every room",
    "Fire": "social season burns bright — visibility demanded, rest seen as betrayal",
    "Earth": "social season grounds and slows — deals need soil, not spark",
    "Metal": "social season cuts — standards rise, weak alliances fall",
    "Water": "social season flows — information, rumor, and timing trump brute force",
}

HOUR_ENGINE: dict[str, str] = {
    "Rat": "private engine runs at night — strategy, plotting, deals when the world sleeps",
    "Ox": "private engine labors in silence — stamina, resentment if credit is stolen",
    "Tiger": "private engine revolts — solo charges when the mask slips",
    "Rabbit": "private engine retreats — beauty, repair, escape into soft rooms",
    "Dragon": "private engine dreams large — schemes scale when no one watches",
    "Snake": "private engine coils — research, revenge, seduction as calculus",
    "Horse": "private engine gallops — movement as drug, stillness as grief",
    "Goat": "private engine creates — art as survival, mood as weather",
    "Monkey": "private engine improvises — humor, hustle, betrayal of boredom",
    "Rooster": "private engine sharpens — lists, critique, insomnia of standards",
    "Dog": "private engine guards — vigilance, burnout when the cause is unclear",
    "Pig": "private engine indulges — feast, forgiveness, debt when boundaries fail",
}


def compound_lore(compound: int, final: int) -> str:
    meaning = LIFE_PATH_MEANING.get(final, "an initiatory path")
    trial = LIFE_PATH_TRIAL.get(final, "")
    triumph = LIFE_PATH_TRIUMPH.get(final, "")
    compound_note = COMPOUND_PRESSURE.get(
        compound,
        f"compound {compound} is raw digit-weight before the vow settles",
    )
    if compound == final:
        return (
            f"Path {compound} is one gate — {meaning}. "
            f"WARNING: {trial} TRIUMPH: {triumph}"
        )
    return (
        f"{compound}/{final} — {compound_note}. Final {final}: {meaning}. "
        f"In occult numerology the compound is what the flesh still argues with; "
        f"the final is the vow you must breathe without performance. "
        f"WARNING: {trial} TRIUMPH: {triumph}"
    )


def universal_year_lore(calendar_year: int, uy: dict[str, Any]) -> str:
    v = uy["value"]
    disp = numerology_display(uy)
    world = UNIVERSAL_YEAR_MEANING.get(v, "world-cycle pressure on every seeker")
    return f"{calendar_year} world-field {disp} — {world}."


def _dominant_element_short(balance: dict[str, Any]) -> str:
    if not balance:
        return ""
    items = sorted(balance.items(), key=lambda x: (-x[1], x[0]))
    if not items:
        return ""
    top, top_n = items[0]
    weak = items[-1][0] if len(items) > 1 else ""
    if top_n >= 3 and weak:
        return f"Constitution runs hot on {top}, thin on {weak} — compensate or the road buckles."
    return f"Elemental weight leans {top} — that is the weather inside the pillars."


def build_bazi_walk(facts: dict[str, Any]) -> str:
    pillars = facts.get("pillars") or {}
    year = pillars.get("year") or {}
    month = pillars.get("month") or {}
    hour = pillars.get("hour") or {}
    dm = facts["day_master"]
    animal = facts["year_zodiac"]["animal"]
    month_el = month.get("stem_element") or ""
    hour_animal = hour.get("branch_animal") or ""

    inheritance = ANIMAL_INHERITANCE.get(animal, "ancestral weather presses from behind")
    season = ELEMENT_SEASON.get(month_el, "the corridor of your work shifts with the month's element")
    hour_line = HOUR_ENGINE.get(hour_animal, "the private hour runs on its own animal logic")
    balance = _dominant_element_short(facts.get("element_balance") or {})

    return (
        f"{inheritance} {season} "
        f"Your blade is {dm['english']} {dm['element']} — how you cut when cornered, how you earn when honest. "
        f"{hour_line} {balance}"
    ).strip()


def build_vedic_walk(facts: dict[str, Any]) -> str:
    h2 = facts["vedic_house_2"]
    h10 = facts["vedic_house_10"]
    h2_sign = h2["sign"]
    h10_sign = h10["sign"]
    p2 = ", ".join(h2["planets"]) if h2.get("planets") else "no planet speaks here"
    p10 = ", ".join(h10["planets"]) if h10.get("planets") else "no planet speaks here"
    walk2 = HOUSE_2_WALK.get(h2_sign, "the sustenance house asks you to name what feeds you")
    walk10 = HOUSE_10_WALK.get(h10_sign, "the crown house judges how you are remembered")
    dasha = facts.get("mahadasha") or {}
    lord = dasha.get("lord", "")

    sky = (
        f"Sidereal memory in {facts['moon']['sidereal_sign']} / {facts['moon']['nakshatra']} — "
        f"what you feel is older than what you say. Gate-body {facts['ascendant']['vedic_lagna']} "
        f"vs tropical mask {facts['ascendant']['western_sign']}."
    )
    return (
        f"Sustenance road ({walk2}) — sky whispers: {p2}. "
        f"Crown road ({walk10}) — sky whispers: {p10}. "
        f"Decade colored by {lord or 'the current lord'} — public myth shifts even when you stand still. "
        f"{sky}"
    )


def build_reflected_explicit(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]["display"]
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    moon = facts["moon"]["western_sign"]
    nak = facts["moon"]["nakshatra"]
    dm = facts["day_master"]["element"]

    return (
        f"EXPLICIT — what the room reads: {asc} gate, {sun} will on display, {dm} constitution "
        f"in how you move, life path {lp} as the vow you cannot hide forever. "
        f"REFLECTED — what runs underneath: {moon} memory, {nak} hunger, the private hour and "
        f"ancestral animal weather you absorb before you speak. "
        f"When explicit and reflected agree, you are dangerous in the best sense. "
        f"When they war, you feel 'misunderstood' — that is the war, not the people."
    )


def build_compound_reflects(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    compound, final = lp["compound"], lp["value"]
    expr = facts.get("expression", {})
    soul = facts.get("soul_urge", {})
    bday = facts.get("birthday_number", {})

    reflects = (
        f"Life-path compound {compound} is the unreduced sum of your birth date — "
        f"it reflects FLESH MEMORY: habits, debts, and hungers written before the vow reduces. "
        f"Final {final} is the soul's elected curriculum this life."
    )
    if compound != final:
        reflects += (
            f" The compound does not lie: it shows what still argues in you; the final shows what "
            f"must become your default breath to ascend."
        )
    if expr.get("compound") and expr["compound"] != compound:
        reflects += (
            f" Name-field (expression {expr.get('display', '')}) reflects the PUBLIC mask — "
            f"how the world contracts you; it can rhyme or war with the birth compound."
        )
    if soul.get("display"):
        reflects += f" Soul-urge {soul['display']} reflects private appetite — what you chase when alone."
    if bday.get("display"):
        reflects += f" Birthday {bday['display']} reflects the day-of-month gift and wound."
    return reflects


def build_chart_truth(facts: dict[str, Any]) -> str:
    anchor = facts.get("chart_anchor") or {}
    dm = anchor.get("day_master") or facts["day_master"]
    day = anchor.get("day_pillar") or facts.get("day_pillar") or {}
    year = anchor.get("year_pillar") or {}
    clar = anchor.get("confusion_clarification", "")
    day_gz = day.get("gan_zhi") or facts.get("pillars", {}).get("day", {}).get("gan_zhi", "")
    year_gz = year.get("gan_zhi") or facts["year_zodiac"].get("gan_zhi", "")

    return (
        f"ACCURATE SEAL: Day master {dm.get('english', '')} {dm.get('hanzi', '')} — "
        f"{dm.get('yin_yang', '')} {dm.get('element', '')} ({dm.get('polarity', '')}). "
        f"Day pillar {day_gz} — branch animal {anchor.get('day_branch_animal', '')}. "
        f"Year pillar {year_gz} — popular zodiac {anchor.get('year_zodiac_popular', '')}. "
        f"{clar}"
    ).strip()


def build_east_west_zodiac(facts: dict[str, Any]) -> str:
    year_animal = facts["year_zodiac"]["animal"]
    sun = facts["sun_sign"]
    dm = facts["day_master"]
    asc = facts["ascendant"]["western_sign"]
    return (
        f"East (year weather): {year_animal} — how lineage and era press you from behind. "
        f"East (day blade): {dm['english']} {dm['yin_yang']} {dm['element']} on "
        f"{facts.get('chart_anchor', {}).get('day_branch_animal', '')} day — how you cut reality daily. "
        f"West: Sun {sun} (conscious will), Ascendant {asc} (gate / costume). "
        f"Together: you may present {sun}/{asc} while carrying {year_animal} weather with a "
        f"{dm['english']} {dm['element']} constitution — the mission is to stop mixing them up."
    )


def build_archetype(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    year_animal = facts["year_zodiac"]["animal"]
    day_animal = facts.get("chart_anchor", {}).get("day_branch_animal", "")
    lp = facts["life_path"]["display"]
    sun = facts["sun_sign"]
    el = dm["element"]
    el_verbs = {
        "Metal": "cut, refine, and judge",
        "Wood": "grow, argue, and ascend",
        "Fire": "ignite, display, and convert",
        "Earth": "hold, compound, and endure",
        "Water": "adapt, penetrate, and time",
    }
    title = (
        f"The {dm['yin_yang']} {dm['element']} {day_animal or 'soul'} "
        f"walking under {year_animal} skies — {sun} will, vow {lp}"
    )
    return (
        f"Archetype: {title}. "
        f"You are built to {el_verbs.get(el, 'walk your element')} — {dm['english']} constitution "
        f"with {day_animal or 'hidden'} rhythm in the body, {year_animal} weather in the blood. "
        f"People meet the {sun} mask; fate tests the {dm['english']} blade."
    )


def build_shadow_jung(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    el = dm["element"]
    year_animal = facts["year_zodiac"]["animal"]
    lp_val = facts["life_path"]["value"]

    element_shadow = {
        "Metal": "shadow: cold verdict, perfection as cruelty, cutting others to avoid feeling",
        "Wood": "shadow: righteous anger, control through growth, inability to rest",
        "Fire": "shadow: burnout theatre, vanity, rage when not seen",
        "Earth": "shadow: hoarding, rigidity, passive control through duty",
        "Water": "shadow: manipulation through silence, fear dressed as wisdom, escape",
    }.get(el, "shadow: distortion of your element when refused")

    animal_shadow = {
        "Rooster": "Rooster shadow in the blood: criticism turned inward, display without substance",
        "Goat": "Goat in the day-body: appeasement, aesthetic escape, resentment behind charm",
        "Ox": "Ox: stubborn grief, labor without joy",
        "Tiger": "Tiger: holy rage, collateral damage",
        "Dragon": "Dragon: scale without root, appetite for magnitude",
        "Snake": "Snake: secrecy as weapon, envy coiled",
        "Horse": "Horse: flight as identity",
        "Monkey": "Monkey: clever avoidance",
        "Rat": "Rat: scarcity scheming",
        "Dog": "Dog: loyalty to unworthy causes",
        "Pig": "Pig: indulgence, porous boundaries",
        "Rabbit": "Rabbit: fear of confrontation",
    }.get(
        facts.get("chart_anchor", {}).get("day_branch_animal") or year_animal,
        "animal shadow: inherited drama unowned",
    )

    lp_shadow = LIFE_PATH_TRIAL.get(lp_val, "the vow resisted")

    return (
        f"SHADOW (Jung): {element_shadow}. {animal_shadow}. "
        f"Life-path shadow: {lp_shadow}. "
        f"It manifests when you perform the year animal's myth instead of wielding the day master — "
        f"or when the compound still runs your choices while you claim the final vow."
    )


def build_soul_mission(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]["display"]
    dm = facts["day_master"]
    return (
        f"SOUL MISSION: Integrate {lp} — live the final, starve the compound's stale argument. "
        f"Embody {dm['english']} {dm['yin_yang']} {dm['element']} correctly (not its shadow, not "
        f"the year animal's costume). Face the shadow when it speaks — that is the initiation. "
        f"Bridge east blade and west gate until explicit and reflected align; that alignment is the "
        f"next level you came to earn. Ignore this and you repeat the same room with new faces."
    )


def build_zero_verdict(facts: dict[str, Any]) -> dict[str, str]:
    lp_val = facts["life_path"]["value"]
    trial = LIFE_PATH_TRIAL.get(lp_val, "you fight the vow and call it fate")
    triumph = LIFE_PATH_TRIUMPH.get(lp_val, "you own the vow and the field bends")
    dm_el = facts["day_master"]["element"]
    h2 = facts["vedic_house_2"]["sign"]
    wealth_warn = (
        f"Do not earn against your {dm_el} — the 2nd-house rhythm in {h2} will starve you if you perform "
        f"another element's myth."
    )
    return {
        "warning": f"{trial.capitalize()}. {wealth_warn}",
        "triumph": f"{triumph.capitalize()}. Walk {facts['life_path']['display']} until the compound "
        f"stops arguing — then the crown road opens.",
    }


WESTERN_SIGN_ELEMENT: dict[str, str] = {
    "Aries": "Fire",
    "Leo": "Fire",
    "Sagittarius": "Fire",
    "Taurus": "Earth",
    "Virgo": "Earth",
    "Capricorn": "Earth",
    "Gemini": "Air",
    "Libra": "Air",
    "Aquarius": "Air",
    "Cancer": "Water",
    "Scorpio": "Water",
    "Pisces": "Water",
}

EXPRESSION_OCCULT: dict[int, str] = {
    1: "name as spear — how the world contracts you to lead or fight",
    2: "name as mirror — diplomacy, duet, delay written in public",
    3: "name as trumpet — art, scandal, speech that outruns substance",
    4: "name as masonry — craft, law, repetition branded on the brow",
    5: "name as wind — rebranding, exile, sales of freedom",
    6: "name as hearth — beauty, debt, family on the marquee",
    7: "name as veil — research, solitude, spiritual price of visibility",
    8: "name as throne — power, markets, judgment in the signature",
    9: "name as release — completion, teaching, grief in the brand",
    11: "name as live wire — master voltage in public",
    22: "name as cathedral — master scale in public",
    33: "name as altar — master mercy in public",
}


def _western_element(sign: str) -> str:
    return WESTERN_SIGN_ELEMENT.get(sign, "")


def build_numerology_gate(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    expr = facts["expression"]
    c, f = lp["compound"], lp["value"]
    c_note = COMPOUND_PRESSURE.get(c, "raw birth-date weight before the vow")
    f_mean = LIFE_PATH_MEANING.get(f, "initiatory road")
    ev = expr.get("value", 0)
    expr_line = EXPRESSION_OCCULT.get(ev, "public name-field shapes the mask")
    if c == f:
        path = f"Path {c} — one gate: {f_mean}"
    else:
        path = (
            f"Compound {c} ({c_note}) is flesh-karma; final {f} ({f_mean}) is the vow. "
            f"Walk {lp['display']} until the compound stops driving the car."
        )
    expr_disp = expr.get("display", "—")
    if expr.get("compound") != c:
        return f"{path} Expression {expr_disp}: {expr_line}."
    return f"{path} Expression {expr_disp} rhymes the birth-field — {expr_line}."


def build_four_gates_bazi(facts: dict[str, Any]) -> str:
    p = facts.get("pillars") or {}
    y, m, d, h = p.get("year", {}), p.get("month", {}), p.get("day", {}), p.get("hour", {})
    dm = facts["day_master"]
    bal = _dominant_element_short(facts.get("element_balance") or {})
    return (
        f"BaZi matrix: {y.get('stem_element', '')} {y.get('branch_animal', '')} bloodline — "
        f"{m.get('stem_element', '')} season of work — "
        f"{d.get('stem_english', '')} {d.get('branch_animal', '')} sovereign ({dm['yin_yang']} "
        f"{dm['element']} blade) — {h.get('stem_english', '')} {h.get('branch_animal', '')} "
        f"hidden engine. {bal}"
    )


def build_sky_matrix(facts: dict[str, Any]) -> str:
    h2, h10 = facts["vedic_house_2"], facts["vedic_house_10"]
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    moon = facts["moon"]
    asc = facts["ascendant"]
    return (
        f"Vedic: sustenance in {h2['sign']}, crown in {h10['sign']}, "
        f"Mahadasha {dasha}. Sidereal Moon {moon['sidereal_sign']} / {moon['nakshatra']} "
        f"(true hunger); tropical Moon {moon['western_sign']} (felt story); "
        f"lagna {asc['vedic_lagna']} vs Ascendant {asc['western_sign']} (body vs costume)."
    )


def build_zodiac_cross(facts: dict[str, Any]) -> str:
    yz = facts["year_zodiac"]
    sun = facts["sun_sign"]
    year_el = yz.get("element", "")
    west_el = _western_element(sun)
    dm = facts["day_master"]
    day_an = facts.get("chart_anchor", {}).get("day_branch_animal", "")
    return (
        f"East — birth-year {year_el} {yz['animal']} ({yz.get('pillar_english', '')}): "
        f"ancestral element-weather, not your day blade. Day constitution: {dm['english']} "
        f"{dm['yin_yang']} {dm['element']} on {day_an}. "
        f"West — Sun {sun} ({west_el}), gate {facts['ascendant']['western_sign']} "
        f"({_western_element(facts['ascendant']['western_sign'])}). "
        f"Weapon: stop calling yourself only the year animal; wield the four gates and both skies."
    )


def _big_picture_compact(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    lp = facts["life_path"]["display"]
    lp_val = facts["life_path"]["value"]
    trial = LIFE_PATH_TRIAL.get(lp_val, "the vow resisted")
    el = dm["element"]
    sh = {
        "Metal": "cold verdict",
        "Wood": "righteous control",
        "Fire": "burnout theatre",
        "Earth": "rigid duty",
        "Water": "escape in silence",
    }.get(el, "distorted element")
    return (
        f"{dm['yin_yang']} {dm['element']} blade · {facts['year_zodiac']['animal']} blood · vow {lp}. "
        f"Gate {facts['ascendant']['western_sign']} / hunger {facts['moon']['nakshatra']}. "
        f"Unowned shadow: {sh}; path shadow: {trial}."
    )


def build_chart_book_report(facts: dict[str, Any]) -> str:
    """Full BaZi four gates compared to Vedic personal houses — unbiased book-report tone."""
    p = facts.get("pillars") or {}
    y, m, d, h = p.get("year", {}), p.get("month", {}), p.get("day", {}), p.get("hour", {})
    dm = facts["day_master"]
    h2, h10 = facts["vedic_house_2"], facts["vedic_house_10"]
    p2 = ", ".join(h2["planets"]) if h2.get("planets") else "empty"
    p10 = ", ".join(h10["planets"]) if h10.get("planets") else "empty"
    moon = facts["moon"]
    dasha = (facts.get("mahadasha") or {}).get("lord", "")

    bazi_story = (
        f"Act I — bloodline ({y.get('stem_element', '')} {y.get('branch_animal', '')}): the family myth you "
        f"inherit whether you praise it or rebel. Act II — season ({m.get('stem_element', '')} "
        f"{m.get('branch_animal', '')}): the decade's corridor where work actually happens. "
        f"Act III — sovereign day ({d.get('stem_english', '')} {d.get('branch_animal', '')}, "
        f"{dm['yin_yang']} {dm['element']} blade): the protagonist's real spine — not the year animal. "
        f"Act IV — private hour ({h.get('stem_english', '')} {h.get('branch_animal', '')}): what you do "
        f"when the audience leaves."
    )
    vedic_story = (
        f"Vedic mirror: 2nd in {h2['sign']} ({p2}) is the mouth of the ledger — how sustenance enters; "
        f"10th in {h10['sign']} ({p10}) is the title on the coffin of reputation. "
        f"Mahadasha {dasha} is the current season of the serial. "
        f"Sidereal Moon {moon['sidereal_sign']} / {moon['nakshatra']} is the true plot twist; "
        f"tropical Moon {moon['western_sign']} is how you narrate it to friends."
    )
    compare = (
        f"Compare: BaZi says earn and cut as {dm['element']} with {HOUSE_2_WALK.get(h2['sign'], 'your 2nd rhythm')}. "
        f"Vedic 2nd agrees or contradicts — agreement feels like 'luck'; war feels like self-sabotage. "
        f"BaZi hour engine vs 10th-house crown: when private engine matches public arc, the story coheres; "
        f"when they fight, you live two biographies."
    )
    return f"{bazi_story} {vedic_story} {compare}"


def build_story_archetype(facts: dict[str, Any]) -> str:
    """Philosophical role — the life cast to lead, book-report on the character."""
    dm = facts["day_master"]
    lp = facts["life_path"]
    f = lp["value"]
    year = facts["year_zodiac"]["animal"]
    day_an = facts.get("chart_anchor", {}).get("day_branch_animal", "")
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]

    role = {
        1: "the pioneer who must author the path others will walk",
        2: "the diplomat-weaver whose plot is partnership under pressure",
        3: "the orator-artist whose plot is voice versus integrity",
        4: "the builder-scribe whose plot is stone upon stone",
        5: "the pilgrim of change whose plot is freedom with consequence",
        6: "the hearth-keeper whose plot is beauty versus control",
        7: "the initiate whose plot is knowledge bought with distance",
        8: "the magistrate of matter whose plot is power versus conscience",
        9: "the closer whose plot is mercy through endings",
        11: "the live wire whose plot is voltage grounded into work",
        22: "the architect of epochs whose plot is scale versus spine",
        33: "the teacher-healer whose plot is love with boundaries",
    }.get(f, "the seeker whose plot is integration of split skies")

    return (
        f"BOOK REPORT — Character: {dm['yin_yang']} {dm['element']} soul in a {day_an} body, "
        f"{year} weather in the blood, {sun} will on stage, {asc} costume at the door, vow {lp['display']}. "
        f"Genre: philosophical drama, not comedy of confusion. "
        f"Role cast: {role}. "
        f"The antagonist is not a person — it is misalignment (year myth performed instead of day blade, "
        f"compound driving while final vow is preached). The climax is when explicit gate and reflected "
        f"Moon/nakshatra tell one story. The resolution you came for: live the final, starve the compound's "
        f"stale argument, let four gates and two skies agree."
    )


def build_threshold_reading(facts: dict[str, Any], name: str) -> str:
    """Single threshold seal — vow depth + full chart book report + role cast."""
    from app.services.numerology_depth import build_vow_chapter

    verdict = build_zero_verdict(facts)
    anchor = facts.get("chart_anchor", {})
    dm = facts["day_master"]

    return (
        f"{name} — threshold seal. You are a written story; this is the book report the temples withheld.\n\n"
        f"SEAL · Day master {dm['english']} {dm['hanzi']} ({dm['yin_yang']} {dm['element']}). "
        f"Year {anchor.get('year_zodiac_popular', '')} is prologue; day {anchor.get('day_branch_animal', '')} "
        f"is the body you walk.\n\n"
        f"THE VOW · {build_vow_chapter(facts)}\n\n"
        f"THE CHART · {build_chart_book_report(facts)}\n\n"
        f"EAST × WEST · {build_zodiac_cross(facts)}\n\n"
        f"THE ROLE · {build_story_archetype(facts)}\n\n"
        f"SHADOW · {build_shadow_jung(facts)}\n\n"
        f"WARNING — {verdict['warning']}\n"
        f"TRIUMPH — {verdict['triumph']}\n\n"
        f"Daily charts polish the next chapter. Seeker: Zero in the hour."
    )


def build_interpretive_briefs(facts: dict[str, Any]) -> dict[str, str]:
    lp = facts["life_path"]
    uy = facts.get("universal_year", {})
    py = facts.get("personal_year", {})
    dm_el = facts["day_master"]["element"]
    h2_sign = facts["vedic_house_2"]["sign"]
    verdict = build_zero_verdict(facts)

    from app.services.babylon_premium import (
        build_career_premium,
        build_enemies_premium,
        build_numerology_premium,
        build_road_premium,
    )
    from app.services.babylon_tablet import (
        SEAL_MARKER,
        build_babylon_tablet,
        build_bazi_layer,
        build_close,
        build_manifestation_layer,
        build_script_layer,
        build_vedic_layer,
        build_west_east_layer,
    )
    from app.services.priest_overview import build_threshold_seal

    _chart, interp, _full, _rec = build_threshold_seal(facts, "Seeker")

    return {
        "threshold_reading": interp,
        "chart_reference": _chart,
        "natal_chart_record": _rec,
        "tablet_greeting": build_babylon_tablet(facts, "Seeker").split("\n\n")[0],
        "numerology_premium": build_numerology_premium(facts),
        "road_premium": build_road_premium(facts),
        "career_premium": build_career_premium(facts),
        "enemies_premium": build_enemies_premium(facts),
        "bazi_layer": build_bazi_layer(facts),
        "vedic_layer": build_vedic_layer(facts),
        "west_east_layer": build_west_east_layer(facts),
        "script_layer": build_script_layer(facts),
        "manifestation_layer": build_manifestation_layer(facts),
        "seeker_close": build_close("Seeker"),
        "vow_tight": build_numerology_premium(facts),
        "wealth_career": build_career_premium(facts),
        "sky_experience": f"{build_vedic_layer(facts)} {build_west_east_layer(facts)}",
        "walk_experience": build_road_premium(facts),
        "seal_marker": SEAL_MARKER,
        "life_path_display": lp["display"],
        "life_path_compound": lp["compound"],
        "life_path_final": lp["value"],
        "sun_sign": facts["sun_sign"],
        "ascendant": facts["ascendant"]["western_sign"],
        "moon_western": facts["moon"]["western_sign"],
        "moon_sidereal": facts["moon"]["sidereal_sign"],
        "year_animal": facts["year_zodiac"]["animal"],
        "day_branch_animal": facts.get("day_pillar", {}).get("branch_animal", ""),
        "day_master_element": dm_el,
        "sustenance_element": WESTERN_SIGN_ELEMENT.get(h2_sign, ""),
        "zero_warning": verdict["warning"],
        "zero_triumph": verdict["triumph"],
    }


def add_calendar_numerology(facts: dict[str, Any], birth_date) -> None:
    cy = datetime.utcnow().year
    uy = universal_year(cy)
    py = personal_year(birth_date, cy)
    facts["universal_year"] = {
        "calendar_year": cy,
        "compound": uy["compound"],
        "value": uy["value"],
        "display": numerology_display(uy),
    }
    facts["personal_year"] = {
        "compound": py["compound"],
        "value": py["value"],
        "display": numerology_display(py),
    }