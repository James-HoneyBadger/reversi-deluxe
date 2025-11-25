"""
Main game class for Iago Deluxe
"""

import pygame as pg
import sys
import math
import json
from typing import Tuple
from board import Board
from ai import AI
from config import *


class Game:
    """Main game class"""

    def __init__(self):
        pg.init()
        self.board_size = DEFAULT_BOARD_SIZE
        self.cell_size = CELL_SIZE
        self.margin = MARGIN
        self.ui_height = UI_HEIGHT

        self.screen_width = self.board_size * self.cell_size + 2 * self.margin
        self.screen_height = (
            self.board_size * self.cell_size + 2 * self.margin + self.ui_height
        )

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Iago Deluxe - Full Featured Edition")
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)

        # Initialize sound system
        pg.mixer.init()
        self.sounds = {}
        self._load_sounds()

        self.board = Board(self.board_size)
        self.ai = AI(difficulty=2)
        self.player_color = PLAYER_BLACK
        self.ai_color = PLAYER_WHITE
        self.show_valid_moves = True
        self.ai_thinking = False

        # Game state
        self.game_started = False
        self.selected_square = None

        # Animation state
        self.animations = []  # List of active animations
        self.animation_speed = ANIMATION_SPEED

        # Move history for undo/redo
        self.move_history = []  # Stack of game states
        self.redo_stack = []  # Stack for redo functionality

        # Statistics tracking
        self.stats = self._load_stats()
        self.current_game_moves = 0

    def _load_sounds(self):
        """Load sound effects"""
        # Create simple sound effects programmatically since we don't have audio files
        self.sounds = {
            "move": self._create_move_sound(),
            "win": self._create_win_sound(),
            "lose": self._create_lose_sound(),
            "draw": self._create_draw_sound(),
        }

    def _create_move_sound(self) -> pg.mixer.Sound:
        """Create a simple move sound effect"""
        # Create a short beep sound
        sample_rate = 44100
        duration = 0.1  # 100ms
        frequency = 800  # Hz

        samples = int(sample_rate * duration)
        buffer = bytearray()

        for i in range(samples):
            # Generate sine wave
            sample = int(127 + 50 * math.sin(2 * math.pi * frequency * i / sample_rate))
            buffer.append(sample)

        sound = pg.mixer.Sound(buffer=bytes(buffer))
        sound.set_volume(0.3)
        return sound

    def _create_win_sound(self) -> pg.mixer.Sound:
        """Create a victory sound effect"""
        sample_rate = 44100
        duration = 0.5
        buffer = bytearray()

        samples = int(sample_rate * duration)
        for i in range(samples):
            # Ascending tone
            freq = 400 + (i / samples) * 400
            sample = int(127 + 60 * math.sin(2 * math.pi * freq * i / sample_rate))
            buffer.append(sample)

        sound = pg.mixer.Sound(buffer=bytes(buffer))
        sound.set_volume(0.4)
        return sound

    def _create_lose_sound(self) -> pg.mixer.Sound:
        """Create a defeat sound effect"""
        sample_rate = 44100
        duration = 0.5
        buffer = bytearray()

        samples = int(sample_rate * duration)
        for i in range(samples):
            # Descending tone
            freq = 600 - (i / samples) * 300
            sample = int(127 + 40 * math.sin(2 * math.pi * freq * i / sample_rate))
            buffer.append(sample)

        sound = pg.mixer.Sound(buffer=bytes(buffer))
        sound.set_volume(0.3)
        return sound

    def _create_draw_sound(self) -> pg.mixer.Sound:
        """Create a draw sound effect"""
        sample_rate = 44100
        duration = 0.3
        buffer = bytearray()

        samples = int(sample_rate * duration)
        for i in range(samples):
            # Neutral tone
            sample = int(127 + 30 * math.sin(2 * math.pi * 500 * i / sample_rate))
            buffer.append(sample)

        sound = pg.mixer.Sound(buffer=bytes(buffer))
        sound.set_volume(0.2)
        return sound

    def play_sound(self, sound_name: str):
        """Play a sound effect if sound is enabled"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except (pg.error, ValueError, TypeError):
                pass  # Silently fail if sound can't be played

    def _load_stats(self) -> GameStats:
        """Load statistics from file"""
        try:
            with open("stats.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return GameStats(**data)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return GameStats()

    def _save_stats(self):
        """Save statistics to file"""
        try:
            with open("stats.json", "w", encoding="utf-8") as f:
                json.dump(asdict(self.stats), f, indent=2)
        except (OSError, TypeError):
            pass  # Silently fail

    def update_stats(self):
        """Update statistics based on game result"""
        self.stats.games_played += 1
        self.stats.total_moves += self.current_game_moves

        if self.board.winner == self.player_color:
            self.stats.games_won += 1
        elif self.board.winner == self.ai_color:
            self.stats.games_lost += 1
        else:
            self.stats.games_drawn += 1

        black_score, white_score = self.board.get_score()
        if self.player_color == PLAYER_BLACK:
            self.stats.best_score = max(self.stats.best_score, black_score)
        else:
            self.stats.best_score = max(self.stats.best_score, white_score)

        self._save_stats()

    def start_animation(
        self, row: int, col: int, player: int, anim_type: str = "place"
    ):
        """Start a piece animation"""
        animation = Animation(
            row=row,
            col=col,
            player=player,
            start_time=pg.time.get_ticks() / 1000.0,
            duration=self.animation_speed,
            anim_type=anim_type,
        )
        self.animations.append(animation)

    def update_animations(self):
        """Update active animations"""
        current_time = pg.time.get_ticks() / 1000.0
        # Remove completed animations
        self.animations = [
            anim
            for anim in self.animations
            if current_time - anim.start_time < anim.duration
        ]

    def save_game_state(self):
        """Save current game state for undo functionality"""
        state = GameState(
            board_grid=[row[:] for row in self.board.grid],
            current_player=self.board.current_player,
            move_history=[],  # We'll handle this separately
            black_score=self.board.get_score()[0],
            white_score=self.board.get_score()[1],
            game_over=self.board.game_over,
            winner=self.board.winner,
            settings={},
        )
        self.move_history.append(state)
        # Clear redo stack when new move is made
        self.redo_stack.clear()

    def undo_move(self):
        """Undo the last move"""
        if self.move_history:
            # Save current state to redo stack
            current_state = GameState(
                board_grid=[row[:] for row in self.board.grid],
                current_player=self.board.current_player,
                move_history=[],
                black_score=self.board.get_score()[0],
                white_score=self.board.get_score()[1],
                game_over=self.board.game_over,
                winner=self.board.winner,
                settings={},
            )
            self.redo_stack.append(current_state)

            # Restore previous state
            prev_state = self.move_history.pop()
            self.board.grid = [row[:] for row in prev_state.board_grid]
            self.board.current_player = prev_state.current_player
            self.board.game_over = prev_state.game_over
            self.board.winner = prev_state.winner

            # Clear animations
            self.animations.clear()

    def redo_move(self):
        """Redo the last undone move"""
        if self.redo_stack:
            # Save current state to history
            current_state = GameState(
                board_grid=[row[:] for row in self.board.grid],
                current_player=self.board.current_player,
                move_history=[],
                black_score=self.board.get_score()[0],
                white_score=self.board.get_score()[1],
                game_over=self.board.game_over,
                winner=self.board.winner,
                settings={},
            )
            self.move_history.append(current_state)

            # Restore redo state
            redo_state = self.redo_stack.pop()
            self.board.grid = [row[:] for row in redo_state.board_grid]
            self.board.current_player = redo_state.current_player
            self.board.game_over = redo_state.game_over
            self.board.winner = redo_state.winner

            # Clear animations
            self.animations.clear()

    def save_game(self, filename: str = "saved_game.json"):
        """Save current game state to file"""
        try:
            game_state = GameState(
                board_grid=self.board.grid,
                current_player=self.board.current_player,
                move_history=[],  # Could be extended to save full history
                black_score=self.board.get_score()[0],
                white_score=self.board.get_score()[1],
                game_over=self.board.game_over,
                winner=self.board.winner,
                settings={
                    "theme": "Classic",  # Could be extended
                    "sound_enabled": True,
                    "show_hints": self.show_valid_moves,
                    "ai_difficulty": self.ai.difficulty,
                    "board_size": self.board_size,
                    "player_color": self.player_color,
                },
            )

            # Convert to dictionary for JSON serialization
            state_dict = {
                "board_grid": game_state.board_grid,
                "current_player": game_state.current_player,
                "black_score": game_state.black_score,
                "white_score": game_state.white_score,
                "game_over": game_state.game_over,
                "winner": game_state.winner,
                "settings": game_state.settings,
                "timestamp": pg.time.get_ticks() / 1000.0,
            }

            with open(filename, "w") as f:
                json.dump(state_dict, f, indent=2)

            return True
        except Exception:
            return False

    def load_game(self, filename: str = "saved_game.json"):
        """Load game state from file"""
        try:
            with open(filename, "r") as f:
                state_dict = json.load(f)

            # Restore board state
            self.board.grid = state_dict["board_grid"]
            self.board.current_player = state_dict["current_player"]
            self.board.game_over = state_dict["game_over"]
            self.board.winner = state_dict["winner"]

            # Restore settings
            settings = state_dict.get("settings", {})
            self.show_valid_moves = settings.get("show_hints", True)
            self.ai.difficulty = settings.get("ai_difficulty", 2)
            self.player_color = settings.get("player_color", PLAYER_BLACK)
            self.ai_color = 3 - self.player_color

            # Clear history and animations
            self.move_history.clear()
            self.redo_stack.clear()
            self.animations.clear()

            return True
        except Exception:
            return False

    def get_animation_scale(self, row: int, col: int) -> float:
        """Get the current scale for an animated piece"""
        for anim in self.animations:
            if anim.row == row and anim.col == col:
                current_time = pg.time.get_ticks() / 1000.0
                progress = (current_time - anim.start_time) / anim.duration
                progress = min(max(progress, 0.0), 1.0)  # Clamp to [0, 1]

                if anim.anim_type == "place":
                    # Smooth scale in
                    scale_diff = anim.end_scale - anim.start_scale
                    return anim.start_scale + scale_diff * progress
                elif anim.anim_type == "flip":
                    # Pulse effect for flipping
                    if progress < 0.5:
                        return 1.0 - progress * 0.3
                    else:
                        return 0.85 + (progress - 0.5) * 0.3
        return 1.0  # No animation

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pg.quit()
        sys.exit()

    def handle_events(self):
        """Handle user input"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)
            elif event.type == pg.KEYDOWN:
                self.handle_key(event.key)

    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click"""
        x, y = pos

        # Check if click is on board
        board_x = x - MARGIN
        board_y = y - MARGIN

        if (
            0 <= board_x < self.board_size * self.cell_size
            and 0 <= board_y < self.board_size * self.cell_size
        ):
            col = board_x // CELL_SIZE
            row = board_y // CELL_SIZE

            if self.board.current_player == self.player_color:
                if self.board.is_valid_move(row, col, self.player_color):
                    self.make_player_move(row, col)

    def handle_key(self, key):
        """Handle keyboard input"""
        if key == pg.K_r:  # Reset game
            self.board.reset()
            self.move_history.clear()
            self.redo_stack.clear()
            self.animations.clear()
            self.game_started = False
            self.current_game_moves = 0
        elif key == pg.K_h:  # Toggle hints
            self.show_valid_moves = not self.show_valid_moves
        elif key == pg.K_u:  # Undo move
            self.undo_move()
        elif key == pg.K_y:  # Redo move
            self.redo_move()
        elif key == pg.K_s:  # Save game
            self.save_game()
        elif key == pg.K_l:  # Load game
            self.load_game()
        elif key == pg.K_ESCAPE:  # Quit
            pg.quit()
            sys.exit()

    def make_player_move(self, row: int, col: int):
        """Make a player move"""
        # Save state before move for undo functionality
        self.save_game_state()

        flipped = self.board.make_move(row, col, self.player_color)
        self.start_animation(row, col, self.player_color, "place")

        # Animate flipped pieces
        for flip_row, flip_col in flipped:
            self.start_animation(flip_row, flip_col, self.player_color, "flip")

        self.play_sound("move")
        self.current_game_moves += 1
        self.board.switch_player()
        self.board.check_game_over()

        # Check for game end
        if self.board.game_over:
            self.update_stats()
            if self.board.winner == self.player_color:
                self.play_sound("win")
            elif self.board.winner == self.ai_color:
                self.play_sound("lose")
            else:
                self.play_sound("draw")

        # AI turn
        if not self.board.game_over and self.board.current_player == self.ai_color:
            self.ai_thinking = True

    def update(self):
        """Update game state"""
        self.update_animations()

        if self.ai_thinking and self.board.current_player == self.ai_color:
            move = self.ai.get_move(self.board)
            if move:
                flipped = self.board.make_move(move[0], move[1], self.ai_color)
                self.start_animation(move[0], move[1], self.ai_color, "place")

                # Animate flipped pieces
                for flip_row, flip_col in flipped:
                    self.start_animation(flip_row, flip_col, self.ai_color, "flip")

                self.play_sound("move")
                self.current_game_moves += 1
                self.board.switch_player()
                self.board.check_game_over()

                # Check for game end after AI move
                if self.board.game_over:
                    self.update_stats()
                    if self.board.winner == self.player_color:
                        self.play_sound("win")
                    elif self.board.winner == self.ai_color:
                        self.play_sound("lose")
                    else:
                        self.play_sound("draw")

            self.ai_thinking = False

    def draw(self):
        """Draw everything"""
        self.screen.fill(GREEN)

        # Draw board
        self.draw_board()

        # Draw pieces
        self.draw_pieces()

        # Draw valid moves
        if self.show_valid_moves and self.board.current_player == self.player_color:
            self.draw_valid_moves()

        # Draw UI
        self.draw_ui()

        pg.display.flip()

    def draw_board(self):
        """Draw the game board"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE

                # Alternate colors for checkerboard pattern
                color = LIGHT_GRAY if (row + col) % 2 == 0 else DARK_GREEN
                pg.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))

                # Draw grid lines
                pg.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def draw_pieces(self):
        """Draw game pieces"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board.grid[row][col]
                if piece != EMPTY:
                    x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
                    y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2

                    # Get animation scale
                    scale = self.get_animation_scale(row, col)
                    radius = int((CELL_SIZE // 2 - 5) * scale)

                    color = BLACK if piece == PLAYER_BLACK else WHITE
                    pg.draw.circle(self.screen, color, (x, y), radius)
                    if scale > 0.8:  # Only draw outline when piece is mostly formed
                        outline_radius = max(1, int(radius * 0.9))
                        pg.draw.circle(self.screen, BLACK, (x, y), outline_radius, 2)

    def draw_valid_moves(self):
        """Draw valid move indicators"""
        valid_moves = self.board.get_valid_moves(self.board.current_player)
        for row, col in valid_moves:
            x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
            y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
            radius = 8

            pg.draw.circle(self.screen, BLUE, (x, y), radius)
            pg.draw.circle(self.screen, BLACK, (x, y), radius, 1)

    def draw_ui(self):
        """Draw user interface"""
        ui_y = self.margin + self.board_size * self.cell_size + 10

        # Score
        black_score, white_score = self.board.get_score()
        score_text = f"Black: {black_score}  White: {white_score}"
        score_surf = self.font.render(score_text, True, BLACK)
        self.screen.blit(score_surf, (MARGIN, ui_y))

        # Current player
        player_text = (
            "Black's turn"
            if self.board.current_player == PLAYER_BLACK
            else "White's turn"
        )
        if self.board.game_over:
            if self.board.winner == PLAYER_BLACK:
                player_text = "Black wins!"
            elif self.board.winner == PLAYER_WHITE:
                player_text = "White wins!"
            else:
                player_text = "It's a draw!"

        player_surf = self.font.render(
            player_text, True, RED if self.board.game_over else BLACK
        )
        self.screen.blit(player_surf, (MARGIN, ui_y + 40))

        # Instructions
        instructions = [
            "Click to place pieces",
            "R: Reset game",
            "H: Toggle hints",
            "U: Undo move",
            "Y: Redo move",
            "S: Save game",
            "L: Load game",
            "ESC: Quit",
        ]

        for i, text in enumerate(instructions):
            instr_surf = self.small_font.render(text, True, GRAY)
            self.screen.blit(instr_surf, (self.screen_width - 200, ui_y + i * 25))

        # AI thinking indicator
        if self.ai_thinking:
            thinking_surf = self.small_font.render("AI thinking...", True, RED)
            self.screen.blit(thinking_surf, (MARGIN, ui_y + 70))
