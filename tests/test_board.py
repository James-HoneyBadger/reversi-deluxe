"""
Tests for board logic
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from board import Board
from config import PLAYER_BLACK, PLAYER_WHITE, EMPTY


def test_board_initialization():
    """Test board initializes correctly"""
    board = Board()
    assert board.size == 8
    assert board.current_player == PLAYER_BLACK
    assert not board.game_over
    assert board.winner is None

    # Check initial pieces
    assert board.grid[3][3] == PLAYER_WHITE
    assert board.grid[3][4] == PLAYER_BLACK
    assert board.grid[4][3] == PLAYER_BLACK
    assert board.grid[4][4] == PLAYER_WHITE


def test_valid_moves():
    """Test valid move detection"""
    board = Board()

    # Should have 4 valid moves initially
    valid_moves = board.get_valid_moves(PLAYER_BLACK)
    assert len(valid_moves) == 4

    # Test specific valid moves (standard Reversi opening moves)
    assert (2, 3) in valid_moves  # Valid move
    assert (3, 2) in valid_moves  # Valid move
    assert (4, 5) in valid_moves  # Valid move
    assert (5, 4) in valid_moves  # Valid move


def test_make_move():
    """Test making moves"""
    board = Board()

    # Make a move
    flipped = board.make_move(2, 3, PLAYER_BLACK)
    assert len(flipped) == 1
    assert board.grid[2][3] == PLAYER_BLACK
    assert board.grid[3][3] == PLAYER_BLACK  # Should be flipped

    # Check player switched
    assert board.current_player == PLAYER_WHITE


def test_game_end():
    """Test game end detection"""
    board = Board()

    # Create a simple endgame scenario
    board.grid = [
        [PLAYER_BLACK] * 8,
        [PLAYER_BLACK] * 8,
        [PLAYER_BLACK] * 8,
        [PLAYER_BLACK] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
    ]

    board.check_game_over()
    assert board.game_over
    assert board.winner == PLAYER_BLACK


def test_score_calculation():
    """Test score calculation"""
    board = Board()

    # Initial score should be 2-2
    black, white = board.get_score()
    assert black == 2
    assert white == 2

    # Make a move and check score
    board.make_move(2, 3, PLAYER_BLACK)
    black, white = board.get_score()
    assert black == 4  # Placed 1 + flipped 1
    assert white == 1  # Lost 1 piece
