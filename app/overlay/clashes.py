"""BaZi branch clash and harmony relations."""

from app.services.imprint_labels import branch_animal

SAN_HE = [
    {"申", "子", "辰"},
    {"亥", "卯", "未"},
    {"寅", "午", "戌"},
    {"巳", "酉", "丑"},
]

LIU_HE = [
    ("子", "丑"), ("寅", "亥"), ("卯", "戌"),
    ("辰", "酉"), ("巳", "申"), ("午", "未"),
]

CHONG_PAIRS = {
    ("子", "午"), ("午", "子"),
    ("丑", "未"), ("未", "丑"),
    ("寅", "申"), ("申", "寅"),
    ("卯", "酉"), ("酉", "卯"),
    ("辰", "戌"), ("戌", "辰"),
    ("巳", "亥"), ("亥", "巳"),
}


def branch_clashes(natal_branch: str, current_branch: str) -> list[str]:
    if (natal_branch, current_branch) in CHONG_PAIRS:
        a = branch_animal(natal_branch)
        b = branch_animal(current_branch)
        return [f"{a}–{b} clash (冲)"]
    return []


def branch_harmony(a: str, b: str) -> str | None:
    if a == b:
        return "same_branch"
    for group in SAN_HE:
        if a in group and b in group:
            return "san_he_三合"
    for p in LIU_HE:
        if set(p) == {a, b}:
            return "liu_he_六合"
    if branch_clashes(a, b):
        return "chong_冲"
    return None