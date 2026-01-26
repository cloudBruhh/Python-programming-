import math
a, b, c = map(int, input(
    "Enter the lengths of the three sides of the triangle separated by spaces: ").split())
if a + b > c and a + c > b and b + c > a:
    print("The lengths can form a triangle.")
    s = (a + b + c) / 2
    area = math.sqrt((s * (s - a) * (s - b) * (s - c)))
    print(f"The area of the triangle is: {area}")
else:
    print("The lengths cannot form a triangle.")
# This program checks if three lengths can form a triangle and calculates its area if they can.
