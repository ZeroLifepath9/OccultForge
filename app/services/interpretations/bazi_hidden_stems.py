"""Hidden Stems (藏干, Cáng Gān) — concealed heavenly stems within earthly branches."""

from __future__ import annotations

from typing import Any, Literal

from app.calculators.bazi import STEM_ELEMENTS
from app.services.imprint_labels import branch_animal, stem_english

QiRole = Literal["root", "center", "remnant"]

# Classical correspondences: Root (本气), Center (中气), Remnant (余气) per branch.
BRANCH_HIDDEN_STEMS: dict[str, list[tuple[str, QiRole]]] = {
    "子": [("癸", "root")],
    "丑": [("己", "root"), ("癸", "center"), ("辛", "remnant")],
    "寅": [("甲", "root"), ("丙", "center"), ("戊", "remnant")],
    "卯": [("乙", "root")],
    "辰": [("戊", "root"), ("乙", "center"), ("癸", "remnant")],
    "巳": [("丙", "root"), ("戊", "center"), ("庚", "remnant")],
    "午": [("丁", "root"), ("己", "center")],
    "未": [("己", "root"), ("丁", "center"), ("乙", "remnant")],
    "申": [("庚", "root"), ("壬", "center"), ("戊", "remnant")],
    "酉": [("辛", "root")],
    "戌": [("戊", "root"), ("辛", "center"), ("丁", "remnant")],
    "亥": [("壬", "root"), ("甲", "center")],
}

QI_LABEL: dict[QiRole, str] = {
    "root": "本气",
    "center": "中气",
    "remnant": "余气",
}

QI_WEIGHT: dict[QiRole, float] = {
    "root": 0.70,
    "center": 0.22,
    "remnant": 0.08,
}

QI_WEIGHT_LABEL: dict[QiRole, str] = {
    "root": "~70%",
    "center": "~22%",
    "remnant": "~8%",
}

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

TEN_GOD_LABEL: dict[str, str] = {
    "companion": "Companion (比劫)",
    "output": "Output (食伤)",
    "wealth": "Wealth (财)",
    "officer": "Officer (官杀)",
    "resource": "Resource (印)",
}

TEN_GOD_PLAIN: dict[str, str] = {
    "companion": "peer drive",
    "output": "creative output",
    "wealth": "resources and gain",
    "officer": "discipline and demand",
    "resource": "support and recovery",
}

HIDDEN_DEFINITION = (
    "Cáng Gān (藏干): concealed Heavenly Stems within each Earthly Branch — latent drives, "
    "dormant talents, and elemental support beneath the visible Four Pillars."
)

HIDDEN_FORMULA = (
    "Total element strength = heavenly stem + Σ hidden stems "
    "(本气 ~70% + 中气 ~22% + 余气 ~8% per branch)."
)


def _stem_info(stem: str, role: QiRole) -> dict[str, str | float]:
    element = STEM_ELEMENTS.get(stem, "")
    return {
        "stem": stem,
        "stem_en": stem_english(stem),
        "element": element,
        "role": role,
        "role_label": QI_LABEL[role],
        "weight": QI_WEIGHT[role],
        "weight_label": QI_WEIGHT_LABEL[role],
    }


def hidden_stems_for_branch(branch: str) -> list[dict[str, str | float]]:
    """All hidden stems for a branch, root first."""
    return [_stem_info(stem, role) for stem, role in BRANCH_HIDDEN_STEMS.get(branch, [])]


def root_hidden_stem(branch: str) -> dict[str, str | float] | None:
    """Primary 本气 hidden stem — most relevant for display."""
    stems = hidden_stems_for_branch(branch)
    return stems[0] if stems else None


def ten_god_role(day_master_el: str, other_el: str) -> str:
    """Map hidden-stem element to Ten God (十神) relative to Day Master."""
    if not day_master_el or not other_el:
        return ""
    if day_master_el == other_el:
        return "companion"
    if ELEMENT_GENERATES.get(day_master_el) == other_el:
        return "output"
    if ELEMENT_GENERATES.get(other_el) == day_master_el:
        return "resource"
    if ELEMENT_CONTROLS.get(day_master_el) == other_el:
        return "wealth"
    if ELEMENT_CONTROLS.get(other_el) == day_master_el:
        return "officer"
    return ""


