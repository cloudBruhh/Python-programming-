import random
import time

OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10


def generate_problem():

    op1 = random.randint(MIN_OPERAND, MAX_OPERAND)
    op2 = random.randint(MIN_OPERAND, MAX_OPERAND)
    operator = random.choice(OPERATORS)
    expr = str(op1) + " " + operator + " " + str(op2)
    answer = eval(expr)
    return expr, answer


wrong = 0
start_time = time.time()
for i in range(TOTAL_PROBLEMS):
    expr, answer = generate_problem()
    while True:
        guess = input("Problem#" + str(i + 1) + ": " + expr + " = ?")
        if guess == str(answer):
            print("Correct!")
            break
        wrong += 1

end_time = time.time()
elapsed_time = round(end_time - start_time, 2)
print(
    "You got " + str(TOTAL_PROBLEMS - wrong) + " correct and " + str(wrong) + " wrong."
)
print("Your time was " + str(elapsed_time) + " seconds.")
