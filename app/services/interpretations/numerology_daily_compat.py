"""Daily numerology imprint — ally/enemy field between calendar day and user seal."""

from __future__ import annotations

import calendar
from datetime import date
from typing import Any, Literal

from app.calculators.numerology import (
    MASTER_NUMBERS,
    calendar_day_number,
    calendar_gate_number,
    life_path_day_number,
    personal_day,
)
from app.services.imprint_labels import numerology_display
from app.services.numerology_depth import PATH_ENEMY_NUMBERS, PATH_FRIEND_NUMBERS

Relation = Literal["friend", "enemy", "neutral"]

MASTER_ENEMY_PAIRS: frozenset[tuple[int, int]] = frozenset(
    {(9, 11), (11, 9), (9, 22), (22, 9), (7, 11), (11, 7)}
)

# Day-field pairs that clash before user overlay (moon vs eclipse, etc.)
DAY_FIELD_TENSION: frozenset[tuple[int, int]] = frozenset({(2, 4), (4, 2)})

# Birth-day digit vs calendar-day digit — oppositional imprint (e.g. 3 vs 6)
IMPRINT_TENSION: frozenset[tuple[int, int]] = frozenset({(3, 6), (6, 3)})

NUMBER_ESSENCE: dict[int, str] = {
    1: "initiative and solo stand",
    2: "moon tide, mirror, and partnership pull",
    3: "voice, visibility, and creative scatter",
    4: "structure, eclipse of feeling, and stone law",
    5: "motion, truth, and restless road",
    6: "hearth, beauty, and service appetite",
    7: "cave study, solitude, and sceptical depth",
    8: "power, accounts, and material crown",
    9: "closure, release, and humanitarian finish",
    11: "master voltage, prophetic nerve, and nervous-system antenna",
    22: "master builder, cathedral scale, and civilizational weight",
    33: "master teacher, compassion as discipline, and healing broadcast",
}

DAY_FIELD_CLASH_LIVED: dict[tuple[int, int], str] = {
    (2, 4): (
        "the moon tide of 2 meets the eclipse of 4 — feeling wants flow while law wants freeze; "
        "controversial, enemy-universal energy in the day itself"
    ),
    (4, 2): (
        "stone law of 4 eclipses the moon tide of 2 — structure blocks the feeling that needed room; "
        "the calendar argues with itself before you even enter"
    ),
}

IMPRINT_CLASH_LIVED: dict[tuple[int, int], str] = {
    (3, 6): (
        "expression meets hearth appetite — charm and care pull in opposite directions; "
        "what looks friendly on paper feels oppositional in the body"
    ),
    (6, 3): (
        "hearth duty meets broadcast voice — service wants order while the day wants performance; "
        "your birth-day rhythm resists the room's volume"
    ),
}

DAY_FIELD_CLASH_ESSENCE: dict[tuple[int, int], str] = {
    (2, 4): (
        "moon tide meets stone law in the universal field — feeling wants flow while structure wants freeze; "
        "the calendar argues with itself before you enter"
    ),
    (4, 2): (
        "stone law eclipses moon tide — structure blocks the feeling that needed room; "
        "contested energy lives in the day itself"
    ),
}


def daily_gate(value: int | None) -> int | None:
    """Reduce for essence clauses — masters keep their face in relation logic."""
    return relation_gate(value)


def relation_gate(value: int | None) -> int | None:
    """Ally/enemy gate — preserve master numbers; do not fold 11→2 for field reads."""
    if value is None:
        return None
    if value in MASTER_NUMBERS:
        return value
    if value <= 9:
        return value
    digits = sum(int(d) for d in str(value))
    if digits in MASTER_NUMBERS:
        return digits
    return digits if digits <= 9 else relation_gate(digits)


def _is_master_value(value: int | None) -> bool:
    return value is not None and value in MASTER_NUMBERS


def _number_face(value: int, num: dict[str, Any] | None = None) -> str:
    """Human label — call out master numbers that do not reduce."""
    if num is not None and num.get("value") == value:
        if num.get("is_master"):
            disp = numerology_display(num)
            suffix = f" ({disp})" if disp != str(value) else ""
            return f"Master {value}{suffix}"
        disp = numerology_display(num)
        if disp != str(value):
            return disp
    if _is_master_value(value):
        return f"Master {value}"
    return str(value)


