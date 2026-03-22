import random


def roll_die():
    return random.randint(1, 6)


def get_player_count():
    while True:
        players = input("How many players are there? (2-4) ")
        if players.isdigit():
            players = int(players)
            if 2 <= players <= 4:
                return players
        print("Please enter a number between 2 and 4.")


def get_turn_action():
    return input("Roll (r) or Hold (h)? ").lower().strip()


def show_scores(player_scores):
    for i, score in enumerate(player_scores):
        print(f"Player {i + 1}: {score}")
    print()


def play_game():
    players = get_player_count()
    max_score = 100
    player_scores = [0] * players

    while max(player_scores) < max_score:
        for player_idx in range(players):
            print(f"\n--- Player {player_idx + 1}'s turn ---")
            print(f"Total scores: {player_scores}")
            current_score = 0

            while True:
                print(f"Turn score: {current_score}")
                action = get_turn_action()

                if action != "r":
                    break

                roll = roll_die()
                print(f"You rolled: {roll}")

                if roll == 1:
                    print("Rolled a 1! You lose your turn points.")
                    current_score = 0
                    break

                current_score += roll

            player_scores[player_idx] += current_score
            print(f"Player {player_idx + 1}'s total: {player_scores[player_idx]}")

            if player_scores[player_idx] >= max_score:
                print(f"\nPlayer {player_idx + 1} wins with {player_scores[player_idx]} points!")
                return

    print("Game over!")


if __name__ == "__main__":
    play_game()
    while input("Play again? (y/n) ").lower().strip() == "y":
        play_game()
