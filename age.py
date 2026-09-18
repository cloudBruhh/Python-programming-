def main():
    age = 18
    if age < 18 and age > 0:
        print("You are a minor.")
    elif age == 18:
        print("Congratulations on reaching adulthood!")
    else:
        print("idk what you are!")

    for i in range(5):
        print(f"Hello, World! {i + 1}")

    print("\n")

    j = 0
    while j < 5:
        print(f"Hello, World! {j + 1}")
        j += 1


if __name__ == "__main__":
    name = input("What is your name? ")
    print(f"welcome {name} to the world of programming!")
    main()
