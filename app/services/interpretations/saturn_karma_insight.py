"""Sidereal Saturn — house debt + sign lesson + zodiac manifestation layer."""

from __future__ import annotations

from typing import Any

# What Saturn in this sign teaches — the karmic curriculum.
SIGN_LESSON: dict[str, str] = {
    "Aries": "fair play is not the default — you take what you want or you wait forever.",
    "Taurus": "what you hold has hidden cost — stability and beauty carry hindrances you must see.",
    "Gemini": "being understood is the exam — words get misread when they matter most.",
    "Cancer": "blood-memory — familial weight, hereditary pattern, or a line you must break.",
    "Leo": "pride and self-validation — confidence must survive without applause.",
    "Virgo": "timing and choice under anxiety — perfection delayed becomes the debt itself.",
    "Libra": "exaltation — rare luck in rise and hierarchy; do not waste the exception.",
    "Scorpio": "hidden enemies and strategy — defend on every plane or shadow wins.",
    "Sagittarius": "freedom spent without conclusion — leisure, money, and follow-through taxed.",
    "Capricorn": "rigidity and conservative structure — growth stalls until you think outside the box.",
    "Aquarius": "think different on purpose — innovation and routine are how you get ahead.",
    "Pisces": "adaptation through bond — fluid situations teach; resistance compounds debt.",
}

# How each sign manifests debt — the zodiac's style of pressure.
SIGN_MANIFEST_STYLE: dict[str, str] = {
    "Aries": "through force, claim, and competition",
    "Taurus": "through possession, aesthetics, and what you try to secure",
    "Gemini": "through words, messages, and misread intent",
    "Cancer": "through family, memory, and emotional inheritance",
    "Leo": "through pride, visibility, and the need to be seen",
    "Virgo": "through worry, analysis, and delayed decisions",
    "Libra": "through partnership, charm, and social balance",
    "Scorpio": "through secrecy, leverage, and hidden opposition",
    "Sagittarius": "through freedom, belief, and unfinished conclusions",
    "Capricorn": "through structure, duty, and conservative conviction",
    "Aquarius": "through disruption, systems, and unconventional moves",
    "Pisces": "through fluid bonds, surrender, and adaptive change",
}

# House = where the debt lands (occult field).
HOUSE_DEBT: dict[int, str] = {
    1: "self, body, and how far you can see yourself going",
    2: "money, possession, and belief in what you deserve",
    3: "early education, siblings, local hierarchy, and authority figures",
    4: "home, roots, and the maternal line",
    5: "creativity, pleasure, children, and the path to success",
    6: "health, daily labor, enemies of routine, and material grind",
    7: "marriage, contracts, open enemies, and mirrored self",
    8: "taboo, shared resources, hidden enemies, and government exposure",
    9: "philosophy, teachers, travel, and higher law",
    10: "career, public name, and legacy",
    11: "networks, allies, and gains from community",
    12: "loss, isolation, spirit, and what hides behind the veil",
}

HOUSE_ORDINAL = {
    1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th",
    7: "7th", 8: "8th", 9: "9th", 10: "10th", 11: "11th", 12: "12th",
}

LP_KARMA_TUNE: dict[int, str] = {
    1: "solo initiative and standing alone",
    2: "partnership mirrors and emotional tides",
    3: "voice, visibility, and creative scatter",
    4: "structure, law, and emotional eclipse",
    5: "motion, truth, and restless freedom",
    6: "hearth, beauty, and service debt",
    7: "cave study, solitude, and sceptical depth",
    8: "power, accounts, and material crown",
    9: "closure, release, and humanitarian finish",
    11: "master intuition under double vibration",
    22: "builder legacy under master pressure",
    33: "teacher service under master sacrifice",
}


def _saturn_house(imprint: dict[str, Any]) -> tuple[int | None, str | None]:
    for row in imprint.get("vedic", {}).get("houses", []):
        if "Saturn" in (row.get("planets") or []):
            return row.get("house"), row.get("sign")
    return None, None


