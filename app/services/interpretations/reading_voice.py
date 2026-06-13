"""
Unified chart reading voice — plain English, everyday examples, chart-anchored meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DeepGate:
    title: str
    chart_shows: str
    what_it_means: str
    how_you_notice: str
    when_it_works: str
    when_it_trips: str
    like_this: str

    # Legacy aliases for gradual migration
    @property
    def occult_depth(self) -> str:
        return self.what_it_means

    @property
    def life_projection(self) -> str:
        return self.how_you_notice

    @property
    def strengths(self) -> str:
        return self.when_it_works

    @property
    def watch_out(self) -> str:
        return self.when_it_trips

    @property
    def leverage(self) -> str:
        return self.like_this

    def render(self) -> str:
        return "\n".join(
            [
                self.title.upper(),
                f"On your chart: {self.chart_shows}",
                f"What this means: {self.what_it_means}",
                f"How you might notice it: {self.how_you_notice}",
                f"When it works: {self.when_it_works}",
                f"When it trips you: {self.when_it_trips}",
                f"Like this: {self.like_this}",
            ]
        )


@dataclass
class ChartReading:
    tradition_title: str
    in_your_chart: str
    at_a_glance: str
    picture_this: str = ""
    how_parts_interact: str = ""
    deep_gates: list[DeepGate] = field(default_factory=list)
    when_complicated: str = ""
    everyday_life: list[str] = field(default_factory=list)
    extra_sections: list[str] = field(default_factory=list)

    @property
    def what_this_is(self) -> str:
        return self.in_your_chart

    @property
    def leverage(self) -> list[str]:
        return self.everyday_life

    def render(self) -> list[str]:
        lines = [
            self.tradition_title,
            "",
            "IN YOUR CHART",
            self.in_your_chart,
            "",
            "YOUR CHART AT A GLANCE",
            self.at_a_glance,
        ]
        if self.picture_this:
            lines.extend(["", "PICTURE THIS", self.picture_this])
        if self.how_parts_interact:
            lines.extend(["", "HOW THESE FIT TOGETHER", self.how_parts_interact])
        if self.deep_gates:
            lines.extend(["", "WHAT EACH PART MEANS FOR YOU"])
            for i, gate in enumerate(self.deep_gates):
                if i:
                    lines.append("")
                lines.append(gate.render())
        for block in self.extra_sections:
            lines.extend(["", block])
        if self.when_complicated:
            lines.extend(["", "WHEN LIFE GETS MESSY", self.when_complicated])
        if self.everyday_life:
            lines.extend(["", "IN EVERYDAY LIFE"])
            lines.extend(self.everyday_life)
        return lines

    def build(self) -> str:
        return "\n".join(self.render())


def everyday_list(items: list[str]) -> list[str]:
    return [x.strip() for x in items if x and x.strip()]