# Iago Deluxe - User Guide

## Getting Started

### Installation
1. Ensure Python 3.7+ is installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py` or `python src/Reversi.py`

### First Game
1. The game starts with 4 pieces in the center
2. Black moves first
3. Click on valid squares (shown with blue circles) to place pieces
4. Goal: Have more pieces than opponent when board is full

## Gameplay

### Basic Rules
- Pieces must flank opponent pieces
- Flanked pieces are captured and flip to your color
- Game ends when no valid moves remain
- Player with most pieces wins

### Advanced Features

#### AI Opponents
- **Easy**: Random moves
- **Medium**: Prefers corners and edges
- **Hard**: Uses minimax strategy
- **Expert**: Advanced evaluation

#### Move Hints
- Press 'H' to toggle valid move indicators
- Blue circles show where you can play

#### Undo/Redo
- Press 'U' to undo last move
- Press 'Y' to redo undone move

#### Save/Load
- Press 'S' to save current game
- Press 'L' to load saved game
- Games saved as JSON files

## Statistics

The game tracks:
- Games played
- Win/loss/draw record
- Total moves made
- Best score achieved

Statistics are automatically saved and persist between sessions.

## Troubleshooting

### Game Won't Start
- Ensure Pygame is installed: `pip install pygame`
- Check Python version: `python --version`

### No Sound
- Sound is generated programmatically
- May not work on all systems
- Game functions normally without sound

### Performance Issues
- Expert AI may be slow on complex boards
- Try Medium or Hard difficulty for better performance

## Tips

- Control the corners early
- Avoid moves that give corners to opponent
- Keep pieces connected when possible
- Use undo to explore different strategies