def _zodiac_in_house(sign: str, house: int | None) -> str:
    """How the sign manifests the debt inside the house — the zodiac play-in layer."""
    if not house:
        return (
            f"Saturn in {sign} still runs {SIGN_MANIFEST_STYLE.get(sign, 'through karmic pressure')} — "
            "house placement would name the exact lane."
        )

    keyed = (sign, house)
    specific: dict[tuple[str, int], str] = {
        ("Aries", 1): "the fight lands on the self — body and will must claim territory; moral fantasy loses.",
        ("Aries", 10): "career becomes combat — public rise through taking ground others won't.",
        ("Taurus", 2): "income and beauty lock together — what you possess slows until material and aesthetic discipline align.",
        ("Taurus", 4): "home and land hide the hindrance — the stability you chase may be the weight itself.",
        ("Gemini", 3): "every authority conversation misreads you — siblings, school, and local power test your words.",
        ("Gemini", 7): "partners and contracts garble intent — one-to-one deals carry the loudest static.",
        ("Cancer", 4): "the roof and maternal line concentrate curse or pattern — blood-debt at home.",
        ("Cancer", 7): "partners reopen family memory — bonds trigger what you thought you left.",
        ("Leo", 1): "pride sits on the face — confidence builds slow through body and public self, not performance alone.",
        ("Leo", 5): "creative ego taxed — pleasure and recognition cost until validation is internal.",
        ("Virgo", 6): "worry becomes physical — health and labor demand systems; late decisions tax the body.",
        ("Virgo", 10): "public rise through proof — career delayed until competence outlasts anxiety.",
        ("Libra", 7): "partnership lifts you — contracts and bonds can rise faster than peers if purpose leads charm.",
        ("Libra", 11): "network as throne — allies and hierarchy favor you when utility beats vanity.",
        ("Scorpio", 8): "deadly focus — taboo, shared money, and covert enemies become a strategist's war college.",
        ("Scorpio", 12): "shadow behind the veil — spiritual and hidden opposition strike before you see them.",
        ("Sagittarius", 9): "belief and travel punish inconclusive freedom — philosophy demands follow-through.",
        ("Sagittarius", 11): "social reach taxed — network power crushes when spent without business conclusion.",
        ("Capricorn", 4): "conservative roots press the home — leave respectfully; think outside the family box to grow.",
        ("Capricorn", 10): "slow crown — prestige arrives late because rigidity must melt first.",
        ("Aquarius", 10): "career through invention — public path rises when unconventional thinking gets structure.",
        ("Aquarius", 11): "allies reward disruption — network gains when routine serves purpose, not rebellion alone.",
        ("Pisces", 7): "bonds teach through fluidity — relationships demand adaptation; rigidity drowns.",
        ("Pisces", 12): "loss behind the curtain — isolation instructs when you adapt instead of staying in the wound.",
    }
    if keyed in specific:
        return specific[keyed]

    field = HOUSE_DEBT.get(house, "this life area")
    style = SIGN_MANIFEST_STYLE.get(sign, "through karmic pressure")
    ord_label = HOUSE_ORDINAL.get(house, str(house))
    return (
        f"in the {ord_label} house ({field}), Saturn in {sign} manifests {style} — "
        f"the sign colors how the debt hits; the house names where it hits."
    )


