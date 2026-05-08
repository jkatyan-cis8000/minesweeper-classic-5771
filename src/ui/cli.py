"""CLI interface for Minesweeper."""

import sys
from typing import Optional

from src.types import GameState, CellState
from src.service.game_engine import GameEngine


class CommandLineInterface:
    """CLI interface for playing Minesweeper."""
    
    def __init__(self):
        self.engine = GameEngine()
    
    def display_board(self, state: GameState) -> None:
        """Render the board to the console."""
        board = state.board
        rows, cols = board.rows, board.cols
        
        # Print column headers
        print("   " + " ".join(f"{c:2d}" for c in range(cols)))
        
        # Print separator
        print("  " + "+" + "-" * (cols * 3 - 1) + "+")
        
        # Print each row
        for r, row in enumerate(board.cells):
            print(f"{r:2d}|", end="")
            for cell in row:
                if cell.state == CellState.HIDDEN:
                    print(" . ", end="")
                elif cell.state == CellState.FLAGGED:
                    print(" F ", end="")
                elif cell.state == CellState.REVEALED:
                    if cell.is_mine:
                        print(" * ", end="")
                    elif cell.adjacent_mines == 0:
                        print("   ", end="")
                    else:
                        print(f" {cell.adjacent_mines} ", end="")
                else:
                    print(" ? ", end="")
            print("|")
        
        # Print separator
        print("  " + "+" + "-" * (cols * 3 - 1) + "+")
        
        # Print status
        if state.game_status == "in_progress":
            print(f"\nStatus: In progress ({state.difficulty})")
        elif state.game_status == "won":
            print(f"\nStatus: YOU WON! All mines found!")
        else:
            print(f"\nStatus: GAME OVER - You hit a mine!")
    
    def get_user_input(self) -> Optional[tuple[str, int, int]]:
        """Get and parse user input. Returns (action, row, col) or None."""
        try:
            line = input("\nEnter command (r <row> <col> to reveal, f <row> <col> to flag, q to quit): ").strip()
            
            if not line:
                return None
            
            parts = line.split()
            
            if parts[0].lower() == 'q':
                return ('quit', -1, -1)
            
            if len(parts) != 3:
                print("Invalid format. Use: r <row> <col> or f <row> <col>")
                return None
            
            action = parts[0].lower()
            if action not in ('r', 'f'):
                print("Invalid action. Use 'r' to reveal or 'f' to flag")
                return None
            
            try:
                row = int(parts[1])
                col = int(parts[2])
            except ValueError:
                print("Row and column must be integers")
                return None
            
            return (action, row, col)
        
        except EOFError:
            return ('quit', -1, -1)
    
    def display_message(self, message: str) -> None:
        """Display a message to the user."""
        print(message)
    
    def play_game(self, difficulty: str = "beginner") -> None:
        """Main game loop."""
        self.display_message(f"Starting Minesweeper - {difficulty.upper()} mode")
        self.display_message("Enter 'q' to quit at any time")
        
        # Initialize game
        state = self.engine.create_game(difficulty)
        self.display_board(state)
        
        while not self.engine.is_game_over():
            cmd = self.get_user_input()
            
            if cmd is None:
                continue
            
            action, row, col = cmd
            
            if action == 'quit':
                self.display_message("Quitting game...")
                break
            
            if action == 'r':
                state = self.engine.reveal_cell(row, col)
            elif action == 'f':
                state = self.engine.flag_cell(row, col)
            
            self.display_board(state)
        
        # Final status
        state = self.engine.get_game_state()
        if state.game_status == "won":
            self.display_message("\nCongratulations! You cleared the minefield!")
        elif state.game_status == "lost":
            self.display_message("\nGame over. Better luck next time!")
        
        self.display_message("Thanks for playing!")
