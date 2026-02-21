# A program to do string related things


def count_string(string, c):
    """Counts the number of times char appears in string."""
    count = 0
    for char in string:
        if char == c:
            count += 1
    return count


def main():
    string = input("Enter a string: ")
    c = input("Enter a character to count: ")
    result = count_string(string, c)
    print(f"The character '{c}' appears {result} times in the string.")


if __name__ == "__main__":
    main()
