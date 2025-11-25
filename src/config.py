"""
Configuration and constants for Iago Deluxe
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from enum import Enum

# Constants
DEFAULT_BOARD_SIZE = 8
CELL_SIZE = 60
MARGIN = 20
UI_HEIGHT = 120
ANIMATION_SPEED = 0.3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Game pieces
EMPTY = 0
PLAYER_BLACK = 1
PLAYER_WHITE = 2

# Themes
THEMES = {
    "Classic": {
        "board": (34, 139, 34),
        "board_alt": (0, 100, 0),
        "text": BLACK,
        "accent": BLUE,
        "highlight": YELLOW,
        "background": GREEN,
    },
    "Ocean": {
        "board": (25, 25, 112),
        "board_alt": (0, 0, 139),
        "text": WHITE,
        "accent": CYAN,
        "highlight": YELLOW,
        "background": (0, 0, 128),
    },
    "Sunset": {
        "board": (139, 69, 19),
        "board_alt": (160, 82, 45),
        "text": WHITE,
        "accent": (255, 165, 0),
        "highlight": YELLOW,
        "background": (178, 34, 34),
    },
    "Forest": {
        "board": (34, 139, 34),
        "board_alt": (0, 100, 0),
        "text": WHITE,
        "accent": (50, 205, 50),
        "highlight": YELLOW,
        "background": (0, 100, 0),
    },
}


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


@dataclass
class GameSettings:
    """Game settings that persist between sessions"""

    theme: str = "Classic"
    sound_enabled: bool = True
    show_hints: bool = True
    ai_difficulty: str = "MEDIUM"
    board_size: int = DEFAULT_BOARD_SIZE
    player_color: int = PLAYER_BLACK
    animations: bool = True


@dataclass
class GameStats:
    """Player statistics"""

    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0
    games_drawn: int = 0
    total_moves: int = 0
    best_score: int = 0


@dataclass
class Animation:
    """Represents a piece placement or flip animation"""

    row: int
    col: int
    player: int
    start_time: float
    duration: float
    anim_type: str  # 'place' or 'flip'
    start_scale: float = 0.0
    end_scale: float = 1.0


@dataclass
class GameState:
    """Complete game state for saving/loading"""

    board_grid: List[List[int]]
    current_player: int
    move_history: List[Dict[str, Any]]
    black_score: int
    white_score: int
    game_over: bool
    winner: int
    settings: Dict[str, Any]
