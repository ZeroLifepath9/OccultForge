"""Luck Pillar (大运) interpretation — current decade only for advice."""

from __future__ import annotations

from datetime import date
from typing import Any

from app.overlay.clashes import branch_clashes, branch_harmony
from app.services.interpretations.bazi_hidden_stems import (
    ELEMENT_CONTROLS,
    ELEMENT_GENERATES,
    TEN_GOD_PLAIN,
    pillar_hidden_display,
    ten_god_role,
)
from app.services.imprint_labels import branch_animal, stem_english

TEN_GOD_THEME: dict[str, str] = {
    "resource": "support and learning",
    "companion": "peers and collaboration",
    "output": "expression and creative output",
    "wealth": "resources and material gain",
    "officer": "discipline and authority",
}

TEN_GOD_TEASER: dict[str, str] = {
    "resource": "Resource decade — growth and backing ahead",
    "companion": "Companion decade — peers and shared momentum ahead",
    "output": "Output decade — expression and projects ahead",
    "wealth": "Wealth decade — income and resources ahead",
    "officer": "Officer decade — structure and demand ahead",
}


def _element_relation(dm_el: str, other_el: str) -> str:
    if not dm_el or not other_el:
        return "neutral"
    if dm_el == other_el:
        return "same"
    if ELEMENT_GENERATES.get(other_el) == dm_el:
        return "resource"
    if ELEMENT_GENERATES.get(dm_el) == other_el:
        return "output"
    if ELEMENT_CONTROLS.get(other_el) == dm_el:
        return "officer"
    if ELEMENT_CONTROLS.get(dm_el) == other_el:
        return "wealth"
    return "neutral"


def _luck_pillar_card(pillar: dict[str, Any]) -> dict[str, Any]:
    animal = pillar.get("branch_en") or branch_animal(pillar.get("branch", ""))
    display = pillar_hidden_display({**pillar, "branch_en": animal})
    return {
        "identity": display["label"] or _identity_from_pillar(pillar),
        "display_line": display.get("display_line", ""),
        "gan_zhi": pillar.get("gan_zhi", ""),
        "stem_element": pillar.get("stem_element", ""),
        "branch_en": animal,
        "hidden_stem_element": display.get("hidden_stem_element", ""),
        "start_year": pillar.get("start_year"),
        "end_year": pillar.get("end_year"),
        "years_into_decade": pillar.get("years_into_decade"),
        "years_remaining": pillar.get("years_remaining"),
        "phase": pillar.get("phase", ""),
        "phase_label": pillar.get("phase_label", ""),
        "is_minor_period": pillar.get("is_minor_period", False),
    }


def _identity_from_pillar(pillar: dict[str, Any]) -> str:
    el = pillar.get("stem_element", "")
    animal = pillar.get("branch_en") or branch_animal(pillar.get("branch", ""))
    return f"{el} {animal}".strip() if el else animal


def _natal_branch_notes(
    luck_pillar: dict[str, Any],
    natal_pillars: dict[str, Any],
) -> tuple[list[str], list[str]]:
    branch = luck_pillar.get("branch", "")
    if not branch:
        return [], []
    with_you: list[str] = []
    against: list[str] = []
    for name, natal in natal_pillars.items():
        if not isinstance(natal, dict):
            continue
        nb = natal.get("branch", "")
        if not nb:
            continue
        harmony = branch_harmony(branch, nb)
        if harmony == "liu_he_六合":
            with_you.append(f"Luck branch harmonizes with natal {name} pillar ({natal.get('gan_zhi', '')})")
        elif harmony == "san_he_三合":
            with_you.append(f"Luck branch combines with natal {name} branch — amplified element frame")
        elif branch_clashes(branch, nb):
            against.append(
                f"Luck branch clashes natal {name} pillar ({natal.get('gan_zhi', '')}) — "
                f"shifts and friction in {name} themes"
            )
    return with_you, against


