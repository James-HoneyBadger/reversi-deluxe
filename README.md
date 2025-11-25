# Iago Deluxe - Clean Edition

A clean, simple, and working implementation of the classic Reversi (Othello) board game.

## ✨ Features

- **Clean Codebase** - Simple, readable Python code
- **Working AI** - Intelligent computer opponent with 3 difficulty levels
- **Beautiful Graphics** - Smooth pygame graphics with checkerboard board
- **Move Validation** - Clear indicators for legal moves
- **Score Tracking** - Real-time score display
- **Game Over Detection** - Proper win/loss/draw detection

## 🎮 How to Play

1. **Black moves first** - Click on any highlighted blue circle to place a piece
2. **Capture opponent pieces** - Pieces are flipped when surrounded
3. **Control the board** - The player with more pieces at the end wins
4. **No moves?** - Turn passes to the other player

### Controls
- **Mouse Click** - Place piece on valid squares
- **R** - Reset game
- **H** - Toggle move hints
- **ESC** - Quit game

## 🚀 Quick Start

### Requirements
- Python 3.6+
- pygame

### Installation & Running

```bash
# Install dependencies
pip install pygame

# Run the game
python3 main.py
```

Or use the provided launcher:
```bash
./play.sh
```

## 🎯 Game Rules

Reversi (also known as Othello) is played on an 8x8 board with 64 discs. Players take turns placing discs on the board with their color facing up.

- **Objective**: Have more discs of your color than your opponent when the board is full
- **Valid Moves**: You can only place a disc if it captures at least one opponent disc
- **Capturing**: When you place a disc, all opponent discs between your new disc and another of your discs are flipped to your color
- **Game End**: Game ends when neither player can make a valid move

## 🤖 AI Difficulty

- **Easy (1)** - Random moves
- **Medium (2)** - Prefers corners and edges
- **Hard (3)** - Uses minimax algorithm

## 📁 Project Structure

```
Iago_Deluxe/
├── main.py          # Main game file
├── requirements.txt # Dependencies
├── play.sh         # Launcher script
├── setup.sh        # Setup script
└── README.md       # This file
```

## 🔧 Development

The entire game is contained in a single `main.py` file for simplicity and clarity. The code is well-commented and easy to understand.

### Key Classes
- `Board` - Game board logic and move validation
- `AI` - Computer opponent with different difficulty levels
- `Game` - Main game loop and user interface

## 📝 License

This project is open source and available under the MIT License.
./play.sh
```

**Direct execution:**
```bash
.venv/bin/python3 main.py
```

**With system Python (if pygame installed globally):**
```bash
python3 main.py
```

### Command-Line Options

The game supports extensive command-line configuration:

```bash
# Display help
./play.sh --help

# Custom board size (4, 6, 8, 10, 12, 14, or 16)
./play.sh -s 10

# Set AI difficulty (1-6) and theme
./play.sh -d 5 -t midnight

# Disable sound effects
./play.sh --no-sound

# Disable hints
./play.sh --no-hints

# Enable debug logging
./play.sh --debug

# Combination example: 10x10 board, hard AI, ocean theme
./play.sh -s 10 -d 5 -t ocean
```

## 📁 Project Structure

```
Iago_Deluxe/
├── main.py                  # Entry point with dependency management
├── play.sh                  # Convenient launcher script
├── setup.sh                 # Installation and environment setup
├── requirements.txt         # Python dependencies
├── .flake8                  # Linting configuration
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── Iago.py             # Main game implementation (5000+ lines)
│   ├── config.py           # Configuration constants and settings
│   ├── logger.py           # Logging system with file rotation
│   └── error_handling.py   # Custom exceptions and validation
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── run_tests.py        # Test runner
│   ├── test_board.py       # Board logic tests
│   ├── test_ai.py          # AI behavior tests
│   ├── test_settings.py    # Settings management tests
│   ├── test_ai_levels.py   # AI difficulty verification
│   └── verify_ai_levels.py # AI performance benchmarking
│
├── docs/                    # Documentation
│   ├── README.md           # Documentation index
│   ├── DEVELOPMENT.md      # Architecture and technical details
│   ├── QUICK_REFERENCE.md  # Command reference and shortcuts
│   ├── IMPLEMENTATION_SUMMARY.md  # Feature implementation notes
│   ├── IMPROVEMENTS.md     # Enhancement history
│   ├── ENHANCEMENTS.md     # Detailed feature descriptions
│   ├── AI_LEVELS_VERIFICATION.md  # AI testing methodology
│   └── MENU_IMPROVEMENTS.txt      # UI enhancement notes
│
├── assets/                  # Game assets
│   └── iago-icon.png       # Application icon
│
├── config/                  # Runtime configuration
│   └── iago-settings.json   # User preferences (auto-generated)
│
└── data/                    # Game data
    └── *.pgn, *.json       # Saved games (auto-generated)
```

## 🎯 Game Controls

### Mouse Controls
- **Click** - Make a move on highlighted squares
- **Menu Navigation** - Click menu items or use hover effects

### Keyboard Shortcuts
- **ESC** - Toggle pause menu
- **U** - Undo move
- **R** - Redo move
- **H** - Toggle hints
- **S** - Save game
- **N** - New game

### Menu System
- **Game Menu** - New game, board size, save/load, quit
- **AI Menu** - Difficulty levels, AI color selection
- **Settings Menu** - Themes, sound, hints, move preview
- **View Menu** - Analysis window, statistics, tutorial

## 🛠️ Development

### Requirements
- **Python 3.7+** (tested on 3.13)
- **Pygame 2.0+**
- **Linux/macOS/Windows** (cross-platform)

### Running Tests
```bash
# Run all tests
.venv/bin/python3 tests/run_tests.py

# Run specific test file
.venv/bin/python3 -m pytest tests/test_board.py

# Run with coverage
.venv/bin/python3 -m pytest --cov=src tests/

# Verify AI difficulty levels
.venv/bin/python3 tests/verify_ai_levels.py
```

### Code Quality
```bash
# Run linter
.venv/bin/python3 -m flake8 src/ tests/

# Format code (if black is installed)
.venv/bin/python3 -m black src/ tests/
```

### Architecture Highlights
- **Minimax AI** with alpha-beta pruning and transposition tables
- **Move Analysis System** evaluating strategic factors
- **Settings Persistence** via JSON configuration
- **Modular Design** with clear separation of concerns
- **Comprehensive Logging** for debugging and monitoring
- **Error Handling** with custom exception hierarchy

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- **[Documentation Index](docs/README.md)** - Overview of all documentation
- **[Development Guide](docs/DEVELOPMENT.md)** - Architecture and implementation details
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Commands and shortcuts
- **[AI Verification](docs/AI_LEVELS_VERIFICATION.md)** - AI testing methodology

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Classic Reversi/Othello game rules
- Pygame community for excellent documentation
- Python community for best practices

## 📧 Contact

**Author:** James "HoneyBadger"  
**Repository:** [https://github.com/James-HoneyBadger/Iago_Deluxe](https://github.com/James-HoneyBadger/Iago_Deluxe)

---

**Version:** 2.0 - Refactored Edition  
**Last Updated:** November 19, 2025
