"""
Matrix Decoder Advisor — blunt 3-part reads from sealed chart data.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo

from app.services.imprint_labels import combined_pillar_label, stem_english
from app.services.overview_lore import LIFE_PATH_TRIAL, LIFE_PATH_TRIUMPH, build_zero_verdict

MATRIX_CLOSE = "Matrix decoded."
DAILY_MATRIX_PAYWALL_TEASE = (
    "Daily Matrix read — today's sky overlaid on this sealed chart — "
    "premium access opening soon."
)

_SECTION_DIRECT = "**Direct Answer**"
_SECTION_DECODED = "**Decoded Insight**"
_SECTION_ACTION = "**Action**"


def format_matrix_reading(
    direct: str,
    decoded: str,
    action: str,
    *,
    close_with_matrix_decoded: bool = False,
) -> str:
    parts = [
        f"{_SECTION_DIRECT}\n{direct.strip()}",
        f"{_SECTION_DECODED}\n{decoded.strip()}",
        f"{_SECTION_ACTION}\n{action.strip()}",
    ]
    body = "\n\n".join(parts)
    if close_with_matrix_decoded:
        body = f"{body}\n\n{MATRIX_CLOSE}"
    return body


def _birth_tz(imprint: dict[str, Any]) -> ZoneInfo:
    tz_name = (imprint.get("birth") or {}).get("timezone") or "UTC"
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return ZoneInfo("UTC")


def current_sky_month_pillar(imprint: dict[str, Any], reference: date | None = None) -> dict[str, Any]:
    ref = reference or date.today()
    tz = _birth_tz(imprint)
    local_noon = datetime(ref.year, ref.month, ref.day, 12, 0, tzinfo=tz)
    from app.overlay.daily import _current_bazi_pillars

    sky = _current_bazi_pillars(local_noon)
    return sky.get("month") or {}


def chart_data_blurb(
    facts: dict[str, Any],
    imprint: dict[str, Any],
    *,
    luck_lens: dict[str, Any] | None = None,
    month_sky: dict[str, Any] | None = None,
) -> str:
    birth = imprint.get("birth") or {}
    bdt = birth.get("datetime_local", "")[:16].replace("T", " ")
    place = birth.get("place_label") or birth.get("birth_place_label") or ""
    dm = facts["day_master"]
    day_p = facts.get("day_pillar") or imprint["bazi"]["pillars"]["day"]
    day_combined = combined_pillar_label(day_p)
    stem = stem_english(day_p.get("stem", ""))
    branch = day_p.get("branch_en") or day_p.get("branch_animal", "")
    sun = facts.get("sun_sign", "")
    moon = (facts.get("moon") or {}).get("western_sign", "")
    asc = (facts.get("ascendant") or {}).get("western_sign", "")
    lp = facts["life_path"]["display"]
    chunks = [
        f"Born {bdt} {place}".strip(),
        f"{dm['yin_yang']} {dm['element']} Day Master {stem} on {branch} branch ({day_combined})",
        f"{sun} Sun {moon} Moon {asc} Rising",
        f"Life Path {lp}",
    ]
    luck = luck_lens or {}
    current = luck.get("current") or {}
    if current.get("identity"):
        yrs = ""
        if current.get("start_year") and current.get("end_year"):
            yrs = f" ({current['start_year']}–{current['end_year']})"
        chunks.append(f"current {current['identity']} luck pillar{yrs}")
    if month_sky:
        m_stem = month_sky.get("stem_en") or stem_english(month_sky.get("stem", ""))
        m_branch = month_sky.get("branch_en") or month_sky.get("branch", "")
        m_el = month_sky.get("stem_element", "")
        if m_stem or m_branch:
            chunks.append(f"current {m_el} {m_stem} {m_branch} month".strip())
    return "; ".join(c for c in chunks if c)


def _element_control_note(controller: str, target: str) -> str:
    from app.services.interpretations.bazi_hidden_stems import ELEMENT_CONTROLS, ELEMENT_GENERATES

    if ELEMENT_CONTROLS.get(controller) == target:
        return f"{controller} controls {target}"
    if ELEMENT_GENERATES.get(controller) == target:
        return f"{controller} feeds {target}"
    if ELEMENT_CONTROLS.get(target) == controller:
        return f"{target} checks {controller}"
    if ELEMENT_GENERATES.get(target) == controller:
        return f"{target} feeds {controller}"
    if controller == target:
        return f"{controller} stacks on itself"
    return f"{controller} and {target} run parallel pressure"


def build_luck_pillar_matrix(
    luck_lens: dict[str, Any],
    facts: dict[str, Any],
    imprint: dict[str, Any],
    *,
    month_sky: dict[str, Any] | None = None,
) -> str:
    current = luck_lens.get("current")
    if not current:
        minor = luck_lens.get("framework_insight") or (
            "Minor-luck window — natal pillars lead until the first formal decade locks."
        )
        return format_matrix_reading(
            "No formal luck decade is active yet — structure comes from natal pillars, not a 大运 overlay.",
            minor,
            "Build habits on natal day and month rhythm; do not force decade-scale bets before the luck sequence begins.",
            close_with_matrix_decoded=True,
        )

    dm = facts["day_master"]
    dm_el = dm["element"]
    stem_el = current.get("stem_element", "")
    branch_el = current.get("branch_element", "")
    identity = current.get("identity", "")
    gz = current.get("gan_zhi", "")
    phase = current.get("phase_label", "")
    with_you = current.get("working_with_you") or []
    against = current.get("working_against_you") or []
    align = luck_lens.get("alignment_with_natal") or {}
    month_sky = month_sky or {}
    m_el = month_sky.get("stem_element", "")
    m_id = ""
    if month_sky:
        m_stem = month_sky.get("stem_en") or stem_english(month_sky.get("stem", ""))
        m_branch = month_sky.get("branch_en", "")
        m_id = f"{m_el} {m_stem} {m_branch}".strip()

    if against and not with_you:
        direct = f"This decade presses your {dm_el} Day Master — discipline and drag outrun easy expansion."
    elif with_you and not against:
        direct = f"This decade backs your {dm_el} Day Master — output and support land when you finish before you pitch."
    else:
        direct = f"Mixed decade for your {dm_el} Day Master — wins require structure, not mood."

    if m_id and m_el:
        overlap = _element_control_note(m_el, dm_el)
        direct += f" Current month ({m_id}) adds {overlap} on the same clock."

    decoded_parts = [
        f"Luck pillar {identity} ({gz}): stem {stem_el} shapes outward events; branch environment holds {branch_el or 'latent'} undertow.",
        _element_control_note(stem_el, dm_el) + f" against your {dm['yin_yang']} {dm_el} {dm['english']} core.",
    ]
    if phase:
        decoded_parts.append(phase)
    if with_you:
        decoded_parts.append(with_you[0])
    if against:
        decoded_parts.append(against[0])
    summary = align.get("summary", "")
    if summary:
        decoded_parts.append(summary)
    if m_id:
        decoded_parts.append(
            f"Month pillar {m_id} compounds the decade — same-element months accelerate; control-cycle months invoice patience."
        )
    decoded = " ".join(decoded_parts)

    action_bits = []
    if against:
        action_bits.append("Guard against forced merges and unsigned scope — the decade fines speed without structure.")
    if with_you:
        action_bits.append("Schedule one finished deliverable before visibility plays; leverage stem openings in the first half if phase is stem-led.")
    if (current.get("years_remaining") or 99) <= 2:
        action_bits.append("You are in a luck transition (交运) — stabilize books and health, not rebrands.")
    if not action_bits:
        action_bits.append("Track decade pace against month tempo — act on proof, not applause.")
    action = " ".join(action_bits[:3])

    return format_matrix_reading(direct, decoded, action, close_with_matrix_decoded=True)


def _who(imprint: dict[str, Any]) -> str:
    birth = imprint.get("birth") or {}
    alias = (birth.get("commonly_known_as") or "").strip()
    return alias or birth.get("name") or birth.get("display_name") or "you"


def build_bazi_matrix(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    from app.services.bazi_enrich import ensure_bazi_canonical

    imp = ensure_bazi_canonical(imprint)
    who = _who(imprint)
    lens = imp["bazi"].get("interpretation_lens") or {}
    luck_lens = lens.get("luck_pillar") or imp["bazi"].get("luck", {}).get("interpretation") or {}
    pillars = imp["bazi"]["pillars"]
    dm = facts["day_master"]
    el = dm["element"]
    stem = dm["english"]
    yy = dm["yin_yang"]
    day_combined = combined_pillar_label(pillars["day"])
    year_combined = combined_pillar_label(pillars["year"], year_style=True)
    month_el = pillars["month"].get("stem_element", "")
    yz_an = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    hour_an = pillars["hour"].get("branch_animal", "")
    lens_pillars = lens.get("pillars") or {}
    interactions = lens.get("chart_interactions") or []
    directives = lens.get("advice_directives") or []
    balance = (lens.get("balance") or {}).get("balance_insight", "")
    latent = (lens.get("balance") or {}).get("latent_insight", "")

    if yz_an == day_an:
        direct = (
            f"{who}, you are {yy} {el} {stem} with {day_an} daily rhythm — "
            f"family cast and weekday self agree, so drift is the main risk."
        )
    else:
        direct = (
            f"{who}, you are {yy} {el} {stem} with {day_an} weekday grind against {yz_an} year inheritance — "
            f"charm lands fast; finished work must be scheduled or resentment follows."
        )

    decoded_parts = [
        f"Day pillar {day_combined}: stem {stem} ({el}), branch {day_an} — this is the hand on daily execution.",
        f"Year pillar {year_combined} sets room entry; month {month_el} sets seasonal pace; hour {hour_an} is private fuel.",
    ]
    for key in ("year", "month", "day", "hour"):
        card = lens_pillars.get(key) or {}
        hook = card.get("advice_hook", "")
        if hook:
            decoded_parts.append(hook)
    if interactions:
        decoded_parts.append(interactions[0])
    if balance:
        decoded_parts.append(balance)
    if latent:
        decoded_parts.append(latent)
    luck_cite = (luck_lens.get("current") or {}).get("advice_citation", "")
    if luck_cite:
        decoded_parts.append(luck_cite)
    decoded = " ".join(decoded_parts[:8])

    action_parts = []
    if directives:
        action_parts.append(directives[0].split("—")[-1].strip() if "—" in directives[0] else directives[0])
    action_parts.append(
        f"Finish one {el} deliverable before the next pitch; protect recovery the way you protect payroll."
    )
    if month_el and month_el != el:
        action_parts.append(f"When {month_el} seasons push faster than {stem} wants to commit, narrow scope — that is timing pressure, not rejection.")
    action = " ".join(action_parts[:3])

    return format_matrix_reading(direct, decoded, action)


def build_zero_matrix_overview(facts: dict[str, Any], name: str) -> str:
    from app.services.interpretations.zero_forge_lens import build_zero_forge_lens_reading

    return build_zero_forge_lens_reading(facts, name)


def build_numerology_matrix(
    facts: dict[str, Any],
    imprint: dict[str, Any],
    panels: dict[str, Any] | None = None,
) -> str:
    from app.services.interpretations.numerology_panels import build_numerology_panels

    panels = panels or build_numerology_panels(facts, imprint)
    who = (imprint.get("birth") or {}).get("commonly_known_as") or imprint["birth"]["name"]
    lp = panels["life_path"]
    friends = ", ".join(str(n) for n in panels.get("friend_numbers", []))
    enemies = ", ".join(str(n) for n in panels.get("enemy_numbers", []))
    pi = panels["path_insight"]

    direct = (
        f"{who}, life path {lp['display']} sets the finish — "
        f"{panels['compound_title']}; public mask and private heat either rhyme or tax the same road."
    )
    decoded = (
        f"Born {panels['birth_date']} ({panels['birth_digit_sum']}). "
        f"Friend field: {friends}. Enemy field: {enemies}. "
        f"{panels['compound_subtitle']} Avatar pattern: {pi['avatar']} "
        + " ".join(
            f"{row['label']} {row['display']}: {row['advice']}"
            for row in panels.get("other_totals", [])
        )
    )
    action = (
        f"Stack care on friend-field numbers ({friends}); treat enemy-field numbers ({enemies}) as high-risk contracts. "
        f"Finish life path {lp['display']} work before marketing the mask."
    )
    return format_matrix_reading(direct, decoded, action)


def build_vedic_matrix(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    from app.services.interpretations.vedic_forge_lens import build_vedic_forge_reading

    return build_vedic_forge_reading(facts, imprint)


def build_hellenistic_matrix(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    from app.services.interpretations.hellenistic_forge_lens import build_hellenistic_forge_reading

    return build_hellenistic_forge_reading(facts, imprint)


def build_financial_matrix(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    from app.services.interpretations.financial_forge_lens import build_financial_forge_reading

    return build_financial_forge_reading(facts, imprint)


def build_wealth_matrix(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    from app.services.interpretations.wealth_chart_lens import build_wealth_chart_lens, wealth_flow_paragraphs

    wealth_lens = build_wealth_chart_lens(imprint)
    p1, p2, p3 = wealth_flow_paragraphs(wealth_lens, facts, imprint)
    direct = p1
    decoded = p2
    action = p3.replace("What costs you:", "").strip() if "What costs you:" in p3 else p3
    return format_matrix_reading(direct, decoded, action)


def build_relationships_matrix(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    from app.services.interpretations.relationships_framing import (
        VENUS_LOVE,
        MARS_FIGHT,
        MOON_RECOVERY,
        _chart_chorus,
        _house_action,
        _nakshatra_lived,
        _vedic_house,
        compute_signs_to_avoid,
    )
    from app.services.overview_lore import HOUSE_10_WALK, HOUSE_7_WALK
    from app.services.phoenix_insight import SIGN_MEANS
    from app.services.imprint_labels import numerology_display

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
    who = _who(imprint)
    avoid = compute_signs_to_avoid(facts)
    rhyme, warn = _chart_chorus(venus, moon_w, h5_sign, h7_sign, h10_sign)

    direct = (
        f"{who}, you are not a sun-sign headline — you are a whole bond machine. "
        f"Venus in {venus} colors how you give and receive love: {VENUS_LOVE.get(venus, SIGN_MEANS.get(venus, ''))}"
    )
    decoded = (
        f"Mars in {mars} is where passion and argument heat: {MARS_FIGHT.get(mars, '')} "
        f"Moon in {moon_w} is repair after conflict: {MOON_RECOVERY.get(moon_w, '')} "
        f"5th house {h5_sign} romance: {_house_action(5, h5_sign)} "
        f"7th house {h7_sign} partnership: {_house_action(7, h7_sign) or HOUSE_7_WALK.get(h7_sign, '')} "
        f"10th house {h10_sign} public bonds: {_house_action(10, h10_sign) or HOUSE_10_WALK.get(h10_sign, '')} "
        f"Vedic Moon {moon_sid}; nakshatra {nak}: {_nakshatra_lived(nak) if nak and nak != '—' else ''} "
        f"Soul urge {soul_disp} is private appetite. {rhyme} {warn}"
    )
    avoid_clause = (
        f" Lean away from {', '.join(avoid)} pacing until fairness is written."
        if avoid
        else ""
    )
    action = (
        f"You're strongest when you write one fairness sentence in {h7_sign} language before bodies negotiate. "
        f"Feed Moon recovery before you renegotiate terms; otherwise you sign treaties while still bleeding. "
        f"Action this week: one boundary sentence, one repair ritual after conflict, one ledger separating "
        f"{h10_sign} work bonds from {h7_sign} intimacy.{avoid_clause} "
        f"Year {yz} is first charm; day {day_an} is month-three truth — hire partners for Tuesday, not only Saturday."
    )
    return format_matrix_reading(direct, decoded, action)


def is_matrix_reading(text: str) -> bool:
    return _SECTION_DIRECT in text and _SECTION_DECODED in text and _SECTION_ACTION in text