def build_luck_pillar_lens(
    imprint: dict[str, Any],
    *,
    reference: date | None = None,
) -> dict[str, Any]:
    """Interpret current luck decade relative to natal chart."""
    from app.calculators.bazi_luck import refresh_luck_bundle

    ref = reference or date.today()
    bazi = imprint.get("bazi") or {}
    pillars = bazi.get("pillars") or {}
    dm_el = (bazi.get("day_master") or {}).get("element", "")
    dm_stem = (pillars.get("day") or {}).get("stem", "")
    luck = refresh_luck_bundle(imprint, reference=ref)
    current_raw = luck.get("current")
    if not current_raw or current_raw.get("is_minor_period") or not current_raw.get("gan_zhi"):
        from app.services.imprint_labels import build_display_bundle
        from app.services.interpretations.matrix_decoder_voice import build_luck_pillar_matrix

        minor_matrix = build_luck_pillar_matrix({}, build_display_bundle(imprint), imprint)
        return {
            "current": None,
            "framework_insight": minor_matrix,
            "matrix_insight": minor_matrix,
            "alignment_with_natal": {"expands": [], "tensions": [], "summary": ""},
            "future_preview": luck.get("future_preview") or [],
            "access": luck.get("access") or {"current": "full", "future": "preview"},
        }

    card = _luck_pillar_card(current_raw)
    stem_el = current_raw.get("stem_element", "")
    branch_el = current_raw.get("branch_element", "")
    hidden_el = card.get("hidden_stem_element", "")
    stem_tg = ten_god_role(dm_el, stem_el)
    branch_tg = ten_god_role(dm_el, branch_el)
    hidden_tg = ten_god_role(dm_el, hidden_el) if hidden_el else ""
    stem_rel = _element_relation(dm_el, stem_el)
    branch_rel = _element_relation(dm_el, branch_el)

    working_with: list[str] = []
    working_against: list[str] = []

    if stem_rel in ("resource", "same"):
        working_with.append(
            f"Luck stem {stem_el} ({TEN_GOD_THEME.get(stem_tg, stem_tg)}) supports your {dm_el} Day Master"
        )
    elif stem_rel in ("officer", "wealth") and stem_tg == "officer":
        working_against.append(
            f"Luck stem {stem_el} presses your {dm_el} Day Master — discipline and demand dominate the decade surface"
        )
    elif stem_rel == "output":
        working_with.append(
            f"Luck stem {stem_el} draws expression from your {dm_el} Day Master — projects and visibility"
        )

    if branch_rel == "resource":
        working_with.append(f"Luck branch environment feeds {dm_el} from beneath")
    elif branch_rel == "officer":
        working_against.append(f"Luck branch undertow checks {dm_el} — internal regulation and constraint")
    elif branch_rel == "output":
        working_with.append(f"Luck branch carries output energy — inner craft wants an outlet")

    natal_with, natal_against = _natal_branch_notes(current_raw, pillars)
    working_with.extend(natal_with)
    working_against.extend(natal_against)

    phase = card.get("phase_label", "")
    stem_theme = TEN_GOD_THEME.get(stem_tg, stem_tg or "neutral cycle")
    branch_theme = TEN_GOD_THEME.get(branch_tg, branch_tg or "environmental undertow")

    if card.get("phase") == "stem_half":
        phase_advice = f"External stem energy leads — {stem_theme} shows in career moves and visible events."
    else:
        phase_advice = f"Branch foundation leads — {branch_theme} stabilizes or shifts what the decade built outward."

    citation_parts = [phase_advice]
    if working_with:
        citation_parts.append(working_with[0].lower())
    elif working_against:
        citation_parts.append(working_against[0].lower())
    advice_citation = (
        "Your current luck pillar suggests "
        + "; ".join(citation_parts[:2])
        + "."
    )

    transition_note = ""
    if (card.get("years_remaining") or 99) <= 2:
        transition_note = (
            " You are within a luck-pillar transition window (交运) — expect volatility as the old decade "
            "hands off to the next; plan structure, not impulsive rebrands."
        )

    framework_insight = (
        f"Luck Pillars (大运) are ten-year chapters that overlay your natal Four Pillars. "
        f"You are in {card['identity']} ({card['gan_zhi']}) from {card.get('start_year')} to {card.get('end_year')} "
        f"— year {card.get('years_into_decade')} of this decade. "
        f"The heavenly stem ({stem_el}, {stem_english(current_raw.get('stem', ''))}) shapes outward events; "
        f"the branch ({card.get('branch_en')}, hidden {hidden_el or '—'}) holds environment and latent support. "
        f"Relative to your {dm_el} Day Master ({stem_english(dm_stem)}), this decade runs as "
        f"stem {TEN_GOD_PLAIN.get(stem_tg, stem_tg)} and branch {TEN_GOD_PLAIN.get(branch_tg, branch_tg)}. "
        f"{phase_label_detail(card)}"
        f"{transition_note}"
    )

    expands, tensions, summary = _alignment_with_natal(imprint, card, stem_tg, hidden_tg)

    future = []
    for fp in luck.get("future_preview") or []:
        p = next(
            (x for x in luck.get("pillars", []) if x.get("gan_zhi") == fp.get("gan_zhi")),
            {},
        )
        stem = p.get("stem_element", "")
        tg = ten_god_role(dm_el, stem) if stem else ""
        future.append({**fp, "teaser": TEN_GOD_TEASER.get(tg, f"{fp.get('identity', '')} ahead")})

    from app.services.imprint_labels import build_display_bundle
    from app.services.interpretations.matrix_decoder_voice import (
        build_luck_pillar_matrix,
        current_sky_month_pillar,
    )

    facts = build_display_bundle(imprint)
    month_sky = current_sky_month_pillar(imprint, reference=ref)
    matrix_insight = build_luck_pillar_matrix(
        {
            "current": {
                **card,
                "stem_ten_god": stem_tg,
                "branch_ten_god": branch_tg,
                "hidden_ten_god": hidden_tg,
                "luck_stem_role": TEN_GOD_PLAIN.get(stem_tg, ""),
                "luck_branch_role": TEN_GOD_PLAIN.get(branch_tg, ""),
                "working_with_you": working_with,
                "working_against_you": working_against,
                "advice_citation": advice_citation,
            },
            "alignment_with_natal": {"expands": expands, "tensions": tensions, "summary": summary},
        },
        facts,
        imprint,
        month_sky=month_sky,
    )

    return {
        "current": {
            **card,
            "stem_ten_god": stem_tg,
            "branch_ten_god": branch_tg,
            "hidden_ten_god": hidden_tg,
            "luck_stem_role": TEN_GOD_PLAIN.get(stem_tg, ""),
            "luck_branch_role": TEN_GOD_PLAIN.get(branch_tg, ""),
            "working_with_you": working_with,
            "working_against_you": working_against,
            "advice_citation": advice_citation,
        },
        "framework_insight": matrix_insight,
        "matrix_insight": matrix_insight,
        "legacy_framework_insight": framework_insight,
        "alignment_with_natal": {
            "expands": expands,
            "tensions": tensions,
            "summary": summary,
        },
        "future_preview": future,
        "access": luck.get("access") or {"current": "full", "future": "preview"},
    }


