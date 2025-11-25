"""
Error handling utilities for Iago Deluxe
"""

import sys
import traceback
from typing import Optional, Callable


class GameError(Exception):
    """Base exception for game-related errors"""

    pass


class BoardError(GameError):
    """Exception for board-related errors"""

    pass


class AIError(GameError):
    """Exception for AI-related errors"""

    pass


def handle_error(error: Exception, context: str = "", fatal: bool = False) -> None:
    """Handle and log errors gracefully"""
    error_msg = f"Error in {context}: {str(error)}"
    print(error_msg, file=sys.stderr)

    if fatal:
        traceback.print_exc()
        sys.exit(1)


def safe_call(func: Callable, *args, **kwargs) -> Optional:
    """Safely call a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handle_error(e, f"calling {func.__name__}")
        return None
