"""hello world program to sort a list in ascending order using bubble sort algorithm"""
n = int(input("Enter the number of elements to sort: "))
t = []
for i in range(n):
    num = int(input(f"Enter element {i+1}: "))
    t.append(num)
for i in range(n):
    for j in range(0, n-i-1):
        if t[j] > t[j+1]:
            t[j], t[j+1] = t[j+1], t[j]
print("Sorted list in ascending order:")
for i in range(n):
    print(t[i])