def numerology_relation(
    a: int | None,
    b: int | None,
    *,
    context: Literal["path", "day_field", "imprint"] = "path",
) -> Relation:
    ga, gb = relation_gate(a), relation_gate(b)
    if ga is None or gb is None:
        return "neutral"
    if ga == gb:
        return "friend"
    pair = (ga, gb)
    if pair in MASTER_ENEMY_PAIRS or (gb, ga) in MASTER_ENEMY_PAIRS:
        return "enemy"
    if context == "day_field" and pair in DAY_FIELD_TENSION:
        return "enemy"
    if context == "imprint" and pair in IMPRINT_TENSION:
        return "enemy"
    if gb in PATH_ENEMY_NUMBERS.get(ga, []) or ga in PATH_ENEMY_NUMBERS.get(gb, []):
        return "enemy"
    if gb in PATH_FRIEND_NUMBERS.get(ga, []) or ga in PATH_FRIEND_NUMBERS.get(gb, []):
        return "friend"
    return "neutral"


def _relation_note(
    a: int,
    b: int,
    relation: Relation,
    *,
    context: str,
    a_num: dict[str, Any] | None = None,
    b_num: dict[str, Any] | None = None,
) -> str:
    ga, gb = relation_gate(a) or a, relation_gate(b) or b
    face_a, face_b = _number_face(ga, a_num), _number_face(gb, b_num)
    if context == "day_field":
        if _is_master_value(gb) or (b_num and b_num.get("is_master")):
            return (
                f"Calendar gate {face_b} — a master number that does not reduce. "
                f"{NUMBER_ESSENCE.get(gb, 'master voltage')} shapes the whole field before you enter."
            )
        if relation == "friend":
            essence = NUMBER_ESSENCE.get(gb, "today's vibration")
            return (
                f"Calendar gate {face_b} compounds cleanly — "
                f"collective energy ({essence}) aligns across the date."
            )
        if relation == "enemy":
            lived = DAY_FIELD_CLASH_LIVED.get((ga, gb))
            if lived:
                return lived
            return (
                f"Calendar gate {face_b} contests the room — "
                f"the collective overlay drags before you enter."
            )
        return (
            f"Calendar gate {face_b} sits neutral — "
            f"the collective backdrop is open; discipline sets the tone."
        )
    if context == "imprint":
        if relation == "enemy":
            lived = IMPRINT_CLASH_LIVED.get((ga, gb))
            if lived:
                return lived
        return (
            f"Birth-day number {ga} modulates today's calendar gate {gb} — "
            f"{NUMBER_ESSENCE.get(ga, 'your day-of-month theme')} meets "
            f"{NUMBER_ESSENCE.get(gb, 'the universal gate')} in the body, not only on paper."
        )
    if relation == "friend":
        path_note = NUMBER_ESSENCE.get(ga, "your path")
        field_note = NUMBER_ESSENCE.get(gb, "today's field")
        return (
            f"Life Path {face_a} harmonizes with Universal Day {face_b} — "
            f"your constant baseline ({path_note}) "
            f"rides today's collective overlay ({field_note}) with ease."
        )
    if relation == "enemy":
        if (ga, gb) in MASTER_ENEMY_PAIRS or (gb, ga) in MASTER_ENEMY_PAIRS:
            return (
                f"Life Path {face_a} meets Universal Day {face_b} as intense enemies — "
                f"master voltage contests your closure field; proof before you merge energy or spend your name."
            )
        return (
            f"Life Path {face_a} meets a challenging Universal Day {face_b} — "
            f"your long-term purpose contrasts today's collective energy; "
            f"growth may come through friction, not flow."
        )
    return (
        f"Life Path {face_a} and Universal Day {face_b} hold neutral field — "
        f"neither harmony nor declared tension; discipline beats drift."
    )


def month_day_field_skew(year: int, month: int) -> dict[str, Any]:
    days = calendar.monthrange(year, month)[1]
    counts = {"friend": 0, "enemy": 0, "neutral": 0}
    for day in range(1, days + 1):
        d = date(year, month, day)
        dom = calendar_day_number(d)["value"]
        gate = calendar_gate_number(d)["value"]
        counts[numerology_relation(dom, gate, context="day_field")] += 1
    dominant = max(counts, key=counts.get)
    ratio = counts[dominant] / days
    return {
        "days_in_month": days,
        "friend_days": counts["friend"],
        "enemy_days": counts["enemy"],
        "neutral_days": counts["neutral"],
        "dominant_tone": dominant,
        "dominant_ratio": round(ratio, 2),
    }


def _essence_pair_clause(a: int, b: int) -> tuple[str, str]:
    ga, gb = daily_gate(a) or a, daily_gate(b) or b
    return NUMBER_ESSENCE.get(ga, "this rhythm"), NUMBER_ESSENCE.get(gb, "that rhythm")


