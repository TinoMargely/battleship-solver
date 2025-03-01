from battleship.strategy import RandomStrategy
from battleship.core import Board

def benchmark_strategy(num_games : int = 100, strategy_name : str = "random"):
    """
    Benchmarks a strategy's board clearing abilities.

    Args:
        num_games: Number of games to simulate
        strategy: Name of the first strategy
    """
    strategies = {
        "random" : RandomStrategy
    }
    strategy = strategies[strategy_name]()

    # Initialize counter
    turns = []

    print(f"Simulating {num_games} games for strategy {strategy_name}...")

    for i in range(num_games):
        # Set up board
        board = Board()
        board.random_placement()

        # Reset strategy
        strategy.reset()

        # Play until one strategy wins
        turn_count = 0

        while True:
            turn_count += 1

            # Get next shot
            shot = strategy.get_next_shot()

            # Process shot
            result = board.receive_shot(shot)

            # Register result
            strategy.register_result(shot, result)

            # Check if game is over
            if board.are_all_ships_sunk():
                turns.append(turn_count)
                break

        # Print progress
        if (i + 1) % 10 == 0:
            print(f"Completed {i + 1} games...")

    # Print results
    print("\nSimulation Results:")
    avg_turns = sum(turns) / len(turns)
    print(f"Average turns for {strategy_name} to win: {avg_turns:.1f}")


if __name__ == "__main__":
    benchmark_strategy()