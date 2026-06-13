"""
Eastern Rising — pure BaZi + Vedic/Jyotish forge read.
Battle-tested brother voice; no Western, numerology, or raw pillar recitation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.services.bazi_enrich import ensure_bazi_canonical
from app.services.imprint_labels import branch_animal
from app.services.interpretations.matrix_decoder_voice import format_matrix_reading
from app.services.interpretations.vedic_house_sign_engine import interpret_house_sign, interpret_lagna

_ELEMENT_RHYTHM: dict[str, str] = {
    "Wood": "You grow in bursts — plant, stretch, prune, repeat. Peaks when one living project gets your full spine; valleys when you scatter seed everywhere.",
    "Fire": "You run hot then need ash time. Peaks when you ship while the flame is honest; valleys when you perform brightness with nothing behind it.",
    "Earth": "You build slow and mean it. Peaks when brick-by-brick work compounds; valleys when you rush a foundation to look finished.",
    "Metal": "You cut, refine, and hold the line. Peaks when standards protect the mission; valleys when perfection becomes a cage.",
    "Water": "You read depth others miss. Peaks when you research then move once; valleys when you drift on mood instead of rhythm.",
}

_STEM_CORE: dict[str, str] = {
    "Jia": "Yang Wood — the starter who breaks ground and pushes through resistance",
    "Yi": "Yin Wood — the connector who bends, adapts, and grows through people",
    "Bing": "Yang Fire — the broadcaster who needs honest visibility to stay fueled",
    "Ding": "Yin Fire — the focused crafter who wins in sharp, small intense bursts",
    "Wu": "Yang Earth — the mountain backbone who endures and holds the line",
    "Ji": "Yin Earth — the soil that receives, stores, and ripens until work is actually done",
    "Geng": "Yang Metal — the blade that decides fast, cuts clean, and finishes with clarity",
    "Xin": "Yin Metal — the jeweler who refines detail, taste, and inward standards",
    "Ren": "Yang Water — the river that wins on timing, scope, and wide movement",
    "Gui": "Yin Water — the intuitive reader who feels the room before the facts land",
}

_STEM_FORGE: dict[str, str] = {
    "Jia": "start one real project and push it through first resistance — prune a dead branch if the canopy is crowded",
    "Yi": "connect two people or ideas that help one living project breathe — adapt, don't force",
    "Bing": "ship one visible proof while the heat is honest — hiding taxes your income and nerve",
    "Ding": "finish one tight craft task in a single focused burst — one sharp offer, fully done",
    "Wu": "hold one boundary or foundation line that should not move — outlast the noise around it",
    "Ji": "land one practical foundation — budget line, meal rhythm, shelter fix, or process that ripens slow and holds",
    "Geng": "make one clean cut — boundary, ending, or decision — and close the loop the same day",
    "Xin": "polish one detail standard until it is shippable — perfection only counts if it leaves your hands",
    "Ren": "move one network or timing play with scope — ride current, skip fighting the whole river",
    "Gui": "take one quiet read of mood and data before you answer the room — boundaries before absorption",
}

_BRANCH_DAY: dict[str, dict[str, str]] = {
    "Rat": {
        "lens": "quick mind and survival smarts",
        "sovereignty": "Freedom means staying ahead of problems — you feel sovereign when you have options, cash buffer, and an exit plan.",
        "grind": "Weekdays win when you batch errands and decisions early; scatter late and leaks show up in money and mood.",
    },
    "Ox": {
        "lens": "slow endurance and physical follow-through",
        "sovereignty": "Freedom is pace you own — you feel sovereign when nobody can rush you off a job half-done.",
        "grind": "Treat the weekday list like heavy labor with a finish time; outlast beats dramatize every time.",
    },
    "Tiger": {
        "lens": "bold initiative and clean breaks",
        "sovereignty": "Freedom is room to move first — you feel caged when committees slow a necessary cut.",
        "grind": "Win the day by making one brave move early; waiting for permission drains your best hours.",
    },
    "Rabbit": {
        "lens": "tact, timing, and soft navigation",
        "sovereignty": "Freedom is peace with teeth — you need calm space, but ambiguity in deals feels like a trap.",
        "grind": "Schedule gentle pace with hard deadlines; niceness without a due date turns into unpaid labor.",
    },
    "Dragon": {
        "lens": "visible chapter energy and pride in the plot",
        "sovereignty": "Freedom is naming the direction — you feel sovereign when the story is yours, not borrowed.",
        "grind": "Ship one chapter-ending move per day; performing the legend without a finish line burns you.",
    },
    "Snake": {
        "lens": "strategic patience and depth reads",
        "sovereignty": "Freedom is information advantage — you feel sovereign when you see the play before the room does.",
        "grind": "Research first, act second, but set a decision clock; endless watch mode becomes avoidance.",
    },
    "Horse": {
        "lens": "motion, independence, and open road",
        "sovereignty": "Freedom is movement with purpose — cages, micromanagers, and stalled projects hit you first.",
        "grind": "Book movement into the day like appointments; idle Horse energy turns restless and expensive.",
    },
    "Goat": {
        "lens": "cooperative craft and aesthetic peace",
        "sovereignty": "Freedom is beauty with fair terms — harmony matters, but vague agreements poison the well.",
        "grind": "Pair kindness with written scope; creative peace needs borders to survive weekdays.",
    },
    "Monkey": {
        "lens": "clever fixes and improvised solutions",
        "sovereignty": "Freedom is mental agility — you feel trapped when rules are dumb and you cannot hack a path.",
        "grind": "Channel wit into one solved problem daily; twelve jokes and zero finishes leak power.",
    },
    "Rooster": {
        "lens": "precision, audit, and clean standards",
        "sovereignty": "Freedom is precision — chaos feels like chains; clean schedules and finished details feel like room to breathe.",
        "grind": "you win; wing it and repeat fixes leak here first.",
    },
    "Dog": {
        "lens": "loyalty, guard duty, and fair protection",
        "sovereignty": "Freedom is trusted duty — you feel sovereign guarding something real, not performing for strangers.",
        "grind": "Protect one mission and one roster per day; scattered loyalty turns into burnout and bitterness.",
    },
    "Pig": {
        "lens": "generous appetite and full-table energy",
        "sovereignty": "Freedom is honest enjoyment with limits — feast or famine extremes tax the long game.",
        "grind": "Feed the day with one scheduled pleasure and one scheduled bill — balance keeps appetite from becoming debt.",
    },
}

_BRANCH_HOUR: dict[str, dict[str, str]] = {
    "Rat": {"engine": "the night strategist", "craft": "planning, option maps, and quiet deal math", "protect": "sleep, mental quiet, and unfollowed curiosity spend"},
    "Ox": {"engine": "the slow rebuild tank", "craft": "body recovery, meal prep, and physical order", "protect": "rest, joints, and unhurried completion time"},
    "Tiger": {"engine": "the dawn charge", "craft": "solo training, bold prep, and pre-dawn focus blocks", "protect": "adrenal recovery and space to cool down after a fight"},
    "Rabbit": {"engine": "the soft landing", "craft": "home order, comfort craft, and nervous-system repair", "protect": "quiet home, gentle evenings, and drama-free wind-down"},
    "Dragon": {"engine": "the legend workshop", "craft": "big-vision drafting and private pride projects", "protect": "creative solitude and ego recovery after public heat"},
    "Snake": {"engine": "the depth chamber", "craft": "research, pattern reads, and strategic notes", "protect": "uninterrupted think time and secrets kept until ripe"},
    "Horse": {"engine": "the open-road refill", "craft": "travel thinking, movement, and independence resets", "protect": "physical roam time and escape from micromanagement"},
    "Goat": {"engine": "the beauty bench", "craft": "art, care, and cooperative craft in private", "protect": "aesthetic calm and emotional safety without obligation fog"},
    "Monkey": {"engine": "the tinkering bench", "craft": "experiments, fixes, and playful skill reps", "protect": "play space that is not judged and mental novelty without burnout"},
    "Rooster": {"engine": "the early auditor", "craft": "detail sorting, routine tightening, and closing loops", "protect": "sleep, clean routines, and the right to finish one task completely"},
    "Dog": {"engine": "the watch post", "craft": "loyalty logs, vetting people, and protective planning", "protect": "trusted inner circle time and off-duty from guard mode"},
    "Pig": {"engine": "the replenishment hearth", "craft": "cooking, comfort, and resource sharing in private", "protect": "full rest, honest pleasure, and budgets that prevent glutton debt"},
}

_NAKSHATRA_FORGE: dict[str, str] = {
    "Ashwini": "Move on the first honest instinct today — waiting for applause stalls your best starts.",
    "Bharani": "Name what is ending before you grab what is new — reinvention needs a closed door.",
    "Krittika": "Say the sharp truth once, cleanly — sugarcoating costs more than conflict here.",
    "Rohini": "Feed one cultivated appetite with real resource — comfort needs funding, not fantasy.",
    "Mrigashira": "Pick one search lane this week — endless hunting without a target drains bond and focus.",
    "Ardra": "Let weather clear before big promises — storm moods make expensive contracts.",
    "Punarvasu": "Give one second chance with written terms — light returns when scope is clear.",
    "Pushya": "Nourish home and one trusted ally — protection is action, not sentiment.",
    "Ashlesha": "Watch manipulation in self and others — name the coil before it tightens.",
    "Magha": "Honor legacy without borrowing crown weight — pride needs service behind it.",
    "Purva Phalguni": "Enjoyment is fine with a clock — pleasure without budget leaks future peace.",
    "Uttara Phalguni": "Say what loyalty and fair exchange look like in love and work — vague deals drain you.",
    "Hasta": "Use your hands on one skilled task — craft beats talk in your emotional ledger.",
    "Chitra": "Build one thing worth looking at — spectacle without structure fades fast.",
    "Swati": "Keep independence in contracts — cages disguised as love fail here first.",
    "Vishakha": "Choose one victory path — split ambition spends both altars.",
    "Anuradha": "Invest in one friendship like infrastructure — devotion needs reciprocity.",
    "Jyeshta": "Lead or defer clearly — seniority games without role clarity rot trust.",
    "Mula": "Uproot one dead root fully — half-endings fund repeat pain.",
    "Purva Ashadha": "Declare belief after one proof point — conviction without evidence is noise.",
    "Uttara Ashadha": "Public wins need private rehearsal — late triumph still needs prep.",
    "Shravana": "Listen first, advise second — fame here comes through counsel kept honest.",
    "Dhanishta": "Rhythm and resource in motion — stack income beats and keep the drum steady.",
    "Shatabhisha": "Heal in private before marketing recovery — isolation can be medicine if bounded.",
    "Purva Bhadrapada": "Intensity needs a container — penance without plan becomes self-harm.",
    "Uttara Bhadrapada": "Surrender what is done; keep boundaries on what is not — depth without drowning.",
    "Revati": "Finish the passage — mercy at the road's end means closure with care, not endless carry.",
}

_DASHA_PLAIN: dict[str, str] = {
    "Sun": "Current Vedic chapter highlights name and visibility — the room watches what you refuse to dim.",
    "Moon": "Current Vedic chapter highlights home and body — comfort is operating cost, not luxury.",
    "Mars": "Current Vedic chapter highlights fight and cuts — clean conflict beats slow resentment.",
    "Mercury": "Current Vedic chapter highlights messages and deals — paperwork is destiny work right now.",
    "Jupiter": "Current Vedic chapter highlights growth and teaching — measured risk has tailwind if honest.",
    "Venus": "Current Vedic chapter highlights bonds and money — charm still needs math.",
    "Saturn": "Current Vedic chapter highlights limits and contracts — shortcuts bill compound interest.",
    "Rahu": "Current Vedic chapter highlights hunger and disruption — appetite is not the same as mission.",
    "Ketu": "Current Vedic chapter highlights release — strip noise; less can be the power move.",
}

_GATE_CONTEXT: dict[str, str] = {
    "year": "Year gate — public inheritance: family cast, first impression, how strangers read you before you pick the script.",
    "month": "Month gate — working-years season: career pace, boss energy, adult-life scheduling from your 20s through your 50s.",
    "day": "Day gate — Monday-morning you: daily habits, grind, the self that shows up when nobody staged the scene.",
    "hour": "Hour gate — private fuel: inner engine, recovery, craft when the room clears out.",
}

_MONTH_STRUCTURE_ASK: dict[str, str] = {
    "Wood": "growth plans with room to stretch",
    "Fire": "visible output with honest heat behind it",
    "Earth": "schedules, foundations, and brick-by-brick structure",
    "Metal": "standards, contracts, and clean cuts",
    "Water": "research, timing, and depth before motion",
}

_BRANCH_DEFAULT_DAY = {
    "lens": "distinct daily rhythm",
    "sovereignty": "Freedom is a weekday rhythm you own — not mood, not performance.",
    "grind": "When the day is scheduled like payroll, you win; when it is vague, leaks hit first.",
}
_BRANCH_DEFAULT_HOUR = {
    "engine": "your private engine",
    "craft": "recovery and quiet skill work",
    "protect": "sleep, solitude, and unfinished inner business",
}


def _who(imprint: dict[str, Any]) -> str:
    birth = imprint.get("birth") or {}
    alias = (birth.get("commonly_known_as") or "").strip()
    return alias or birth.get("name") or birth.get("display_name") or "Seeker"


def _spoken_birth(facts: dict[str, Any]) -> str:
    raw = (facts.get("birth") or {}).get("datetime_local") or ""
    raw = raw.replace("Z", "")
    if not raw:
        return "your sealed birth moment"
    try:
        dt = datetime.fromisoformat(raw)
        hour = dt.strftime("%I").lstrip("0") or "12"
        minute = dt.strftime("%M")
        ampm = dt.strftime("%p")
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}, {hour}:{minute} {ampm}"
    except ValueError:
        return raw[:16].replace("T", " ")


def _birth_place(facts: dict[str, Any]) -> str:
    return (facts.get("birth") or {}).get("place") or ""


def _branch_day(animal: str) -> dict[str, str]:
    return _BRANCH_DAY.get(animal, _BRANCH_DEFAULT_DAY)


def _branch_hour(animal: str) -> dict[str, str]:
    return _BRANCH_HOUR.get(animal, _BRANCH_DEFAULT_HOUR)


def _simplify_hook(hook: str) -> str:
    text = (hook or "").strip()
    if "—" in text:
        text = text.split("—", 1)[-1].strip()
    return text or "this lane sets tone in daily outcomes"


def _plain_pillar_line(pillar_key: str, card: dict[str, Any]) -> str:
    context = _GATE_CONTEXT[pillar_key]
    animal = card.get("branch_animal", "")
    day_lens = _branch_day(animal) if animal else {}
    visible = card.get("visible_element", "")
    hook = _simplify_hook(card.get("advice_hook", "") or card.get("synergy_note", ""))
    lens = day_lens.get("lens", "distinct rhythm")
    inner = (card.get("hidden") or {}).get("element", "")
    inner_bit = ""
    if inner and inner != visible:
        inner_bit = (
            f" Underneath runs quieter {inner} — the feeling before you can explain it in words."
        )
    if pillar_key == "day" and day_lens:
        return (
            f"{context} Yours moves with {lens} and {visible} on top — "
            f"sovereignty feels like: {day_lens.get('sovereignty', '')} In practice: {hook}.{inner_bit}"
        )
    return (
        f"{context} Yours moves with {lens} energy and {visible} on top — in practice: {hook}.{inner_bit}"
    )


def _balance_alert(lens: dict[str, Any], dm_el: str) -> str | None:
    balance = (lens.get("balance") or {}).get("balance_insight", "")
    if not balance:
        return None
    low = balance.lower()
    if "light on" not in low and "watch for" not in low and "strong on" not in low:
        return None
    plain = balance.split("Day Master")[0].strip().rstrip(".").replace("藏干", "hidden energy")
    return (
        "Element balance — five fuel tanks in your chart. "
        f"{plain} When one tank runs low, life feels uphill by default — "
        f"feed the weak lane with real food, people, and work that match it."
    )


def _luck_influence_line(luck_lens: dict[str, Any]) -> str:
    intro = (
        "Luck pillar — ten-year life chapter over your birth gates; long arc for career, moves, and what the world hands you."
    )
    current = luck_lens.get("current") or {}
    if not current or current.get("is_minor_period"):
        return (
            f"{intro} Still in warm-up — build day and month gates; "
            "skip betting the whole mission before the chapter fully opens."
        )
    years_in = current.get("years_into_decade")
    years_left = current.get("years_remaining")
    citation = luck_lens.get("advice_citation", "")
    years_bit = f" Year {years_in} of this chapter." if years_in else ""
    left_bit = f" ~{years_left} years left — plan handoffs, not panic pivots." if years_left and years_left <= 5 else ""
    core = citation or f"Active chapter: {current.get('identity', 'this season')}."
    return f"{intro}{years_bit} {core}{left_bit}"


def _luck_direct_sentence(luck_lens: dict[str, Any]) -> str:
    current = luck_lens.get("current") or {}
    if not current or current.get("is_minor_period"):
        return "Luck pillar still warming — day and month gates carry most weight for now."
    identity = current.get("identity", "this decade")
    years_in = current.get("years_into_decade")
    bit = f", year {years_in}" if years_in else ""
    return f"Luck pillar runs {identity}{bit} — big moves land cleaner when they fit this chapter, not last one's costume."


def _forge_day_master(dm: dict[str, Any]) -> str:
    stem = dm["english"]
    core = _STEM_CORE.get(stem, f"{dm['yin_yang']} {dm['element']}")
    action = _STEM_FORGE.get(stem, f"land one {dm['element'].lower()} deliverable that compounds before you perform")
    return (
        f"Day Master — core is {core}. Finish one thing first: {action} — "
        f"then step into rooms that did not build it."
    )


def _forge_day_gate(day_an: str) -> str:
    b = _branch_day(day_an)
    return (
        f"Day gate — weekday sovereignty. {b['sovereignty']} "
        f"Grind rule: treat the weekday list like paychecks and bills — {b['grind']}"
    )


def _forge_hour_gate(hour_an: str) -> str:
    h = _branch_hour(hour_an)
    return (
        f"Hour gate — private engine: {h['engine']}. "
        f"This is where you recover and do {h['craft']}. "
        f"Protect {h['protect']} — public gates (year first-impression and month work-season pressure) "
        f"spend your hour-gate fuel if this tank is empty."
    )


def _forge_luck() -> str:
    return (
        "Luck pillar — this ten-year chapter is weather, not orders. Focus visible feats brick by brick; "
        "put in the work and commit to the grind — skip getting lost in twelve parallel fantasies."
    )


def _forge_nakshatra(nak: str) -> str:
    tip = _NAKSHATRA_FORGE.get(nak, "Name what you need emotionally before bodies negotiate — unspoken appetite becomes fight.")
    return f"Moon lane ({nak}) — {tip}" if nak else f"Moon lane — {tip}"


def _nakshatra_influence(nak: str) -> str:
    tip = _NAKSHATRA_FORGE.get(nak, "private emotional hunger moves before logic in bond.")
    return f"Moon emotional lane ({nak}) — how you feel in partnership before words catch up: {tip}"


def build_eastern_rising_reading(facts: dict[str, Any], imprint: dict[str, Any]) -> str:
    imp = ensure_bazi_canonical(imprint)
    who = _who(imprint)
    spoken = _spoken_birth(facts)
    place = _birth_place(facts)
    place_bit = f", {place}" if place else ""

    dm = facts["day_master"]
    el = dm["element"]
    stem = dm["english"]
    yz_an = facts["year_zodiac"]["animal"]
    day_an = facts.get("day_pillar", {}).get("branch_animal", "")
    hour_pillar = imp["bazi"]["pillars"]["hour"]
    hour_an = hour_pillar.get("branch_animal") or branch_animal(hour_pillar.get("branch", ""))
    if not day_an:
        day_an = branch_animal(facts.get("day_pillar", {}).get("branch_hanzi", "") or imp["bazi"]["pillars"]["day"].get("branch", ""))

    lens = imp["bazi"].get("interpretation_lens") or {}
    lens_pillars = lens.get("pillars") or {}
    luck_lens = lens.get("luck_pillar") or imp["bazi"].get("luck", {}).get("interpretation") or {}
    month_card = lens_pillars.get("month") or {}
    month_el = month_card.get("visible_element", "")

    lagna = facts.get("ascendant", {}).get("vedic_lagna", "")
    moon = facts.get("moon") or {}
    nak = moon.get("nakshatra", "")
    sid_moon = moon.get("sidereal_sign", "")
    dasha = facts.get("mahadasha") or {}
    lord = (dasha.get("lord") or "").strip()
    h7 = facts.get("vedic_house_7") or {}
    h10 = facts.get("vedic_house_10") or {}

    day_lens = _branch_day(day_an)
    year_lens = _branch_day(yz_an)
    rhythm = _ELEMENT_RHYTHM.get(el, _ELEMENT_RHYTHM["Earth"])
    stem_core = _STEM_CORE.get(stem, f"{dm['yin_yang']} {el}")

    year_day = (
        f"Year gate ({year_lens['lens']}) and day gate ({day_lens['lens']}) rhyme — charm and grind speak one language; "
        "main risk is hiding from your own volume."
        if yz_an == day_an
        else (
            f"Year gate ({year_lens['lens']}) meets the world fast; day gate ({day_lens['lens']}) finishes the work — "
            "schedule the grind or resentment follows."
        )
    )

    direct = (
        f"{who}, born {spoken}{place_bit} — Eastern imprint, straight talk. "
        f"Four gates stack life: year is public inheritance, month is work-season, day is weekday you, hour is private fuel. "
        f"Core: {stem_core}. {rhythm} {year_day} {_luck_direct_sentence(luck_lens)}"
    )

    influence_lines: list[str] = []
    for key in ("year", "month", "day", "hour"):
        card = lens_pillars.get(key) or {}
        if card:
            influence_lines.append(_plain_pillar_line(key, card))

    alert = _balance_alert(lens, el)
    if alert:
        influence_lines.append(alert)
    influence_lines.append(_luck_influence_line(luck_lens))

    if lagna:
        influence_lines.append(
            f"Rising body — how you enter rooms and hold stamina: {interpret_lagna(lagna)}"
        )
    if nak:
        influence_lines.append(_nakshatra_influence(nak))
    if sid_moon:
        influence_lines.append(
            f"Private Moon weather ({sid_moon}) — moods behind the face finance or drain bonds before logic kicks in."
        )
    if lord:
        influence_lines.append(_DASHA_PLAIN.get(lord, f"Current Vedic chapter: {lord} sets timing drum."))

    if h10.get("sign"):
        career = interpret_house_sign(10, h10["sign"])
        influence_lines.append(f"Career and legacy — how you are remembered: {career['weave']}")
    if h7.get("sign"):
        bond = interpret_house_sign(7, h7["sign"])
        influence_lines.append(f"Partnership and contracts — fair exchange in bond: {bond['weave']}")

    decoded = "\n".join(influence_lines)
    month_ask = _MONTH_STRUCTURE_ASK.get(month_el, "structure and honest pacing")

    steps = [
        _forge_day_master(dm),
        _forge_day_gate(day_an),
        _forge_hour_gate(hour_an),
        _forge_luck(),
        _forge_nakshatra(nak),
        (
            "Element balance — weekly check which fuel tank feels empty; "
            "feed it with real food, people, and tasks that match, not performance."
        ),
        (
            "Timing journal — once a month write what peaked, what drained, "
            "and what the same gate keeps asking until you answer it."
        ),
    ]

    avoids = [
        (
            f"Core drift — you run {stem_core}. Performing against that to impress a room that will not pay you "
            f"drains the forge — {_STEM_FORGE.get(stem, 'return to one honest deliverable')}."
        ),
        (
            f"Charm vs grind — year energy ({year_lens['lens']}) opens doors; day energy ({day_lens['lens']}) closes tasks. "
            "Letting first impression spend what weekday work has not earned taxes the mission."
        ),
        (
            "Wrong decade costume — each ten-year luck chapter has different homework. "
            "Last chapter's playbook in a new chapter replays the same stuck season."
        ),
        (
            "Body override — rising body is stamina truth before theory. "
            "Skipping sleep, food, or nervous-system signal for performance bills the flesh first."
        ),
        (
            f"Month gate avoidance — month gate runs career seasons; yours wants {month_ask}. "
            "Blaming bad luck for messy structure when the assignment was order replays the valley."
        ),
    ]

    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(steps[:7], 1))
    avoid_lines = "\n".join(f"- {a}" for a in avoids[:5])
    action = f"Forge now:\n{step_lines}\n\nWatch out:\n{avoid_lines}"

    return format_matrix_reading(direct, decoded, action)