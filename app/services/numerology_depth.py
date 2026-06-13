"""Occult numerology depth — compound, life path, allies, alignment."""

from __future__ import annotations

from typing import Any



PATH_PROS: dict[int, str] = {
    1: "sovereign initiative, clean breaks, destiny bends when you stand first",
    2: "diplomatic genius, emotional intelligence, peace as engineered outcome",
    3: "charisma, creative command, language that moves crowds and markets",
    4: "reliability, structural genius, wealth through sacred repetition",
    5: "adaptability, crossroads luck, truth-telling that unlocks doors",
    6: "healing presence, aesthetic authority, family systems you repair",
    7: "research mind, spiritual credit, counsel others pay for",
    8: "executive force, material mastery, legacy in institutions",
    9: "closure craft, mercy with teeth, wisdom that outlives you",
    11: "prophetic nerve, invention, voltage that builds if grounded",
    22: "cathedral thinking, civilizational touch, scale others fear",
    33: "compassion as discipline, teaching love without savior disease",
}

PATH_CONS: dict[int, str] = {
    1: "isolation, tyranny of self, burned bridges from pride",
    2: "codependency, passive aggression, decisions deferred until rot",
    3: "scandal, scattered talent, words that promise more than bone",
    4: "rigidity, joylessness, resentment of chaos you secretly need",
    5: "instability, addiction to motion, oaths broken for novelty",
    6: "control through care, moral debt, beauty used as leash",
    7: "loneliness, suspicion, knowledge hoarded until it poisons",
    8: "ruthlessness, gold without soul, empire that eats children",
    9: "melancholy, savior fatigue, endings refused until catastrophe",
    11: "nervous collapse, fantasy over form, channel without ground",
    22: "burden of vision, body fails blueprint, hubris of scale",
    33: "martyrdom, porous boundaries, love that invoices the world",
}

PATH_ALIGNED: dict[int, str] = {
    1: "you name the direction — health, respect, allies arrive as followers not masters",
    2: "you choose partnership consciously — harmony becomes infrastructure",
    3: "you speak on rhythm — fame serves message, not ego",
    4: "you honor slow build — compound interest in body and bank",
    5: "you tell truth before you move — freedom with a spine",
    6: "you serve beauty without controlling — home becomes temple",
    7: "you study then share — solitude fuels public clarity",
    8: "you lead with conscience — power feeds legacy",
    9: "you release cleanly — grief becomes wisdom others can drink",
    11: "you ground voltage — intuition ships work into matter",
    22: "you build in phases — world-touching without spinal snap",
    33: "you teach ascent — compassion sets boundaries",
}

PATH_MISALIGNED: dict[int, str] = {
    1: "you wait for permission — life assigns you side roles and bitter mirrors",
    2: "you merge without discernment — others' chaos becomes your biography",
    3: "you perform without root — audience loves the mask, abandons the person",
    4: "you rebel against your own method — shortcuts tax twice",
    5: "you flee before the lesson — luck turns to scandal",
    6: "you rescue to control — love curdles to obligation",
    7: "you hide in research — paranoia wears mystic robes",
    8: "you seize without ethics — gold buys isolation",
    9: "you cling — every ending returns harsher",
    11: "you burn ungrounded — prophecy without product",
    22: "you architect without body — collapse at altitude",
    33: "you pay everyone's bill — resentment masquerades as holiness",
}

PATH_FRIEND_NUMBERS: dict[int, list[int]] = {
    1: [1, 5, 7],
    2: [2, 4, 8],
    3: [3, 6, 9],
    4: [2, 4, 8],
    5: [1, 5, 7],
    6: [3, 6, 9],
    7: [1, 5, 7],
    8: [2, 4, 8],
    9: [3, 6, 9],
    11: [2, 11, 6],
    22: [4, 22, 8],
    33: [6, 9, 33],
}

PATH_ENEMY_NUMBERS: dict[int, list[int]] = {
    1: [2, 5, 8],
    2: [1, 5, 7],
    3: [4, 7, 8],
    4: [5, 3, 1],
    5: [6, 4, 8],
    6: [1, 7, 8],
    7: [3, 2, 8],
    8: [5, 9, 3],
    9: [1, 4, 7],
    11: [4, 8, 5],
    22: [3, 5, 33],
    33: [1, 7, 8],
}

