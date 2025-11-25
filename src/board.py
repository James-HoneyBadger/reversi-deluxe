"""
Board logic for Reversi/Othello game
"""

from typing import List, Tuple
from config import EMPTY, PLAYER_BLACK, PLAYER_WHITE, DEFAULT_BOARD_SIZE


class Board:
    """Reversi game board"""

    def __init__(self, size: int = DEFAULT_BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.current_player = PLAYER_BLACK
        self.game_over = False
        self.winner = None
        self.reset()

    def reset(self):
        """Reset the board to initial state"""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        # Place initial pieces
        center = self.size // 2
        self.grid[center - 1][center - 1] = PLAYER_WHITE
        self.grid[center - 1][center] = PLAYER_BLACK
        self.grid[center][center - 1] = PLAYER_BLACK
        self.grid[center][center] = PLAYER_WHITE
        self.current_player = PLAYER_BLACK
        self.game_over = False
        self.winner = None

    def is_valid_move(self, row: int, col: int, player: int) -> bool:
        """Check if a move is valid"""
        if self.grid[row][col] != EMPTY:
            return False

        # Check all 8 directions
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for dr, dc in directions:
            if self._would_flip(row, col, dr, dc, player):
                return True

        return False

    def _would_flip(self, row: int, col: int, dr: int, dc: int, player: int) -> bool:
        """Check if pieces would be flipped in a direction"""
        r, c = row + dr, col + dc
        opponent = 3 - player  # Switch player
        found_opponent = False

        while 0 <= r < self.size and 0 <= c < self.size:
            if self.grid[r][c] == EMPTY:
                return False
            if self.grid[r][c] == opponent:
                found_opponent = True
            elif self.grid[r][c] == player:
                return found_opponent
            r += dr
            c += dc

        return False

    def get_valid_moves(self, player: int) -> List[Tuple[int, int]]:
        """Get all valid moves for a player"""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves

    def make_move(self, row: int, col: int, player: int) -> List[Tuple[int, int]]:
        """Make a move and return flipped pieces"""
        if not self.is_valid_move(row, col, player):
            return []

        self.grid[row][col] = player
        flipped = []

        # Check all directions and flip pieces
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for dr, dc in directions:
            flipped.extend(self._flip_direction(row, col, dr, dc, player))

        # Switch to the other player
        self.switch_player()

        return flipped

    def _flip_direction(
        self, row: int, col: int, dr: int, dc: int, player: int
    ) -> List[Tuple[int, int]]:
        """Flip pieces in a direction"""
        r, c = row + dr, col + dc
        opponent = 3 - player
        to_flip = []

        while 0 <= r < self.size and 0 <= c < self.size:
            if self.grid[r][c] == opponent:
                to_flip.append((r, c))
            elif self.grid[r][c] == player:
                # Flip all pieces in between
                for fr, fc in to_flip:
                    self.grid[fr][fc] = player
                return to_flip
            else:
                break
            r += dr
            c += dc

        return []

    def get_score(self) -> Tuple[int, int]:
        """Get current score (black, white)"""
        black = sum(row.count(PLAYER_BLACK) for row in self.grid)
        white = sum(row.count(PLAYER_WHITE) for row in self.grid)
        return black, white

    def check_game_over(self):
        """Check if game is over"""
        black_moves = self.get_valid_moves(PLAYER_BLACK)
        white_moves = self.get_valid_moves(PLAYER_WHITE)

        if not black_moves and not white_moves:
            self.game_over = True
            black_score, white_score = self.get_score()
            if black_score > white_score:
                self.winner = PLAYER_BLACK
            elif white_score > black_score:
                self.winner = PLAYER_WHITE
            else:
                self.winner = 0  # Draw
            return True

        # Skip turn if no moves
        if not (black_moves if self.current_player == PLAYER_BLACK else white_moves):
            self.current_player = 3 - self.current_player
            return False

        return False

    def switch_player(self):
        """Switch to the other player"""
        self.current_player = 3 - self.current_player
