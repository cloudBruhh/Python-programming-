"""A Python program to compute binomial coefficients using factorials."""


def fact(n):
    """Compute factorial of n."""
    if n == 0:
        return 1
    return n * fact(n - 1)


def binomial_coeff(n, r):
    """Compute binomial coefficient C(n, r)."""
    if (r == 0 or r == 1):
        return 1
    else:
        return fact(n) // (fact(r) * fact(n - r))


def main():
    """Main function to execute binomial coefficient computation."""
    n = int(input("Enter n (total items): "))
    r = int(input("Enter r (items to choose): "))
    print(f"The binomial coefficient C({n}, {r}) is: {binomial_coeff(n, r)}")


if __name__ == "__main__":
    main()
