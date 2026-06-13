"""
Master-insight chart reading — personalized how-to, not metric recitation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

MAX_WORDS = 720
MIN_WORDS = 140

FORBIDDEN_MODAL_SECTIONS = (
    "IN YOUR CHART",
    "YOUR CHART AT A GLANCE",
    "WHAT EACH PART MEANS FOR YOU",
    "HOW THESE FIT TOGETHER",
    "HOW THIS MANIFESTS",
    "STRENGTHS",
    "WHAT PRESSURES THIS CHART",
    "WHEN LIFE GETS MESSY",
    "IN EVERYDAY LIFE",
    "On your chart:",
    "What this means:",
)

FORBIDDEN_GLOSSARY = (
    "ba zi maps",
    "numerology maps",
    "jyotish emphasizes",
    "hellenistic astrology",
    "whole-sign houses are",
    "nakshatra belt",
    "mahadasha is a",
)

REQUIRED_SECTIONS = (
    "THE SCENE",
    "WORK YOUR EDGE",
    "STAY MINDFUL",
    "WHEN IT COSTS YOU",
    "THIS EPISODE TOGETHER",
)


@dataclass
class EpisodeReading:
    tradition_title: str
    scene: str
    edge: str
    mindful: str
    costs: list[str] = field(default_factory=list)
    together: str = ""

    def word_count(self) -> int:
        return len(self.build().split())

    def render(self) -> list[str]:
        lines = [
            self.tradition_title,
            "",
            "THE SCENE",
            self.scene,
            "",
            "WORK YOUR EDGE",
            self.edge,
            "",
            "STAY MINDFUL",
            self.mindful,
        ]
        if self.costs:
            lines.extend(["", "WHEN IT COSTS YOU"])
            lines.extend(f"  · {c}" for c in self.costs)
        if self.together:
            lines.extend(["", "THIS EPISODE TOGETHER", self.together])
        return lines

    def build(self) -> str:
        return "\n".join(self.render())


def bullet_list(items: list[str]) -> list[str]:
    return [x.strip() for x in items if x and x.strip()]