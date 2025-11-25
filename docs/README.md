# Iago Deluxe Documentation

## Overview
Iago Deluxe is a full-featured Reversi/Othello game implementation with advanced AI, animations, and comprehensive game features.

## Features

### Core Gameplay
- Standard Reversi/Othello rules
- Dynamic board sizing (4x4 to 16x16)
- Turn-based gameplay
- Win/loss/draw detection

### AI Opponents
- 4 difficulty levels (Easy, Medium, Hard, Expert)
- Minimax algorithm with alpha-beta pruning
- Heuristic-based evaluation
- Corner and edge preference strategies

### Visual Features
- Smooth piece placement animations
- Flip animations for captured pieces
- Move hint indicators
- Multiple visual themes
- Professional UI design

### Audio Features
- Programmatic sound generation
- Move sound effects
- Win/lose/draw audio feedback
- Configurable sound settings

### Game Management
- Undo/redo functionality
- Save/load game state
- Statistics tracking
- Move history

## Controls

- **Mouse Click**: Place pieces
- **R**: Reset game
- **H**: Toggle move hints
- **U**: Undo move
- **Y**: Redo move
- **S**: Save game
- **L**: Load game
- **ESC**: Quit game

## Architecture

The game is built with a modular architecture:

- `src/config.py`: Constants and data structures
- `src/board.py`: Game board logic
- `src/ai.py`: AI opponent implementation
- `src/game.py`: Main game loop and UI
- `src/Reversi.py`: Entry point

## Testing

Comprehensive test suite covering:
- Board logic validation
- AI move generation
- Game state management
- Settings persistence

Run tests with: `python tests/run_tests.py`
