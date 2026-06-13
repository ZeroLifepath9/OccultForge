"""
Inline occult teaching — no deferral to external lookup.
Plain language for beginners; depth from Pythagorean, Tarot, BaZi, Vedic, Chaldean threads.
"""

from __future__ import annotations

from typing import Any

from app.services.babylon_lore import (
    CHALDEAN_DIGIT,
    DASHA_SEASON,
    NAKSHATRA_SCRIPT,
    SIGN_CHALDEAN_BRIDGE,
)
from app.services.compound_occult import get_compound_entry
from app.services.compound_registry import COMPOUND_DIRECTORY, PATH_FINAL_DIRECTORY

# ── Compound deep teachings (paragraphs taught on the seal) ─────────────────
COMPOUND_DEEP: dict[int, list[str]] = {
    27: [
        "Your birth sum holds 27 before it breaks to 9. In the Pythagorean current, 27 is three cubed — three threes stacked — which is why this compound is not 'generic nine.' It is compassion with structure: feeling that must be organized or it becomes exhaustion.",
        "Two is the High Priestess in the major arcana. That is not a mood; it is a function. You perceive the unfinished business in rooms other people leave. You are wired to read silence, complete cycles, and hold standards when others want comfort.",
        "Seven is the Chariot of mysteries — the mind that travels inward before it moves outward. Research, oath, solitude, and spiritual discipline are not hobbies here; they are how the Sceptre stays upright.",
        "Occult wave name: the Sceptre — authority through service and closure. You are not here to perform nine as vague humanitarian theater. You are here to end things fairly, document the ending, and let people walk away with dignity — while you refuse to carry their book forever.",
    ],
    18: [
        "Eighteen folds sun and moon before nine: leadership tested in matter, then release through feeling. Tarot's Moon (XVIII) is not romance — it is tidal memory. Endings arrive through family, mood, and private grief before the public ever hears the story.",
        "The Lunar Crown means completion happens in bedrooms of the soul first. You may look composed while something in you drowns. The work is to grieve on schedule, not to rescue others to avoid your own tide.",
    ],
    36: [
        "Thirty-six is nine multiplied by four — completion that must be seen. Three is the Empress (voice, creation); six is the Lovers (hearth, duty). The Throne of Nine demands legacy others can witness; private closure alone will feel like failure to your nervous system.",
        "You are allowed to finish on a stage — but the finish must be true. Performance without release becomes a cage with better lighting.",
    ],
    9: [
        "Single gate nine is the Hermit in Tarot and the ennead in Pythagorean mysticism: the gestation number, the number that walks downhill to give the grain away. When compound equals nine, flesh and vow agree — endings are your craft, not your accident.",
    ],
    11: [
        "Eleven is a master frequency — two pillars side by side. The nervous system is part of the instrument. Downloads, shivers, knowing before proof: these are real, but ungrounded voltage becomes anxiety, scandal, or prophecy that never ships.",
        "The Live Wire must be paid like a craft, not a curse.",
    ],
    22: [
        "Twenty-two is the master mason — cathedral thinking in the body before the crew arrives. Vision is not the problem; sequencing is. The Unbuilt Cathedral breaks spines that jump to scale without brick, partner, or sleep.",
    ],
    33: [
        "Thirty-three doubles creative fire into service — Christic Labor in the occult numerology schools (symbolic, not a religious demand). Love becomes work; boundaries become theology. Without a floor price on compassion, the body collapses.",
    ],
    1: [
        "One is the Magician — pure monadic fire. Initiation, name, direction. The blade is not cruelty; it is the refusal to wait for permission that rots your fate.",
    ],
    8: [
        "Eight is Strength/Justice in the major arcana — matter, infinity, executive force. The Material Crown must keep conscience or gold eats the throne.",
    ],
    13: [
        "Thirteen is Death in Tarot — transformation, never mere ending. The Phoenix Tax means every few years identity must burn: title, body image, job myth. Structure (four) only arrives after the fire is honest.",
    ],
    15: [
        "Fifteen is the Devil — magnetism with a contract written in shadow. Charm binds when you confuse heat with home. The Devil's Magnet in soul or name means appetite must be named, not dramatized.",
    ],
    6: [
        "Six is the Lovers — beauty and duty as one rope. The Hearth Seal heals by organizing care; it controls when love invoices others.",
    ],
    31: [
        "Thirty-one is three (voice) meeting one (monad) before four (law). The Veiled Builder speaks, then codifies. Rigidity arrives when you keep teaching a room that already left.",
    ],
    25: [
        "Twenty-five is partnership (two) sent into the road of change (five) before seven's cave. The Partnership Mystic learns through bond, then researches alone — betrayal cuts when partners read your notes without consent.",
    ],
    20: [
        "Twenty is Judgment in Tarot — partnerships as courtroom. The Judgment Pair feels fated because bonds are your initiation; delay is not peace, it is unpaid verdict.",
    ],
    10: [
        "Ten is the Wheel — reputation spins before will is earned. The Crown Before the Throne promotes visibility first; crashes come when the room discovers the gap between mask and root.",
    ],
    19: [
        "Nineteen is the Sun Prince — solar visibility before the throne is earned. Fame must survive an ending; otherwise the king is poster only.",
    ],
}