def phase_label_detail(card: dict[str, Any]) -> str:
    if card.get("phase") == "stem_half":
        return "First half of the decade: stem dominates — act on visible openings while the branch matures beneath. "
    return "Second half of the decade: branch dominates — inner foundation and health of the chapter matter as much as headlines. "


def _alignment_with_natal(
    imprint: dict[str, Any],
    luck_card: dict[str, Any],
    stem_tg: str,
    hidden_tg: str,
) -> tuple[list[str], list[str], str]:
    bazi = imprint.get("bazi") or {}
    lens = bazi.get("interpretation_lens") or {}
    day_card = (lens.get("pillars") or {}).get("day") or {}
    year_card = (lens.get("pillars") or {}).get("year") or {}
    expands: list[str] = []
    tensions: list[str] = []

    day_hook = day_card.get("advice_hook", "")
    if day_hook and stem_tg == "officer" and day_card.get("ten_god_vs_dm") == "output":
        expands.append(
            "Officer luck decade presses outward while your day pillar carries inner Metal output — "
            "discipline refines what you publish."
        )
    elif day_hook and stem_tg == "output":
        expands.append(f"Luck decade output theme expands your day pillar pattern: {day_hook}")

    if year_card.get("advice_hook"):
        expands.append(
            f"Year pillar inheritance ({year_card.get('identity', '')}) sets the room; "
            f"luck decade {luck_card.get('identity', '')} is the ten-year weather inside it."
        )

    balance = lens.get("balance") or {}
    latent = balance.get("latent_insight", "")
    if latent and "inside" in latent.lower():
        expands.append(f"Weighted chart balance: {latent}")

    if tensions:
        summary = (
            f"Your current luck pillar suggests {luck_card.get('luck_stem_role', 'this cycle')} — "
            f"natal chart tensions: {'; '.join(tensions[:1])}."
        )
    elif expands:
        summary = (
            f"Your current luck pillar suggests {luck_card.get('luck_stem_role', 'this cycle')} — "
            f"natal chart expands this through: {expands[0]}"
        )
    else:
        summary = (
            f"Your current luck pillar suggests pacing with {luck_card.get('stem_element', '')} "
            f"stem energy while your {bazi.get('day_master', {}).get('element', '')} Day Master stays central."
        )

    return expands, tensions, summary


def interpret_luck_pillar_for_registry(
    pillars: dict[str, Any],
    day_master_el: str,
    *,
    imprint: dict[str, Any] | None = None,
) -> tuple[list[str], list[str]]:
    """Registry hook — current luck only."""
    if not imprint:
        return [], []
    luck_lens = build_luck_pillar_lens(imprint)
    current = luck_lens.get("current")
    if not current:
        return [], []
    interactions: list[str] = []
    directives: list[str] = []
    citation = current.get("advice_citation", "")
    if citation:
        directives.append(citation)
    align = luck_lens.get("alignment_with_natal") or {}
    summary = align.get("summary", "")
    if summary:
        interactions.append(summary)
    for line in align.get("expands") or []:
        interactions.append(line)
    return interactions, directives