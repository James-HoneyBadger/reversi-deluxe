#!/usr/bin/env python3
"""
Iago Deluxe - Main launcher
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from game import Game  # noqa: E402


def main():
    """Main function"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