_REL_SCORE: dict[Relation, float] = {"friend": 1.0, "neutral": 0.0, "enemy": -1.0}

_BAZI_TONE_ADJ: dict[str, float] = {
    "supportive": 0.22,
    "neutral": 0.0,
    "clash_muted": -0.06,
    "strained": -0.16,
    "clash_bruised": -0.18,
    "clash_mixed": -0.24,
    "clash_harsh": -0.30,
}


def _score_to_relation(score: float) -> Relation:
    if score >= 0.38:
        return "friend"
    if score <= -0.38:
        return "enemy"
    return "neutral"


DAY_FIELD_PREMIUM_TEASER = (
    "Seeker+ Daily Overlay — how your sealed life path, personal day, and natal sky "
    "compound or strain today's universal field. Premium — opening soon."
)

LIFE_PATH_GATE_PREMIUM_TEASER = (
    "Seeker+ — how your sealed life path meets today's universal day. "
    "Full gate read — premium, opening soon."
)


def _master_day_tail(gv: int) -> str:
    if gv == 11:
        return (
            "Master 11 runs prophetic nerve and nervous-system antenna — ground the voltage, "
            "document proof, and refuse scatter before you merge energy or spend your name."
        )
    if gv == 22:
        return (
            "Master 22 loads cathedral scale — build in phases or the body fails the blueprint; "
            "proof before you touch civilizational weight."
        )
    if gv == 33:
        return (
            "Master 33 broadcasts healing discipline — compassion with boundaries, not savior drift; "
            "teach without paying everyone's bill."
        )
    return (
        "Master days carry double voltage — ground the signal, document proof, "
        "and narrow scope before you merge energy."
    )


def build_universal_territory_read(
    num_overlay: dict[str, Any],
    *,
    life_path_display: str | None = None,
) -> dict[str, Any]:
    """Brief visible read — universal life-path day as territory vs personal and sealed life path."""
    compat = num_overlay.get("compat") or {}
    day_field = compat.get("day_field") or {}
    lpd_num = num_overlay.get("life_path_day") or {}
    pd_num = num_overlay.get("personal_day") or {}
    dom_num = num_overlay.get("day_of_month") or num_overlay.get("calendar_day") or {}

    lpd_val = lpd_num.get("value") or 0
    pd_val = pd_num.get("value") or 0
    dom_val = dom_num.get("value") or day_field.get("calendar_day") or 0
    lpd_disp = lpd_num.get("display", str(lpd_val))
    pd_disp = pd_num.get("display", str(pd_val))
    dom_disp = dom_num.get("display", str(dom_val))
    lp_disp = life_path_display or num_overlay.get("life_path_display") or str(
        num_overlay.get("user_life_path", "")
    )

    day_field_rel: Relation = day_field.get("relation", "neutral")
    lp_vs_lpd = compat.get("user_life_path_vs_life_path_day") or {}
    lp_gate_rel: Relation = lp_vs_lpd.get("relation", "neutral")
    pd_vs_univ = numerology_relation(pd_val, lpd_val, context="path")

    gv = relation_gate(lpd_val) or lpd_val
    is_master = lpd_num.get("is_master") or _is_master_value(gv)
    essence = NUMBER_ESSENCE.get(gv, "today's collective pace")

    if is_master:
        lead = f"Universal day {lpd_disp} is today's territory — master voltage that does not reduce."
    else:
        lead = f"Universal day {lpd_disp} is today's territory — {essence}."

    if pd_vs_univ == "friend":
        personal_line = (
            f"Personal day {pd_disp} walks with the territory — stack finish order while the field backs you."
        )
    elif pd_vs_univ == "enemy":
        personal_line = (
            f"Personal day {pd_disp} contests the territory — proof before you imprint energy today."
        )
    else:
        personal_line = f"Personal day {pd_disp} sits neutral on the territory — timing beats drift."

    if lp_gate_rel == "friend":
        path_line = (
            f"Life Path {lp_disp} harmonizes with universal day {lpd_disp} — your baseline rides the room."
        )
    elif lp_gate_rel == "enemy":
        if is_master or lp_vs_lpd.get("life_path_day_is_master"):
            path_line = (
                f"Life Path {lp_disp} and universal day {lpd_disp} are intense enemies — "
                f"proof before you merge energy."
            )
        else:
            path_line = (
                f"Life Path {lp_disp} meets universal day {lpd_disp} as foes — narrow scope and document."
            )
    else:
        path_line = f"Life Path {lp_disp} holds neutral against universal day {lpd_disp}."

    calendar_line = ""
    if dom_val != lpd_val:
        if day_field_rel == "friend":
            calendar_line = (
                f"Calendar day {dom_disp} and universal day {lpd_disp} are powerful companions — "
                f"the clearest read in the room."
            )
        elif day_field_rel == "enemy":
            calendar_line = (
                f"Calendar day {dom_disp} clashes the territory — step in deliberately."
            )

    parts = [lead, personal_line, path_line]
    if calendar_line:
        parts.append(calendar_line)

    territory_read = " ".join(parts)
    words = territory_read.split()
    if len(words) > 58:
        territory_read = " ".join(words[:58]) + "."

    return {
        "territory_read": territory_read,
        "territory_lead": lead,
        "personal_vs_universal_line": personal_line,
        "life_path_vs_universal_line": path_line,
        "calendar_companion_line": calendar_line,
        "personal_vs_universal_relation": pd_vs_univ,
    }


