"""This program is for calculation of matrix multiplication."""

# Get dimensions
r1, c1 = map(int, input("Enter the row and column of first matrix: ").split())
r2, c2 = map(int, input("Enter the row and column of second matrix: ").split())

# Check if multiplication is possible
if c1 != r2:
    print("Matrix multiplication not possible! Columns of first matrix must equal rows of second.")
else:
    # Initialize matrices
    matrix1 = []
    matrix2 = []
    result = []

    # Input first matrix
    print("\n--- First Matrix ---")
    for i in range(r1):
        row = []
        for j in range(c1):
            val = int(input(f"Enter element [{i+1}][{j+1}]: "))
            row.append(val)
        matrix1.append(row)

    # Input second matrix
    print("\n--- Second Matrix ---")
    for i in range(r2):
        row = []
        for j in range(c2):
            val = int(input(f"Enter element [{i+1}][{j+1}]: "))
            row.append(val)
        matrix2.append(row)

    # Initialize result matrix with zeros
    for i in range(r1):
        row = [0] * c2
        result.append(row)

    # Matrix multiplication
    for i in range(r1):
        for j in range(c2):
            for k in range(c1):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    # Display matrices
    print("\n--- First Matrix ---")
    for row in matrix1:
        print(row)

    print("\n--- Second Matrix ---")
    for row in matrix2:
        print(row)

    print("\n--- Result Matrix ---")
    for row in result:
        print(row)
