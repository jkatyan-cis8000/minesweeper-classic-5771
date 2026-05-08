"""Board data class for Minesweeper."""

from dataclasses import dataclass
from typing import List
from src.types.cell import Cell


@dataclass
class Board:
    """Represents the game board."""
    rows: int
    cols: int
    cells: List[List[Cell]]
