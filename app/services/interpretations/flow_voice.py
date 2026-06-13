"""
Flowing chart insight — one prose layer, no scene framing.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

MAX_WORDS_BOX = 480
MAX_WORDS_ZERO = 620
MAX_WORDS_BAZI = 1120
MAX_WORDS_WESTERN_SETTING = 640
MAX_WORDS_EASTERN = 1120
MAX_WORDS_VEDIC = 1120
MIN_WORDS_BOX = 115
MIN_WORDS_ZERO = 180

FORBIDDEN_SECTIONS = (
    "THE SCENE",
    "WORK YOUR EDGE",
    "STAY MINDFUL",
    "WHEN IT COSTS YOU",
    "THIS EPISODE TOGETHER",
    "HOW THIS MANIFESTS",
    "STRENGTHS",
    "WHAT PRESSURES THIS CHART",
    "PICTURE THIS",
    "WHEN LIFE GETS MESSY",
    "IN EVERYDAY LIFE",
    "ZERO'S READ",
    "IN YOUR CHART",
    "YOUR CHART AT A GLANCE",
)

FORBIDDEN_FRAMING = (
    "cold open",
    "episode cast",
    "opening shot",
    "money episode",
    "bond episode",
    "paycheck episode",
    "scene one",
    "picture this",
    "your edge lands",
    "watch pace",
    "environment (",
    "day pillar (",
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


@dataclass
class FlowReading:
    body: str

    def word_count(self) -> int:
        return len(self.body.split())

    def build(self) -> str:
        return self.body.strip()


def weave_flow(paragraphs: list[str]) -> str:
    parts = [" ".join(p.split()) for p in paragraphs if p and p.strip()]
    return "\n\n".join(parts)


def _dedupe_words(text: str) -> str:
    return " ".join(text.split())