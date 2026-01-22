n1 = int(input("Enter number 1: "))
n2 = int(input("Enter number 2: "))
n3 = int(input("Enter number 3: "))
avg = (n1 + n2 + n3) / 3
print(f"The average of {n1}, {n2}, and {n3} is {avg}")
if n1 >= n2 and n1 >= n3:
    print(f"{n1} is the largest number.")
elif n2 >= n1 and n2 >= n3:
    print(f"{n2} is the largest number.")
else:
    print(f"{n3} is the largest number.")
