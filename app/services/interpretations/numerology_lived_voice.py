"""Plain lived voice for numerology walk, calling, weaknesses, and total paths."""

from __future__ import annotations

import re
from typing import Any

from app.services.compound_occult import get_compound_entry
from app.services.interpretations.manifestation_voice import plain_flesh
from app.services.interpretations.numerology_number_insight import build_total_insight

FINAL_MEANS_PLAIN: dict[int, str] = {
    1: "Leadership and initiative — name the direction and stand first.",
    2: "Partnership and patience — harmony built through chosen allies.",
    3: "Communication and creative output — words, art, and performance as your product.",
    4: "Slow build and repetition — trust, wealth, and legacy from steady work.",
    5: "Freedom and honest movement — variety, travel, and truth before motion.",
    6: "Home, beauty, and service — healing and order in what you touch.",
    7: "Depth and study — solitude that eventually feeds public clarity.",
    8: "Wealth, resources, and executive power — money and legacy when conscience leads.",
    9: "Closure and release — mercy through finished endings, not endless rescue.",
    11: "Early pattern-sense — intuition that must ship into real work.",
    22: "Big vision in phases — scale only when the body and team can hold it.",
    33: "Teaching through care — compassion with firm boundaries.",
}

WALK_BY_FINAL: dict[int, tuple[str, str]] = {
    1: (
        "Name one direction only you can take — start before the room agrees.",
        "Strong looks like: a visible decision shipped this week; allies follow, they never drag you.",
    ),
    2: (
        "Choose one partnership and polish it — patience beats rushing the mirror.",
        "Strong looks like: one boundary spoken kindly; peace becomes routine, not drama.",
    ),
    3: (
        "Finish one real creative piece before you post, pitch, or perform it.",
        "Strong looks like: draft done Tuesday, share Wednesday — applause follows proof, not a loud empty intro.",
    ),
    4: (
        "Ship one brick you will repeat for a year — document, payment, or habit.",
        "Strong looks like: the same reliable finish each week; trust compounds in body and bank.",
    ),
    5: (
        "Tell one truth before you move — job, city, or hard conversation.",
        "Strong looks like: honest risk taken cleanly; freedom with a spine, not escape.",
    ),
    6: (
        "Fix one domestic or aesthetic system — schedule, meal, or space — without lecturing anyone.",
        "Strong looks like: home runs smoother; beauty serves people, it does not control them.",
    ),
    7: (
        "Block focused alone time with one research question — no inbox.",
        "Strong looks like: insight returns as counsel someone would pay for, not hoarded notes.",
    ),
    8: (
        "Audit one account — money, time, or energy — and cut what dishonors conscience.",
        "Strong looks like: resources move ethically; power feeds legacy, not ego.",
    ),
    9: (
        "Close one door publicly this season — letter, resignation, or archive.",
        "Strong looks like: grief turns into wisdom others can use; endings stay clean.",
    ),
    11: (
        "Turn one insight into one tangible deliverable this week.",
        "Strong looks like: intuition lands as finished work, not a floating download.",
    ),
    22: (
        "Cut the big plan to the next ninety days — one foundation pour only.",
        "Strong looks like: scale grows in phases; the spine keeps up with the blueprint.",
    ),
    33: (
        "Set one fee or limit on help — time, money, or access.",
        "Strong looks like: care teaches ascent; boundaries stay kind and firm.",
    ),
}

CALLING_BY_FINAL: dict[int, tuple[str, str]] = {
    1: (
        "You are called to lead and name the road — not wait for permission.",
        "When you do: respect arrives as followership; the path bends toward your stand.",
    ),
    2: (
        "You are called to build peace through chosen partnership.",
        "When you do: harmony becomes infrastructure; the right mirror sharpens you.",
    ),
    3: (
        "You are called to create and speak — but only from finished work.",
        "When you do: people stay for the person behind the post; the message outlives the performance.",
    ),
    4: (
        "You are called to outlast — stone upon stone, no shortcut tax.",
        "When you do: wealth and trust arrive from sacred repetition, not hype.",
    ),
    5: (
        "You are called to move honestly — truth before motion.",
        "When you do: luck follows clean risk; freedom keeps a spine.",
    ),
    6: (
        "You are called to make home and beauty real — service without control.",
        "When you do: the hearth repairs people; duty and grace share one rope.",
    ),
    7: (
        "You are called to finish initiation — study, then share.",
        "When you do: solitude feeds public clarity; counsel replaces isolation.",
    ),
    8: (
        "You are called to run resources with justice — wealth as legacy, not trophy.",
        "When you do: money and power feed what lasts; the crown keeps conscience.",
    ),
    9: (
        "You are called to close cycles cleanly — release without amnesia.",
        "When you do: mercy lands with teeth; wisdom offered, not imposed.",
    ),
    11: (
        "You are called to ground voltage — sense early, ship into matter.",
        "When you do: invention builds; the nerve serves the work.",
    ),
    22: (
        "You are called to build in phases — cathedral thinking, human pace.",
        "When you do: world-touching work lands; scale and body stay aligned.",
    ),
    33: (
        "You are called to teach through care — love with limits.",
        "When you do: compassion sets boundaries; ascent without martyrdom.",
    ),
}