def build_universal_day_field_interpretation(
    territory_value: int,
    relation: Relation,
    *,
    territory_num: dict[str, Any] | None = None,
    calendar_day_display: str | None = None,
) -> str:
    """Brief day-field footer — calendar day vs universal territory."""
    gv = relation_gate(territory_value) or territory_value
    gate_num = (
        territory_num
        if territory_num and territory_num.get("value") == territory_value
        else None
    )
    face = _number_face(gv, gate_num)
    essence = NUMBER_ESSENCE.get(gv, "today's collective vibration")
    is_master = (gate_num or {}).get("is_master") or _is_master_value(gv)
    cal_face = calendar_day_display or ""

    if is_master:
        return (
            f"Territory {face} — master voltage shapes the room. "
            f"{_master_day_tail(gv)}"
        )

    if relation == "friend" and cal_face:
        return (
            f"Calendar day {cal_face} and territory {face} are companions — "
            f"{essence}; finish something visible without over-editing."
        )
    if relation == "enemy" and cal_face:
        return f"Calendar day {cal_face} clashes territory {face} — narrow scope today."
    if relation == "friend":
        return f"Territory {face} compounds cleanly — {essence}."
    if relation == "enemy":
        return f"Territory {face} carries contested pace — avoid forced merges."
    return f"Territory {face} stays open — discipline beats drift."


def _blend_day_field_relation(
    day_field_rel: Relation,
    lp_vs_lpd: Relation,
    personal_rel: Relation,
    bazi_tone: str,
) -> Relation:
    """Numerology-led day field — BaZi day pillar and element adjust the read."""
    num_score = (
        _REL_SCORE[day_field_rel] * 0.42
        + _REL_SCORE[lp_vs_lpd] * 0.33
        + _REL_SCORE[personal_rel] * 0.25
    )
    blended = num_score * 0.78 + _BAZI_TONE_ADJ.get(bazi_tone, 0.0)
    return _score_to_relation(blended)