def attach_hidden_stems_to_pillar(pillar: dict[str, Any]) -> dict[str, Any]:
    """Attach root 藏干 fields onto a pillar dict (mutates and returns)."""
    branch = pillar.get("branch", "")
    root = root_hidden_stem(branch)
    stems = hidden_stems_for_branch(branch)
    if root:
        pillar["hidden_stem"] = root["stem"]
        pillar["hidden_stem_en"] = root["stem_en"]
        pillar["hidden_stem_element"] = root["element"]
        pillar["hidden_role"] = root["role"]
        pillar["hidden_role_label"] = root["role_label"]
    pillar["all_hidden_stems"] = stems
    return pillar


def attach_hidden_stems_to_pillars(pillars: dict[str, Any]) -> dict[str, Any]:
    for name in pillars:
        p = pillars.get(name)
        if isinstance(p, dict):
            attach_hidden_stems_to_pillar(p)
    return pillars


def pillar_identity_label(pillar: dict[str, str]) -> str:
    """Visible stem element + branch animal — never 藏干."""
    el = pillar.get("stem_element", "")
    animal = pillar.get("branch_en") or branch_animal(pillar.get("branch", ""))
    return f"{el} {animal}".strip()


def pillar_element_synergy(visible_el: str, hidden_el: str) -> str:
    """How visible stem element and branch 本气 work together."""
    if not visible_el or not hidden_el:
        return ""
    if visible_el == hidden_el:
        return (
            f"Visible {visible_el} and branch 本气 {hidden_el} align — "
            f"inner reservoir echoes the stem; latent talent is easier to access."
        )
    if ELEMENT_GENERATES.get(visible_el) == hidden_el:
        return (
            f"Visible {visible_el} generates hidden {hidden_el} — "
            f"outward expression feeds an inner layer that sharpens and extends what you show."
        )
    if ELEMENT_GENERATES.get(hidden_el) == visible_el:
        return (
            f"Hidden {hidden_el} generates visible {visible_el} — "
            f"the branch supplies grounding and fuel beneath your stem."
        )
    if ELEMENT_CONTROLS.get(visible_el) == hidden_el:
        return (
            f"Visible {visible_el} regulates hidden {hidden_el} — "
            f"you discipline inner drives before they surface."
        )
    if ELEMENT_CONTROLS.get(hidden_el) == visible_el:
        return (
            f"Hidden {hidden_el} checks visible {visible_el} — "
            f"inner pressure tests and refines outward expression."
        )
    return (
        f"Visible {visible_el} and hidden {hidden_el} sit outside direct 生克 cycles — "
        f"they run as parallel tracks until timing activates the branch."
    )


def pillar_display_line(pillar: dict[str, str]) -> str:
    """Augmented display: visible element · hidden element · zodiac."""
    visible_el = pillar.get("stem_element", "")
    animal = pillar.get("branch_en") or branch_animal(pillar.get("branch", ""))
    identity = pillar_identity_label(pillar)
    branch = pillar.get("branch", "")
    root = root_hidden_stem(branch)
    if not root or not animal:
        return identity
    hidden_el = str(root["element"])
    hidden_en = str(root["stem_en"])
    if hidden_el == visible_el:
        return identity
    return f"{visible_el} · hidden {hidden_en} {hidden_el} · {animal}"


def pillar_hidden_display(pillar: dict[str, str]) -> dict[str, Any]:
    """Display payload: identity = visible stem; 藏干 is supplementary."""
    branch = pillar.get("branch", "")
    animal = pillar.get("branch_en") or branch_animal(branch)
    visible_el = pillar.get("stem_element", "")
    identity = pillar_identity_label(pillar)
    root = root_hidden_stem(branch)
    base: dict[str, Any] = {
        "label": identity,
        "stem_element": visible_el,
        "display_line": identity,
        "branch_hidden_label": "",
        "synergy_note": "",
        "hidden_stem": "",
        "hidden_stem_en": "",
        "hidden_stem_element": "",
        "hidden_role": "",
        "hidden_role_label": "",
        "branch_en": animal,
    }
    if not root:
        return base
    hidden_el = str(root["element"])
    base.update(
        {
            "display_line": pillar_display_line(pillar),
            "branch_hidden_label": f"{hidden_el} {animal}".strip(),
            "synergy_note": pillar_element_synergy(visible_el, hidden_el),
            "hidden_stem": root["stem"],
            "hidden_stem_en": root["stem_en"],
            "hidden_stem_element": hidden_el,
            "hidden_role": root["role"],
            "hidden_role_label": root["role_label"],
            "all_hidden": hidden_stems_for_branch(branch),
        }
    )
    return base