FINAL_DEEP: dict[int, str] = {
    9: "Final vow nine (the Ennead Gate): release, teach what you learned, and stop hoarding roles. Completion is an action — a signed letter, a returned key — not a feeling you nurse for years.",
    4: "Final vow four (the Stone Code): build slow, repeat sacredly, own the foundation. Empire here is repetition, not drama.",
    7: "Final vow seven (the Inner Sanctum): depth feeds output. Crowds are expensive; the cave is profitable when you share what you found.",
    1: "Final vow one (the Monad Blade): stand first without apology. Followers arrive after you name the direction.",
    8: "Final vow eight (the Material Crown): resources answer when conscience leads.",
    6: "Final vow six (the Hearth Seal): beauty and duty are one rope — not control dressed as care.",
}

NAKSHATRA_DEEP: dict[str, str] = {
    "Uttara Phalguni": (
        "Uttara Phalguni is the 'later red star' — patronage after pleasure. In Vedic mansion lore you are wired for "
        "contracts, legitimate exchange, and making power lawful through service. You improve what you touch when "
        "the deal is fair and written. Flirting with power without documentation stains you longer than a bad breakup."
    ),
    "Rohini": "Rohini is fertility and appetite — what is cultivated grows wealth. Mood and body are business partners; neglect either and both rot.",
    "Magha": "Magha is the ancestral throne — pride, legacy, kingship of blood. You feel watched by lineages; honor them without becoming their puppet.",
    "Mula": "Mula uproots — endings fund beginnings. There is no neutral ground; half-roots invite the same ghost.",
}

STEM_DEEP: dict[str, str] = {
    "Jia": (
        "Jia is Yang Wood — the tree that breaks soil upward. You grow by starting things and pushing through resistance. "
        "Prune dead projects or the canopy blocks your own light."
    ),
    "Yi": (
        "Yi is Yin Wood — vine, flower, and flex. You win by adapting, connecting people, and teaching growth — not by "
        "force alone."
    ),
    "Bing": (
        "Bing is Yang Fire — the sun, broadcast, visibility. You need to be seen doing honest work; hiding taxes your energy "
        "and income."
    ),
    "Ding": (
        "Ding is Yin Fire — candle, focus, refinement. You succeed in small intense bursts — craft, insight, one sharp offer "
        "at a time."
    ),
    "Wu": (
        "Wu is Yang Earth — mountain, wall, backbone. You endure and outlast; people trust you to hold the line. Rigidity "
        "is the tax when you refuse necessary change."
    ),
    "Ji": (
        "Ji is Yin Earth — soil that receives, stores, and ripens. Not passive: composting. You build value by holding "
        "standard — meals, money, shelter, schedules — until the thing is actually done."
    ),
    "Geng": (
        "Geng is Yang Metal — blade, axe, outward cut. You decide fast, set boundaries, and finish with clarity. Blunt force "
        "without a plan wastes your edge."
    ),
    "Xin": (
        "Xin is Yin Metal — jewel, precision, inward refinement. You polish details, aesthetics, and standards. Perfectionism "
        "becomes paralysis if nothing ships."
    ),
    "Ren": (
        "Ren is Yang Water — river, flood, wide movement. You win on timing, networks, and scope. Fighting the current on "
        "principle alone doubles your cost."
    ),
    "Gui": (
        "Gui is Yin Water — rain, seep, intuition. You read rooms and moods before facts. Without boundaries you absorb "
        "other people's weather."
    ),
}

PADA_COLOR: dict[int, str] = {
    1: "pada 1 — fire of initiative: act first, explain after.",
    2: "pada 2 — earth of substance: make it tangible or it did not happen.",
    3: "pada 3 — air of message: name it in speech and writing.",
    4: "pada 4 — water of release: endings need feeling and rest, not performance.",
}


def _auto_compound_deep(c: int, f: int, glyph: str, equation: str) -> list[str]:
    lib = COMPOUND_DIRECTORY.get(c, {})
    flesh = lib.get("flesh", "")
    parts = [f"Compound {c} resolves to final {f} — occult name {glyph}. Equation on the seal: {equation}."]
    if flesh:
        parts.append(f"In the body: {flesh}")
    for digit in str(c):
        if digit.isdigit() and int(digit) in CHALDEAN_DIGIT:
            parts.append(f"Digit {digit} in Chaldean tone: {CHALDEAN_DIGIT[int(digit)]}.")
    fin = PATH_FINAL_DIRECTORY.get(f, {})
    if fin.get("plain"):
        parts.append(f"Final gate: {fin['plain']}")
    return parts