def build_day_field_assessment(
    num_overlay: dict[str, Any],
    astrology_layer: dict[str, Any],
) -> dict[str, Any]:
    """One-sentence day field — numerology leads, BaZi compounds or contrasts."""
    compat = num_overlay.get("compat") or {}
    day_field = compat.get("day_field") or {}
    day_field_rel: Relation = day_field.get("relation", "neutral")
    lp_vs_lpd: Relation = (compat.get("user_life_path_vs_life_path_day") or {}).get(
        "relation", "neutral"
    )
    user_lp = num_overlay.get("user_life_path") or 0
    pd_val = (num_overlay.get("personal_day") or {}).get("value") or 0
    lpd_val = (num_overlay.get("life_path_day") or {}).get("value") or 0
    personal_rel = numerology_relation(user_lp, pd_val, context="path")
    personal_vs_lpd = numerology_relation(pd_val, lpd_val, context="path")
    dom_val = (day_field.get("calendar_day") or 0)
    gate_val = day_field.get("calendar_gate") or lpd_val
    personal_vs_calendar = numerology_relation(pd_val, gate_val, context="path")

    day_cmp = (astrology_layer.get("compares") or {}).get("day_vs_sky_day") or {}
    bazi_tone = day_cmp.get("effective_tone", "neutral")
    natal_el = day_cmp.get("natal_element", "")
    sky_el = day_cmp.get("sky_element", "")
    sky_label = day_cmp.get("sky_label") or day_cmp.get("sky_animal", "sky day")
    lpd_disp = (num_overlay.get("life_path_day") or {}).get("display", str(lpd_val))
    pd_disp = (num_overlay.get("personal_day") or {}).get("display", str(pd_val))

    relation = _blend_day_field_relation(
        day_field_rel, lp_vs_lpd, personal_rel, bazi_tone
    )
    user_day_relation = personal_vs_calendar

    lpd_num = num_overlay.get("life_path_day") or {}
    dom_num = num_overlay.get("day_of_month") or num_overlay.get("calendar_day") or {}
    lp_disp = num_overlay.get("life_path_display") or str(user_lp)
    lpd_master = lpd_num.get("is_master") or _is_master_value(lpd_val)
    gate_face = _number_face(lpd_val, lpd_num) if lpd_master else lpd_disp
    if lpd_master:
        num_lead = f"Numerology leads master voltage — calendar gate {gate_face} runs the field"
    elif day_field_rel == "friend":
        num_lead = f"Numerology leads harmony — calendar gate {lpd_disp} aligns the collective field"
    elif day_field_rel == "enemy":
        num_lead = f"Numerology leads challenge — calendar gate {lpd_disp} contests the room"
    else:
        num_lead = f"Numerology reads neutral on calendar gate {lpd_disp}"

    if bazi_tone == "supportive":
        if day_field_rel == "enemy":
            bazi_tail = (
                f"today's {sky_el} sky day pillar feeds your {natal_el} day master "
                f"and softens the numerology drag"
            )
        else:
            bazi_tail = (
                f"today's {sky_el} sky day pillar compounds it through your {natal_el} day master"
            )
    elif bazi_tone in ("clash_harsh", "clash_mixed"):
        if day_field_rel == "friend":
            bazi_tail = (
                f"today's {sky_label} sky day clashes your pillar — BaZi contrasts the numerology tailwind"
            )
        else:
            bazi_tail = (
                f"today's {sky_label} sky day presses your {natal_el} pillar — "
                f"BaZi confirms the numerology strain"
            )
    elif bazi_tone == "strained":
        bazi_tail = (
            f"today's {sky_el} element strains your {natal_el} day master — "
            f"BaZi narrows the numerology read"
        )
    elif bazi_tone == "clash_muted":
        bazi_tail = (
            f"sign clash mutes while {natal_el} holds against {sky_el} — "
            f"BaZi steadies the numerology signal"
        )
    else:
        bazi_tail = (
            f"{natal_el} meets today's {sky_el} sky stem in measured balance with the numerology field"
        )

    assessment = f"{num_lead}; {bazi_tail}."
    words = assessment.split()
    if len(words) > 42:
        assessment = " ".join(words[:42]) + "."

    dom_disp = dom_num.get("display", str(dom_val))
    territory = build_universal_territory_read(num_overlay, life_path_display=lp_disp)
    universal_interpretation = build_universal_day_field_interpretation(
        lpd_val,
        day_field_rel,
        territory_num=lpd_num,
        calendar_day_display=dom_disp,
    )

    return {
        "relation": relation,
        "universal_relation": day_field_rel,
        "life_path_day_is_master": lpd_master,
        "calendar_gate_is_master": lpd_master,
        "universal_interpretation": universal_interpretation,
        "territory_read": territory["territory_read"],
        "territory_lead": territory["territory_lead"],
        "personal_vs_universal_line": territory["personal_vs_universal_line"],
        "life_path_vs_universal_line": territory["life_path_vs_universal_line"],
        "calendar_companion_line": territory["calendar_companion_line"],
        "personal_vs_universal_relation": territory["personal_vs_universal_relation"],
        "life_path_display": lp_disp,
        "premium_teaser": DAY_FIELD_PREMIUM_TEASER,
        "premium_assessment": assessment,
        "user_day_relation": user_day_relation,
        "personal_day_relation": personal_vs_lpd,
        "personal_vs_calendar_relation": personal_vs_calendar,
        "life_path_gate_relation": lp_vs_lpd,
        "life_path_gate_premium_teaser": LIFE_PATH_GATE_PREMIUM_TEASER,
        "numerology_lead": day_field_rel,
        "assessment": assessment,
        "life_path_day_display": lpd_disp,
        "personal_day_display": pd_disp,
        "calendar_day_display": dom_disp,
    }


