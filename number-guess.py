import random

print("Welcome to the Number Guessing Game!")
top_of_number = input("Enter the maximum number for the guessing range: ")

if top_of_number.isdigit():
    top_of_number = int(top_of_number)
    if top_of_number <= 0:
        print("Please enter a number greater than 0.")
        exit()
else:
    print("Please enter a valid number.")
    exit()

random_number = random.randint(0, top_of_number)
guesses = 0
while True:
    guesses += 1
    user_guess = input("Make a guess: ")

    if user_guess.isdigit():
        user_guess = int(user_guess)
    else:
        print("Please enter a valid number.")
        continue

    if user_guess == random_number:
        print("Congratulations! You've guessed the number!")
        break
    elif user_guess < random_number:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")

    if guesses >= 7:
        print(
            "Game over! You've used all 7 guesses. The number was "
            + str(random_number)
            + "."
        )
        break

print("You guessed the number in " + str(guesses) + " guesses.")
