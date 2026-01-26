

sum_even = 0
prod_odd = 1
odd_count = 0
i = 1
n = int(input("How many numbers will you enter? "))

for i in range(n):
    num = int(input(f"Enter  number {i+1} : "))
    if num % 2 == 0:
        sum_even = sum_even + num
    else:
        prod_odd = prod_odd * num
        odd_count += 1

if odd_count == 0:
    prod_odd = 0

print(f"Sum of even numbers: {sum_even}")
print(f"Product of odd numbers: {prod_odd}")
# This program calculates the sum of even numbers and the product of odd numbers from user input.
