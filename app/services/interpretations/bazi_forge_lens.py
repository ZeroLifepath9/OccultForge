"""
BaZi Pillars forge lens — pure Four Pillars read only.
No Vedic, Western, or numerology overlay. Battle-tested brother voice.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.services.bazi_enrich import ensure_bazi_canonical
from app.services.interpretations.eastern_rising_lens import (
    _BRANCH_DAY,
    _BRANCH_DEFAULT_DAY,
    _BRANCH_DEFAULT_HOUR,
    _BRANCH_HOUR,
    _ELEMENT_RHYTHM,
    _GATE_CONTEXT,
    _MONTH_STRUCTURE_ASK,
    _STEM_CORE,
    _STEM_FORGE,
)
from app.services.imprint_labels import branch_animal, combined_pillar_label
from app.services.interpretations.matrix_decoder_voice import format_matrix_reading


def _who(imprint: dict[str, Any]) -> str:
    birth = imprint.get("birth") or {}
    alias = (birth.get("commonly_known_as") or "").strip()
    return alias or birth.get("name") or birth.get("display_name") or "Seeker"


def _spoken_birth(facts: dict[str, Any]) -> str:
    raw = (facts.get("birth") or {}).get("datetime_local") or ""
    raw = raw.replace("Z", "")
    if not raw:
        return "your sealed birth moment"
    try:
        dt = datetime.fromisoformat(raw)
        hour = dt.strftime("%I").lstrip("0") or "12"
        minute = dt.strftime("%M")
        ampm = dt.strftime("%p")
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}, {hour}:{minute} {ampm}"
    except ValueError:
        return raw[:16].replace("T", " ")


def _birth_place(facts: dict[str, Any]) -> str:
    return (facts.get("birth") or {}).get("place") or ""


def _branch_day(animal: str) -> dict[str, str]:
    return _BRANCH_DAY.get(animal, _BRANCH_DEFAULT_DAY)


def _branch_hour(animal: str) -> dict[str, str]:
    return _BRANCH_HOUR.get(animal, _BRANCH_DEFAULT_HOUR)


def _simplify_hook(hook: str) -> str:
    text = (hook or "").strip()
    if "—" in text:
        text = text.split("—", 1)[-1].strip()
    return text or "this lane sets tone in daily outcomes"


def _plain_pillar_line(pillar_key: str, card: dict[str, Any]) -> str:
    context = _GATE_CONTEXT[pillar_key]
    animal = card.get("branch_animal", "")
    day_lens = _branch_day(animal) if animal else {}
    visible = card.get("visible_element", "")
    hook = _simplify_hook(card.get("advice_hook", "") or card.get("synergy_note", ""))
    lens = day_lens.get("lens", "distinct rhythm")
    inner = (card.get("hidden") or {}).get("element", "")
    inner_bit = ""
    if inner and inner != visible:
        inner_bit = (
            f" Underneath runs quieter {inner} — the feeling before you can explain it in words."
        )
    tg = card.get("ten_god_plain", "")
    tg_bit = f" Ten-god read vs Day Master: {tg}." if tg else ""
    if pillar_key == "day" and day_lens:
        return (
            f"{context} Yours moves with {lens} and {visible} on top — "
            f"sovereignty feels like: {day_lens.get('sovereignty', '')} In practice: {hook}.{inner_bit}{tg_bit}"
        )
    return (
        f"{context} Yours moves with {lens} energy and {visible} on top — in practice: {hook}.{inner_bit}"
    )


def _balance_alert(lens: dict[str, Any], dm_el: str) -> str | None:
    balance = (lens.get("balance") or {}).get("balance_insight", "")
    if not balance:
        return None
    low = balance.lower()
    if "light on" not in low and "watch for" not in low and "strong on" not in low:
        return None
    plain = balance.split("Day Master")[0].strip().rstrip(".").replace("藏干", "hidden energy")
    return (
        "Element balance — five fuel tanks in your chart. "
        f"{plain} When one tank runs low, life feels uphill by default — "
        f"feed the weak lane with real food, people, and work that match it."
    )


def _latent_alert(lens: dict[str, Any]) -> str | None:
    latent = (lens.get("balance") or {}).get("latent_insight", "")
    if not latent:
        return None
    plain = latent.replace("藏干", "hidden stems").strip()
    return (
        f"Hidden stem weight — what counts inside the math: {plain} "
        "Schedule proof before you pitch when inner weight outruns the visible stem."
    )


def _luck_influence_line(luck_lens: dict[str, Any]) -> str:
    intro = (
        "Luck pillar — ten-year life chapter over your birth gates; long arc for career, moves, and what the world hands you."
    )
    current = luck_lens.get("current") or {}
    if not current or current.get("is_minor_period"):
        return (
            f"{intro} Still in warm-up — build day and month gates; "
            "skip betting the whole mission before the chapter fully opens."
        )
    years_in = current.get("years_into_decade")
    years_left = current.get("years_remaining")
    citation = luck_lens.get("advice_citation", "")
    years_bit = f" Year {years_in} of this chapter." if years_in else ""
    left_bit = f" ~{years_left} years left — plan handoffs, not panic pivots." if years_left and years_left <= 5 else ""
    core = citation or f"Active chapter: {current.get('identity', 'this season')}."
    return f"{intro}{years_bit} {core}{left_bit}"


def _luck_direct_sentence(luck_lens: dict[str, Any]) -> str:
    current = luck_lens.get("current") or {}
    if not current or current.get("is_minor_period"):
        return "Luck pillar still warming — day and month gates carry most weight for now."
    identity = current.get("identity", "this decade")
    years_in = current.get("years_into_decade")
    bit = f", year {years_in}" if years_in else ""
    return f"Luck pillar runs {identity}{bit} — big moves land cleaner when they fit this chapter, not last one's costume."


def _forge_day_master(dm: dict[str, Any]) -> str:
    stem = dm["english"]
    core = _STEM_CORE.get(stem, f"{dm['yin_yang']} {dm['element']}")
    action = _STEM_FORGE.get(stem, f"land one {dm['element'].lower()} deliverable that compounds before you perform")
    return (
        f"Day Master — core is {core}. Finish one thing first: {action} — "
        f"then step into rooms that did not build it."
    )


def _forge_day_gate(day_an: str) -> str:
    b = _branch_day(day_an)
    return (
        f"Day gate — weekday sovereignty. {b['sovereignty']} "
        f"Grind rule: treat the weekday list like paychecks and bills — {b['grind']}"
    )


def _forge_hour_gate(hour_an: str) -> str:
    h = _branch_hour(hour_an)
    return (
        f"Hour gate — private engine: {h['engine']}. "
        f"This is where you recover and do {h['craft']}. "
        f"Protect {h['protect']} — public gates spend hour-gate fuel if this tank is empty."
    )


def _forge_luck() -> str:
    return (
        "Luck pillar — this ten-year chapter is weather, not orders. Focus visible feats brick by brick; "
        "put in the work and commit to the grind — skip getting lost in twelve parallel fantasies."
    )


def _pillar_anchor_line(pillar_key: str, pillar: dict[str, Any], card: dict[str, Any] | None) -> str:
    label = combined_pillar_label(pillar, year_style=(pillar_key == "year"))
    stem = pillar.get("stem_en") or pillar.get("stem", "")
    branch = pillar.get("branch_en") or pillar.get("branch_animal") or branch_animal(pillar.get("branch", ""))
    visible = card.get("visible_element", "") if card else pillar.get("stem_element", "")
    role = _GATE_CONTEXT.get(pillar_key, pillar_key)
    return (
        f"{role.split('—')[0].strip()} — {label}: "
        f"stem carries {visible or 'element'} tone; branch {branch} sets animal rhythm."
    )


def build_bazi_forge_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    imp = ensure_bazi_canonical(imprint)
    who = _who(imprint)
    spoken = _spoken_birth(facts)
    place = _birth_place(facts)
    place_bit = f", {place}" if place else ""

    dm = facts["day_master"]
    el = dm["element"]
    stem = dm["english"]
    yy = dm["yin_yang"]
    pillars = imp["bazi"]["pillars"]
    day_combined = combined_pillar_label(pillars["day"])
    year_combined = combined_pillar_label(pillars["year"], year_style=True)
    yz_an = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    hour_pillar = pillars["hour"]
    hour_an = hour_pillar.get("branch_animal") or branch_animal(hour_pillar.get("branch", ""))
    if not day_an:
        day_an = branch_animal(
            facts.get("day_pillar", {}).get("branch_hanzi", "")
            or pillars["day"].get("branch", "")
        )

    lens = imp["bazi"].get("interpretation_lens") or {}
    lens_pillars = lens.get("pillars") or {}
    luck_lens = lens.get("luck_pillar") or imp["bazi"].get("luck", {}).get("interpretation") or {}
    month_card = lens_pillars.get("month") or {}
    month_el = month_card.get("visible_element", "")

    day_lens = _branch_day(day_an)
    year_lens = _branch_day(yz_an)
    rhythm = _ELEMENT_RHYTHM.get(el, _ELEMENT_RHYTHM["Earth"])
    stem_core = _STEM_CORE.get(stem, f"{yy} {el}")

    year_day = (
        f"Year gate ({year_lens['lens']}) and day gate ({day_lens['lens']}) rhyme — charm and grind speak one language; "
        "main risk is hiding from your own volume."
        if yz_an == day_an
        else (
            f"Year gate ({year_lens['lens']}) meets the world fast; day gate ({day_lens['lens']}) finishes the work — "
            "schedule the grind or resentment follows."
        )
    )

    direct = (
        f"{who}, born {spoken}{place_bit} — BaZi imprint, straight talk. "
        f"Four gates stack life: year is public inheritance, month is work-season, day is weekday you, hour is private fuel. "
        f"You are {yy} {el} Day Master {stem} on a {day_an} branch — day pillar {day_combined}; year pillar {year_combined}. "
        f"Core: {stem_core}. {rhythm} {year_day} {_luck_direct_sentence(luck_lens)}"
    )

    influence_lines: list[str] = []
    for key in ("year", "month", "day", "hour"):
        pillar = pillars.get(key) or {}
        card = lens_pillars.get(key) or {}
        if pillar:
            influence_lines.append(_pillar_anchor_line(key, pillar, card))
        if card:
            influence_lines.append(_plain_pillar_line(key, card))

    for line in (lens.get("chart_interactions") or [])[:3]:
        if line and line not in influence_lines:
            influence_lines.append(line)

    alert = _balance_alert(lens, el)
    if alert:
        influence_lines.append(alert)
    latent = _latent_alert(lens)
    if latent:
        influence_lines.append(latent)
    influence_lines.append(_luck_influence_line(luck_lens))

    decoded = "\n".join(influence_lines)
    month_ask = _MONTH_STRUCTURE_ASK.get(month_el, "structure and honest pacing")

    steps = [
        _forge_day_master(dm),
        _forge_day_gate(day_an),
        _forge_hour_gate(hour_an),
        _forge_luck(),
        (
            "Element balance — weekly check which fuel tank feels empty; "
            "feed it with real food, people, and tasks that match, not performance."
        ),
        (
            "Timing journal — once a month write what peaked, what drained, "
            "and what the same gate keeps asking until you answer it."
        ),
    ]
    for directive in (lens.get("advice_directives") or [])[:2]:
        clean = directive.split("—")[-1].strip() if "—" in directive else directive.strip()
        if clean and clean not in steps:
            steps.insert(4, clean)

    avoids = [
        (
            f"Core drift — you run {stem_core}. Performing against that to impress a room that will not pay you "
            f"drains the forge — {_STEM_FORGE.get(stem, 'return to one honest deliverable')}."
        ),
        (
            f"Charm vs grind — year energy ({year_lens['lens']}) opens doors; day energy ({day_lens['lens']}) closes tasks. "
            "Letting first impression spend what weekday work has not earned taxes the mission."
        ),
        (
            "Wrong decade costume — each ten-year luck chapter has different homework. "
            "Last chapter's playbook in a new chapter replays the same stuck season."
        ),
        (
            f"Month gate avoidance — month gate runs career seasons; yours wants {month_ask}. "
            "Blaming bad luck for messy structure when the assignment was order replays the valley."
        ),
        (
            "Hidden stem override — when inner element outruns the visible stem, pitch before proof "
            "and everyone reads confidence instead of competence."
        ),
    ]

    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:7], 1))
    avoid_lines = "\n".join(f"- {a}" for a in avoids[:5])
    action = f"Forge now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"

    return format_matrix_reading(direct, decoded, action)