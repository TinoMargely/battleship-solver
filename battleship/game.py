from typing import Dict, Tuple, Optional
from battleship.core import Board, CellState
from battleship.strategy import Strategy, RandomStrategy


class Game:
    """Manages a game of Battleship with customizable strategies."""

    def __init__(self, board_size: int = 10, ai_strategy: Optional[Strategy] = None):
        """
        Initialize a game.

        Args:
            board_size: Size of the game board (default: 10x10)
            ai_strategy: Strategy for the AI player (default: RandomStrategy)
        """
        self.player_board = Board(board_size)
        self.ai_board = Board(board_size)
        self.board_size = board_size
        self.turn_count = 0
        self.game_over = False
        self.winner = None

        # Set AI strategy
        if ai_strategy is None:
            self.ai_strategy = RandomStrategy(board_size)
        else:
            self.ai_strategy = ai_strategy

    def setup_game(self):
        """Set up the game by placing ships on both boards."""
        # Place ships randomly for both players
        self.player_board.random_placement()
        self.ai_board.random_placement()

        # Reset the AI strategy
        self.ai_strategy.reset()

    def player_shoot(self, position: Tuple[int, int]) -> CellState:
        """
        Process a player's shot.

        Args:
            position: (row, col) tuple indicating the shot position

        Returns:
            CellState: The result of the shot
        """
        if self.game_over:
            return CellState.UNKNOWN

        result = self.ai_board.receive_shot(position)

        # Check if game is over
        if self.ai_board.are_all_ships_sunk():
            self.game_over = True
            self.winner = "Player"

        return result

    def ai_shoot(self) -> Tuple[Tuple[int, int], CellState]:
        """
        Process an AI shot based on the current strategy.

        Returns:
            Tuple[Tuple[int, int], CellState]: The shot position and result
        """
        if self.game_over:
            return ((-1, -1), CellState.UNKNOWN)

        # Get next shot position from strategy
        position = self.ai_strategy.get_next_shot()

        if position == (-1, -1):
            return ((-1, -1), CellState.UNKNOWN)  # No available positions

        # Process the shot
        result = self.player_board.receive_shot(position)

        # Register the result with the strategy
        self.ai_strategy.register_result(position, result)

        # Check if game is over
        if self.player_board.are_all_ships_sunk():
            self.game_over = True
            self.winner = "AI"

        return (position, result)

    def play_turn(self, player_shot_position: Tuple[int, int]) -> Dict:
        """
        Play a single turn of the game.

        Args:
            player_shot_position: The position the player wants to shoot

        Returns:
            Dict: Information about the turn results
        """
        if self.game_over:
            return {
                "game_over": True,
                "winner": self.winner
            }

        self.turn_count += 1

        # Player's turn
        player_result = self.player_shoot(player_shot_position)

        # Check if player won
        if self.game_over:
            return {
                "player_shot": player_shot_position,
                "player_result": player_result,
                "game_over": True,
                "winner": self.winner
            }

        # AI's turn
        ai_position, ai_result = self.ai_shoot()

        return {
            "player_shot": player_shot_position,
            "player_result": player_result,
            "ai_shot": ai_position,
            "ai_result": ai_result,
            "game_over": self.game_over,
            "winner": self.winner,
            "turn_count": self.turn_count
        }

    def display_boards(self):
        """Display both game boards."""
        print("\nPlayer's Board:")
        self.player_board.print_board(show_ships=True)

        print("\nAI's Board:")
        self.ai_board.print_board(show_ships=False)

        print("\nLegend: · = Unknown, O = Miss, X = Hit, S = Ship")
