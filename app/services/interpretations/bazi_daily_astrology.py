"""BaZi daily astrology layer — element-first, Wuxing cycles, conversational insight."""

from __future__ import annotations

from typing import Any, Literal

from app.overlay.clashes import branch_harmony
from app.services.interpretations.bazi_five_elements import (
    build_bazi_framework,
    compare_framing,
    cycle_name,
)
from app.services.interpretations.bazi_hidden_stems import count_weighted_element_balance, pillar_hidden_display
from app.services.interpretations.bazi_interpretation_lens import (
    build_bazi_interpretation_lens,
    distill_daily_bazi_advice,
)
from app.services.imprint_labels import branch_animal, stem_english

ElementRelation = Literal[
    "same", "generates", "generated_by", "controls", "controlled_by", "neutral"
]
EffectiveTone = Literal[
    "supportive", "neutral", "strained", "clash_muted", "clash_bruised", "clash_mixed", "clash_harsh"
]

ELEMENT_GENERATES: dict[str, str] = {
    "Wood": "Fire",
    "Fire": "Earth",
    "Earth": "Metal",
    "Metal": "Water",
    "Water": "Wood",
}

ELEMENT_CONTROLS: dict[str, str] = {
    "Wood": "Earth",
    "Earth": "Water",
    "Water": "Fire",
    "Fire": "Metal",
    "Metal": "Wood",
}

GENERATIVE_IMAGE: dict[tuple[str, str], str] = {
    ("Wood", "Fire"): "wood feeds the flame",
    ("Fire", "Earth"): "fire ash enriches soil",
    ("Earth", "Metal"): "earth yields ore",
    ("Metal", "Water"): "metal gathers condensation",
    ("Water", "Wood"): "water nourishes growth",
}

CONTROLLING_IMAGE: dict[tuple[str, str], str] = {
    ("Wood", "Earth"): "roots work the soil",
    ("Earth", "Water"): "earth dams the flood",
    ("Water", "Fire"): "water puts out fire",
    ("Fire", "Metal"): "fire melts metal",
    ("Metal", "Wood"): "metal cuts wood",
}

TONE_WEIGHT: dict[EffectiveTone, float] = {
    "supportive": 0.06,
    "neutral": 0.0,
    "strained": -0.08,
    "clash_muted": -0.04,
    "clash_bruised": -0.1,
    "clash_mixed": -0.12,
    "clash_harsh": -0.22,
}

TONE_SCORE: dict[EffectiveTone, float] = {
    "supportive": 0.82,
    "neutral": 0.55,
    "strained": 0.42,
    "clash_muted": 0.48,
    "clash_bruised": 0.35,
    "clash_mixed": 0.30,
    "clash_harsh": 0.18,
}


def element_relation(natal_el: str, sky_el: str) -> ElementRelation:
    if not natal_el or not sky_el:
        return "neutral"
    if natal_el == sky_el:
        return "same"
    if ELEMENT_GENERATES.get(natal_el) == sky_el:
        return "generates"
    if ELEMENT_GENERATES.get(sky_el) == natal_el:
        return "generated_by"
    if ELEMENT_CONTROLS.get(natal_el) == sky_el:
        return "controls"
    if ELEMENT_CONTROLS.get(sky_el) == natal_el:
        return "controlled_by"
    return "neutral"