def build_numerology_gate_line(
    life_path_display: str,
    life_path_day_display: str,
    relation: Relation,
    *,
    life_path_day_is_master: bool = False,
) -> str:
    """One direct sentence — Life Path baseline vs today's Universal Day overlay."""
    day_label = (
        f"Master Universal Day {life_path_day_display}"
        if life_path_day_is_master
        else f"Universal Day {life_path_day_display}"
    )
    if relation == "friend":
        return (
            f"Life Path {life_path_display} harmonizes with {day_label} — "
            f"your constant purpose rides today's collective energy with ease."
        )
    if relation == "enemy":
        if life_path_day_is_master:
            return (
                f"Life Path {life_path_display} meets {day_label} as intense enemies — "
                f"master voltage contests your path; proof before you merge energy."
            )
        return (
            f"Life Path {life_path_display} meets a challenging {day_label} — "
            f"introspection and proof before you merge energy."
        )
    return (
        f"Life Path {life_path_display} and {day_label} hold neutral field — "
        f"your discipline sets the tone more than the calendar."
    )


def build_daily_numerology_insight(
    *,
    user_lp: int,
    user_bday: int,
    personal_day: int,
    compat: dict[str, Any],
    month_skew: dict[str, Any],
) -> str:
    """
    Daily numerology insight — life path baseline against today's universal and personal gates.
    Uses ally/enemy field logic only; no sealed-chart compatibility layer.
    """
    day_field = compat.get("day_field") or {}
    day_field_rel = day_field.get("relation", "neutral")
    lp_vs_lpd = (compat.get("user_life_path_vs_life_path_day") or {}).get("relation", "neutral")
    lp_vs_cal = (compat.get("user_life_path_vs_calendar_day") or {}).get("relation", "neutral")
    bday_vs_cal = (compat.get("user_birthday_vs_calendar_day") or {}).get("relation", "neutral")
    pd_rel = numerology_relation(user_lp, personal_day, context="path")

    lines: list[str] = []

    if day_field_rel == "friend":
        lines.append(
            "Today's Universal Day harmonizes with the calendar gate — collective energy compounds cleanly. "
            "The room carries motion without stealing your finish order."
        )
    elif day_field_rel == "enemy":
        lines.append(
            day_field.get("note", "Today's Universal Day contests the calendar — step in deliberately.")
        )
    else:
        lines.append(
            "The Universal Day field is neutral — your Life Path baseline sets the tone more than the calendar."
        )

    if lp_vs_lpd == "friend":
        lines.append(
            "Your Life Path harmonizes with today's Universal Day — schedule what matters; public moves land cleaner."
        )
    elif lp_vs_lpd == "enemy":
        lines.append(
            (compat.get("user_life_path_vs_life_path_day") or {}).get("note", "")
            or "Your Life Path meets a challenging Universal Day — finish your part, document, and avoid forced merges."
        )
    elif lp_vs_lpd == "neutral":
        lines.append(
            "Your Life Path and today's Universal Day are neutral — discipline beats drift."
        )

    if lp_vs_cal == "friend":
        lines.append(
            "Today's calendar gate harmonizes with your Life Path — contracts and visible stands get tailwind."
        )
    elif lp_vs_cal == "enemy":
        lines.append(
            "Today's calendar gate challenges your Life Path — step lighter on signatures, pitches, and public fights."
        )

    if bday_vs_cal == "enemy":
        lines.append(
            (compat.get("user_birthday_vs_calendar_day") or {}).get("note", "")
            or "Your birth-day number resists today's calendar gate — trust body signal before the room votes."
        )

    if pd_rel == "friend":
        lines.append(
            f"Personal Day {personal_day} compounds your Life Path — stack finish order before novelty."
        )
    elif pd_rel == "enemy":
        lines.append(
            f"Personal Day {personal_day} challenges your Life Path — proof before you imprint energy."
        )

    if month_skew.get("dominant_tone") == "friend" and month_skew.get("dominant_ratio", 0) >= 0.55:
        lines.append(
            "This month leans harmonious — more days where Universal Day and calendar gate align."
        )
    elif month_skew.get("dominant_tone") == "enemy" and month_skew.get("dominant_ratio", 0) >= 0.45:
        lines.append(
            "This month leans challenging — more contested Universal Days land before your chart speaks."
        )

    text = " ".join(line for line in lines if line).strip()
    words = text.split()
    if len(words) > 95:
        text = " ".join(words[:95]) + "."
    return text


