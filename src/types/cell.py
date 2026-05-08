"""Cell data class for Minesweeper."""

from dataclasses import dataclass
from src.types.cell_state import CellState


@dataclass
class Cell:
    """Represents a single cell on the board."""
    is_mine: bool = False
    adjacent_mines: int = 0
    state: CellState = CellState.HIDDEN