def _wuxing_frame(natal_el: str, sky_el: str, el_rel: ElementRelation) -> dict[str, str]:
    """Loose strength/weakness framing from generative or controlling cycle."""
    if el_rel == "same":
        return {
            "cycle": "resonance",
            "flow": f"{natal_el} meets the same {sky_el} note",
            "strength": "less translation — what you are and what the sky asks line up",
            "weakness": "echo chamber — blind spots repeat unless you invite contrast",
        }
    if el_rel == "generates":
        img = GENERATIVE_IMAGE.get((natal_el, sky_el), "productive flow")
        return {
            "cycle": "generative",
            "flow": f"your {natal_el} feeds today's {sky_el} — {img}",
            "strength": "momentum and generosity land; you are the fuel in the room",
            "weakness": "over-giving or burnout if you do not refill after you feed the day",
        }
    if el_rel == "generated_by":
        img = GENERATIVE_IMAGE.get((sky_el, natal_el), "productive flow")
        return {
            "cycle": "generative",
            "flow": f"today's {sky_el} feeds your {natal_el} — {img}",
            "strength": "tailwind arrives; receive support before you push alone",
            "weakness": "passivity — waiting for the sky to do work you still owe",
        }
    if el_rel == "controls":
        img = CONTROLLING_IMAGE.get((natal_el, sky_el), "balancing restraint")
        return {
            "cycle": "controlling",
            "flow": f"your {natal_el} steadies today's {sky_el} — {img}",
            "strength": "structure and discipline hold; you set an honest pace",
            "weakness": "over-control — steamrolling nuance when soft touch would win",
        }
    if el_rel == "controlled_by":
        img = CONTROLLING_IMAGE.get((sky_el, natal_el), "balancing restraint")
        return {
            "cycle": "controlling",
            "flow": f"today's {sky_el} tempers your {natal_el} — {img}",
            "strength": "excess gets checked; cooperation restores balance",
            "weakness": "friction and ego drain if you fight the regulation instead of using it",
        }
    return {
        "cycle": "neutral",
        "flow": f"{natal_el} and {sky_el} sit outside the main cycles today",
        "strength": "ordinary footing — neither fed nor fought",
        "weakness": "no elemental tailwind; you supply the spark yourself",
    }


def _pillar_label(pillar: dict[str, str]) -> str:
    el = pillar.get("stem_element") or ""
    animal = branch_animal(pillar.get("branch", ""))
    return f"{el} {animal}".strip()


def _compare_pillar(
    natal: dict[str, str],
    sky: dict[str, str],
    *,
    level: str,
) -> dict[str, Any]:
    natal_el = natal.get("stem_element", "")
    sky_el = sky.get("stem_element", "")
    el_rel = element_relation(natal_el, sky_el)
    branch_rel = branch_harmony(natal.get("branch", ""), sky.get("branch", ""))
    tone, glitch = _effective_tone(el_rel, branch_rel)
    wuxing = _wuxing_frame(natal_el, sky_el, el_rel)

    return {
        "level": level,
        "natal_label": _pillar_label(natal),
        "sky_label": _pillar_label(sky),
        "natal_gan_zhi": natal.get("gan_zhi", ""),
        "sky_gan_zhi": sky.get("gan_zhi", ""),
        "natal_element": natal_el,
        "sky_element": sky_el,
        "natal_animal": branch_animal(natal.get("branch", "")),
        "sky_animal": branch_animal(sky.get("branch", "")),
        "element_relation": el_rel,
        "branch_relation": branch_rel,
        "effective_tone": tone,
        "element_glitch": glitch,
        "element_first": el_rel == "same" and branch_rel == "chong_冲",
        "wuxing": wuxing,
    }


def _effective_tone(
    el_rel: ElementRelation,
    branch_rel: str | None,
) -> tuple[EffectiveTone, str | None]:
    if branch_rel == "chong_冲":
        if el_rel == "same":
            return (
                "clash_muted",
                "Enemy sign, same element — the animal shouts, the stem holds.",
            )
        if el_rel == "controls":
            return (
                "clash_bruised",
                "Sign clash, but your element leads — friction without a full break.",
            )
        if el_rel == "controlled_by":
            return (
                "clash_harsh",
                "Enemy sign plus a stronger sky element — tighten timing and ego.",
            )
        if el_rel in ("generates", "generated_by"):
            return (
                "clash_mixed",
                "Sign opposes while elements trade — conflict possible, cleaner exit likely.",
            )
        return ("clash_harsh", "Branch clash with no elemental cover.")

    if el_rel == "same":
        return ("supportive", None)
    if el_rel in ("generates", "generated_by"):
        return ("supportive", None)
    if branch_rel in ("san_he_三合", "liu_he_六合"):
        return ("supportive", None)
    if el_rel == "controls":
        return ("neutral", None)
    if el_rel == "controlled_by":
        return ("strained", None)
    return ("neutral", None)


def _branch_clause(cmp: dict[str, Any]) -> str:
    rel = cmp.get("branch_relation")
    if cmp.get("element_first"):
        return (
            f"The {cmp['sky_animal']} sign clashes your pillar on paper, "
            f"but shared {cmp['natal_element']} means most people feel the hit — you may not."
        )
    if rel == "chong_冲":
        return (
            f"The {cmp['sky_animal']} sign opposes yours — read the animal second, "
            f"after you measure {cmp['natal_element']} against {cmp['sky_element']}."
        )
    if rel in ("san_he_三合", "liu_he_六合"):
        return f"The animals harmonize underneath — that softens the day even when elements tug."
    return ""


