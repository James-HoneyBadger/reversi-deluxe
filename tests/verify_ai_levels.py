#!/usr/bin/env python3
"""
Verify AI levels work correctly
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.ai import AI
from src.board import Board


def verify_ai_levels():
    """Verify all AI levels work"""
    board = Board()

    print("Testing AI levels...")

    for level in [1, 2, 3]:
        ai = AI(difficulty=level)
        move = ai.get_move(board)

        if move:
            print(f"  Level {level}: Move found at {move}")
        else:
            print(f"  Level {level}: No move found")
            return False

    print("All AI levels working correctly!")
    return True


if __name__ == "__main__":
    success = verify_ai_levels()
    sys.exit(0 if success else 1)
