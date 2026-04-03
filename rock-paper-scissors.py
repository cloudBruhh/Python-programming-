import random

user_wins = 0
computer_wins = 0

option = ["rock", "paper", "scissors"]
while True:
    user_input = input("Type Rock/Paper/Scissors or Q to quit: ").lower()
    if user_input == "q":
        break

    if user_input not in option:
        print("Invalid input. Please try again.")
        continue

    random_number = random.randint(0, 2)
    # 0 - rock, 1 - paper, 2 - scissors
    computer_pick = option[random_number]
    print(f"Computer picked {computer_pick}.")

    if user_input == computer_pick:
        print("It's a tie!")

    elif user_input == "rock" and computer_pick == "scissors":
        print("You win!")
        user_wins += 1

    elif user_input == "paper" and computer_pick == "rock":
        print("You win!")
        user_wins += 1

    elif user_input == "scissors" and computer_pick == "paper":
        print("You win!")
        user_wins += 1

    else:
        print("You lose!")
        computer_wins += 1

print(f"You won {user_wins} times.")
print(f"Computer won {computer_wins} times.")
print("Goodbye!")