def _integrated_insight(sign: str, house: int | None, house_sign: str | None) -> dict[str, str]:
    ord_label = HOUSE_ORDINAL.get(house, "—") if house else "—"
    hz = f" ({house_sign})" if house_sign and house else ""

    house_line = (
        f"The {ord_label} house is where the debt lands — {HOUSE_DEBT.get(house, 'life terrain')}."
        if house
        else "House placement unknown — debt lane is blurred."
    )
    lesson = SIGN_LESSON.get(sign, "karmic curriculum through this sign").rstrip(".")
    sign_line = f"Saturn in {sign} is what Saturn teaches — {lesson}."
    zodiac_line = (
        f"How {sign} plays in: {_zodiac_in_house(sign, house)}"
    )

    body = (
        f"Saturn in {sign}, {ord_label} house{hz}. After numerology, this is your heaviest karmic weight. "
        f"{house_line} {sign_line} {zodiac_line} "
        f"Saturn is equal and opposite — beat the lesson and it builds; dodge it and the boot stays."
    )

    return {
        "house_debt": house_line,
        "sign_lesson": sign_line,
        "zodiac_manifestation": zodiac_line,
        "insight": body,
    }


def _teaser(sign: str, house: int | None) -> str:
    ord_label = HOUSE_ORDINAL.get(house, "—") if house else "—"
    return f"Karmic Debt Insight · Saturn in {sign} in the {ord_label} house"


def _actions(sign: str, house: int | None) -> list[str]:
    steps: list[str] = []
    if house == 1:
        steps.append("Train the body slow — physical exertion is the karmic gate.")
    elif house == 2:
        steps.append("Prove competence on one thing you doubt you deserve.")
    elif house == 3:
        steps.append("Navigate authority with strategy — reflex rebellion loses.")
    elif house == 4:
        steps.append("Honor elders while forging your own path — leave if home shrinks you.")
    elif house == 6:
        steps.append("Systematize health and income — Saturn punishes shortcuts here.")
    elif house == 7:
        steps.append("Hold integrity in one bond — remain yourself even if trust broke.")
    elif house in (8, 12) or sign == "Scorpio":
        steps.append("Close one hidden exposure — legal, financial, or relational.")
    elif house == 10:
        steps.append("Place one long-horizon career brick — prestige is slow-built.")
    elif house == 12:
        steps.append("Name one loss as lesson, extract the rule, release the story.")
    elif sign == "Sagittarius":
        steps.append("Finish one open loop before you spend new freedom.")
    elif sign == "Libra":
        steps.append("Use social luck with purpose — rise without aim wastes exaltation.")
    else:
        steps.append("Walk the Saturn lesson today — pressure becomes build when met.")

    if house and len(steps) < 2:
        steps.append(
            f"Read the {HOUSE_ORDINAL.get(house, house)} house as the lane; "
            f"{sign} is how the debt moves inside it."
        )
    return steps[:2]


def build_saturn_karma_insight(
    imprint: dict[str, Any],
    *,
    user_life_path: int | None = None,
) -> dict[str, Any]:
    vedic = imprint.get("vedic", {})
    sat = (vedic.get("planets") or {}).get("Saturn") or {}
    sign = sat.get("sign") or "—"
    house, house_sign = _saturn_house(imprint)
    ord_label = HOUSE_ORDINAL.get(house, str(house)) if house else "—"

    layers = _integrated_insight(sign, house, house_sign)
    numerology_note = ""
    if user_life_path is not None:
        tune = LP_KARMA_TUNE.get(user_life_path, "your life-path rhythm")
        numerology_note = (
            f"Numerology leads — life path {user_life_path} calls {tune}. "
            f"That is the tune; Saturn in {sign} is how the debt plays in the {ord_label} house."
        )

    return {
        "system": "vedic_sidereal",
        "sign": sign,
        "house": house,
        "house_sign": house_sign,
        "modal_title": "Your karmic debt insight",
        "tab_label": _teaser(sign, house),
        "placement_label": f"Saturn in {sign} · {ord_label} house",
        "house_debt": layers["house_debt"],
        "sign_lesson": layers["sign_lesson"],
        "zodiac_manifestation": layers["zodiac_manifestation"],
        "insight": layers["insight"],
        "numerology_karma_note": numerology_note,
        "actions": _actions(sign, house),
        "weight": "heavy" if sign in ("Scorpio",) or house in (8, 12) else "standard",
    }