"""Tests for the CommandLineInterface."""

import pytest
from io import StringIO
from src.ui.cli import CommandLineInterface
from src.types.game_state import GameState
from src.types.board import Board
from src.types.cell import Cell
from src.types.cell_state import CellState


class TestCommandLineInterface:
    """Tests for the CommandLineInterface class."""

    def test_display_board(self, capsys):
        """Test that the board is displayed correctly."""
        cli = CommandLineInterface()
        
        # Create a simple test board
        cells = [
            [Cell(is_mine=False, adjacent_mines=0, state=CellState.HIDDEN) 
             for _ in range(3)]
            for _ in range(3)
        ]
        board = Board(rows=3, cols=3, cells=cells)
        game_state = GameState(
            board=board,
            difficulty="beginner",
            game_status="in_progress"
        )
        
        cli.display_board(game_state)
        captured = capsys.readouterr()
        
        # Check that the board contains expected content
        assert "+" in captured.out
        assert "|" in captured.out

    def test_get_user_input_reveal(self, monkeypatch):
        """Test getting reveal command input."""
        cli = CommandLineInterface()
        
        # Mock input to return "r 2 3"
        monkeypatch.setattr('builtins.input', lambda _: "r 2 3")
        
        result = cli.get_user_input()
        assert result is not None
        assert result[0] == 'r'
        assert result[1] == 2
        assert result[2] == 3

    def test_get_user_input_flag(self, monkeypatch):
        """Test getting flag command input."""
        cli = CommandLineInterface()
        
        # Mock input to return "f 2 3"
        monkeypatch.setattr('builtins.input', lambda _: "f 2 3")
        
        result = cli.get_user_input()
        assert result is not None
        assert result[0] == 'f'
        assert result[1] == 2
        assert result[2] == 3

    def test_get_user_input_quit(self, monkeypatch):
        """Test getting quit command input."""
        cli = CommandLineInterface()
        
        # Mock input to return "q"
        monkeypatch.setattr('builtins.input', lambda _: "q")
        
        result = cli.get_user_input()
        assert result is not None
        assert result[0] == 'quit'

    def test_get_user_input_invalid_format(self, monkeypatch, capsys):
        """Test handling invalid format."""
        cli = CommandLineInterface()
        
        # Mock input to return invalid format
        monkeypatch.setattr('builtins.input', lambda _: "invalid")
        
        result = cli.get_user_input()
        assert result is None
        
        captured = capsys.readouterr()
        assert "Invalid" in captured.out

    def test_get_user_input_missing_args(self, monkeypatch, capsys):
        """Test handling missing arguments."""
        cli = CommandLineInterface()
        
        # Mock input to return only action
        monkeypatch.setattr('builtins.input', lambda _: "r")
        
        result = cli.get_user_input()
        assert result is None
        
        captured = capsys.readouterr()
        assert "Invalid format" in captured.out

    def test_display_message(self, capsys):
        """Test displaying a message."""
        cli = CommandLineInterface()
        
        cli.display_message("Test message")
        captured = capsys.readouterr()
        
        assert "Test message" in captured.out

    def test_display_game_over_win(self, capsys):
        """Test displaying game over for win."""
        cli = CommandLineInterface()
        
        cells = [[Cell(is_mine=False, adjacent_mines=0, state=CellState.REVEALED) 
                  for _ in range(9)] for _ in range(9)]
        board = Board(rows=9, cols=9, cells=cells)
        game_state = GameState(
            board=board,
            difficulty="beginner",
            game_status="won"
        )
        
        cli.display_board(game_state)
        captured = capsys.readouterr()
        
        assert "YOU WON" in captured.out.upper() or "WON" in captured.out.upper()

    def test_display_game_over_lose(self, capsys):
        """Test displaying game over for loss."""
        cli = CommandLineInterface()
        
        cells = [[Cell(is_mine=False, adjacent_mines=0, state=CellState.REVEALED) 
                  for _ in range(9)] for _ in range(9)]
        board = Board(rows=9, cols=9, cells=cells)
        game_state = GameState(
            board=board,
            difficulty="beginner",
            game_status="lost"
        )
        
        cli.display_board(game_state)
        captured = capsys.readouterr()
        
        assert "GAME OVER" in captured.out.upper() or "LOST" in captured.out.upper()