_COMPOUND_PACE: dict[int, str] = {
    10: "Earn visibility before you claim the throne.",
    12: "Pay the cost in private before the public voice speaks.",
    13: "Reinvent on schedule — finish the old chapter before marketing the new one.",
    17: "Hope after strip-down — proof before hype.",
    19: "Let skill catch up to spotlight.",
    21: "Merge two worlds in the draft before you broadcast.",
    27: "Carry the heavy service load in private before you release.",
    28: "Build alliance and contract before solo crown.",
    30: "One finished story before many platforms.",
    33: "Master care in the body before teaching the room.",
}

_TOTAL_KEY_PLAIN: dict[str, str] = {
    "expression": "public name-field",
    "soul_urge": "private appetite",
    "personality": "first-impression mask",
    "birthday_number": "monthly rhythm",
}

_TOTAL_COMPOUND_PLAIN: dict[tuple[int, int], str] = {
    (10, 1): "Visibility shows up before the title is fully earned.",
    (17, 8): "Your inner drive wants wealth after a hard reset — real accounts, not hype.",
    (27, 9): "Heavy service and compassion work sit before clean release.",
    (28, 1): "Partnership and contracts come before any solo crown.",
}


def _normalize_line(text: str) -> str:
    return " ".join(text.split())


_LP_WALK_METHOD: dict[int, str] = {
    1: "your stand-first birth walk",
    2: "your partnership-first birth walk",
    3: "your finish-before-you-speak birth walk",
    4: "your slow-build birth walk",
    5: "your truth-before-motion birth walk",
    6: "your hearth-and-beauty birth walk",
    7: "your study-then-share birth walk",
    8: "your ethical-power birth walk",
    9: "your clean-closure birth walk",
    11: "your ground-the-insight birth walk",
    22: "your phased-build birth walk",
    33: "your bounded-care birth walk",
}


def _compound_pace_clause(c: int, f: int) -> str:
    if c == f:
        return ""
    pace = _COMPOUND_PACE.get(c)
    if pace:
        return pace.rstrip(". ").strip()
    flesh = plain_flesh(
        get_compound_entry(c, f, f"{c}/{f}" if c != f else str(c)).get("flesh", "")
    ).split(".")[0]
    return flesh.rstrip(". ").strip()


def _total_meaning_plain(tc: int, tv: int) -> str:
    special = _TOTAL_COMPOUND_PLAIN.get((tc, tv))
    if special:
        return special
    if tc == tv:
        return FINAL_MEANS_PLAIN.get(tv, "")
    pace = _COMPOUND_PACE.get(tc)
    final = FINAL_MEANS_PLAIN.get(tv, "")
    if pace and final:
        return f"{pace.rstrip('.')} — then {final[0].lower() + final[1:]}"
    return final


def _walk_how_sentence(method: str, pace: str, role: str) -> str:
    if pace:
        return (
            f"Use {method}: {pace.lower()}, then finish the work this {role} describes."
        )
    return f"Use {method} to finish the work first, then let this {role} show in public."


def build_walk_action(c: int, f: int) -> str:
    action, strong = WALK_BY_FINAL.get(
        f,
        (
            "Walk your finish in order — body earns before voice speaks.",
            "Strong looks like: one completed step before the next announcement.",
        ),
    )
    pace = _compound_pace_clause(c, f)
    if pace:
        action = f"{pace} — {action[0].lower() + action[1:]}"
    return f"{action} {strong}"


def build_calling_action(c: int, f: int) -> str:
    call, gain = CALLING_BY_FINAL.get(
        f,
        (
            "You are called to walk your chart in order.",
            "When you do: people trust your pace and follow your lead.",
        ),
    )
    pace = _compound_pace_clause(c, f)
    if pace:
        call = f"{call.rstrip('.')} — {pace.lower()}."
    return f"{call} {gain}"