def count_surface_elements(pillars: dict[str, Any]) -> dict[str, int]:
    """Visible stems only (no 藏干)."""
    counts: dict[str, int] = {}
    for pillar in pillars.values():
        if not isinstance(pillar, dict):
            continue
        el = pillar.get("stem_element")
        if el:
            counts[el] = counts.get(el, 0) + 1
    return counts


def count_hidden_elements(pillars: dict[str, Any], *, all_qi: bool = False) -> dict[str, int]:
    """Count hidden-stem elements (root qi by default, or all layers unweighted)."""
    counts: dict[str, int] = {}
    for pillar in pillars.values():
        if not isinstance(pillar, dict):
            continue
        branch = pillar.get("branch", "")
        stems = hidden_stems_for_branch(branch)
        if not stems:
            continue
        if all_qi:
            for hs in stems:
                el = str(hs["element"])
                if el:
                    counts[el] = counts.get(el, 0) + 1
        else:
            el = str(stems[0]["element"])
            if el:
                counts[el] = counts.get(el, 0) + 1
    return counts


def count_weighted_element_balance(pillars: dict[str, Any]) -> dict[str, float]:
    """Stem element (1.0) + weighted 藏干 layers per classical hierarchy."""
    elements = ("Wood", "Fire", "Earth", "Metal", "Water")
    counts: dict[str, float] = {el: 0.0 for el in elements}
    for pillar in pillars.values():
        if not isinstance(pillar, dict):
            continue
        stem_el = pillar.get("stem_element")
        if stem_el in counts:
            counts[stem_el] += 1.0
        for hs in hidden_stems_for_branch(pillar.get("branch", "")):
            el = str(hs["element"])
            role = hs["role"]
            if el in counts and isinstance(role, str):
                counts[el] += QI_WEIGHT.get(role, 0.5)  # type: ignore[arg-type]
    return {k: round(v, 2) for k, v in counts.items() if v > 0}


def _latent_balance_note(surface: dict[str, int], weighted: dict[str, float]) -> str:
    notes: list[str] = []
    for el, w in sorted(weighted.items(), key=lambda x: -x[1]):
        s = surface.get(el, 0)
        if w >= s + 0.5 and w > 0:
            notes.append(
                f"{el} reads stronger inside the chart ({w:.1f} weighted with 藏干 vs {s} visible stem{'s' if s != 1 else ''})"
            )
    weak_surface = [el for el in ("Wood", "Fire", "Earth", "Metal", "Water") if surface.get(el, 0) == 0]
    for el in weak_surface[:2]:
        if weighted.get(el, 0) >= 0.5:
            notes.append(
                f"surface looks {el}-light but hidden stems supply internal {el.lower()} — latent support is real"
            )
    return ". ".join(notes[:2])


def _day_branch_qi_clause(stems: list[dict[str, str | float]]) -> str:
    if not stems:
        return ""
    if len(stems) == 1:
        hs = stems[0]
        return (
            f"Pure branch — single 本气 {hs['stem_en']} {hs['element']} "
            f"({hs['weight_label']} of branch force)."
        )
    layers = ", ".join(
        f"{hs['stem_en']} {hs['element']} as {hs['role_label']} ({hs['weight_label']})"
        for hs in stems[:3]
    )
    return f"Day branch layers: {layers}."


def build_hidden_stems_framework(pillars: dict[str, Any], day_master: str) -> dict[str, Any]:
    """Classical 藏干 framework for narration and UI."""
    surface = count_surface_elements(pillars)
    weighted = count_weighted_element_balance(pillars)
    day = pillars.get("day") or {}
    day_stems = hidden_stems_for_branch(day.get("branch", ""))
    root = day_stems[0] if day_stems else None
    root_el = str(root["element"]) if root else ""
    tg_key = ten_god_role(day_master, root_el)
    tg_label = TEN_GOD_LABEL.get(tg_key, "")

    pillar_hidden = {}
    for name in ("year", "month", "day", "hour"):
        p = pillars.get(name) or {}
        pillar_hidden[name] = hidden_stems_for_branch(p.get("branch", ""))

    return {
        "definition": HIDDEN_DEFINITION,
        "formula": HIDDEN_FORMULA,
        "qi_layers": {
            "root": {"label": "本气 Root Qi", "weight": QI_WEIGHT_LABEL["root"], "note": "core traits"},
            "center": {"label": "中气 Center Qi", "weight": QI_WEIGHT_LABEL["center"], "note": "nuanced support"},
            "remnant": {"label": "余气 Residual Qi", "weight": QI_WEIGHT_LABEL["remnant"], "note": "subtle, conditional"},
        },
        "surface_balance": surface,
        "weighted_balance": weighted,
        "latent_insight": _latent_balance_note(surface, weighted),
        "day_branch": {
            "branch": day.get("branch", ""),
            "gan_zhi": day.get("gan_zhi", ""),
            "hidden_stems": day_stems,
            "root": root,
            "ten_god": tg_label,
            "ten_god_key": tg_key,
            "qi_clause": _day_branch_qi_clause(day_stems),
        },
        "pillar_hidden": pillar_hidden,
    }


