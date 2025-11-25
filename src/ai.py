"""
AI logic for Reversi/Othello game
"""

import random
from typing import Optional, Tuple, List
from board import Board
from config import PLAYER_BLACK


class AI:
    """Simple AI for the game"""

    def __init__(self, difficulty: int = 1):
        self.difficulty = difficulty  # 1-3, higher is better

    def get_move(self, board: Board) -> Optional[Tuple[int, int]]:
        """Get AI move"""
        valid_moves = board.get_valid_moves(board.current_player)
        if not valid_moves:
            return None

        if self.difficulty == 1:
            # Random move
            return random.choice(valid_moves)
        elif self.difficulty == 2:
            # Prefer corners and edges
            return self._get_best_move_simple(board, valid_moves)
        else:
            # Simple minimax
            return self._get_best_move_minimax(board, valid_moves)

    def _get_best_move_simple(
        self, board: Board, valid_moves: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        """Simple heuristic: prefer corners, then edges, then center"""
        size = board.size
        corners = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
        edges = []

        # Add edge positions (excluding corners)
        for i in range(1, size - 1):
            edges.extend([(0, i), (size - 1, i), (i, 0), (i, size - 1)])

        # Score moves
        best_move = None
        best_score = -1

        for move in valid_moves:
            score = 1  # Base score

            if move in corners:
                score += 10
            elif move in edges:
                score += 3
            else:
                # Center preference
                row, col = move
                center_start = size // 2 - 1
                center_end = size // 2 + 1
                if (
                    center_start <= row <= center_end
                    and center_start <= col <= center_end
                ):
                    score += 2

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _get_best_move_minimax(
        self, board: Board, valid_moves: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        """Enhanced minimax with alpha-beta pruning and better evaluation"""
        best_move = None
        best_score = -float("inf")
        alpha = -float("inf")
        beta = float("inf")

        # Use deeper search for expert level
        depth = 4 if self.difficulty == 3 else 2

        for move in valid_moves:
            # Try the move
            board_copy = self._copy_board(board)
            board_copy.make_move(move[0], move[1], board.current_player)
            board_copy.switch_player()

            # Evaluate with alpha-beta pruning
            score = self._minimax_alpha_beta(board_copy, depth - 1, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move

    def _minimax_alpha_beta(
        self, board: Board, depth: int, maximizing: bool, alpha: float, beta: float
    ) -> int:
        """Minimax with alpha-beta pruning"""
        if depth == 0 or board.check_game_over():
            return self._evaluate_board_advanced(board)

        valid_moves = board.get_valid_moves(board.current_player)

        if not valid_moves:
            # No moves available, pass turn
            board_copy = self._copy_board(board)
            board_copy.switch_player()
            return self._minimax_alpha_beta(
                board_copy, depth - 1, not maximizing, alpha, beta
            )

        if maximizing:
            max_eval = -float("inf")
            for move in valid_moves:
                board_copy = self._copy_board(board)
                board_copy.make_move(move[0], move[1], board.current_player)
                board_copy.switch_player()
                eval_score = self._minimax_alpha_beta(
                    board_copy, depth - 1, False, alpha, beta
                )
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float("inf")
            for move in valid_moves:
                board_copy = self._copy_board(board)
                board_copy.make_move(move[0], move[1], board.current_player)
                board_copy.switch_player()
                eval_score = self._minimax_alpha_beta(
                    board_copy, depth - 1, True, alpha, beta
                )
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def _evaluate_board_advanced(self, board: Board) -> int:
        """Advanced board evaluation with positional values and mobility"""
        if board.game_over:
            if board.winner == board.current_player:
                return 10000
            elif board.winner == 0:  # Draw
                return 0
            else:
                return -10000

        black_score, white_score = board.get_score()
        current_player = board.current_player
        opponent = 3 - current_player

        # Base score difference
        if current_player == PLAYER_BLACK:
            score = black_score - white_score
        else:
            score = white_score - black_score

        # Positional value (corners are worth more)
        positional_value = self._calculate_positional_value(
            board, current_player
        ) - self._calculate_positional_value(board, opponent)

        # Mobility (number of valid moves)
        current_mobility = len(board.get_valid_moves(current_player))
        opponent_mobility = len(board.get_valid_moves(opponent))
        mobility_value = 10 * (current_mobility - opponent_mobility)

        # Corner control bonus
        corner_value = self._calculate_corner_value(
            board, current_player
        ) - self._calculate_corner_value(board, opponent)

        # Edge control bonus
        edge_value = self._calculate_edge_value(
            board, current_player
        ) - self._calculate_edge_value(board, opponent)

        total_score = (
            score * 10
            + positional_value
            + mobility_value
            + corner_value * 20
            + edge_value * 5
        )

        return total_score

    def _calculate_positional_value(self, board: Board, player: int) -> int:
        """Calculate positional value for a player"""
        size = board.size
        value = 0

        # Position values (corners highest, edges medium, center low)
        position_weights = [[0] * size for _ in range(size)]

        # Corners
        position_weights[0][0] = 100
        position_weights[0][size - 1] = 100
        position_weights[size - 1][0] = 100
        position_weights[size - 1][size - 1] = 100

        # Edges (excluding corners)
        for i in range(1, size - 1):
            position_weights[0][i] = 10
            position_weights[size - 1][i] = 10
            position_weights[i][0] = 10
            position_weights[i][size - 1] = 10

        # Count pieces in valuable positions
        for row in range(size):
            for col in range(size):
                if board.grid[row][col] == player:
                    value += position_weights[row][col]

        return value

    def _calculate_corner_value(self, board: Board, player: int) -> int:
        """Calculate corner control value"""
        size = board.size
        corners = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
        value = 0

        for row, col in corners:
            if board.grid[row][col] == player:
                value += 1

        return value

    def _calculate_edge_value(self, board: Board, player: int) -> int:
        """Calculate edge control value (excluding corners)"""
        size = board.size
        value = 0

        # Top and bottom edges
        for col in range(1, size - 1):
            if board.grid[0][col] == player:
                value += 1
            if board.grid[size - 1][col] == player:
                value += 1

        # Left and right edges
        for row in range(1, size - 1):
            if board.grid[row][0] == player:
                value += 1
            if board.grid[row][size - 1] == player:
                value += 1

        return value

    def _copy_board(self, board: Board) -> Board:
        """Create a copy of the board"""
        new_board = Board()
        new_board.grid = [row[:] for row in board.grid]
        new_board.current_player = board.current_player
        new_board.game_over = board.game_over
        new_board.winner = board.winner
        return new_board