def _cap_flow(flow: str) -> str:
    return flow[0].upper() + flow[1:] if flow else flow


def _action_for_compare(cmp: dict[str, Any]) -> str | None:
    level = cmp["level"]
    tone = cmp["effective_tone"]
    sky = cmp["sky_label"]
    natal_el = cmp["natal_element"]
    w = cmp["wuxing"]
    flow = _cap_flow(w["flow"])

    if level == "day_vs_sky_day":
        if tone == "clash_muted":
            return f"Treat {sky} as background noise — same {natal_el} holds; do the task, skip the duel."
        if tone == "clash_bruised":
            return f"{flow}; finish one hard item, walk away from the argument."
        if tone == "clash_harsh":
            return f"Sky presses your {natal_el} — batch admin early, no fresh fights after noon."
        if tone == "supportive" and w["cycle"] == "generative":
            return f"{flow}; ship one visible piece while the lane stays open."
        if tone == "strained":
            return f"Let the sky regulate you today — narrow scope, keep receipts, no heroics."
        if w["cycle"] == "controlling":
            return f"{flow}; lead with structure, not speed."
        return f"Ordinary {natal_el} pacing — one deliberate block, then stop."

    if level == "day_vs_sky_year":
        if tone in ("clash_muted", "clash_bruised"):
            return f"Year climate {sky} rattles the sign, not your {natal_el} stem — long view stays steadier than the headline."
        if tone == "clash_harsh":
            return f"Year {sky} outweighs your day element — secure what is moving, defer new bets."
        if w["cycle"] == "generative":
            return f"Year {sky} feeds your {natal_el} day over time — align one quarterly move with today's push."
        return f"Year {sky} sets the season; match pace to the climate, not today's mood."

    if level == "day_vs_sky_month":
        if tone in ("clash_muted", "supportive"):
            return f"Month tone {sky} colors the week — pick one priority inside that weather."
        if tone in ("clash_harsh", "strained"):
            return f"Month strains {natal_el} — trim the calendar to what must move."
        return None

    if level == "year_vs_sky_year":
        if tone == "clash_muted":
            return f"Public year {sky} clashes your birth animal but shares element — noise outside, root stable inside."
        if w["cycle"] == "generative":
            return f"Birth {cmp['natal_label']} and sky year {sky} trade support — environment can amplify your root."
        if tone == "clash_harsh":
            return f"Sky year {sky} presses birth {cmp['natal_label']} — guard reputation, skip impulsive rebrands."
        return None

    return None


def _daily_primary_advice(day_day: dict[str, Any], day_year: dict[str, Any]) -> str:
    """One sentence: your chart vs today's sky — conclusion only."""
    tone = day_day["effective_tone"]
    cycle = day_day["wuxing"]["cycle"]
    sky_animal = day_day["sky_animal"]

    if day_day.get("element_first"):
        return (
            "Today's sign opposes yours, but your element holds steady — "
            "do the work in front of you and ignore the noise."
        )
    if tone == "clash_muted":
        return (
            "The zodiac signs clash today, yet your element stays aligned — "
            "stay on task and do not take the bait."
        )
    if tone == "clash_harsh":
        return (
            "Today's sky weighs on your chart — handle essentials early, "
            "trim your calendar, and defer new fights."
        )
    if tone == "clash_mixed":
        return (
            f"Signs pull against each other while elements trade — "
            f"measure your pace before answering the {sky_animal} energy."
        )
    if tone == "strained":
        return (
            "Today's element checks yours — narrow scope, keep receipts, "
            "and cooperate instead of forcing outcomes."
        )
    if tone == "supportive" and cycle == "generative":
        return (
            "Today's sky feeds your nature — move one important thing forward "
            "while the window stays open."
        )
    if tone == "supportive":
        return "Today's sky backs your chart — act on what matters while conditions are favorable."
    if cycle == "controlling":
        return "Today asks for structure over speed — set the pace and hold the line."
    if day_year["effective_tone"] in ("clash_harsh", "strained"):
        return "The wider year climate presses today — secure what is moving and skip risky bets."
    return "Lead with your core element today, not the animal headline — one deliberate block, then stop."


