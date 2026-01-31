def fib(n):
    """Compute the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def main():
    n = int(input("Enter a number to compute its Fibonacci: "))
    for i in range(n):
        if i == n - 1:
            print(f"{fib(i)}")  # Last number without comma
        else:
            print(f"{fib(i)}", end=" ,")
    return 0


if __name__ == "__main__":
    main()
