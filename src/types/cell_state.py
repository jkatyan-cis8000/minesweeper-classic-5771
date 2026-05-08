"""CellState enum for Minesweeper."""

from enum import Enum


class CellState(Enum):
    """Represents the state of a cell."""
    HIDDEN = "hidden"
    FLAGGED = "flagged"
    REVEALED = "revealed"
