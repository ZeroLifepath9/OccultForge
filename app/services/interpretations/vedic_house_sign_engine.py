"""Vedic house = lens, sign = filter — woven prose without label recitation."""

from __future__ import annotations

from typing import Any

from app.services.overview_lore import HOUSE_10_WALK, HOUSE_2_WALK, HOUSE_7_WALK
from app.services.phoenix_insight import SIGN_MEANS
from app.services.priest_overview import VEDIC_HOUSE_ROLE

HOUSE_LENS: dict[int, dict[str, str]] = {
    1: {"name": "self and body", "purushartha": "dharma", "focus": "how you enter rooms and hold vitality"},
    2: {"name": "personal resources and speech", "purushartha": "artha", "focus": "what you earn, value, and say aloud about money"},
    3: {"name": "courage and skill", "purushartha": "kama", "focus": "initiative, siblings, and short journeys"},
    4: {"name": "home and emotional root", "purushartha": "moksha", "focus": "shelter, mother-line, private peace"},
    5: {"name": "creativity and risk", "purushartha": "dharma", "focus": "children, romance, speculative gain"},
    6: {"name": "daily work and health", "purushartha": "artha", "focus": "service, debt, enemies, routine"},
    7: {"name": "partnership and contract", "purushartha": "kama", "focus": "marriage, rivals, fair exchange in bonds"},
    8: {"name": "transformation and shared depth", "purushartha": "moksha", "focus": "inheritance, crisis, occult leverage"},
    9: {"name": "belief and fortune", "purushartha": "dharma", "focus": "teachers, luck, long travel, ethics"},
    10: {"name": "career and public name", "purushartha": "artha", "focus": "reputation, authority, how you are remembered"},
    11: {"name": "gains and networks", "purushartha": "kama", "focus": "allies, income streams, fulfilled ambition"},
    12: {"name": "release and exile", "purushartha": "moksha", "focus": "expenses, solitude, spiritual surrender"},
}

SIGN_TEMPERAMENT: dict[str, str] = {
    "Aries": "assertive and pioneering",
    "Taurus": "stable and material-focused",
    "Gemini": "communicative and adaptable",
    "Cancer": "protective and emotionally rooted",
    "Leo": "visible and pride-driven",
    "Virgo": "precise and service-minded",
    "Libra": "diplomatic and exchange-focused",
    "Scorpio": "intense and transformational",
    "Sagittarius": "philosophical and roaming",
    "Capricorn": "disciplined and institutional",
    "Aquarius": "innovative and network-oriented",
    "Pisces": "compassionate and boundary-soft",
}

LAGNA_BODY: dict[str, str] = {
    "Aries": "energetic entry — lead fast, guard against impulse spend and accident stress",
    "Taurus": "steadfast body — patience builds purse; throat and weight need honest upkeep",
    "Gemini": "nervous quick mind — words are currency; scatter taxes health and accounts",
    "Cancer": "nurturing shell — home and food policy govern earning stamina",
    "Leo": "heart-forward presence — visibility is fuel; pride overspends when unmoored",
    "Virgo": "analytical upkeep — craft and health routines protect income",
    "Libra": "aesthetic balance — fair exchange in body and brand; indecision leaks money",
    "Scorpio": "intense reserve — leverage and crisis craft; secrecy can hoard poison",
    "Sagittarius": "roaming truth — teaching and distance products; dogma wastes margin",
    "Capricorn": "disciplined climb — delay as strategy; joints and spine need respect",
    "Aquarius": "future-tribe wiring — odd contracts and networks; rebellion without vault chaos",
    "Pisces": "dissolving empathy — art and healing income; boundaries prevent drowning",
}

# Split walk tables into do (first clause) / dont (second clause) heuristics
def _split_walk(walk: str) -> tuple[str, str]:
    if "; " in walk:
        parts = walk.split("; ", 1)
        return parts[0].strip(), parts[1].strip()
    if " when " in walk.lower():
        idx = walk.lower().index(" when ")
        return walk[:idx].strip(), walk[idx:].strip()
    if " — " in walk:
        parts = walk.split(" — ", 1)
        return parts[0].strip(), parts[1].strip()
    return walk.strip(), "forcing the lane when temperament and season disagree"


def _walk_for_house(house_num: int, sign: str) -> str:
    if house_num == 2:
        return HOUSE_2_WALK.get(sign, "resources ask you to name what feeds you honestly")
    if house_num == 7:
        return HOUSE_7_WALK.get(sign, "partnership asks for written fairness")
    if house_num == 10:
        return HOUSE_10_WALK.get(sign, "public life asks how you want to be remembered")
    role = VEDIC_HOUSE_ROLE.get(house_num, "this life arena")
    return f"{role} runs through {SIGN_TEMPERAMENT.get(sign, 'this temperament')}"


def interpret_house_sign(house_num: int, sign: str) -> dict[str, str]:
    """Lens + filter weave without citing house number or sign name."""
    lens = HOUSE_LENS.get(house_num, {"focus": VEDIC_HOUSE_ROLE.get(house_num, "life domain")})
    temperament = SIGN_TEMPERAMENT.get(sign, "distinct temperament")
    walk = _walk_for_house(house_num, sign)
    do_part, dont_part = _split_walk(walk)
    focus = lens.get("focus", lens.get("name", "this domain"))
    weave = (
        f"Where {focus}, {temperament} tone colors the lane — {do_part.lower() if do_part[0].isupper() else do_part}."
    )
    return {
        "do": do_part,
        "dont": dont_part,
        "weave": weave,
        "temperament": temperament,
        "focus": focus,
    }


def interpret_lagna(lagna_sign: str) -> str:
    return LAGNA_BODY.get(lagna_sign, SIGN_MEANS.get(lagna_sign, "body-truth governs entry and stamina."))


def tropical_ascendant_overlay(lagna: str, tropical: str) -> str:
    if not lagna or not tropical or lagna == tropical:
        return ""
    return (
        f"Sidereal body runs {LAGNA_BODY.get(lagna, 'deeper stamina law')[:60]} — "
        f"tropical first impression wears a {SIGN_TEMPERAMENT.get(tropical, 'different')} mask; "
        f"health and vocation must honor the body chart before the costume wins."
    )


def build_vedic_interpretation_lens(facts: dict[str, Any]) -> dict[str, Any]:
    """Precomputed house weaves for imprint attach."""
    asc = facts.get("ascendant") or {}
    lagna = asc.get("vedic_lagna") or ""
    tropical = asc.get("western_sign") or ""
    h2 = (facts.get("vedic_house_2") or {}).get("sign", "")
    h7 = (facts.get("vedic_house_7") or {}).get("sign", "")
    h10 = (facts.get("vedic_house_10") or {}).get("sign", "")
    return {
        "lagna_body": interpret_lagna(lagna) if lagna else "",
        "tropical_mask": tropical_ascendant_overlay(lagna, tropical),
        "wealth": interpret_house_sign(2, h2) if h2 else {},
        "partnership": interpret_house_sign(7, h7) if h7 else {},
        "career": interpret_house_sign(10, h10) if h10 else {},
    }