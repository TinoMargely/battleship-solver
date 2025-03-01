import random
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class CellState(Enum):
    """Represents the state of a cell on the board."""
    UNKNOWN = 0  # Not yet targeted
    MISS = 1     # Targeted, no ship
    HIT = 2      # Targeted, hit a ship


class ShipType(Enum):
    """Types of ships in the game with their respective sizes."""
    CARRIER = 5
    BATTLESHIP = 4
    CRUISER = 3
    SUBMARINE = 3
    DESTROYER = 2


class Orientation(Enum):
    """Ship orientation."""
    HORIZONTAL = 0
    VERTICAL = 1


class Ship:
    """Represents a ship in the game."""

    def __init__(self, ship_type: ShipType, orientation: Orientation, start_position: Tuple[int, int]):
        """
        Initialize a ship.

        Args:
            ship_type: Type of the ship
            orientation: Horizontal or vertical orientation
            start_position: (row, col) tuple indicating the starting position
        """
        self.ship_type = ship_type
        self.size = ship_type.value
        self.orientation = orientation
        self.start_position = start_position
        self.hit_positions: Set[Tuple[int, int]] = set()

    def is_sunk(self) -> bool:
        """Check if the ship is sunk (all positions hit)."""
        return len(self.hit_positions) == self.size

    def get_positions(self) -> List[Tuple[int, int]]:
        """Get all positions occupied by the ship."""
        row, col = self.start_position
        positions = []

        for i in range(self.size):
            if self.orientation == Orientation.HORIZONTAL:
                positions.append((row, col + i))
            else:  # VERTICAL
                positions.append((row + i, col))

        return positions

    def register_hit(self, position: Tuple[int, int]) -> bool:
        """
        Register a hit on the ship.

        Args:
            position: (row, col) tuple indicating the hit position

        Returns:
            bool: True if the hit was successful, False if already hit
        """
        if position in self.get_positions() and position not in self.hit_positions:
            self.hit_positions.add(position)
            return True
        return False


class Board:
    """Represents a Battleship game board."""

    def __init__(self, size: int = 10):
        """
        Initialize a board.

        Args:
            size: Size of the board (default: 10x10)
        """
        self.size = size
        self.ships: List[Ship] = []
        self.shots: Dict[Tuple[int, int], CellState] = {}

    def place_ship(self, ship: Ship) -> bool:
        """
        Place a ship on the board.

        Args:
            ship: The ship to place

        Returns:
            bool: True if the ship was successfully placed, False otherwise
        """
        # Check if ship is within board boundaries
        for row, col in ship.get_positions():
            if row < 0 or row >= self.size or col < 0 or col >= self.size:
                return False

        # Check if ship overlaps with any existing ships
        for existing_ship in self.ships:
            existing_positions = set(existing_ship.get_positions())
            new_positions = set(ship.get_positions())
            if existing_positions.intersection(new_positions):
                return False

        # Place the ship
        self.ships.append(ship)
        return True

    def receive_shot(self, position: Tuple[int, int]) -> CellState:
        """
        Process a shot at the given position.

        Args:
            position: (row, col) tuple indicating the shot position

        Returns:
            CellState: The result of the shot (MISS or HIT)
        """
        if position in self.shots:
            return self.shots[position]  # Shot already taken at this position

        for ship in self.ships:
            if position in ship.get_positions():
                ship.register_hit(position)
                self.shots[position] = CellState.HIT
                return CellState.HIT

        self.shots[position] = CellState.MISS
        return CellState.MISS

    def are_all_ships_sunk(self) -> bool:
        """Check if all ships on the board are sunk."""
        return all(ship.is_sunk() for ship in self.ships)

    def get_ship_at_position(self, position: Tuple[int, int]) -> Optional[Ship]:
        """Get the ship at a specific position, if any."""
        for ship in self.ships:
            if position in ship.get_positions():
                return ship
        return None

    def random_placement(self) -> bool:
        """
        Place all standard ships randomly on the board.

        Returns:
            bool: True if all ships were successfully placed, False otherwise
        """
        self.ships = []  # Clear existing ships
        ship_types = [
            ShipType.CARRIER,
            ShipType.BATTLESHIP,
            ShipType.CRUISER,
            ShipType.SUBMARINE,
            ShipType.DESTROYER
        ]

        for ship_type in ship_types:
            # Try to place the ship up to 100 times
            for _ in range(100):
                orientation = random.choice(list(Orientation))

                if orientation == Orientation.HORIZONTAL:
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - ship_type.value)
                else:  # VERTICAL
                    row = random.randint(0, self.size - ship_type.value)
                    col = random.randint(0, self.size - 1)

                ship = Ship(ship_type, orientation, (row, col))
                if self.place_ship(ship):
                    break
            else:
                # Failed to place a ship after 100 attempts
                return False

        return True

    def print_board(self, show_ships: bool = False):
        """
        Print the current state of the board.

        Args:
            show_ships: Whether to show ships or not
        """
        # Print column numbers
        print("  ", end="")
        for col in range(self.size):
            print(f" {col}", end="")
        print()

        for row in range(self.size):
            print(f"{row} ", end="")

            for col in range(self.size):
                position = (row, col)

                if position in self.shots:
                    if self.shots[position] == CellState.HIT:
                        print(" X", end="")
                    else:  # MISS
                        print(" O", end="")
                elif show_ships and any(position in ship.get_positions() for ship in self.ships):
                    print(" S", end="")
                else:
                    print(" ·", end="")

            print()
