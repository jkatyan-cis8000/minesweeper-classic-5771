"""Difficulty configurations for Minesweeper."""

from typing import NamedTuple


class DifficultyConfig(NamedTuple):
    """Configuration for a difficulty level."""
    rows: int
    cols: int
    mine_count: int


BEGINNER_CONFIG = DifficultyConfig(rows=9, cols=9, mine_count=10)
INTERMEDIATE_CONFIG = DifficultyConfig(rows=16, cols=16, mine_count=40)
EXPERT_CONFIG = DifficultyConfig(rows=16, cols=30, mine_count=99)
