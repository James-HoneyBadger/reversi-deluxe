"""
Tests for game settings
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import GameSettings, THEMES


def test_game_settings():
    """Test game settings dataclass"""
    settings = GameSettings()
    assert settings.theme == "Classic"
    assert settings.sound_enabled is True
    assert settings.show_hints
    assert settings.ai_difficulty == "MEDIUM"
    assert settings.board_size == 8
    assert settings.player_color == 1  # PLAYER_BLACK
    assert settings.animations is True


def test_themes():
    """Test theme definitions"""
    assert "Classic" in THEMES
    assert "Ocean" in THEMES
    assert "Sunset" in THEMES
    assert "Forest" in THEMES

    # Check theme structure
    classic = THEMES["Classic"]
    required_keys = ["board", "board_alt", "text", "accent", "highlight", "background"]
    for key in required_keys:
        assert key in classic
