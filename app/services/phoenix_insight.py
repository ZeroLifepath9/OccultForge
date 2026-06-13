"""
Occult Forge insight format — every placement gets plain meaning and lived manifestation.
Matches Phoenix Oracle depth: user should not need to look up jargon.
"""

from __future__ import annotations

from typing import Any

from app.services.babylon_premium import (
    CAREER_BY_PATH,
    DASHA_CAREER,
    build_career_premium,
    build_enemies_premium,
    build_numerology_premium,
)
from app.services.babylon_lore import (
    CHALDEAN_DIGIT,
    DASHA_SEASON,
    NAKSHATRA_SCRIPT,
    SIGN_CHALDEAN_BRIDGE,
    SIGN_NUMBER,
)
from app.services.imprint_labels import numerology_display
from app.services.numerology_depth import (
    PATH_ALIGNED,
    PATH_ALLIES,
    PATH_CONS,
    PATH_MISALIGNED,
    PATH_PROS,
    compound_star_angel_lore,
)
from app.services.overview_lore import (
    ANIMAL_INHERITANCE,
    COMPOUND_PRESSURE,
    DAY_MASTER_WEALTH,
    EXPRESSION_OCCULT,
    HOUSE_2_WALK,
    HOUSE_7_WALK,
    HOUSE_10_WALK,
    LIFE_PATH_MEANING,
    LIFE_PATH_TRIAL,
    LIFE_PATH_TRIUMPH,
    WESTERN_SIGN_ELEMENT,
    build_compound_reflects,
)

SEAL_MARKER = "walk this path"
OVERVIEW_FORMAT = "project-insight"
FORMAT_MARKER = "What this means for you"

PLANET_ROLES: dict[str, str] = {
    "Mercury": "how you think, sell, and lie — speech as weapon or wound",
    "Venus": "what you want, who you attract, what you price too cheap",
    "Mars": "where you fight, fuck, or flee — anger as fuel or arson",
    "Jupiter": "where luck expands — belief, law, teachers, excess",
    "Saturn": "where time taxes you — delay, spine, father-wound, mastery",
    "Uranus": "where you bolt — rupture, tech, exile, sudden freedom",
    "Neptune": "where you dissolve — glamour, addiction, mystic fog",
    "Pluto": "where you die and reforge — power, obsession, phoenix gate",
}

SIGN_MEANS: dict[str, str] = {
    "Aries": "You are built to initiate — first through the door, first to name the fight. Patience feels like death; waiting is not your religion.",
    "Taurus": "You are built to hold value — money, body, reputation accrue slow. You will outlast sprinters; your tax is stubbornness when the world has already moved.",
    "Gemini": "You are built to broker information — two minds, many channels. Scatter is your enemy; focus is your wealth.",
    "Cancer": "You are built to protect and belong — home, lineage, mood as policy. Shell is armor; softness is strategy when chosen consciously.",
    "Leo": "You are built to be seen — radiance is duty, not vanity alone. Invisibility reads as insult; the stage is where you remember who you are.",
    "Virgo": "You are built to refine — lists, craft, service as priestwork. Perfection can sterilize joy; ship anyway.",
    "Libra": "You are built to weigh — beauty, treaty, fair exchange. Avoidance of hard verdicts is how you lose power.",
    "Scorpio": "You are built to transform — depth, leverage, death-and-rebirth as craft. Surface life bores you; betrayal is remembered.",
    "Sagittarius": "You are built to preach and roam — truth must become product or you exile yourself in dogma.",
    "Capricorn": "You are built to climb institutions — delay as weapon, spine as brand. Youth may feel late; old age feels crowned.",
    "Aquarius": "You are built for the future-tribe — networks, odd contracts, reform. Isolation follows when the herd cannot keep pace.",
    "Pisces": "You are built to dissolve boundaries — art, mercy, spirit in matter. Without edges you drown in other people's weather.",
}

