"""Main entry point for Minesweeper."""

import sys
from src.ui.cli import CommandLineInterface


def main():
    """Main entry point."""
    difficulty = "beginner"
    
    if len(sys.argv) > 1:
        difficulty = sys.argv[1].lower()
        if difficulty not in ("beginner", "intermediate", "expert"):
            print(f"Unknown difficulty: {difficulty}")
            print("Usage: python -m minesweeper [beginner|intermediate|expert]")
            sys.exit(1)
    
    cli = CommandLineInterface()
    cli.play_game(difficulty)


if __name__ == "__main__":
    main()