def teach_compound(c: int, f: int, disp: str) -> str:
    lib = get_compound_entry(c, f, disp)
    glyph, eq = lib["glyph"], lib["equation"]
    paras = COMPOUND_DEEP.get(c) or _auto_compound_deep(c, f, glyph, eq)
    if c != f:
        kin = lib.get("kin", "")
        if kin:
            paras = paras + [f"How you are not your neighbor's number: {kin}"]
    return "\n\n".join(paras)


def teach_final(f: int) -> str:
    return FINAL_DEEP.get(
        f,
        PATH_FINAL_DIRECTORY.get(f, {}).get("plain", f"Walk final {f} as daily vow, not as mood."),
    )


def teach_nakshatra(name: str, pada: int | None = None) -> str:
    base = NAKSHATRA_DEEP.get(name) or NAKSHATRA_SCRIPT.get(name, "a lunar mansion fixing hunger older than speech")
    if name not in NAKSHATRA_DEEP and name in NAKSHATRA_SCRIPT:
        base = (
            f"In the 27 nakshatra belt, {name} fixes the Moon's appetite: {NAKSHATRA_SCRIPT[name]}. "
            "This is the private plot twist — what you need emotionally is not always what you say in public."
        )
    if pada and pada in PADA_COLOR:
        return f"{base} {PADA_COLOR[pada]}"
    return base


def teach_day_master(facts: dict[str, Any]) -> str:
    dm = facts["day_master"]
    stem = dm.get("english", "")
    el = dm["element"]
    yy = dm.get("yin_yang", "")
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    stem_txt = STEM_DEEP.get(stem, f"{stem} carries {yy} {el} — your daily metabolism in the four pillars.")
    branch_txt = {
        "Rooster": "Rooster day branch is Metal precision — cut cleanly, audit, do not leave half-closures.",
        "Goat": "Goat day branch is aesthetic and cooperative — peace matters, but ambiguity is poison.",
        "Ox": "Ox day branch is slow endurance — outlast, do not dramatize.",
        "Dragon": "Dragon day branch wants visible chapter endings.",
        "Tiger": "Tiger day branch needs bold cuts when the cycle is done.",
    }.get(day_an, f"{day_an} day branch colors how the day master stem moves in the world.")
    return (
        f"Day master stem: {stem_txt} Day branch animal ({day_an}): {branch_txt} "
        "Stem and branch together are the day pillar storm — read both, not the stem alone."
    )


def teach_sky_weave(facts: dict[str, Any], glyph: str) -> str:
    sun = facts["sun_sign"]
    asc = facts["ascendant"]["western_sign"]
    lagna = facts["ascendant"].get("vedic_lagna")
    moon = facts["moon"]
    moon_sign = moon["western_sign"]
    sidereal = moon.get("sidereal_sign", "")
    nak = moon.get("nakshatra", "")
    pada = moon.get("nakshatra_pada")
    h10 = facts["vedic_house_10"]["sign"]
    h7 = facts["vedic_house_7"]["sign"]
    h2 = facts["vedic_house_2"]["sign"]
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")

    sun_n = {
        "Libra": "Libra Sun is cardinal air — justice, design, treaty. You are here to make endings fair and beautiful; ugly undocumented exits stick in reputation.",
        "Scorpio": "Scorpio Sun is fixed water — depth, leverage, truth. You finish in honesty, not in performance.",
        "Virgo": "Virgo Sun is mutable earth — craft, body, service. The nervous system is part of the product.",
    }.get(sun, f"{sun} Sun colors will and vitality.")

    asc_n = {
        "Scorpio": "Scorpio rising is the mask of intensity — the room feels you before you speak. Trust earned slowly; soften on purpose after.",
        "Libra": "Libra rising sells charm first — decisions must follow or you look decorative.",
    }.get(asc, f"{asc} rising is the costume at the door.")

    lagna_n = ""
    if lagna and lagna != asc:
        lagna_n = (
            f"Vedic lagna {lagna} is the body's truth; tropical Ascendant {asc} is the costume. "
            f"Health and vocation must honor lagna first — or the body misfires while the mask wins."
        )

    moon_n = {
        "Virgo": "Tropical Moon in Virgo worries in the body — order, sleep, repair after conflict.",
        "Scorpio": "Tropical Moon in Scorpio feels everything — trust must be total or not at all.",
    }.get(moon_sign, f"Tropical Moon in {moon_sign} is the story you tell about feeling.")

    nak_t = teach_nakshatra(nak, pada) if nak else ""

    year_day = ""
    if yz != day_an:
        year_day = (
            f"BaZi year branch {yz} is how the family casts you publicly; day branch {day_an} is your operating system. "
            f"Hire, love, and brand for the day animal — or you exhaust yourself performing the year myth."
        )

    dasha = (facts.get("mahadasha") or {}).get("lord")
    dasha_t = ""
    if dasha:
        dasha_t = f"Active mahadasha of {dasha}: {DASHA_SEASON.get(dasha, 'this planetary season colors timing')}. Major moves in this period must respect that lord."

    return "\n\n".join(
        x
        for x in [
            f"Western: {sun_n} {asc_n}",
            lagna_n,
            f"Moon: {moon_n} Sidereal Moon in {sidereal} — private hunger. {nak_t}",
            f"Vedic houses on your seal: 10th {h10} (reputation), 7th {h7} (bonds), 2nd {h2} (income).",
            year_day,
            dasha_t,
            f"These skies do not replace {glyph}; they pressure it. Synthesis is the product.",
        ]
        if x
    )


