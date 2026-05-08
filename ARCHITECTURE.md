# Minesweeper Architecture

## Module Overview

This document describes the module design for the Minesweeper game implementation.

### Layer Dependencies

```
types → config → repo → service → runtime → ui
providers (cross-cutting, may import from utils)
utils (leaf, no internal imports)
```

### Modules

#### src/types/
**Purpose**: Pure type definitions, no logic.

**Files**:
- `__init__.py`: Exports all types
- `game_state.py`: CellState, Board, GameState types
- `difficulty.py`: DifficultyLevel enum

**Interfaces**:
- `CellState`: Enum for cell states (HIDDEN, REVEALED, FLAGGED)
- `DifficultyLevel`: Enum for difficulty levels
- `Board`: 2D grid of cells with dimensions
- `GameState`: Complete game state including board, status, and metadata

#### src/config/
**Purpose**: Configuration constants and settings.

**Files**:
- `__init__.py`: Exports configuration
- `difficulty.py`: Difficulty configurations (beginner, intermediate, expert)

**Interfaces**:
- `DifficultyConfig`: Named tuple with rows, cols, mine_count
- Configuration objects for each difficulty level

#### src/service/
**Purpose**: Business logic.

**Files**:
- `__init__.py`: Exports game service
- `game_engine.py`: GameEngine class with methods:
  - `create_game(difficulty)`: Initialize new game
  - `reveal_cell(row, col)`: Uncover a cell
  - `flag_cell(row, col)`: Toggle flag on a cell
  - `get_game_state()`: Return current state
  - `is_game_over()`: Check win/loss condition

**Interfaces**:
- `GameEngine`: Main game logic class
  - `create_game(difficulty: DifficultyLevel) -> GameState`
  - `reveal_cell(row: int, col: int) -> GameState`
  - `flag_cell(row: int, col: int) -> GameState`
  - `get_game_state() -> GameState`
  - `is_game_over() -> bool`

#### src/ui/
**Purpose**: CLI interface.

**Files**:
- `__init__.py`: Exports UI
- `cli.py`: CommandLineInterface class with methods:
  - `display_board(game_state)`: Render the board
  - `get_user_input()`: Parse user commands
  - `display_message(msg)`: Show messages

**Interfaces**:
- `CommandLineInterface`: UI layer class
  - `display_board(state: GameState) -> None`
  - `get_user_input() -> str`
  - `display_message(message: str) -> None`

#### src/runtime/
**Purpose**: Application lifecycle.

**Files**:
- `__init__.py`: Entry point
- `main.py`: Main function

**Interfaces**:
- `main()`: Entry point that orchestrates the game loop

#### src/utils/
**Purpose**: Pure helper functions.

**Files**:
- `__init__.py`: Exports utilities
- `board_utils.py`: Helper functions for board operations

**Interfaces**:
- `count_adjacent_mines(board, row, col) -> int`: Count mines around a cell
- `is_valid_position(board, row, col) -> bool`: Check if position is valid

#### src/providers/
**Purpose**: Cross-cutting concerns (placeholder for future).

Currently unused but available for extensibility.

### Game Flow

1. **Initialization** (`runtime/main.py`):
   - Parse difficulty level from arguments or defaults
   - Create `GameEngine`
   - Call `create_game(difficulty)` to get initial `GameState`
   - Enter main loop

2. **Main Loop** (`ui/cli.py`):
   - Display current board state
   - Get user input (reveal/flag commands)
   - Call appropriate `GameEngine` method
   - Update `GameState`
   - Check for game over
   - Repeat or exit

3. **Game Logic** (`service/game_engine.py`):
   - `reveal_cell`: Uncover cell, check for mine, reveal adjacent if empty
   - `flag_cell`: Toggle flag state on cell
   - Win condition: All non-mine cells revealed
   - Loss condition: Mine cell revealed

### Data Flow

1. User input → `CommandLineInterface.get_user_input()`
2. Command → `GameEngine.reveal_cell()` or `GameEngine.flag_cell()`
3. Logic processes → New `GameState`
4. State → `CommandLineInterface.display_board()`

### Testing Strategy

Tests live in `tests/` directory:
- Unit tests for each service method
- Integration tests for full game flow
- Property tests for board generation (valid mine counts, adjacency)
