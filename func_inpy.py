""" this is a TEST or Dummy python file """


def fact(n):
    """Compute factorial of n(dummy implementation)."""
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)


def fib(n):
    """Compute nth Fibonacci number(dummy implementation)."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"


def main():
    print("This is a dummy Python file for testing purposes.")
    n = int(input("Enter the number to compute factorial: "))
    name = input("Enter your name: ")
    fact(n)
    fib(n)
    greet(name)
    print(f"Factorial of {n} is {fact(n)}")
    print(f"{name}, the {n}th Fibonacci number is {fib(n)}")
    print(greet(name))


if __name__ == "__main__":
    main()