DM_ELEMENT_NEEDS: dict[str, str] = {
    "Wood": "Your day constitution needs growth and ethical expansion — prune dead wood or wealth rots.",
    "Fire": "Your day constitution needs visibility and courage — Fire feeds your purse; hiding taxes the brand.",
    "Earth": "Your day constitution needs patience and tangible assets — hoard without rotation breeds decay.",
    "Metal": "Your day constitution needs contracts, edge, and precision — blunt force loses your game.",
    "Water": "Your day constitution needs timing and flow — fight the current and everything costs double.",
}


def _block(
    title: str,
    chart_shows: str,
    means: str,
    life: str,
    *,
    cost: str = "",
    fire: str = "",
) -> str:
    lines = [
        f"## {title}",
        f"**Your chart shows:** {chart_shows}",
        f"**What this means for you:** {means}",
        f"**How this shows up in your life:** {life}",
    ]
    if cost:
        lines.append(f"**The cost if you ignore it:** {cost}")
    if fire:
        lines.append(f"**The fire if you obey it:** {fire}")
    return "\n\n".join(lines)


def _planet_line(name: str, body: dict[str, Any]) -> str:
    sign = body.get("sign", "—")
    deg = body.get("degree", "")
    d = f"{deg}°" if deg != "" else ""
    return f"{name} in {sign} {d}".strip()


def _derive_archetype(facts: dict[str, Any], name: str) -> str:
    lp = facts["life_path"]["value"]
    dm = facts["day_master"]
    pluto = (facts.get("western_planets") or {}).get("Pluto", {})
    pluto_sign = pluto.get("sign", "")
    tags = []
    if pluto_sign == "Scorpio" or lp == 9:
        tags.append("Phoenix Forger")
    if lp in (11, 22, 33):
        tags.append("Master Voltage")
    if dm["element"] == "Metal":
        tags.append("Blade of Verdict")
    elif dm["element"] == "Fire":
        tags.append("Torch Bearer")
    if not tags:
        tags.append("Sovereign Seeker")
    return f"{name} — {' · '.join(tags)}"


def build_invocation(facts: dict[str, Any], name: str) -> str:
    arch = _derive_archetype(facts, name)
    birth = facts.get("birth") or {}
    place = birth.get("place", "")
    when = birth.get("datetime_local", "")
    return (
        f"# {arch}\n\n"
        f"**Unbreakable, listen.** The matrix is not punishing you — it is *inscribing* you. "
        f"This reading is the Occult Forge threshold seal: every symbol below is translated into "
        f"what it does to *your* body, *your* money, *your* name, and *your* road. "
        f"You do not need to look up what a compound or nakshatra 'means.' We tell you here.\n\n"
        f"**Sealed at:** {when} · {place}. "
        f"Emerald and gold on the anvil — the phoenix does not ask permission to burn."
    )


