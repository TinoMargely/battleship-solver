from battleship.strategy import RandomStrategy
from battleship.game import Game


def play_interactive_game(strategy_name="random"):
    """
    Play an interactive game with the chosen AI strategy.

    Args:
        strategy_name: The name of the strategy to use ('random', 'hunt', or 'probability')
    """
    strategy = RandomStrategy()
    print("Playing against Random AI strategy")

    # Initialize and set up the game
    game = Game(ai_strategy=strategy)
    game.setup_game()

    print("Welcome to Battleship!")
    print("Ships have been placed. Let's play!")

    while not game.game_over:
        game.display_boards()

        # Get player's shot
        try:
            row = int(input("\nEnter row for your shot: "))
            col = int(input("Enter column for your shot: "))

            if row < 0 or row >= game.board_size or col < 0 or col >= game.board_size:
                print("Invalid position! Try again.")
                continue

            turn_result = game.play_turn((row, col))

            # Display results
            print(f"\nYour shot at ({row}, {col}) was a {turn_result['player_result'].name}!")

            if not game.game_over:
                ai_row, ai_col = turn_result['ai_shot']
                print(f"AI shot at ({ai_row}, {ai_col}) was a {turn_result['ai_result'].name}!")

        except ValueError:
            print("Please enter valid numbers!")

    # Game over
    game.display_boards()
    print(f"\nGame Over! The winner is: {game.winner}")
    print(f"Total turns: {game.turn_count}")


if __name__ == "__main__":
    print("Battleship Game")

    print("Play interactive game : ")

    play_interactive_game("random")