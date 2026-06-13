"""Luck Pillars (大运) — gender-aware decade timeline from lunar_python."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from app.calculators.bazi import BRANCH_ANIMAL, _pillar

Gender = Literal["male", "female"]


def _yun_gender(gender: Gender) -> int:
    return 1 if gender == "male" else 0


def build_luck_timeline(ec: Any, *, gender: Gender = "male") -> dict[str, Any]:
    """Full luck pillar sequence with onset and decade metadata."""
    yun = ec.getYun(_yun_gender(gender))
    year_stem = ec.getYearGan()
    yang_stems = {"甲", "丙", "戊", "庚", "壬"}
    year_is_yang = year_stem in yang_stems
    if gender == "male":
        forward = year_is_yang
    else:
        forward = not year_is_yang

    pillars: list[dict[str, Any]] = []
    for i, dy in enumerate(yun.getDaYun()[:8]):
        gan_zhi = dy.getGanZhi() or ""
        stem, branch = "", ""
        if len(gan_zhi) >= 2:
            stem, branch = gan_zhi[0], gan_zhi[1]
            pillar = _pillar(stem, branch)
        else:
            pillar = {
                "stem": "",
                "branch": "",
                "gan_zhi": "",
                "stem_element": "",
                "branch_element": "",
            }
        pillars.append(
            {
                "index": i,
                **pillar,
                "branch_en": BRANCH_ANIMAL.get(branch, "") if branch else "",
                "start_age": dy.getStartAge(),
                "end_age": dy.getEndAge(),
                "start_year": dy.getStartYear(),
                "end_year": dy.getEndYear(),
                "is_minor_period": not gan_zhi,
            }
        )

    return {
        "onset": {
            "years": yun.getStartYear(),
            "months": yun.getStartMonth(),
            "days": yun.getStartDay(),
        },
        "sequence_direction": "forward" if forward else "reverse",
        "gender": gender,
        "pillars": pillars,
    }


def _age_on_date(birth_year: int, reference: date) -> int:
    return reference.year - birth_year


def resolve_luck_for_date(
    luck: dict[str, Any],
    birth_year: int,
    reference: date,
) -> dict[str, Any]:
    """Attach current decade + future preview for reference date."""
    ref_year = reference.year
    age = _age_on_date(birth_year, reference)
    pillars = luck.get("pillars") or []
    current: dict[str, Any] | None = None
    current_index = -1

    for i, p in enumerate(pillars):
        if p.get("start_year", 0) <= ref_year <= p.get("end_year", 0):
            current = dict(p)
            current_index = i
            break
        if p.get("start_age", 0) <= age <= p.get("end_age", 0):
            current = dict(p)
            current_index = i
            break

    if current:
        start_age = current.get("start_age", 1)
        years_into = max(0, age - start_age + 1)
        years_remaining = max(0, current.get("end_year", ref_year) - ref_year)
        current["years_into_decade"] = years_into
        current["years_remaining"] = years_remaining
        current["phase"] = "stem_half" if years_into <= 5 else "branch_half"
        current["phase_label"] = (
            "Stem half (external events)" if years_into <= 5 else "Branch half (internal foundation)"
        )

    future_preview: list[dict[str, Any]] = []
    for p in pillars:
        if p.get("is_minor_period") or not p.get("gan_zhi"):
            continue
        start_year = p.get("start_year", 0)
        if start_year > ref_year:
            future_preview.append(
                {
                    "gan_zhi": p.get("gan_zhi", ""),
                    "identity": _luck_identity(p),
                    "start_year": start_year,
                    "end_year": p.get("end_year"),
                    "start_age": p.get("start_age"),
                    "end_age": p.get("end_age"),
                    "years_until": start_year - ref_year,
                    "locked": True,
                }
            )

    return {
        **luck,
        "current": current,
        "current_index": current_index,
        "reference_date": reference.isoformat(),
        "future_preview": future_preview[:6],
        "access": {"current": "full", "future": "preview"},
    }


def _luck_identity(pillar: dict[str, Any]) -> str:
    el = pillar.get("stem_element", "")
    animal = pillar.get("branch_en") or BRANCH_ANIMAL.get(pillar.get("branch", ""), "")
    return f"{el} {animal}".strip() if el and animal else pillar.get("gan_zhi", "")


def refresh_luck_bundle(
    imprint: dict[str, Any],
    *,
    reference: date | None = None,
    gender: Gender | None = None,
) -> dict[str, Any]:
    """Rebuild luck timeline if missing; always refresh current for reference date."""
    from lunar_python import Solar

    bazi = imprint.get("bazi") or {}
    birth = imprint.get("birth") or {}
    ref = reference or date.today()
    gender_val: Gender = gender or birth.get("gender") or "male"  # type: ignore[assignment]

    luck = bazi.get("luck")
    if not luck or not luck.get("pillars"):
        dt = datetime.fromisoformat(birth["datetime_local"].replace("Z", ""))
        solar = Solar.fromYmdHms(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )
        ec = solar.getLunar().getEightChar()
        luck = build_luck_timeline(ec, gender=gender_val)

    birth_year = datetime.fromisoformat(birth["datetime_local"].replace("Z", "")).year
    resolved = resolve_luck_for_date(luck, birth_year, ref)
    resolved["gender"] = gender_val
    return resolved


def luck_pillars_legacy_list(luck: dict[str, Any]) -> list[dict[str, Any]]:
    """Backward-compatible flat list for code expecting luck_pillars."""
    return [p for p in (luck.get("pillars") or []) if p.get("gan_zhi")]