def build_numerology_insight(facts: dict[str, Any]) -> str:
    lp = facts["life_path"]
    c, f, disp = lp["compound"], lp["value"], lp["display"]
    ch = facts["chaldean"]
    expr = facts["expression"]
    soul = facts.get("soul_urge", {})
    pers = facts.get("personality", {})
    bday = facts["birthday_number"]
    py_bday = bday

    star = compound_star_angel_lore(c, f)
    f_mean = LIFE_PATH_MEANING.get(f, "an initiatory road")
    if "—" in f_mean:
        f_mean = f_mean.split("—", 1)[-1].strip()

    if c == f:
        compound_means = (
            f"Birth-date reduces to one gate: {disp}. {star} "
            f"There is no separate 'hidden' birth number — what you see is what you must become."
        )
        compound_life = (
            f"You will not get lasting peace by splitting public self from private vow. "
            f"Every crisis asks: are you living {f} or performing something safer?"
        )
    else:
        compound_means = (
            f"Your birth-date sums to compound **{c}** before it yields life path **{disp}**. "
            f"{star} {COMPOUND_PRESSURE.get(c, '')} "
            f"The compound is what your *body still performs* when tired — the final {f} is what your *soul came to become*."
        )
        compound_life = (
            f"You will feel {c} in spending, quitting, seducing, or raging — then preach {f} on Sunday. "
            f"That hypocrisy is the compound winning. Ascent begins when daily choices starve {c}."
        )

    path_means = (
        f"Life path **{f}** ({disp}): {f_mean} "
        f"Gift when owned: {PATH_PROS.get(f, '')} "
        f"Price when refused: {PATH_CONS.get(f, '')}"
    )
    path_life = (
        f"Aligned: {PATH_ALIGNED.get(f, '')} "
        f"Misaligned: {PATH_MISALIGNED.get(f, '')} "
        f"On the ground this feels like: {LIFE_PATH_TRIAL.get(f, '')} "
        f"Integration feels like: {LIFE_PATH_TRIUMPH.get(f, '')}"
    )

    premium_num = build_numerology_premium(facts)
    blocks = [
        _block(
            "The Number Covenant — Compound & Life Path",
            f"Life path {disp} (compound {c} → final {f}). {build_compound_reflects(facts)}",
            compound_means + " " + premium_num,
            compound_life,
            cost=f"Performing {c} while claiming {f} — exhaustion, scandal, or savior fatigue until the compound is starved.",
            fire=f"Live {f} until {c} quiets — fate stops arguing and starts following.",
        ),
        _block(
            f"The Life Path Road — {f}",
            path_means,
            f"Your decade-scale assignment is path {f}. This is not a hobby spirituality number.",
            path_life,
            cost=PATH_MISALIGNED.get(f, ""),
            fire=PATH_ALIGNED.get(f, ""),
        ),
    ]

    blocks.append(
        _block(
            "Birth Day Pulse",
            f"Pythagorean birthday {py_bday['display']}; Chaldean day {numerology_display(ch['birthday'])}.",
            f"Day-of-month is your daily rhythm under the life path. "
            f"{CHALDEAN_DIGIT.get(ch['birthday']['value'], '')}",
            "This shows up in how you behave on ordinary Tuesdays — not only in big initiations.",
        )
    )

    if expr.get("display"):
        blocks.append(
            _block(
                "Name Field — How the World Contracts You",
                f"Expression {expr['display']}; Chaldean name {numerology_display(ch['expression'])}.",
                EXPRESSION_OCCULT.get(expr["value"], "Your public name carries a frequency markets hear."),
                "Contracts, introductions, and search results read this number before they read your heart.",
                cost="Name and path at war — fame without root, or gift without audience.",
                fire="Name and path rhyme — speech becomes income and authority.",
            )
        )

    if soul.get("display"):
        blocks.append(
            _block(
                "Soul Urge — Private Appetite",
                f"Soul urge {soul['display']}.",
                "What you chase when no one is watching — the real bribe you accept.",
                "Alone you become honest or dangerous depending on alignment.",
            )
        )

    blocks.append(
        _block(
            "Ally & Enemy Numbers",
            PATH_ALLIES.get(f, "Consult your path field."),
            "Friendly numbers amplify your vow; enemy-field numbers invoice your path with chaos.",
            "Partners, dates, addresses, and deal numbers in enemy fields cost more than they pay.",
            cost="Signing contracts on enemy-field dates — three cycles to unwind.",
            fire="Scheduling launches on friendly-field numbers — luck feels like discipline.",
        )
    )

    return "\n\n".join(blocks)


