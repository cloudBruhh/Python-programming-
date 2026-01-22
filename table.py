n = int(input("Enter the number of rows for the table: "))
i = 1
for i in range(1, 11):

    table = n * i
    print(f"{i}. {n} x {i} = {table}")