def teach_name_field(field_key: str, facts: dict[str, Any]) -> str:
    from app.services.name_field_occult import FIELD_META

    num = facts.get(field_key) or {}
    if not num.get("value"):
        return ""
    meta = FIELD_META[field_key]
    c, f, disp = num["compound"], num["value"], num["display"]
    lp = facts["life_path"]
    lib = get_compound_entry(c, f, disp)
    glyph = lib["glyph"]

    if field_key == "expression" and c == lp["compound"]:
        lp_g = get_compound_entry(lp["compound"], lp["value"], lp["display"])["glyph"]
        return (
            f"{meta['title']}: {disp} — {glyph}. The public name amplifies the birth current; "
            f"brand and title must sound like {lp_g}-work, not a generic life-path slogan."
        )
    if field_key == "soul_urge":
        body = teach_compound(c, f, disp) if c not in COMPOUND_DEEP or c != lp["compound"] else (
            f"Soul urge {disp} — {glyph}. Private appetite: {lib['flesh']}"
        )
        return f"{meta['title']}. {meta['role']}\n\n{body}"
    if field_key == "birthday_number":
        return (
            f"{meta['title']}: {disp} — {glyph}. {lib['flesh']} "
            f"This tide returns every month on day {facts.get('birth_day', '—')} — reset craft, not identity."
        )
    if field_key == "personality":
        return f"{meta['title']}: {disp} — {glyph}. Stranger-facing armor: {lib['flesh']}"
    return f"{meta['title']}: {disp} — {glyph}. {lib['flesh']}"


def teach_number_weave(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    lp_g = get_compound_entry(lp["compound"], lp["value"], lp["display"])["glyph"]
    lines = [
        f"Primary initiation: {lp['display']} — {lp_g}. Every other number bends around this.",
    ]
    for key, label in (
        ("expression", "Public name"),
        ("soul_urge", "Soul vowels"),
        ("birthday_number", "Birth day"),
        ("personality", "Consonant armor"),
    ):
        n = facts.get(key) or {}
        if not n.get("value"):
            continue
        g = get_compound_entry(n["compound"], n["value"], n["display"])["glyph"]
        if n["compound"] == lp["compound"]:
            lines.append(f"{label} ({n['display']}): same current — amplifies {lp_g}, not a second life.")
        elif n["value"] == lp["value"]:
            lines.append(f"{label} ({n['display']}): shares final {lp['value']} but compound {n['compound']} — {g} colors the layer.")
        else:
            lines.append(f"{label} ({n['display']}): {g} — tension with birth until you reconcile mask and body.")
    expr, soul = facts.get("expression", {}), facts.get("soul_urge", {})
    if expr.get("value") and soul.get("value") and expr["value"] != soul["value"]:
        lines.append(
            f"Friction: you advertise {expr['display']} while you crave {soul['display']}. Negotiate that in price, partner, and schedule — silence becomes resentment."
        )
    return "\n\n".join(lines)


# Fill nakshatra teachings for every mansion (inline, not deferred)
for _nak, _short in NAKSHATRA_SCRIPT.items():
    NAKSHATRA_DEEP.setdefault(
        _nak,
        f"In the 27 nakshatra belt, {_nak} fixes the Moon's private appetite: {_short}. "
        "Sidereal hunger runs under your tropical Moon story — feed this or mood lies.",
    )

# Ensure every birth compound has at least auto depth available
for _c, _row in COMPOUND_DIRECTORY.items():
    if _c not in COMPOUND_DEEP:
        COMPOUND_DEEP[_c] = _auto_compound_deep(
            _c, _row["final"], _row["glyph"], _row["equation"]
        )