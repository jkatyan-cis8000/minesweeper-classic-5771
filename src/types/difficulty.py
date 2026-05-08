"""Difficulty level configuration for Minesweeper."""

from enum import Enum


class DifficultyLevel(Enum):
    """Difficulty levels for the game."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