def build_weaknesses_avatar_lens(facts: dict[str, Any], c: int, f: int, lib: dict[str, Any]) -> list[str]:
    """Four themed weakness bullets — rescue, proof, reputation, follow-through."""
    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    pers = facts.get("personality") or {}
    expr_val = expr.get("value")
    soul_val = soul.get("value")
    pers_val = pers.get("value")

    if c == 27 or f == 9:
        rescue = (
            "Keep a rescue exit — if they are not ready for your help closing, "
            "step back or you carry their unfinished ending."
        )
    elif f in (2, 6):
        rescue = (
            "Keep a rescue exit — their chaos becomes your weather; "
            "close yourself off when help turns into carrying their book."
        )
    else:
        rescue = (
            "Keep a rescue exit — if they are not ready, close yourself off "
            "or you inherit their unfinished chapter."
        )

    if c in (17, 19, 28) or f == 8:
        proof = (
            "Never invest in an ending before proof — money and relationships "
            "need momentum in the books before you sign."
        )
    elif expr_val and soul_val and expr_val != soul_val:
        proof = (
            "Never invest before proof — private hunger and public calendar disagree; "
            "hold yeses until momentum shows."
        )
    else:
        proof = (
            "Never believe an ending and invest early — "
            "finances and relationships need real momentum first."
        )

    if pers_val and expr_val and pers_val != expr_val:
        reputation = (
            "Never front the ending — charm opens the room while work is empty; "
            "wait for proof before you spend reputation."
        )
    elif c in (10, 19, 30):
        reputation = (
            "Never represent the finish before work is real — "
            "pause the big yes until proof catches appetite."
        )
    else:
        reputation = (
            "Never spend reputation before the work is real — "
            "momentum proof must come before the handshake."
        )

    if pers_val and expr_val and pers_val != expr_val:
        follow = (
            "Charm opens doors you never intend to keep — "
            "leave when the deal outruns your follow-through."
        )
    else:
        follow = (
            "Ease opens doors — leave when the handshake outruns "
            "what you can finish and document."
        )

    items = [rescue, proof, reputation, follow]
    cleaned: list[str] = []
    for item in items:
        line = re.sub(r"\d+/\d+", "", item)
        line = re.sub(r"\bcompound \d+\b", "", line, flags=re.I)
        line = re.sub(r"\blife path \d+\b", "", line, flags=re.I)
        line = _normalize_line(line)
        if line and line not in cleaned:
            cleaned.append(line)
    return cleaned[:4]


def build_weakness_lived(facts: dict[str, Any], c: int, f: int, lib: dict[str, Any]) -> list[str]:
    items: list[str] = []

    if f == 3:
        items.append(
            "Posting before the draft is done — stop when likes land on the intro and the middle is still empty."
        )
    elif f == 8:
        items.append(
            "Chasing pay without conscience — stop when the raise forbids the work you respect."
        )
    elif f == 9:
        items.append(
            "Carrying everyone else's endings — stop when rescue replaces your own closure."
        )
    else:
        items.append(
            "Marketing the mask before the body finishes — stop when applause outruns the deliverable."
        )

    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    if expr.get("value") and soul.get("value") and expr["value"] != soul["value"]:
        items.append(
            "Booking the public calendar while private hunger simmers — hold off signing Sunday night with open tasks."
        )

    if c != f:
        flesh = plain_flesh(lib.get("flesh", "")).split(".")[0]
        if "platform" in flesh.lower() or c == 30:
            items.append(
                "Too many channels, none finished — pick one outlet until one story fully lands."
            )
        elif c in (17, 19, 28):
            items.append(
                "Scaling visibility before proof — pause deals until the books match the story."
            )
        else:
            items.append(
                "Spending reputation before the work is real — wait for proof before the next big yes."
            )

    pers = facts.get("personality") or {}
    if pers.get("value") and expr.get("value") and pers["value"] != expr.get("value"):
        items.append(
            "Charm opens doors you never intend to keep — leave when the handshake outruns the follow-through."
        )

    if f in (3, 5):
        items.append(
            "Scattered talent, sharp words — slow down when promise outruns bone."
        )
    elif f in (2, 6):
        items.append(
            "Merging without discernment — exit when their chaos becomes your daily weather."
        )

    cleaned: list[str] = []
    for item in items:
        line = re.sub(r"\d+/\d+", "", item)
        line = re.sub(r"\bcompound \d+\b", "", line, flags=re.I)
        line = re.sub(r"\blife path \d+\b", "", line, flags=re.I)
        line = _normalize_line(line)
        if line and line not in cleaned:
            cleaned.append(line)

    return cleaned[:4]


def build_total_advice(key: str, facts: dict[str, Any], lp: dict[str, Any]) -> str:
    row = facts.get(key) or {}
    total = {
        "compound": row.get("compound"),
        "value": row.get("value"),
        "display": row.get("display", "—"),
    }
    advice, _ = build_total_insight(key, total, lp)
    return advice


def build_total_path(
    lp: dict[str, Any],
    total_row: dict[str, Any],
    key: str,
) -> str:
    _, path = build_total_insight(key, total_row, lp)
    return path