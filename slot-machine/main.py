import random
import time

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_config = {
    "7": {"count": 1, "value": 10},
    "A": {"count": 2, "value": 7},
    "K": {"count": 3, "value": 5},
    "Q": {"count": 4, "value": 4},
    "J": {"count": 5, "value": 3},
    "10": {"count": 6, "value": 2},
    "9": {"count": 8, "value": 1},
}

symbols = list(symbol_config.keys())


def check_winnings(rows, lines, bet, symbol_values):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbols_in_line = [rows[r][line] for r in range(ROWS)]
        if len(set(symbols_in_line)) == 1:
            symbol = symbols_in_line[0]
            winnings += symbol_values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def spin_animation(rows, cols):
    symbols_list = list(symbol_config.keys())
    for _ in range(8):
        temp_display = []
        for _ in range(ROWS):
            row = [random.choice(symbols_list) for _ in range(COLS)]
            temp_display.append(row)
        print_slot_machine(temp_display)
        time.sleep(0.1)
        print()


def get_slot_machine_spin(rows, cols):
    all_symbols = []
    for symbol, config in symbol_config.items():
        all_symbols.extend([symbol] * config["count"])

    result = []
    for _ in range(ROWS):
        row = random.choices(all_symbols, k=cols)
        result.append(row)

    return result


def print_slot_machine(rows, highlight_lines=None):
    print(" " + "┌───┬───┬───┐")
    for r in range(ROWS):
        line = "│"
        for c in range(COLS):
            symbol = rows[r][c]
            if highlight_lines and r + 1 in highlight_lines:
                line += f" {symbol} │"
            else:
                line += f" {symbol} │"
        print(" " + line)
        if r < ROWS - 1:
            print(" " + "├───┼───┼───┤")
    print(" " + "└───┴───┘")


def deposit():
    while True:
        amount = input("Enter the amount you would like to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a valid number.")
    return amount


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(f"Number of lines must be between 1 and {MAX_LINES}.")
        else:
            print("Please enter a valid number.")
    return lines


def get_bet():
    while True:
        bet = input(f"Enter the bet amount per line (${MIN_BET}-${MAX_BET}): $")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid number.")
    return bet


def get_spin_choice():
    while True:
        choice = input("\nPress ENTER to spin (or 'q' to quit): ").lower().strip()
        if choice == "" or choice == "q":
            return choice
        print("Invalid input. Press ENTER to spin or 'q' to quit.")


def game():
    balance = deposit()

    while True:
        print("\n═══════════════════════════════")
        print(f"  BALANCE: ${balance}")
        print("═══════════════════════════════")

        if balance < MIN_BET:
            print("You don't have enough balance to play!")
            break

        choice = get_spin_choice()
        if choice == "q":
            print(f"\nThanks for playing! You leave with ${balance}")
            break

        lines = get_number_of_lines()

        while True:
            bet = get_bet()
            total_bet = bet * lines
            if total_bet > balance:
                print(f"You do not have enough balance. Current: ${balance}")
            else:
                break

        balance -= total_bet
        print(f"\nSpinning ${total_bet} ({bet} x {lines} lines)...")

        rows = get_slot_machine_spin(ROWS, COLS)
        spin_animation(rows, COLS)

        print_slot_machine(rows)

        symbol_values = {s: symbol_config[s]["value"] for s in symbols}
        winnings, winning_lines = check_winnings(rows, lines, bet, symbol_values)

        if winnings > 0:
            balance += winnings
            print("\n🎉 YOU WIN! 🎉")
            print(
                f"You won ${winnings} on line(s): {', '.join(map(str, winning_lines))}"
            )
        else:
            print("\nNo winning combinations this time.")

        print(f"New balance: ${balance}")


if __name__ == "__main__":
    game()

