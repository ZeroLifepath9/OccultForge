"""
Financial / Mundane forge lens — boom-and-audit rhythm, smooth conversational advice.
Outer planets as weather; sidereal 2nd for income lane where relevant.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.matrix_decoder_voice import format_matrix_reading
from app.services.interpretations.vedic_house_sign_engine import interpret_house_sign
from app.services.interpretations.western_forge_lens import _who


def _expansion_voice(sign: str) -> str:
    voices = {
        "Aries": "spend on starts that can survive a fight week",
        "Taurus": "grow slow assets — land, craft, things you can touch",
        "Gemini": "multiply streams only after one stream pays rent",
        "Cancer": "fund belonging and shelter before you fund image",
        "Leo": "invest in visible proof, not applause alone",
        "Virgo": "expansion through skill stacks and clean books",
        "Libra": "grow through fair deals and designed partnerships",
        "Scorpio": "leverage depth — shared money needs written terms",
        "Sagittarius": "bet on teaching, travel, and belief with receipts",
        "Capricorn": "compound structure — boring wins the decade",
        "Aquarius": "innovation pays when the system is tested, not hyped",
        "Pisces": "fund art and mercy with boundaries, not fog",
    }
    return voices.get(sign, "measured growth with proof before pitch")


def _audit_voice(sign: str) -> str:
    voices = {
        "Aries": "audit catches rushed contracts and ego spends",
        "Taurus": "audit asks what you are holding that no longer earns",
        "Gemini": "audit trims scattered tabs and duplicate subscriptions",
        "Cancer": "audit checks whether comfort spend is care or escape",
        "Leo": "audit invoices pride before it performs broke",
        "Virgo": "audit is your friend — detail season collects leaks",
        "Libra": "audit tests whether charm matched the spreadsheet",
        "Scorpio": "audit finds hidden debt and power tied to money",
        "Sagittarius": "audit asks if the bet had scope or just story",
        "Capricorn": "audit season is backbone — pay the structure tax",
        "Aquarius": "audit separates real systems from trend toys",
        "Pisces": "audit clears fog deals and sympathy discounts",
    }
    return voices.get(sign, "paperwork season collects what hype signed")


def build_financial_forge_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    who = _who(imprint)
    wp = facts.get("western_planets") or {}
    jup = wp.get("Jupiter", {}).get("sign", "")
    sat = wp.get("Saturn", {}).get("sign", "")
    ven = wp.get("Venus", {}).get("sign", "")
    mar = wp.get("Mars", {}).get("sign", "")
    ura = wp.get("Uranus", {}).get("sign", "")
    nep = wp.get("Neptune", {}).get("sign", "")
    plu = wp.get("Pluto", {}).get("sign", "")

    h2 = (facts.get("vedic_house_2") or {}).get("sign", "")
    h2_i = interpret_house_sign(2, h2) if h2 else {}

    direct = (
        f"{who} — money runs on weather, not mood. "
        f"You get expansion seasons and audit seasons; glamour deals that skip paperwork "
        f"always come back on schedule, not as surprises. "
        f"Jupiter in {jup} is your boom leg — {_expansion_voice(jup)}. "
        f"Saturn in {sat} is your audit leg — {_audit_voice(sat)}."
    )

    influence_lines = [
        f"Expansion rhythm — optimism, growth bets, and generosity land in {jup} tone. Ride it with receipts.",
        f"Audit rhythm — limits, delays, and fine print land in {sat} tone. Respect it before you scale.",
        f"Desire pricing — Venus in {ven} sets what you chase for comfort; cheap thrills that fail the spreadsheet are fog.",
        f"Effort pricing — Mars in {mar} sets fight pace on the ledger; sprinting in audit week sours good deals.",
        f"Shock lane — Uranus in {ura} moves money through breaks; budget for surprise, not drama.",
        f"Fog lane — Neptune in {nep} glamours deals; if it feels destined but lacks math, wait one beat.",
        f"Power lane — Pluto in {plu} resets shared money and legacy; clean endings fund clean restarts.",
    ]
    if h2 and h2_i:
        influence_lines.append(
            f"Sidereal income house ({h2}) — {h2_i.get('weave', h2_i.get('do', 'name what you value aloud'))}"
        )
    influence_lines.append(
        "Mundane rule — boom weather signs the check; audit weather collects it. Mistaking weather for wisdom repeats the same excuse every cycle."
    )
    decoded = "\n".join(influence_lines)

    steps = [
        f"Track dates on your Jupiter–Saturn pair, not hype — spend in expansion weather on what survives {sat} audit.",
        f"Price joy through {ven} honestly; one comfort line item with a written cap.",
        f"Let {mar} set effort pace this week — one push, one close, one rest.",
        "Keep boom, audit, shock, and fog on separate ledger tabs — mixing them breeds excuse loops.",
        (
            f"Name one income move aligned with sidereal {h2} — {h2_i.get('do', 'voice what you value')}"
            if h2
            else "Name one income move aligned with what you actually value aloud."
        ),
        "Write one timing note — what peaked, what drained, what the same money lesson keeps asking.",
    ]
    avoids = [
        f"Signing in Jupiter weather and meeting Saturn fine print in month two — the classic leak.",
        "Neptune glamour plus urgency — mirage launches love tired kings.",
        "Uranus jolt spend without a runway — shock is not a budget plan.",
        "Calling audit season bad luck when the assignment was structure.",
    ]
    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:6], 1))
    avoid_lines = "\n".join(f"- {a}" for a in avoids[:4])
    action = f"Forge now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"

    return format_matrix_reading(direct, decoded, action)