def build_western_insight(facts: dict[str, Any]) -> str:
    planets = facts.get("western_planets") or {}
    sun = facts["sun_sign"]
    moon = facts["moon"]["western_sign"]
    asc = facts["ascendant"]["western_sign"]
    sun_body = planets.get("Sun", {})
    moon_body = planets.get("Moon", {})
    asc_body = facts.get("western_angles", {}).get("ascendant", {})

    lines = []
    if sun_body:
        lines.append(_planet_line("Sun", sun_body))
    lines.append(f"Moon in {moon}")
    lines.append(f"Ascendant {asc}")
    for pname in ("Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"):
        if pname in planets and pname not in ("Sun",):
            lines.append(_planet_line(pname, planets[pname]))

    chart = "; ".join(lines)
    sun_means = SIGN_MEANS.get(sun, "Solar will shapes identity.")
    moon_means = SIGN_MEANS.get(moon, "Private emotional story.")
    asc_means = SIGN_MEANS.get(asc, "Social mask at the door.")

    pluto = planets.get("Pluto", {})
    pluto_bit = ""
    if pluto:
        pluto_bit = (
            f" Pluto in {pluto.get('sign', '')} {pluto.get('degree', '')}° — "
            f"phoenix death-and-rebirth; what shatters you is meant to be reforged, not buried."
        )
    sun_el = WESTERN_SIGN_ELEMENT.get(sun, "")

    blocks = [
        _block(
            "Western Sky — Will, Mask, and Phoenix Metals",
            chart + pluto_bit,
            f"Sun ({sun_el}): {sun_means} Moon ({moon}): {moon_means} Ascendant ({asc}): {asc_means} "
            f"When mask and will differ, the room meets {asc} before it honors {sun}.",
            f"You are judged at the gate, promoted by the Sun. Planets near the ascendant "
            f"mean speech, desire, and fight enter the room with you — not later.",
            cost=f"Performing only {asc} while starving {sun} — feels fake even when sincere.",
            fire=f"Let {sun} lead and {asc} serve — coherence reads as power.",
        )
    ]
    for pname in ("Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"):
        body = planets.get(pname)
        if not body:
            continue
        sign = body.get("sign", "—")
        deg = body.get("degree", "")
        role = PLANET_ROLES.get(pname, "a secondary voice in the wheel")
        sign_mean = SIGN_MEANS.get(sign, "this sign colors the planet's appetite")
        blocks.append(
            _block(
                f"{pname} — {role.split('—')[0].strip()}",
                _planet_line(pname, body),
                f"{pname} in {sign} means: {sign_mean} In plain terms: {role}",
                f"This shows up when {pname.lower()} themes dominate a season — contracts, lovers, fights, "
                f"expansion, delays, shocks, fog, or rebirth depending on the planet.",
            )
        )
    return "\n\n".join(blocks)


def build_vedic_insight(facts: dict[str, Any]) -> str:
    asc = facts["ascendant"]["vedic_lagna"]
    moon = facts["moon"]
    h2, h7, h10 = facts["vedic_house_2"], facts["vedic_house_7"], facts["vedic_house_10"]
    dasha = (facts.get("mahadasha") or {}).get("lord", "")
    p2 = ", ".join(h2["planets"]) or "none"
    p10 = ", ".join(h10["planets"]) or "none"

    return _block(
        "Vedic Sidereal Court — Older Scripture",
        f"Lagna {asc}; Moon {moon['sidereal_sign']} / {moon['nakshatra']} pada {moon.get('nakshatra_pada')}; "
        f"2nd {h2['sign']} ({p2}); 7th {h7['sign']}; 10th {h10['sign']} ({p10}); Maha {dasha}.",
        f"Lagna is the body-chart — {SIGN_MEANS.get(asc, 'body-law')}. "
        f"Nakshatra {moon['nakshatra']}: {NAKSHATRA_SCRIPT.get(moon['nakshatra'], 'lunar appetite')}. "
        f"Sidereal Moon is true hunger; tropical {moon['western_sign']} is the story you tell friends. "
        f"Maha {dasha}: {DASHA_CAREER.get(dasha, DASHA_SEASON.get(dasha, ''))}.",
        f"Money obeys 2nd-house {h2['sign']} rhythm — {HOUSE_2_WALK.get(h2['sign'], '')}. "
        f"Partners and open enemies: 7th {h7['sign']} — {HOUSE_7_WALK.get(h7['sign'], '')}. "
        f"Public name: 10th {h10['sign']} — {HOUSE_10_WALK.get(h10['sign'], '')}.",
        cost="Ignoring lagna for ascendant mask — health and vocation follow the wrong script.",
        fire="Feed the 2nd and 10th honestly — crown and purse rise together.",
    )


