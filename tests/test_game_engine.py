"""Tests for the GameEngine service."""

import pytest
from src.types.board import Board
from src.types.cell import Cell
from src.types.cell_state import CellState
from src.config.difficulty import DifficultyConfig
from src.types.game_state import GameState
from src.service.game_engine import GameEngine


class TestGameEngine:
    """Tests for the GameEngine class."""

    def test_create_game_beginner(self):
        """Test creating a beginner game."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        assert state.difficulty == "beginner"
        assert state.board.rows == 9
        assert state.board.cols == 9
        assert state.game_status == "in_progress"

    def test_create_game_intermediate(self):
        """Test creating an intermediate game."""
        engine = GameEngine()
        state = engine.create_game("intermediate")
        
        assert state.difficulty == "intermediate"
        assert state.board.rows == 16
        assert state.board.cols == 16
        assert state.game_status == "in_progress"

    def test_create_game_expert(self):
        """Test creating an expert game."""
        engine = GameEngine()
        state = engine.create_game("expert")
        
        assert state.difficulty == "expert"
        assert state.board.rows == 16
        assert state.board.cols == 30
        assert state.game_status == "in_progress"

    def test_reveal_cell_safe(self):
        """Test revealing a safe cell."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        # Find a non-mine cell (likely at 0,0 if not a mine)
        cell = state.board.cells[0][0]
        
        if not cell.is_mine:
            new_state = engine.reveal_cell(0, 0)
            assert new_state.game_status == "in_progress"
            assert new_state.board.cells[0][0].state == CellState.REVEALED

    def test_reveal_cell_mine(self):
        """Test revealing a mine cell."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        # Find a mine cell
        for row in state.board.cells:
            for cell in row:
                if cell.is_mine:
                    new_state = engine.reveal_cell(cell_row(state.board, cell), cell_col(state.board, cell))
                    assert new_state.game_status == "lost"
                    return
        
        # If no mine found (unlikely but possible with small board), just check we can play
        engine.reveal_cell(0, 0)

    def test_flag_cell(self):
        """Test flagging a cell."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        new_state = engine.flag_cell(0, 0)
        assert new_state.board.cells[0][0].state == CellState.FLAGGED

    def test_unflag_cell(self):
        """Test unflagging a cell."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        # Flag then unflag
        state = engine.flag_cell(0, 0)
        assert state.board.cells[0][0].state == CellState.FLAGGED
        
        new_state = engine.flag_cell(0, 0)
        assert new_state.board.cells[0][0].state == CellState.HIDDEN

    def test_get_game_state(self):
        """Test getting current game state."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        retrieved = engine.get_game_state()
        assert retrieved is state

    def test_is_game_over(self):
        """Test game over check."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        assert not engine.is_game_over()
        
        # Reveal a mine
        for row in state.board.cells:
            for cell in row:
                if cell.is_mine:
                    engine.reveal_cell(cell_row(state.board, cell), cell_col(state.board, cell))
                    assert engine.is_game_over()
                    return

    def test_neighbors_count(self):
        """Test that neighbors are counted correctly."""
        engine = GameEngine()
        state = engine.create_game("beginner")
        
        # Check that neighbors are counted
        # The count should be between 0 and 8
        for row in state.board.cells:
            for cell in row:
                assert 0 <= cell.adjacent_mines <= 8


def cell_row(board: Board, target: Cell) -> int:
    """Get row index of a cell in board."""
    for r, row in enumerate(board.cells):
        for c, cell in enumerate(row):
            if cell is target:
                return r
    return 0


def cell_col(board: Board, target: Cell) -> int:
    """Get column index of a cell in board."""
    for r, row in enumerate(board.cells):
        for c, cell in enumerate(row):
            if cell is target:
                return c
    return 0