def build_daily_number_framing(
    compat: dict[str, Any],
    month_skew: dict[str, Any],
) -> dict[str, list[str]]:
    """Promote/avoid clauses without reciting digits — chips and day-field note carry numbers."""
    promote: list[str] = []
    avoid: list[str] = []

    day_field = compat.get("day_field") or {}
    cd_val = day_field.get("calendar_day")
    lpd_val = day_field.get("life_path_day")
    day_rel = day_field.get("relation", "neutral")
    if cd_val is not None:
        gv = daily_gate(cd_val) or cd_val
        essence = NUMBER_ESSENCE.get(gv, "today's collective vibration")
        is_master = _is_master_value(gv)
        if is_master:
            avoid.append(
                "Master calendar gate — prophetic voltage shapes the room; "
                "ground the signal, document proof, and narrow scope before you merge energy."
            )
        elif day_rel == "friend":
            promote.append(
                f"Calendar gate compounds cleanly — {essence} backs finish order without stealing from you."
            )
        elif day_rel == "enemy":
            avoid.append(f"Calendar gate contests the room — {essence} drags before you enter.")
        else:
            promote.append(
                "Calendar gate is neutral — your Life Path baseline sets the tone more than the calendar."
            )

    lp_vs_lpd = compat.get("user_life_path_vs_life_path_day") or {}
    lp_rel = lp_vs_lpd.get("relation", "neutral")
    if lp_vs_lpd.get("user") is not None and lp_vs_lpd.get("day") is not None:
        ua, da = _essence_pair_clause(lp_vs_lpd["user"], lp_vs_lpd["day"])
        if lp_rel == "friend":
            promote.append(
                f"Life Path harmonizes with Universal Day — {ua} and {da} back your finish order; schedule what matters."
            )
        elif lp_rel == "enemy":
            avoid.append(
                f"Life Path meets a challenging Universal Day — {ua} and {da} cost twice when forced into one room."
            )

    bday_vs_cal = compat.get("user_birthday_vs_calendar_day") or {}
    if bday_vs_cal.get("relation") == "enemy" and bday_vs_cal.get("user") is not None:
        ua, da = _essence_pair_clause(bday_vs_cal["user"], bday_vs_cal["day"])
        ga, gb = daily_gate(bday_vs_cal["user"]) or bday_vs_cal["user"], daily_gate(bday_vs_cal["day"]) or bday_vs_cal["day"]
        lived = IMPRINT_CLASH_LIVED.get((ga, gb))
        avoid.append(
            lived or f"Your birth-day rhythm resists today's gate — {ua} and {da} pull opposite in the body."
        )

    lp_vs_cal = compat.get("user_life_path_vs_calendar_day") or {}
    if lp_vs_cal.get("relation") == "enemy":
        ua, da = _essence_pair_clause(lp_vs_cal.get("user", 0), lp_vs_cal.get("day", 0))
        avoid.append(
            f"Today's calendar gate drags against your path — step lighter on contracts and public stands when {ua} meets {da}."
        )

    if month_skew.get("dominant_tone") == "friend" and month_skew.get("dominant_ratio", 0) >= 0.55:
        promote.append(
            "This month leans harmonious — more days where Universal Day and calendar gate align."
        )
    elif month_skew.get("dominant_tone") == "enemy" and month_skew.get("dominant_ratio", 0) >= 0.45:
        avoid.append(
            "This month leans challenging — more contested Universal Days land before your chart speaks."
        )

    return {"promote": promote[:3], "avoid": avoid[:3]}


def _score_from_relations(relations: list[Relation], *, clashes: list[str]) -> tuple[float, str, str]:
    if clashes:
        return 0.12, "terrible", "caution"
    weights = {"friend": 0.18, "enemy": -0.22, "neutral": 0.0}
    base = 0.52
    for rel in relations:
        base += weights.get(rel, 0.0)
    base = max(0.08, min(0.95, base))
    if base >= 0.78:
        return base, "very-good", "tailwind"
    if base >= 0.58:
        return base, "good", "flow"
    if base >= 0.4:
        return base, "neutral", "ordinary"
    if base >= 0.22:
        return base, "bad", "drag"
    return base, "terrible", "caution"


