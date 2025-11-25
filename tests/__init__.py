"""
Test suite for Iago Deluxe
"""

import pytest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from board import Board
from ai import AI
from config import PLAYER_BLACK, PLAYER_WHITE, EMPTY
