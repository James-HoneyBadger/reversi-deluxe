"""
Tests for AI logic
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai import AI
from board import Board
from config import PLAYER_BLACK


def test_ai_initialization():
    """Test AI initializes correctly"""
    ai = AI(difficulty=1)
    assert ai.difficulty == 1

    ai_hard = AI(difficulty=3)
    assert ai_hard.difficulty == 3


def test_ai_get_move():
    """Test AI can get moves"""
    board = Board()
    ai = AI(difficulty=1)

    move = ai.get_move(board)
    assert move is not None
    assert len(move) == 2
    assert 0 <= move[0] < 8
    assert 0 <= move[1] < 8

    # Move should be valid
    assert board.is_valid_move(move[0], move[1], PLAYER_BLACK)


def test_ai_difficulty_levels():
    """Test different AI difficulty levels"""
    board = Board()

    # Easy AI (random)
    ai_easy = AI(difficulty=1)
    move_easy = ai_easy.get_move(board)
    assert move_easy is not None

    # Medium AI (heuristic)
    ai_medium = AI(difficulty=2)
    move_medium = ai_medium.get_move(board)
    assert move_medium is not None

    # Hard AI (minimax)
    ai_hard = AI(difficulty=3)
    move_hard = ai_hard.get_move(board)
    assert move_hard is not None


def test_ai_no_moves():
    """Test AI behavior when no moves available"""
    board = Board()

    # Fill board so no moves available for current player
    board.grid = [[1] * 8 for _ in range(8)]  # All black pieces
    board.current_player = 2  # White's turn

    ai = AI()
    move = ai.get_move(board)
    assert move is None  # No moves available