def _daily_insight(
    day_day: dict[str, Any],
    day_year: dict[str, Any],
    *,
    interpretation_lens: dict[str, Any] | None = None,
) -> str:
    """Daily card: one or two plain-English advice sentences. No method, no symbols."""
    primary = _daily_primary_advice(day_day, day_year)
    if not interpretation_lens:
        return primary
    return distill_daily_bazi_advice(interpretation_lens, primary_sky_advice=primary)


def _headline(day_day: dict[str, Any]) -> str:
    w = day_day["wuxing"]
    if day_day.get("element_first"):
        return (
            f"Same {day_day['natal_element']} under a clashing sign — "
            f"the animal shouts, your stem holds."
        )
    if day_day["effective_tone"] == "supportive":
        return f"{w['flow'].capitalize()} — act while the window is honest."
    if day_day["effective_tone"] in ("clash_harsh", "clash_mixed"):
        return f"Measure {day_day['natal_element']} before you answer the {day_day['sky_animal']}."
    if day_day["effective_tone"] == "strained":
        return f"Today’s {day_day['sky_element']} regulates your {day_day['natal_element']} — cooperate, don’t wrestle."
    return f"Lead with {day_day['natal_element']}, not the animal."


ELEMENT_ORDER = ("Wood", "Fire", "Earth", "Metal", "Water")

SKY_FRICTION_TIER_META: dict[str, dict[str, str]] = {
    "very-good": {
        "signal": "Clear lane",
        "weather": "Clear skies",
        "weather_class": "clear",
        "advice": "Sky feeds your {dm} — stack one visible finish, then stop.",
    },
    "good": {
        "signal": "Tailwind",
        "weather": "Fair weather",
        "weather_class": "fair",
        "advice": "Elements align enough — lead with {dominant}, move one priority, don't scatter.",
    },
    "neutral": {
        "signal": "Steady air",
        "weather": "Mixed sky",
        "weather_class": "overcast",
        "advice": "Elements are mixed — work your {dominant}, ignore the sky headline.",
    },
    "bad": {
        "signal": "Rough terrain",
        "weather": "Heavy drag",
        "weather_class": "rain",
        "advice": "Sky outruns your chart — cut the calendar, no signatures, no forced merges.",
    },
    "terrible": {
        "signal": "Hold still",
        "weather": "Storm front",
        "weather_class": "storm",
        "advice": "Sky fights your seal — stay out of fights, batch essentials only, stop by noon.",
    },
}


def _element_percentages(counts: dict[str, float]) -> dict[str, int]:
    total = sum(counts.get(el, 0.0) for el in ELEMENT_ORDER)
    if total <= 0:
        return {el: 0 for el in ELEMENT_ORDER}
    raw = {el: int(round((counts.get(el, 0.0) / total) * 100)) for el in ELEMENT_ORDER}
    drift = 100 - sum(raw.values())
    if drift and raw:
        top = max(ELEMENT_ORDER, key=lambda e: raw[e])
        raw[top] = max(0, raw[top] + drift)
    return raw


def _dominant_element(pct: dict[str, int]) -> str:
    best = max(ELEMENT_ORDER, key=lambda e: pct.get(e, 0))
    return best if pct.get(best, 0) > 0 else "Earth"


def _format_element_line(pct: dict[str, int]) -> str:
    parts = [f"{el} {pct[el]}%" for el in ELEMENT_ORDER if pct.get(el, 0) > 0]
    return " · ".join(parts) if parts else "—"


def _tier_from_score(score: float) -> str:
    if score >= 0.78:
        return "very-good"
    if score >= 0.62:
        return "good"
    if score >= 0.45:
        return "neutral"
    if score >= 0.28:
        return "bad"
    return "terrible"


