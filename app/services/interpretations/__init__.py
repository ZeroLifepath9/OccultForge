"""
Occult Forge — interpretations subpackage.

Contains the specialized lenses, voices, deep readings, corpora, and forge modules
that power chart_system_readings, daily enrich, Zero context, Matrix Decoder,
ancients wisdom, and per-tradition "Full insight" panels.

These were consolidated here from the previous flat top-level services/ sprawl
to make the project maintainable while preserving 100% of prior behavior and
public function signatures (build_*_reading, build_*_lens, etc.).

Do not import directly from here in most cases; use the re-exporting top-level
wrappers in chart_system_readings.py / bazi_enrich.py / zero/* etc. or the
explicit from .interpretations.xxx imports after the move.
"""

# Re-exports for the most commonly referenced public builders can be added here
# after the file moves are complete (keeps call sites stable if desired).
# Example (uncomment/adjust once modules are in place):
# from .matrix_decoder_voice import format_matrix_reading, build_zero_matrix_overview, ...
# from .manifestation_voice import plain_flesh, manifest_animal, ...
# from .chart_readings_bundle import build_all_chart_readings
# from .chart_system_readings import VALID_SYSTEMS, build_system_reading, SYSTEM_TITLES

__all__ = [
    # Populated post-move
]
