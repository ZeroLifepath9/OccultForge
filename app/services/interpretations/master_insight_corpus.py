"""
Occult-master insight — chart-grounded, direct, how-first voice.
Chart factors appear in failure vignettes, not as recited labels in the how-to.
"""

from __future__ import annotations

from typing import Any

from app.services.imprint_labels import combined_pillar_label
from app.services.interpretations.manifestation_voice import manifest_animal, manifest_compound, manifest_pillar_element, plain_flesh
from app.services.interpretations.episode_voice import EpisodeReading, bullet_list
from app.services.overview_lore import ELEMENT_SEASON


def _name(imprint: dict[str, Any]) -> str:
    birth = imprint.get("birth") or {}
    alias = (birth.get("commonly_known_as") or "").strip()
    return alias or birth.get("name") or birth.get("display_name") or "you"


def build_bazi_master(facts: dict[str, Any], imprint: dict[str, Any]) -> EpisodeReading:
    dm = facts["day_master"]
    pillars = imprint["bazi"]["pillars"]
    yz = facts["year_zodiac"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    month_el = pillars["month"].get("stem_element", "")
    year_combined = combined_pillar_label(pillars["year"], year_style=True)
    day_combined = combined_pillar_label(pillars["day"])
    hour_an = pillars["hour"].get("branch_animal", facts["pillars"]["hour"].get("branch_animal", ""))
    el = dm["element"]
    stem = dm["english"]
    yy = dm["yin_yang"]
    yz_an = yz["animal"]
    el_how = manifest_pillar_element(el)
    an_how = manifest_animal(day_an)

    scene = (
        f"You grew up inside {yz_an} noise — ENVIRONMENT ({year_combined}) is the room that taught you "
        f"how loud to be before anyone asked your name. Behind closed doors you run {yy} {el} {stem} "
        f"with {day_an} pacing — DAY PILLAR ({day_combined}): stem is constitution, branch is daily movement. "
        f"The reunion version is not the whole story; weekday-you is the person who {an_how.lower()}"
    )

    edge = (
        f"Your edge lands when you finish one real deliverable before you pitch the next one. "
        f"{el_how} Block quiet hours for completion; let {yz_an} charm open doors after the work exists. "
        f"Month {month_el or 'season'} energy {ELEMENT_SEASON.get(month_el, 'shapes offer timing')} — "
        f"take the meeting when the room matches your pace, not when applause is loudest. "
        f"Hour {hour_an} hunger is private fuel — protect sleep and recovery like payroll."
    )

    mindful = (
        f"Watch pace, not identity. When environment and day disagree you feel miscast — "
        f"that is two rhythms, not two selves. {month_el or 'Career'} seasons will push faster "
        f"than {el} craft wants to sign; read timing before you read rejection."
    )

    costs = bullet_list(
        [
            f"You polish the intro until the body never ships — {el} perfection mistaken for readiness.",
            f"You say yes as reunion-{yz_an}, then resent weekday-{day_an} grind — two costumes, one tired body."
            if yz_an != day_an
            else f"You sprint because {yz_an} year taught you visible motion wins rooms — then {el} craft starves for depth.",
            "You wait for permission while a lesser draft takes the credit — spectacle ate substance.",
        ]
    )

    together = (
        f"ENVIRONMENT ({year_combined}) sets noise; DAY PILLAR ({day_combined}) sets Tuesday truth. "
        f"Work the edge through finished output; the leak is performing the year animal while {stem} stem starves."
    )

    return EpisodeReading(
        tradition_title="BAZI PILLARS AND EASTERN ASTROLOGY",
        scene=scene,
        edge=edge,
        mindful=mindful,
        costs=costs,
        together=together,
    )


def build_numerology_master(facts: dict[str, Any], imprint: dict[str, Any]) -> EpisodeReading:
    lp = facts["life_path"]
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    bday = facts.get("birthday_number") or {}
    pers = facts.get("personality") or {}
    who = _name(imprint)
    birth_name = imprint["birth"]["name"]
    flesh = plain_flesh(manifest_compound(lp["compound"], lp["value"], lp["display"]))
    bd = facts.get("birth_day", "—")

    scene = (
        f"{who}, your numbers are not separate lives — one plot with different pockets. "
        f"Birth path {lp['display']} is the road your body already knows: {flesh} "
        f"Public field {expr.get('display', lp['display'])} is the handshake; "
        f"private {soul.get('display', '—')} is appetite after the door shuts."
    )

    edge = (
        f"Lead with what your body has already earned — schedule the {lp['display']} kind of finish first, "
        f"then let {expr.get('display', lp['display'])} market it. On day {bd} each month, run a small "
        f"maintenance pass — one invoice, one boundary, one cleared inbox — before you debate the next big move. "
        f"Personality {pers.get('display', '—')} wins trust in the first five minutes; keep the deeper "
        f"{soul.get('display', lp['display'])} need fed in private so resentment does not write contracts."
    )

    mindful = (
        f"When public {expr.get('display', '')} and birth {lp['display']} pull different directions, "
        f"price and partner choice get loud before words do. Treat birth-day {bday.get('display', '—')} "
        f"as a monthly rhythm, not a mood swing."
    )

    costs = []
    if expr.get("value") and soul.get("value") and expr["value"] != soul["value"]:
        costs.append(
            f"You book the {expr['display']} calendar while {soul['display']} appetite simmers — "
            f"then you sign something tired on a Sunday and call it fate."
        )
    if lp["compound"] != lp["value"]:
        costs.append(
            f"You spend like compound {lp['compound']} landed but only final {lp['value']} is paid for — "
            f"the gap shows up as buyer's remorse, not bad luck."
        )
    costs.extend(
        [
            f"You market a number {birth_name}'s body has not finished earning — trailer before the film exists.",
            "You treat birth-day tide as excuse instead of rhythm — same leak every month on the same date.",
        ]
    )

    return EpisodeReading(
        tradition_title="NUMEROLOGY",
        scene=scene,
        edge=edge,
        mindful=mindful,
        costs=bullet_list(costs[:3]),
        together=(
            f"One suitcase — {lp['display']} is the road. "
            f"The leak is scheduling the mask over the appetite until resentment moves in."
        ),
    )


def build_vedic_master(facts: dict[str, Any], imprint: dict[str, Any]) -> EpisodeReading:
    lagna = imprint["vedic"]["lagna"]["sign"]
    moon = facts["moon"]
    nak = moon.get("nakshatra", "")
    sid = moon.get("sidereal_sign", "")
    dasha = facts.get("mahadasha") or imprint["vedic"]["dasha"]["active_mahadasha"]
    lord = dasha.get("lord", "")
    h2 = facts["vedic_house_2"]["sign"]
    h7 = facts["vedic_house_7"]["sign"]
    h10 = facts["vedic_house_10"]["sign"]
    who = _name(imprint)

    scene = (
        f"{who}, your body walks into rooms on {lagna} law — sleep, food, and entry either match or fatigue "
        f"bills you later. Moon in {nak} ({sid}) is the hunger under every bond; this chapter runs under "
        f"{lord} season — big moves land cleaner when they match the chapter, not the hype."
    )

    edge = (
        f"Honor {lagna} body-truth before you perform for strangers — eat, rest, and enter on your terms. "
        f"After conflict, feed {nak} need before you negotiate again. "
        f"Money habits echo {h2}; fairness echoes {h7}; reputation echoes {h10} — "
        f"keep those three rooms on separate ledgers so love and invoices stop sharing one fight."
    )

    mindful = (
        f"Major moves that ignore {lord} season feel expensive in the body before the spreadsheet. "
        f"When {h7} fairness and {h2} values diverge, the argument looks personal but it is bookkeeping."
    )

    costs = bullet_list(
        [
            f"You perform tropical costume while {lagna} body starves — fatigue arrives before the drama.",
            f"You launch during the wrong chapter — {lord} season says wait, ego says now, and both send a bill.",
            f"You merge love and money in one fight because {h7} and {h2} were never written down separately.",
        ]
    )

    return EpisodeReading(
        tradition_title="VEDIC / JYOTISH",
        scene=scene,
        edge=edge,
        mindful=mindful,
        costs=costs,
        together=f"Body first ({lagna}), hunger second ({nak}), season third ({lord}). The leak is performing health you never live.",
    )


def build_hellenistic_master(facts: dict[str, Any], imprint: dict[str, Any]) -> EpisodeReading:
    asc = imprint["western"]["angles"]["ascendant"]["sign"]
    sun = facts["sun_sign"]
    mc = imprint["western"]["angles"]["midheaven"]["sign"]
    moon = facts["moon"]["western_sign"]
    who = _name(imprint)

    scene = (
        f"{who}, strangers meet {asc} first — the handshake before truth. "
        f"Sun in {sun} is what you keep pushing for when tired; Moon in {moon} is what actually soothes you. "
        f"Midheaven {mc} is what the credits say after the project ends."
    )

    edge = (
        f"Open with {asc} ease, then deliver {sun} will — charm gets the meeting, substance keeps the room. "
        f"Schedule recovery that feeds Moon in {moon}; burnout is what happens when the mask never comes off. "
        f"Build toward {mc} reputation with finished work, not with louder self-promotion."
    )

    mindful = (
        f"When {asc} rising and {sun} Sun want different stories, you can win rooms you did not mean to keep. "
        f"Intensity is not the same as progress — watch the week you are 'on' without rest."
    )

    costs = bullet_list(
        [
            f"You perform {asc} until {sun} will goes quiet — hired for charm, emptied for strategy."
            if asc != sun
            else f"Sun and {asc} share one spotlight — you are 'on' until the body quits before the mind does.",
            "You collect praise for the intro and never ship the middle — reputation runs ahead of reality.",
            f"You soothe with the wrong medicine because Moon in {moon} was skipped after the fight.",
        ]
    )

    return EpisodeReading(
        tradition_title="HELLENISTIC CHART",
        scene=scene,
        edge=edge,
        mindful=mindful,
        costs=costs,
        together=f"Handshake ({asc}), fight ({sun}), soothe ({moon}), legacy ({mc}). The leak is winning the entrance and losing the staying power.",
    )


def build_financial_master(facts: dict[str, Any], imprint: dict[str, Any]) -> EpisodeReading:
    wp = facts.get("western_planets") or {}
    jup = wp.get("Jupiter", {}).get("sign", "")
    sat = wp.get("Saturn", {}).get("sign", "")
    ven = wp.get("Venus", {}).get("sign", "")
    mar = wp.get("Mars", {}).get("sign", "")
    who = _name(imprint)

    scene = (
        f"{who}, your money weather is personal boom-and-audit — optimism leg, paperwork leg. "
        f"Expansion runs {jup}; patience runs {sat}; desire prices through {ven}; push prices through {mar}."
    )

    edge = (
        f"Track dates on your natal pair, not mood. In {jup} seasons, spend on what survives the {sat} audit week. "
        f"Price joy through {ven} honestly — cheap thrills that fail the spreadsheet are fog, not generosity. "
        f"Let {mar} set the pace of effort; sprinting in a paperwork season is how good deals turn sour."
    )

    mindful = (
        "Glamour deals that skip the audit week return as regret, not surprise. "
        "When hype and paperwork share a calendar, the body knows before the bank does."
    )

    costs = bullet_list(
        [
            f"You sign during {jup} weather and discover {sat} fine print in month two — boom ate the audit.",
            "You call fog generosity because the number felt kind before the terms did.",
            "You trade psychology instead of cycles — same personal pattern, new excuse.",
        ]
    )

    return EpisodeReading(
        tradition_title="FINANCIAL ASTROLOGY",
        scene=scene,
        edge=edge,
        mindful=mindful,
        costs=costs,
        together=f"Ride {jup} expansion with {sat} paperwork riding shotgun. The leak is mistaking weather for wisdom.",
    )


def build_wealth_master(facts: dict[str, Any], imprint: dict[str, Any]) -> EpisodeReading:
    dm = facts["day_master"]
    h2 = facts["vedic_house_2"]["sign"]
    lp = facts["life_path"]
    bday = facts.get("birthday_number") or {}
    day_p = facts.get("day_pillar") or facts["pillars"]["day"]
    bd = facts.get("birth_day", "—")
    el = dm["element"]
    who = _name(imprint)

    scene = (
        f"{who}, earning runs {el} craft daily — paychecks that fit Tuesday-you stick. "
        f"Income enters or stalls through {h2}; birth-day {bday.get('display', '—')} on day {bd} "
        f"is monthly fuel; life path {lp['display']} is the finish that still matters when the deposit lands."
    )

    edge = (
        f"Choose work that lets {el} hands finish something tangible each week — income follows completion here. "
        f"On day {bd}, run a money maintenance hour before you say yes to a new lane. "
        f"Keep {h2} values on the invoice: if the pay is right but the toll booth starves {lp['display']} completion, "
        f"the hunger returns after the direct deposit."
    )

    mindful = (
        f"Well-paid work that never lets you finish will outearn you emotionally. "
        f"Vehicle ({day_p.get('gan_zhi', '')}) and toll booth ({h2}) must speak one road language."
    )

    costs = bullet_list(
        [
            f"You take the raise that forbids {el} craft from finishing — rich on paper, hungry on Tuesday.",
            f"You spend birth-day {bday.get('display', '—')} energy on mood, not maintenance — same leak monthly.",
            f"You chase generic money that starves compound {lp['display']} — paycheck without completion.",
        ]
    )

    return EpisodeReading(
        tradition_title="WEALTH CHART",
        scene=scene,
        edge=edge,
        mindful=mindful,
        costs=costs,
        together=f"Earn with {el} hands, enter through {h2}, finish toward {lp['display']}. The leak is pay without completion.",
    )


def build_relationships_master(facts: dict[str, Any], imprint: dict[str, Any]) -> EpisodeReading:
    h7 = facts["vedic_house_7"]["sign"]
    h10 = facts["vedic_house_10"]["sign"]
    moon = facts["moon"]
    nak = moon.get("nakshatra", "")
    soul = facts.get("soul_urge") or {}
    yz = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    who = _name(imprint)

    scene = (
        f"{who}, bonds test at the kitchen table — {h7} fairness is who signs, pays, and gets credit. "
        f"{h10} is mentors, rivals, and work-as-relationship. Moon {nak} is recovery after conflict; "
        f"soul urge {soul.get('display', '—')} is private appetite. Year {yz} is who they think they met; "
        f"day {day_an} is who shows up by month three."
    )

    edge = (
        f"Write fairness in {h7} style before romance or contract deepens — one page beats three resentments. "
        f"Feed Moon {nak} need after fights before you renegotiate. "
        f"Choose partners for weekday-{day_an} rhythm, not only reunion-{yz} charm. "
        f"Keep {h10} professional bonds on career ledgers separate from {h7} intimacy ledgers."
    )

    mindful = (
        "Vague agreements age into resentment quietly. "
        f"When soul urge {soul.get('display', '—')} stays unspoken, the table looks polite and feels starved."
    )

    costs = bullet_list(
        [
            f"You fall for party-{yz}, live with weekday-{day_an} — charm at the door, friction by month three."
            if yz != day_an
            else f"You expect reunion-{yz} chemistry to run the whole house — daily {day_an} pace was never negotiated.",
            "You merge love and money in one argument because fairness was never written down.",
            f"You skip {nak} recovery and sign something emotional while still bleeding from the last fight.",
        ]
    )

    return EpisodeReading(
        tradition_title="RELATIONSHIPS",
        scene=scene,
        edge=edge,
        mindful=mindful,
        costs=costs,
        together=f"Fairness ({h7}), recovery ({nak}), daily truth ({day_an}). The leak is loving the entrance and skipping the rhythm.",
    )