"""GameState data class for Minesweeper."""

from dataclasses import dataclass
from src.types.board import Board


@dataclass
class GameState:
    """Represents the current state of the game."""
    board: Board
    difficulty: str
    game_status: str  # "in_progress", "won", "lost"
    mines_revealed: bool = False
