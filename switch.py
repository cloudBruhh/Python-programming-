choice = int(input("Enter your choice (1-7): "))

match choice:
    case 1:
        print("The day is Sunday")
    case 2:
        print("The day is Monday")
    case 3:
        print("The day is Tuesday")
    case 4:
        print("The day is Wednesday")
    case 5:
        print("The day is Thursday")
    case 6:
        print("The day is Friday")
    case 7:
        print("The day is Saturday")
    case _:
        print("Invalid choice! Please enter a number between 1 and 7.")
