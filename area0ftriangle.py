import math
a, b, c = map(int, input("Enter the three sides of the triangle:").split())

s = (a + b + c) / 2
area = math.sqrt(s * (s - a) * (s - b)*(s - c))
print(f"The area of triangle with sides {a}, {b}, and {c} is {area}")