PATH_ALLIES: dict[int, str] = {
    1: "friendly: 1, 5, 7 (fire of initiative). enemy field: passive 2, ungrounded 5, controlling 8",
    2: "friendly: 2, 4, 8 (earth-water stability). enemy field: aggressive 1, scattered 5, cold 7",
    3: "friendly: 3, 6, 9 (expression triad). enemy field: rigid 4, secretive 7, domineering 8",
    4: "friendly: 2, 4, 8 (builders). enemy field: restless 5, flashy 3, tyrant 1",
    5: "friendly: 1, 5, 7 (change agents). enemy field: clingy 6, rigid 4, hoarding 8",
    6: "friendly: 3, 6, 9 (heart lines). enemy field: cutting 1, isolated 7, mercenary 8",
    7: "friendly: 1, 5, 7 (seers). enemy field: crowd 3, needy 2, empire 8 without soul",
    8: "friendly: 2, 4, 8 (material architects). enemy field: escapist 5, victim 9, vanity 3",
    9: "friendly: 3, 6, 9 (completion). enemy field: selfish 1, rigid 4, cynical 7",
    11: "friendly: 2, 11, 6 (channels). enemy field: blunt 4, greedy 8, unmoored 5",
    22: "friendly: 4, 22, 8 (builders at scale). enemy field: gossip 3, flight 5, martyr 33 unbounded",
    33: "friendly: 6, 9, 33 (healers). enemy field: cruel 1, cold 7, empire 8 without mercy",
}

COMPOUND_STAR_ANGEL: dict[int, str] = {
    10: "star-seed 10 — gate of leadership before the 1 is earned; angelic pressure to stand visible",
    11: "master 11 in the flesh — angel number of voltage; nervous system as antenna before grounding",
    12: "12 — sacrifice cycle (1+2=3) — art through ordeal; apostle frequency in the body",
    13: "13 — death card in tarot numerology — reinvention tax; phoenix compound",
    14: "14 — tempest (1+4=5) — appetite chained to consequence; angel split between freedom and ledger",
    16: "16 — tower digit — ego lightning; humility or fracture",
    17: "17 — star of the magi — hope after stripping; spiritual ambition in flesh",
    18: "18 — moon sun merge (1+8=9) — endings fund power; karmic completion weight",
    19: "19 — sun prince — visibility before the throne is earned",
    20: "20 — judgment day frequency — partnerships as courtroom",
    22: "master 22 unreduced — cathedral in the muscle before the tools exist",
    24: "24 — home + crown (2+4=6) — family law vs public myth",
    27: "27 — triple 9 in 2+7 — compassion labor; angel 27 as amplified 9 service; genius burden",
    29: "29 — 11 in compound (2+9=11) — master voltage dressed as 2's delay",
    30: "30 — expression triad — voice as fate; scatter if unrooted",
    33: "master 33 in flesh — christic labor without savior complex required",
}


def compound_star_angel_lore(compound: int, final: int) -> str:
    base = COMPOUND_STAR_ANGEL.get(
        compound,
        f"compound {compound} — unreduced birth-field; digit sum argues before the vow {final} settles",
    )
    if compound in (11, 22, 33) or final in (11, 22, 33):
        base += " Master-frequency: not casual; the body pays interest on voltage."
    return base


def build_vow_chapter(facts: dict[str, Any]) -> str:
    from app.services.overview_lore import COMPOUND_PRESSURE, LIFE_PATH_MEANING

    lp = facts["life_path"]
    c, f = lp["compound"], lp["value"]
    disp = lp["display"]
    star = compound_star_angel_lore(c, f)
    c_occult = COMPOUND_PRESSURE.get(c, "raw date-weight in the flesh")
    f_occult = LIFE_PATH_MEANING.get(f, "initiatory road")

    if c == f:
        compound_block = (
            f"Single gate {c} — no split between flesh and vow. {star} "
            f"Occult: {c_occult}."
        )
    else:
        compound_block = (
            f"Compound {c} first — what the body still pleads. {star} Occult compound: {c_occult}. "
            f"This is star/angel pressure BEFORE reduction — the hungers you feel but rarely name."
        )

    path_block = (
        f"Life path {f} ({disp}) — soul curriculum: {f_occult} "
        f"Gift when owned: {PATH_PROS.get(f, '')} "
        f"Price when refused: {PATH_CONS.get(f, '')} "
        f"Aligned living: {PATH_ALIGNED.get(f, '')} "
        f"Drift: {PATH_MISALIGNED.get(f, '')} "
        f"Number field: {PATH_ALLIES.get(f, '')}."
    )

    expr = facts.get("expression", {})
    expr_bit = ""
    if expr.get("display"):
        ev = expr.get("value", 0)
        expr_bit = (
            f" Expression {expr['display']} suggests how the world titles you — "
            f"compare to vow: harmony teaches integration; conflict teaches disguise."
        )

    return f"{compound_block} {path_block}{expr_bit}"