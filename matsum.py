"""This progranm is for calculation of matrix summation."""
r1, c1 = map(int, input("Enter the row and column of first matrix: ").split())
r2, c2 = map(int, input("Enter the row and column of second matrix: ").split())
if r1 != r2 or c1 != c2:
    print("Matrix addition not possible! Both matrices must have the same dimensions.")
else:
    a = []
    b = []
    result = []  # Renamed from 'sum' to avoid shadowing built-in
    print("\n--- First Matrix ---")
    for i in range(r1):
        row = []
        for j in range(c1):
            val = int(input(f"Enter element [{i+1}][{j+1}]: "))
            row.append(val)
        a.append(row)

    print("\n--- Second Matrix ---")
    for i in range(r2):
        row = []
        for j in range(c2):
            val = int(input(f"Enter element [{i+1}][{j+1}]: "))
            row.append(val)
        b.append(row)

    print("\n---  Summation ---")
    for i in range(r1):
        row = []
        for j in range(c1):
            # Fixed: append to row instead of indexing
            row.append(a[i][j] + b[i][j])
        result.append(row)

    print("\n--- Result Matrix ---")
    for row in result:
        print(row)