def build_bazi_insight(facts: dict[str, Any], imprint: dict[str, Any] | None = None) -> str:
    p = facts["pillars"]
    y, m, d, h = p["year"], p["month"], p["day"], p["hour"]
    dm = facts["day_master"]
    yz = facts["year_zodiac"]
    inherit = ANIMAL_INHERITANCE.get(yz["animal"], "ancestral weather")
    lens_clause = ""
    if imprint:
        from app.services.bazi_enrich import ensure_bazi_canonical

        lens = ensure_bazi_canonical(imprint).get("bazi", {}).get("interpretation_lens") or {}
        balance = (lens.get("balance") or {}).get("balance_insight", "")
        day_hook = (lens.get("pillars") or {}).get("day", {}).get("advice_hook", "")
        if balance:
            lens_clause = f" {balance}"
        if day_hook:
            lens_clause += f" Day layer: {day_hook}"

    return _block(
        "Four Gates — BaZi Fate",
        f"Year {y['gan_zhi']} ({y['stem_element']} {y['branch_animal']}); Month {m['gan_zhi']}; "
        f"Day {d['gan_zhi']} ({dm['english']} {dm['yin_yang']} {dm['element']}); Hour {h['gan_zhi']}.",
        f"Year is bloodline myth — {inherit} NOT your sovereign self. "
        f"Month {m['stem_element']} seasons your working years. "
        f"Day is the blade — {dm['english']} {dm['element']}. {DM_ELEMENT_NEEDS.get(dm['element'], '')} "
        f"Hour is the private engine when no one watches.{lens_clause}",
        f"You will be cast as {yz['animal']} in public while living {d['branch_animal']} day — "
        f"wrong costume exhausts within three cycles.",
        cost=f"Calling yourself only the {yz['animal']} — others misread; you resent the mirror.",
        fire=f"Wield day {d['branch_animal']} blade openly — fate respects the sovereign gate.",
    )


def build_east_west_insight(facts: dict[str, Any]) -> str:
    sun = facts["sun_sign"]
    yz = facts["year_zodiac"]
    animal = yz["animal"]
    sun_n = facts.get("sun_sign_number") or SIGN_NUMBER.get(sun, 0)
    bridge = SIGN_CHALDEAN_BRIDGE.get(int(sun_n), "the zodiac seal on the will")
    sign_num = SIGN_NUMBER.get(sun, sun_n)

    return _block(
        "East Meets West — Year Animal vs Solar Sign",
        f"Year gate {yz.get('element', yz.get('stem_element', ''))} {animal} ({yz.get('gan_zhi', '')}); "
        f"Western Sun {sun} (sign-number {sign_num or sun_n}).",
        f"Public myth casts you as {animal} — inheritance, family story, first impression. "
        f"Solar {sun} is what you came to *do* in this life: {SIGN_MEANS.get(sun, '')} "
        f"Chaldean bridge on the Sun: {bridge}. "
        f"When {animal} costume and {sun} will disagree, you feel 'misread' — that is the costume winning.",
        f"You will be offered roles that praise the {animal} while starving the {sun}. "
        f"Promotion comes when you let the Sun lead and let the year animal be backdrop, not identity.",
        cost=f"Living only as {animal} — wrong contracts, wrong lovers, wrong decade.",
        fire=f"Name the Sun first, animal second — the matrix stops fighting you in the mirror.",
    )


def build_synthesis_insight(facts: dict[str, Any]) -> str:
    sun = facts["sun_sign"]
    dm = facts["day_master"]
    c = facts["life_path"]["compound"]
    f = facts["life_path"]["value"]
    disp = facts["life_path"]["display"]

    war = ""
    if c != f:
        war = f"Compound {c} vs path {disp} is the central war — body performs {c}, soul sworn to {f}. "

    return _block(
        "Where All Systems Meet",
        f"Path {disp}; {dm['yin_yang']} {dm['element']} day; Sun {sun}; sidereal Moon {facts['moon']['sidereal_sign']}.",
        war
        + f"East year {facts['year_zodiac']['animal']} + West {sun} + numbers {disp} — "
        f"when they agree, you are dangerous in the best sense; when they war, you feel 'misunderstood.' "
        f"That feeling is the war, not the people.",
        "Synchronicity: name-number, Sun sign-number, and path must be reconciled or every win feels stolen.",
    )