def build_sky_element_friction(
    natal_pillars: dict[str, dict[str, str]],
    sky_pillars: dict[str, dict[str, str]],
    astrology_layer: dict[str, Any],
    *,
    imprint: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """User seal vs universal sky — element % lines and one brief actionable warning."""
    pillars = imprint["bazi"]["pillars"] if imprint else natal_pillars
    natal_counts = count_weighted_element_balance(
        {k: pillars[k] for k in ("year", "month", "day", "hour") if k in pillars}
    )
    sky_counts = count_weighted_element_balance(
        {k: sky_pillars[k] for k in ("year", "month", "day") if k in sky_pillars}
    )
    natal_pct = _element_percentages(natal_counts)
    sky_pct = _element_percentages(sky_counts)

    score = bazi_favorability_score(astrology_layer)
    tier = _tier_from_score(score)
    if astrology_layer.get("severe_clash") and tier in ("good", "neutral", "very-good"):
        tier = "bad"
        score = min(score, 0.35)

    day_cmp = (astrology_layer.get("compares") or {}).get("day_vs_sky_day") or {}
    dm = day_cmp.get("natal_element") or astrology_layer.get("primary_element") or _dominant_element(natal_pct)
    dominant = _dominant_element(natal_pct)
    meta = SKY_FRICTION_TIER_META[tier]
    advice = meta["advice"].format(dm=dm, dominant=dominant)

    friction_pct = max(5, min(98, round((1.0 - score) * 100)))

    return {
        "natal_elements": natal_pct,
        "sky_elements": sky_pct,
        "natal_line": _format_element_line(natal_pct),
        "sky_line": _format_element_line(sky_pct),
        "tier": tier,
        "score": score,
        "friction_pct": friction_pct,
        "signal": meta["signal"],
        "weather": meta["weather"],
        "weather_class": meta["weather_class"],
        "advice": advice,
        "day_master_element": dm,
        "has_clash": bool(astrology_layer.get("severe_clash")),
    }


def bazi_favorability_score(astrology_layer: dict[str, Any]) -> float:
    """Map day/year compare tones to a 0–1 favorability anchor for slider blend."""
    compares = astrology_layer.get("compares") or {}
    day_cmp = compares.get("day_vs_sky_day") or {}
    year_cmp = compares.get("day_vs_sky_year") or {}
    birth_year_cmp = compares.get("year_vs_sky_year") or {}

    score = (
        TONE_SCORE.get(day_cmp.get("effective_tone", "neutral"), 0.55) * 0.55
        + TONE_SCORE.get(year_cmp.get("effective_tone", "neutral"), 0.55) * 0.30
        + TONE_SCORE.get(birth_year_cmp.get("effective_tone", "neutral"), 0.55) * 0.15
    )
    if astrology_layer.get("severe_clash"):
        score = min(score, 0.32)
    if astrology_layer.get("element_glitch_active"):
        score = min(0.72, score + 0.06)
    return max(0.08, min(0.95, round(score, 3)))


def build_bazi_daily_framing(astrology_layer: dict[str, Any]) -> dict[str, list[str]]:
    """Promote/avoid from BaZi tone, wuxing, and action steps — no pillar symbols."""
    promote: list[str] = []
    avoid: list[str] = []
    compares = astrology_layer.get("compares") or {}
    day_day = compares.get("day_vs_sky_day") or {}
    tone = day_day.get("effective_tone", "neutral")
    wuxing = day_day.get("wuxing") or {}

    for action in (astrology_layer.get("actions") or [])[:2]:
        if action and action not in promote:
            promote.append(action)

    strength = wuxing.get("strength", "")
    if tone == "supportive" and strength and strength not in promote:
        promote.append(strength)

    weakness = wuxing.get("weakness", "")
    if weakness and weakness not in avoid:
        avoid.append(weakness)

    if tone in ("clash_harsh", "clash_mixed", "clash_bruised"):
        avoid.append("Trim the calendar and defer fresh fights — the sky presses your chart today.")
    elif tone == "strained":
        avoid.append("No heroics — narrow scope, keep receipts, and cooperate instead of forcing outcomes.")

    if astrology_layer.get("severe_clash"):
        avoid.append("Branch clash is live — batch essentials early and skip risky bets after noon.")

    if not promote and tone in ("neutral", "clash_muted"):
        promote.append("One deliberate block on your core element, then stop — ordinary pacing still counts.")

    return {"promote": promote[:2], "avoid": avoid[:2]}


def build_bazi_astrology_layer(
    natal_pillars: dict[str, dict[str, str]],
    sky_pillars: dict[str, dict[str, str]],
    *,
    imprint: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare natal year/day pillars to universal sky year/month/day."""
    natal_year = natal_pillars["year"]
    natal_day = natal_pillars["day"]
    framework = build_bazi_framework(imprint) if imprint else {}
    day_master = framework.get("day_master_element") or natal_day.get("stem_element", "")

    day_vs_year = _compare_pillar(natal_day, sky_pillars["year"], level="day_vs_sky_year")
    day_vs_month = _compare_pillar(natal_day, sky_pillars["month"], level="day_vs_sky_month")
    day_vs_day = _compare_pillar(natal_day, sky_pillars["day"], level="day_vs_sky_day")
    year_vs_year = _compare_pillar(natal_year, sky_pillars["year"], level="year_vs_sky_year")

    compares = {
        "day_vs_sky_year": day_vs_year,
        "day_vs_sky_month": day_vs_month,
        "day_vs_sky_day": day_vs_day,
        "year_vs_sky_year": year_vs_year,
    }

    actions: list[str] = []
    for key in ("day_vs_sky_day", "day_vs_sky_year", "day_vs_sky_month", "year_vs_sky_year"):
        step = _action_for_compare(compares[key])
        if step and step not in actions:
            actions.append(step)
        if len(actions) >= 2:
            break

    modifier = (
        TONE_WEIGHT[day_vs_day["effective_tone"]] * 0.5
        + TONE_WEIGHT[day_vs_year["effective_tone"]] * 0.3
        + TONE_WEIGHT[year_vs_year["effective_tone"]] * 0.2
    )
    element_glitch_active = any(c.get("element_first") for c in compares.values())
    severe_clash = day_vs_day["branch_relation"] == "chong_冲" and not element_glitch_active

    natal_year_branch = branch_animal(natal_year.get("branch", ""))
    natal_day_branch = branch_animal(natal_day.get("branch", ""))
    natal_year_hidden = pillar_hidden_display(
        {**natal_year, "branch_en": natal_year_branch}
    )
    natal_day_hidden = pillar_hidden_display(
        {**natal_day, "branch_en": natal_day_branch}
    )

    def _natal_pillar_display(pillar: dict[str, str], branch_en: str, hidden: dict[str, Any]) -> dict[str, Any]:
        return {
            "label": _pillar_label(pillar),
            "display_line": hidden.get("display_line") or _pillar_label(pillar),
            "branch_hidden_label": hidden.get("branch_hidden_label", ""),
            "synergy_note": hidden.get("synergy_note", ""),
            "gan_zhi": pillar.get("gan_zhi", ""),
            "stem_en": stem_english(pillar.get("stem", "")),
            "stem_element": pillar.get("stem_element", ""),
            "branch_en": branch_en,
            "hidden_stem": hidden["hidden_stem"],
            "hidden_stem_en": hidden["hidden_stem_en"],
            "hidden_stem_element": hidden["hidden_stem_element"],
            "hidden_role_label": hidden.get("hidden_role_label", ""),
        }

    natal_display = {
        "year": _natal_pillar_display(natal_year, natal_year_branch, natal_year_hidden),
        "day": _natal_pillar_display(natal_day, natal_day_branch, natal_day_hidden),
    }

    sky_display = {
        level: {
            "label": _pillar_label(sky_pillars[level]),
            "gan_zhi": sky_pillars[level].get("gan_zhi", ""),
            "stem_element": sky_pillars[level].get("stem_element", ""),
            "branch_en": branch_animal(sky_pillars[level].get("branch", "")),
        }
        for level in ("year", "month", "day")
    }

    interpretation_lens = build_bazi_interpretation_lens(
        natal_pillars,
        imprint=imprint,
        sky_pillars=sky_pillars,
        compares={
            "day_vs_sky_day": day_vs_day,
            "day_vs_sky_year": day_vs_year,
            "day_vs_sky_month": day_vs_month,
            "year_vs_sky_year": year_vs_year,
        },
    )
    if framework is not None:
        framework = {**framework, "interpretation_lens": interpretation_lens}

    insight = _daily_insight(
        day_vs_day,
        day_vs_year,
        interpretation_lens=interpretation_lens,
    )

    return {
        "rule": "bazi_day_master_center; wuxing_sheng_ke; element_over_animal; numerology_supersedes",
        "framework": framework,
        "interpretation_lens": interpretation_lens,
        "wuxing": framework.get("cycles")
        or {
            "generative": "Wood → Fire → Earth → Metal → Water → Wood",
            "controlling": "Wood → Earth → Water → Fire → Metal → Wood",
        },
        "natal": natal_display,
        "sky": sky_display,
        "compares": compares,
        "headline": _headline(day_vs_day),
        "insight": insight,
        "actions": actions,
        "element_glitch_active": element_glitch_active,
        "severe_clash": severe_clash,
        "favorability_modifier": round(modifier, 3),
        "primary_element": natal_day.get("stem_element", ""),
        "luck_pillar": (interpretation_lens or {}).get("luck_pillar")
        or ((imprint or {}).get("bazi", {}).get("luck") or {}).get("interpretation"),
    }