def hidden_stem_insight(
    natal_day: dict[str, str],
    sky_day: dict[str, str],
    *,
    day_master: str,
    branch_relation: str | None = None,
    framework: dict[str, Any] | None = None,
    pillars: dict[str, Any] | None = None,
    imprint: dict[str, Any] | None = None,
) -> str:
    """Layered 藏干 clause — delegates to interpretation lens (single source)."""
    from app.services.interpretations.bazi_interpretation_lens import build_bazi_interpretation_lens

    fw = framework or {}
    natal_pillars = pillars
    imp = imprint
    if imp:
        from app.services.bazi_enrich import ensure_bazi_canonical

        imp = ensure_bazi_canonical(imp)
        natal_pillars = imp["bazi"]["pillars"]
    if not natal_pillars:
        natal_pillars = {"day": natal_day}

    lens = build_bazi_interpretation_lens(
        natal_pillars,
        imprint=imp,
        sky_pillars={"day": sky_day},
        compares={"day_vs_sky_day": {"branch_relation": branch_relation}},
    )
    day_card = (lens.get("pillars") or {}).get("day") or {}
    if not day_card.get("hidden", {}).get("element"):
        return ""

    parts: list[str] = [HIDDEN_DEFINITION]
    if day_card.get("synergy_note"):
        parts.append(day_card["synergy_note"])

    day_fw = fw.get("day_branch") or (fw.get("hidden_stems") or {}).get("day_branch") or {}
    qi_clause = day_fw.get("qi_clause") or _day_branch_qi_clause(
        hidden_stems_for_branch(natal_day.get("branch", ""))
    )
    if qi_clause:
        parts.append(qi_clause)

    tg = day_fw.get("ten_god") or TEN_GOD_LABEL.get(day_card.get("ten_god_vs_dm", ""), "")
    if tg:
        inner_en = day_card["hidden"].get("stem_en", "")
        inner_el = day_card["hidden"].get("element", "")
        parts.append(
            f"Relative to Day Master {day_master}, branch 本气 {inner_en} {inner_el} maps as {tg} (十神) — "
            f"concealed career, wealth, or relational pressure not shown on the surface stem alone."
        )

    latent = (lens.get("balance") or {}).get("latent_insight") or fw.get("latent_insight", "")
    if latent:
        parts.append(f"Weighted 藏干 balance: {latent}.")

    sky_act = (lens.get("sky_activation") or {}).get("day_vs_natal") or {}
    activation = sky_act.get("activation_note", "")
    if activation:
        parts.append(activation)

    for line in lens.get("chart_interactions") or []:
        if line not in parts and "day pillar" in line.lower():
            parts.append(line)

    return " ".join(parts)


def hidden_stem_daily_advice(
    natal_day: dict[str, str],
    sky_day: dict[str, str],
    *,
    day_master: str,
    branch_relation: str | None = None,
) -> str:
    """One plain-English sentence — hidden stem conclusion only, no method."""
    inner = root_hidden_stem(natal_day.get("branch", ""))
    sky_inner = root_hidden_stem(sky_day.get("branch", ""))
    if not inner:
        return ""

    inner_el = str(inner["element"])
    inner_en = str(inner["stem_en"])
    visible = natal_day.get("stem_element", "")
    tg = TEN_GOD_PLAIN.get(ten_god_role(day_master, inner_el), "inner strength")

    if visible and inner_el != visible:
        line = (
            f"You show {visible} outwardly but carry {inner_en} {inner_el} inside — "
            f"let that {tg} guide a choice you would normally play safe on."
        )
    else:
        line = f"Your inner {inner_el.lower()} matches what you show — trust that {tg} today."

    if branch_relation == "chong_冲":
        return f"{line} A sign clash is active; keep your pace steady and skip fresh arguments."
    if sky_inner and str(sky_inner["element"]) == inner_el:
        return f"Today stirs your inner {inner_el.lower()} — act on instinct you usually keep private."
    return line