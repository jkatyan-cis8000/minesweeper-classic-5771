"""Game engine - business logic for Minesweeper."""

import random
from src.types import Cell, CellState, Board, GameState
from src.config.difficulty import (
    DifficultyConfig,
    BEGINNER_CONFIG,
    INTERMEDIATE_CONFIG,
    EXPERT_CONFIG,
)


class GameEngine:
    """Main game logic class."""
    
    def __init__(self):
        self._state: GameState = None
    
    def create_game(self, difficulty: str) -> GameState:
        """Initialize a new game with the given difficulty."""
        config = self._get_config(difficulty)
        board = self._generate_board(config.rows, config.cols, config.mine_count)
        self._state = GameState(
            board=board,
            difficulty=difficulty,
            game_status="in_progress",
            mines_revealed=False
        )
        return self._state
    
    def reveal_cell(self, row: int, col: int) -> GameState:
        """Uncover a cell and return the new state."""
        if self._state is None:
            raise ValueError("Game not initialized")
        
        if self._state.game_status != "in_progress":
            return self._state
        
        board = self._state.board
        
        # Check bounds
        if not (0 <= row < board.rows and 0 <= col < board.cols):
            return self._state
        
        cell = board.cells[row][col]
        
        # Can't reveal already revealed or flagged cells
        if cell.state in (CellState.REVEALED, CellState.FLAGGED):
            return self._state
        
        # Hit a mine
        if cell.is_mine:
            cell.state = CellState.REVEALED
            self._reveal_all_mines(board)
            self._state.game_status = "lost"
            self._state.mines_revealed = True
            return self._state
        
        # Reveal the cell
        cell.state = CellState.REVEALED
        
        # If empty, reveal adjacent cells recursively
        if cell.adjacent_mines == 0:
            self._reveal_adjacent(board, row, col)
        
        # Check win condition
        if self._check_win(board):
            self._state.game_status = "won"
        
        return self._state
    
    def flag_cell(self, row: int, col: int) -> GameState:
        """Toggle flag on a cell and return the new state."""
        if self._state is None:
            raise ValueError("Game not initialized")
        
        if self._state.game_status != "in_progress":
            return self._state
        
        board = self._state.board
        
        # Check bounds
        if not (0 <= row < board.rows and 0 <= col < board.cols):
            return self._state
        
        cell = board.cells[row][col]
        
        # Can't reveal already revealed cells
        if cell.state == CellState.REVEALED:
            return self._state
        
        # Toggle flag
        if cell.state == CellState.HIDDEN:
            cell.state = CellState.FLAGGED
        elif cell.state == CellState.FLAGGED:
            cell.state = CellState.HIDDEN
        
        return self._state
    
    def get_game_state(self) -> GameState:
        """Return the current game state."""
        return self._state
    
    def is_game_over(self) -> bool:
        """Check if the game is over (won or lost)."""
        return self._state is not None and self._state.game_status != "in_progress"
    
    def _get_config(self, difficulty: str) -> DifficultyConfig:
        """Get configuration for the difficulty level."""
        configs = {
            "beginner": BEGINNER_CONFIG,
            "intermediate": INTERMEDIATE_CONFIG,
            "expert": EXPERT_CONFIG,
        }
        return configs.get(difficulty.lower(), BEGINNER_CONFIG)
    
    def _generate_board(self, rows: int, cols: int, mine_count: int) -> Board:
        """Generate a new board with randomly placed mines."""
        # Create empty board
        cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        
        # Place mines randomly
        positions = [(r, c) for r in range(rows) for c in range(cols)]
        random.shuffle(positions)
        
        for r, c in positions[:mine_count]:
            cells[r][c] = Cell(is_mine=True)
        
        # Calculate adjacent mine counts
        for r in range(rows):
            for c in range(cols):
                if not cells[r][c].is_mine:
                    cells[r][c].adjacent_mines = self._count_adjacent_mines(cells, rows, cols, r, c)
        
        return Board(rows=rows, cols=cols, cells=cells)
    
    def _count_adjacent_mines(self, cells: list, rows: int, cols: int, row: int, col: int) -> int:
        """Count mines adjacent to a given cell."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if cells[nr][nc].is_mine:
                        count += 1
        return count
    
    def _reveal_adjacent(self, board: Board, row: int, col: int) -> None:
        """Recursively reveal adjacent empty cells."""
        rows, cols = board.rows, board.cols
        cells = board.cells
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    cell = cells[nr][nc]
                    if cell.state == CellState.HIDDEN:
                        cell.state = CellState.REVEALED
                        if cell.adjacent_mines == 0:
                            self._reveal_adjacent(board, nr, nc)
    
    def _reveal_all_mines(self, board: Board) -> None:
        """Reveal all mines when game is lost."""
        for row in board.cells:
            for cell in row:
                if cell.is_mine and cell.state != CellState.FLAGGED:
                    cell.state = CellState.REVEALED
    
    def _check_win(self, board: Board) -> bool:
        """Check if all non-mine cells are revealed."""
        for row in board.cells:
            for cell in row:
                if not cell.is_mine and cell.state != CellState.REVEALED:
                    return False
        return True