def build_daily_numerology_overlay(
    imprint: dict[str, Any],
    target: date,
) -> dict[str, Any]:
    birth_dt_str = imprint["birth"]["datetime_local"].replace("Z", "")
    birth_date = date.fromisoformat(birth_dt_str[:10])
    py = imprint["numerology"]["schools"]["pythagorean"]
    user_lp = py["life_path"]["value"]
    user_bday = py["birthday"]["value"]

    cd = calendar_gate_number(target)
    lpd = life_path_day_number(target)
    dom = calendar_day_number(target)
    pd = personal_day(birth_date, target)

    cd_val = cd["value"]
    lpd_val = lpd["value"]
    dom_val = dom["value"]

    day_field_rel = numerology_relation(dom_val, lpd_val, context="day_field")
    lp_vs_calendar = numerology_relation(user_lp, cd_val, context="path")
    lp_vs_lpd = numerology_relation(user_lp, lpd_val, context="path")
    bday_vs_calendar = numerology_relation(user_bday, dom_val, context="imprint")
    pd_val = pd["value"]
    personal_vs_calendar = numerology_relation(pd_val, cd_val, context="path")

    month_skew = month_day_field_skew(target.year, target.month)

    user_lp_num = py["life_path"]
    compat = {
        "day_field": {
            "calendar_day": dom_val,
            "calendar_gate": cd_val,
            "life_path_day": lpd_val,
            "life_path_day_is_master": lpd.get("is_master", False),
            "relation": day_field_rel,
            "note": _relation_note(
                dom_val, lpd_val, day_field_rel, context="day_field", a_num=dom, b_num=lpd
            ),
        },
        "user_life_path_vs_calendar_day": {
            "user": user_lp,
            "day": cd_val,
            "relation": lp_vs_calendar,
            "note": _relation_note(
                user_lp, cd_val, lp_vs_calendar, context="path", a_num=user_lp_num, b_num=cd
            ),
        },
        "user_life_path_vs_life_path_day": {
            "user": user_lp,
            "day": lpd_val,
            "life_path_day_is_master": lpd.get("is_master", False),
            "relation": lp_vs_lpd,
            "note": _relation_note(
                user_lp, lpd_val, lp_vs_lpd, context="path", a_num=user_lp_num, b_num=lpd
            ),
        },
        "user_birthday_vs_calendar_day": {
            "user": user_bday,
            "day": dom_val,
            "day_of_month": dom_val,
            "relation": bday_vs_calendar,
            "note": _relation_note(user_bday, dom_val, bday_vs_calendar, context="imprint"),
        },
        "personal_day_vs_calendar_day": {
            "user": pd_val,
            "day": cd_val,
            "relation": personal_vs_calendar,
            "note": _relation_note(pd_val, cd_val, personal_vs_calendar, context="path", b_num=cd),
        },
    }
    insight = build_daily_numerology_insight(
        user_lp=user_lp,
        user_bday=user_bday,
        personal_day=pd_val,
        compat=compat,
        month_skew=month_skew,
    )
    lp_disp = py["life_path"].get("display", str(user_lp))
    lpd_disp = lpd.get("display", str(lpd_val))
    gate_relation = compat["user_life_path_vs_life_path_day"]["relation"]
    gate_line = build_numerology_gate_line(
        lp_disp,
        lpd_disp,
        gate_relation,
        life_path_day_is_master=bool(lpd.get("is_master")),
    )

    score, tier, hint = _score_from_relations(
        [day_field_rel, lp_vs_calendar, lp_vs_lpd, bday_vs_calendar],
        clashes=[],
    )

    cd["display"] = numerology_display(cd)
    lpd["display"] = numerology_display(lpd)
    dom["display"] = numerology_display(dom)
    pd["display"] = numerology_display(pd)

    return {
        "calendar_day": dom,
        "calendar_gate": cd,
        "day_of_month": dom,
        "life_path_display": lp_disp,
        "life_path_day": lpd,
        "personal_day": pd,
        "user_life_path": user_lp,
        "user_birthday_number": user_bday,
        "compat": compat,
        "month_skew": month_skew,
        "insight": insight,
        "gate_relation": gate_relation,
        "gate_line": gate_line,
        "favorability_score": score,
        "favorability_tier": tier,
        "favorability_hint": hint,
    }


def build_ally_enemy_lived_context(final_gate: int) -> str:
    """Life Path baseline vs Universal Day overlay — sealed numerology framing."""
    friends = PATH_FRIEND_NUMBERS.get(final_gate, [])
    enemies = PATH_ENEMY_NUMBERS.get(final_gate, [])
    friend_line = ", ".join(str(n) for n in friends) or "—"
    enemy_line = ", ".join(str(n) for n in enemies) or "—"
    return (
        f"Your Life Path {final_gate} is the constant baseline — long-term purpose and growth lessons. "
        f"Harmonious gates ({friend_line}) compound it when they appear in Universal Day or Personal Day overlays. "
        f"Challenging gates ({enemy_line}) signal tension: partners stall closure, crowds misread your pace, "
        f"or power shows up without spine. "
        f"Read each day by how the Universal Day fluctuates against your Life Path, "
        f"then let your birth-day number and Personal Day fine-tune timing before you imprint energy."
    )