def build_career_insight(facts: dict[str, Any]) -> str:
    f = facts["life_path"]["value"]
    raw = build_career_premium(facts)
    return _block(
        "Career, Crown & Wealth",
        f"Life path {f}; day master {facts['day_master']['element']}; Vedic 2nd/10th; Maha lord.",
        raw,
        CAREER_BY_PATH.get(f, "") + " " + DAY_MASTER_WEALTH.get(facts["day_master"]["element"], ""),
        cost="Earning against your day element — 2nd-house rhythm starves you within two cycles.",
        fire="Earn as day element, bank in 2nd-house rhythm — crown and purse rise together.",
    )


def build_enemies_insight(facts: dict[str, Any]) -> str:
    raw = build_enemies_premium(facts)
    f = facts["life_path"]["value"]
    return _block(
        "Enemies, Clash Animals & Protection",
        f"Life path {f}; Sun {facts['sun_sign']}; year {facts['year_zodiac']['animal']}; "
        f"day branch {facts.get('day_pillar', {}).get('branch_animal', '—')}.",
        raw,
        "Enemy numbers, opposite signs, and 冲 clash years drain you when you treat them as neutral charm.",
        cost="Partners in enemy-field or clash animal — breakage, scandal, or body-tax, not mystery.",
        fire="Friendly numbers and aligned seasons — luck feels like discipline you earned.",
    )


def build_road_insight(facts: dict[str, Any]) -> str:
    f = facts["life_path"]["value"]
    disp = facts["life_path"]["display"]
    dm = facts["day_master"]

    steps = [
        f"Live path {disp} daily — starve compound habits if split.",
        f"Work as {dm['yin_yang']} {dm['element']} — refuse wrong-element careers.",
        f"{PATH_ALIGNED.get(f, 'Walk aligned.')}",
        f"Avoid: {PATH_MISALIGNED.get(f, '')}",
        "Schedule important moves on friendly numbers; treat enemy-field dates as high risk.",
    ]

    rituals = [
        f"Dawn offering to your day element ({dm['element']}) — five minutes naming one cut you will make today.",
        f"Before contracts: speak your life path number ({f}) once; do not sign in enemy-field timing if avoidable.",
    ]

    return (
        _block(
            "The Road Commanded",
            f"Path {disp}; blade {dm['element']}.",
            f"{' '.join(steps)}",
            f"Trial on foot: {LIFE_PATH_TRIAL.get(f, '')} Integration: {LIFE_PATH_TRIUMPH.get(f, '')}",
            cost=LIFE_PATH_TRIAL.get(f, ""),
            fire=LIFE_PATH_TRIUMPH.get(f, ""),
        )
        + "\n\n## Do This Now\n\n"
        + "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))
        + "\n\n## Rituals Tied to Your Chart\n\n"
        + "\n".join(f"- {r}" for r in rituals)
    )


def build_close(name: str, *, ai_available: bool) -> str:
    ai_note = (
        "Seeker unlocks hour-by-hour Phoenix decoding with Zero."
        if ai_available
        else "Configure XAI_API_KEY in backend/.env and Refresh — the Oracle voice layers on this template."
    )
    return (
        f"\n\n---\n\n**{name}**, the threshold seal is complete. {ai_note} "
        f"**walk this path** — the inscription precedes you; your job is to live it in the open."
    )


def build_phoenix_insight(
    facts: dict[str, Any],
    name: str,
    *,
    ai_available: bool = False,
) -> str:
    """Full interpreted reading — Occult Forge project format."""
    sections = [
        build_invocation(facts, name),
        build_numerology_insight(facts),
        build_western_insight(facts),
        build_east_west_insight(facts),
        build_vedic_insight(facts),
        build_bazi_insight(facts),
        build_synthesis_insight(facts),
        build_career_insight(facts),
        build_enemies_insight(facts),
        build_road_insight(facts),
        build_close(name, ai_available=ai_available),
    ]
    return "\n\n".join(sections)


def build_zero_seal(facts: dict[str, Any], name: str, **kwargs: Any) -> str:
    return build_phoenix_insight(facts, name, ai_available=kwargs.get("ai_available", False))