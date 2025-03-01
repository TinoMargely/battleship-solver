from abc import ABC, abstractmethod
from typing import Tuple, List
import random

from battleship.core import CellState


class Strategy(ABC):
    """Abstract base class for battleship shooting strategies."""

    def __init__(self, board_size: int = 10):
        """
        Initialize the strategy.

        Args:
            board_size: Size of the board (default: 10x10)
        """
        self.board_size = board_size
        self.shots: List[Tuple[int, int]] = []
        self.hits: List[Tuple[int, int]] = []
        self.misses: List[Tuple[int, int]] = []

    @abstractmethod
    def get_next_shot(self) -> Tuple[int, int]:
        """
        Determine the next position to shoot.

        Returns:
            Tuple[int, int]: The (row, col) position to target
        """
        pass

    def register_result(self, position: Tuple[int, int], result: CellState):
        """
        Register the result of a shot.

        Args:
            position: The (row, col) position that was shot
            result: The result of the shot (HIT or MISS)
        """
        self.shots.append(position)

        if result == CellState.HIT:
            self.hits.append(position)
        elif result == CellState.MISS:
            self.misses.append(position)

    def get_available_positions(self) -> List[Tuple[int, int]]:
        """
        Get all positions that haven't been shot at yet.

        Returns:
            List[Tuple[int, int]]: List of available positions
        """
        return [
            (row, col)
            for row in range(self.board_size)
            for col in range(self.board_size)
            if (row, col) not in self.shots
        ]

    def reset(self):
        """Reset the strategy state."""
        self.shots = []
        self.hits = []
        self.misses = []


class RandomStrategy(Strategy):
    """A strategy that selects shots randomly."""

    def get_next_shot(self) -> Tuple[int, int]:
        """
        Choose a random position from the available positions.

        Returns:
            Tuple[int, int]: The (row, col) position to target
        """
        available = self.get_available_positions()
        if not available:
            # No available positions, return an invalid position
            return (-1, -1)

        return random.choice(available)

