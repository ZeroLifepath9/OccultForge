"""Relationships exterior + conversational framing — Western tropical + Vedic sidereal."""

from __future__ import annotations

from typing import Any

from app.services.babylon_lore import NAKSHATRA_SCRIPT
from app.services.imprint_labels import build_display_bundle, numerology_display
from app.services.interpretations.manifestation_voice import plain_flesh
from app.services.overview_lore import HOUSE_10_WALK, HOUSE_7_WALK
from app.services.phoenix_insight import SIGN_MEANS
from app.services.interpretations.vedic_house_sign_engine import SIGN_TEMPERAMENT, interpret_house_sign

SIGN_ELEMENTS: dict[str, str] = {
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

SIGNS_BY_ELEMENT: dict[str, list[str]] = {
    "Fire": ["Aries", "Leo", "Sagittarius"],
    "Earth": ["Taurus", "Virgo", "Capricorn"],
    "Air": ["Gemini", "Libra", "Aquarius"],
    "Water": ["Cancer", "Scorpio", "Pisces"],
}

ELEMENT_FRICTION: dict[str, str] = {
    "Fire": "Earth",
    "Earth": "Air",
    "Air": "Water",
    "Water": "Fire",
}

SQUARE_SIGNS: dict[str, list[str]] = {
    "Aries": ["Cancer", "Capricorn"],
    "Taurus": ["Leo", "Aquarius"],
    "Gemini": ["Virgo", "Pisces"],
    "Cancer": ["Aries", "Libra"],
    "Leo": ["Taurus", "Scorpio"],
    "Virgo": ["Gemini", "Sagittarius"],
    "Libra": ["Cancer", "Capricorn"],
    "Scorpio": ["Leo", "Aquarius"],
    "Sagittarius": ["Virgo", "Pisces"],
    "Capricorn": ["Aries", "Libra"],
    "Aquarius": ["Taurus", "Scorpio"],
    "Pisces": ["Gemini", "Sagittarius"],
}

ELEMENT_VOICE: dict[str, str] = {
    "Fire": "rush and heat before terms are written",
    "Earth": "slow proof and caution when you need spontaneity",
    "Air": "clever talk that outruns emotional depth",
    "Water": "mood tides and possession when you need clean air",
}

# Fifth house — romance, pleasure, risk (lived, not label).
HOUSE_5_ROMANCE: dict[str, str] = {
    "Aries": "dating feels like sport — you want spark, chase, and someone who can keep pace; boredom reads as rejection",
    "Taurus": "romance is appetite made slow — touch, food, reliability; you bond when the body trusts the room",
    "Gemini": "flirtation is intelligence — wit, variety, parallel conversations; you need mental play or the affair goes flat",
    "Cancer": "love is shelter — you test partners at the kitchen table, not the nightclub; mood is policy",
    "Leo": "romance wants witness — praise, play, visible devotion; you wither when affection goes private too long",
    "Virgo": "care is your flirt language — acts of service, fixing, refining; critique becomes intimacy until it cuts",
    "Libra": "courtship is aesthetic treaty — beauty, fairness, mirrored effort; ugly imbalance ends the story fast",
    "Scorpio": "desire runs deep or not at all — all-or-nothing appetite, tests before trust; half-measures insult you",
    "Sagittarius": "romance roams — adventure, honesty, foreign beds; cages make you preachy or gone",
    "Capricorn": "love earns its place — status, timing, proof; you commit late but heavy when respect is shown",
    "Aquarius": "attraction is friendship first — odd chemistry, ideals, space; cling reads as suffocation",
    "Pisces": "romance dissolves edges — mercy, art, spiritual merge; without boundaries you drown in their weather",
}

VENUS_LOVE: dict[str, str] = {
    "Aries": "you pursue directly — affection is action, gifts are momentum; you lose interest when a partner waits you out",
    "Taurus": "you love through constancy — touch, taste, shared property; betrayal hits the ledger before the heart admits it",
    "Gemini": "you love through talk — charm, curiosity, duets; inconsistency is your shadow when depth is demanded",
    "Cancer": "you love through nurture — feeding, remembering, protecting; you can mother partners past their adulthood",
    "Leo": "you love through radiance — loyalty, praise, public pride in the bond; neglect feels like humiliation",
    "Virgo": "you love through improvement — practical care, refined rituals; let lovers stay imperfect on purpose",
    "Libra": "you love through balance — fairness, beauty, reciprocal effort; avoiding hard verdicts is how resentment grows",
    "Scorpio": "you love through depth — loyalty tested, intimacy as oath; surface romance feels like insult",
    "Sagittarius": "you love through freedom — honesty, adventure, shared belief; possessiveness triggers exile",
    "Capricorn": "you love through reliability — time, structure, earned trust; warmth may arrive late but it is real when it does",
    "Aquarius": "you love through friendship and principle — space, odd rhythm, ideals; emotional fog without logic drains you",
    "Pisces": "you love through merge — compassion, art, spiritual closeness; you need edges or you pay their debts emotionally",
}

MARS_FIGHT: dict[str, str] = {
    "Aries": "fight is frontal — you snap fast, forgive fast if respect returns; passive aggression enrages you",
    "Taurus": "fight is stubborn — you dig in on values and touch; rushed ultimatums harden you past repair",
    "Gemini": "fight is words — sarcasm, logic, switching angles; you need a spoken truce, not silent treatment",
    "Cancer": "fight is mood — retreat, memory, indirect hurt; you need safety before you can argue cleanly",
    "Leo": "fight is pride — drama, visible wound, demand for honor; humiliation lingers longer than the issue",
    "Virgo": "fight is critique — lists, fixes, control; name appreciation before the next correction",
    "Libra": "fight avoids until it explodes — fairness deferred becomes poison; schedule the hard conversation early",
    "Scorpio": "fight is strategic — silence, leverage, total recall; half-truths are remembered as betrayal",
    "Sagittarius": "fight is moral — truth bombs, exit threats, sermon; you need room to return without losing face",
    "Capricorn": "fight is cold structure — boundaries, duty, delayed emotion; warmth after conflict must be scheduled",
    "Aquarius": "fight is ideological — principle over cuddling; you detach when emotion feels irrational",
    "Pisces": "fight dissolves — tears, escape, spiritual guilt; you need grounding or you absorb their chaos",
}

MOON_RECOVERY: dict[str, str] = {
    "Aries": "after conflict you need movement — a walk, a win, a clean restart; stewing makes you cruel",
    "Taurus": "after conflict you need comfort — food, touch, predictable rhythm; chaos prolongs the wound",
    "Gemini": "after conflict you need talk — naming what happened, lighter air; silence feels like abandonment",
    "Cancer": "after conflict you need nest — privacy, reassurance, remembered care; public repair feels unsafe",
    "Leo": "after conflict you need dignity — apology with respect, affection with witness; neglect replays the fight",
    "Virgo": "after conflict you need order — practical repair, small acts, not grand speeches; mess prolongs anxiety",
    "Libra": "after conflict you need beauty and balance — aesthetic reset, fair wording; ugliness keeps the door open",
    "Scorpio": "after conflict you need truth — full disclosure, no cosmetic peace; partial honesty reopens the cut",
    "Sagittarius": "after conflict you need space and perspective — humor, horizon, a plan; cages restart the war",
    "Capricorn": "after conflict you need time and proof — actions over promises; premature warmth feels fake",
    "Aquarius": "after conflict you need distance and logic — friend-tone, principle, air; emotional flooding exhausts you",
    "Pisces": "after conflict you need softness and sleep — art, water, spiritual quiet; harsh rooms keep you porous",
}


def _vedic_house(imprint: dict[str, Any], num: int) -> dict[str, Any]:
    row = next((h for h in imprint.get("vedic", {}).get("houses", []) if h.get("house") == num), None)
    return row or {"house": num, "sign": "—", "planets": []}


def _house_action(house_num: int, sign: str) -> str:
    """Lived house+sign weave with do/don't from walk tables."""
    if not sign or sign == "—":
        return ""
    interp = interpret_house_sign(house_num, sign)
    walk = HOUSE_7_WALK.get(sign) if house_num == 7 else HOUSE_10_WALK.get(sign) if house_num == 10 else ""
    romance = HOUSE_5_ROMANCE.get(sign, "") if house_num == 5 else ""
    core = romance or walk or interp.get("weave", "")
    dont = interp.get("dont", "")
    if dont and dont not in core:
        return f"{core} Watch the shadow: {dont.lower()}."
    return core


def _nakshatra_lived(nak: str) -> str:
    script = NAKSHATRA_SCRIPT.get(nak, "a lunar mansion fixing hunger older than speech")
    return (
        f"Your nakshatra {nak} ({script}) is the Vedic emotional signature — "
        f"instinct in partnership runs here before Sun charm or Venus taste."
    )


def _chart_chorus(
    venus: str,
    moon_w: str,
    h5_sign: str,
    h7_sign: str,
    h10_sign: str,
) -> tuple[str, str]:
    """What rhymes across principles vs what warns."""
    v_el = SIGN_ELEMENTS.get(venus, "")
    m_el = SIGN_ELEMENTS.get(moon_w, "")
    h7_el = SIGN_ELEMENTS.get(h7_sign, "")
    h5_el = SIGN_ELEMENTS.get(h5_sign, "")
    rhyme_parts: list[str] = []
    warn_parts: list[str] = []

    if v_el and h7_el and v_el == h7_el:
        rhyme_parts.append(
            f"love style and partnership house share {v_el.lower()} — what attracts you and what you contract for speak one language"
        )
    if m_el and h7_el and m_el == h7_el:
        rhyme_parts.append(
            "emotional needs and partnership tone align — fights repair faster when the same element is fed"
        )
    if h5_el and v_el and h5_el == v_el:
        rhyme_parts.append("romance lane and Venus appetite rhyme — dating chemistry can mature into contract")

    if v_el and h7_el and v_el != h7_el:
        friction = ELEMENT_FRICTION.get(v_el, "")
        if friction == h7_el:
            warn_parts.append(
                f"you attract with {v_el.lower()} appetite but sign contracts in {h7_el.lower()} — charm and marriage ask different pacing"
            )
    if m_el and v_el and m_el != v_el:
        warn_parts.append(
            f"Moon wants {m_el.lower()} recovery while Venus leads with {v_el.lower()} taste — partners must learn two love languages"
        )
    if h5_sign and h7_sign and h5_sign != h7_sign:
        warn_parts.append(
            "who thrills you in romance and who you choose for contract are not the same creature — name both before you merge ledgers"
        )
    if h10_sign and h7_sign and SIGN_ELEMENTS.get(h10_sign) == "Fire" and SIGN_ELEMENTS.get(h7_sign) == "Water":
        warn_parts.append("public ambition runs hot while partnership wants depth — work praise can starve home attention")

    rhyme = (
        "What rhymes: " + "; ".join(rhyme_parts) + "."
        if rhyme_parts
        else "What rhymes: your chart asks for one honest conversation tying romance, contract, and recovery."
    )
    warn = (
        "What warns: " + "; ".join(warn_parts) + "."
        if warn_parts
        else "What warns: merging money, sex, and reputation before fairness is written."
    )
    return rhyme, warn


def compute_signs_to_avoid(facts: dict[str, Any]) -> list[str]:
    wp = facts.get("western_planets") or {}
    venus_sign = (wp.get("Venus") or {}).get("sign", "")
    moon_sign = (facts.get("moon") or {}).get("western_sign", "")
    h7_sign = (facts.get("vedic_house_7") or {}).get("sign", "")
    anchor = venus_sign or moon_sign or h7_sign
    anchor_el = SIGN_ELEMENTS.get(anchor, "")

    avoid: set[str] = set()
    clash_el = ELEMENT_FRICTION.get(anchor_el, "")
    if clash_el:
        avoid.update(SIGNS_BY_ELEMENT.get(clash_el, []))
    for sq in SQUARE_SIGNS.get(h7_sign, []):
        avoid.add(sq)

    own = {venus_sign, moon_sign, h7_sign, facts.get("sun_sign", "")}
    avoid -= {s for s in own if s}
    return sorted(avoid)[:5]


def build_relationships_exterior_line(facts: dict[str, Any]) -> str:
    signs = compute_signs_to_avoid(facts)
    if not signs:
        return "No sharp sign friction flagged — still write fairness before romance deepens."
    wp = facts.get("western_planets") or {}
    venus_sign = (wp.get("Venus") or {}).get("sign", "")
    moon_sign = (facts.get("moon") or {}).get("western_sign", "")
    anchor = venus_sign or moon_sign
    anchor_el = SIGN_ELEMENTS.get(anchor, "")
    friction_el = ELEMENT_FRICTION.get(anchor_el, "")
    sign_list = ", ".join(signs)
    if anchor and friction_el:
        return (
            f"Signs to lean away from: {sign_list} — "
            f"{friction_el.lower()} pacing tends to {ELEMENT_VOICE.get(friction_el, 'press your rhythm')} "
            f"against your {anchor} love style."
        )
    return f"Signs to lean away from: {sign_list} — they square your partnership house before terms are clear."


def build_relationships_framing(imprint: dict[str, Any]) -> dict[str, Any]:
    facts = build_display_bundle(imprint)
    signs = compute_signs_to_avoid(facts)
    return {
        "signs_to_avoid": signs,
        "exterior_line": build_relationships_exterior_line(facts),
    }


def build_relationships_conversation(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    """Conversational synthesis — how signs live in houses, planets, and timing."""
    wp = facts.get("western_planets") or {}
    venus = (wp.get("Venus") or {}).get("sign", "—")
    mars = (wp.get("Mars") or {}).get("sign", "—")
    moon_w = facts.get("moon", {}).get("western_sign", "—")
    moon_sid = facts.get("moon", {}).get("sidereal_sign", "—")
    nak = facts.get("moon", {}).get("nakshatra", "—")
    h5_sign = _vedic_house(imprint, 5).get("sign", "—")
    h7 = facts.get("vedic_house_7") or {}
    h7_sign = h7.get("sign", "—")
    h10 = facts.get("vedic_house_10") or {}
    h10_sign = h10.get("sign", "—")
    soul = facts.get("soul_urge") or {}
    soul_disp = soul.get("display") or (numerology_display(soul) if soul.get("value") is not None else "—")
    yz = facts.get("year_zodiac", {}).get("animal", "—")
    day_an = facts.get("day_pillar", {}).get("branch_animal", "—")
    who = (imprint.get("birth") or {}).get("name") or "You"
    avoid = compute_signs_to_avoid(facts)

    venus_live = VENUS_LOVE.get(venus, SIGN_MEANS.get(venus, ""))
    mars_live = MARS_FIGHT.get(mars, "")
    moon_live = MOON_RECOVERY.get(moon_w, "")
    h5_live = _house_action(5, h5_sign)
    h7_live = _house_action(7, h7_sign) or HOUSE_7_WALK.get(h7_sign, "")
    h10_live = _house_action(10, h10_sign) or HOUSE_10_WALK.get(h10_sign, "")
    nak_live = _nakshatra_lived(nak) if nak and nak != "—" else ""
    rhyme, warn = _chart_chorus(venus, moon_w, h5_sign, h7_sign, h10_sign)

    p1 = (
        f"{who}, you are not a sun-sign headline — you are a whole bond machine. "
        f"Venus colors how you give and receive love: {venus_live} "
        f"Mars is where passion and argument heat: {mars_live} "
        f"Moon is what you need after a fight to come back human: {moon_live} "
        f"Western astrology calls this the triangle of desire, fight, and repair; get all three right or the relationship limps."
    )

    p2 = (
        f"In the houses, romance (5th) looks like this in your life: {h5_live} "
        f"Partnership and contract (7th) looks like this: {h7_live} "
        f"Work, mentors, and public reputation (10th) bleed into love unless you fence them: {h10_live} "
        f"You're strongest when you write one fairness sentence in {h7_sign} language before bodies negotiate — "
        f"who pays, who apologizes first, who owns the mistake on paper. "
        f"Feed Moon recovery before you renegotiate terms; otherwise you sign treaties while still bleeding."
    )

    p3 = (
        f"Vedic astrology sharpens the emotional core: Moon in {moon_sid} is the comfort test, not the party face. "
        f"{nak_live} "
        f"Soul urge {soul_disp} is private appetite — what you want when no one is performing. "
        f"Stay mindful when that hunger stays unspoken: you host a polite table while starving, then punish the guest for not reading your mind. "
        f"{rhyme} {warn}"
    )

    conflict = (
        f"chasing reunion-{yz} chemistry while living weekday-{day_an} rhythm — the house fights by month three"
        if yz != day_an
        else f"letting reunion-{yz} charisma run the whole house when daily {day_an} pace was never negotiated"
    )
    avoid_clause = (
        f" Until fairness is written, lean away from {', '.join(avoid)} pacing — those signs press your chart before rhythm is clear."
        if avoid
        else ""
    )
    p4 = (
        f"What costs you: {conflict}; love, money, and reputation in one argument because the contract was never plain. "
        f"Year {yz} is first charm; day {day_an} is month-three truth — hire partners for Tuesday, not only Saturday.{avoid_clause} "
        f"Action this week: one boundary sentence, one repair ritual after conflict, one ledger that separates {h10_sign} work bonds from {h7_sign} intimacy."
    )

    text = " ".join([p1, p2, p3, p4])
    words = text.split()
    if len(words) > 470:
        text = " ".join(words[:470]) + "."
    return plain_flesh(text)