t = int(input("Enter 1 for Celsius to Fahrenheit, 2 for Fahrenheit to Celsius: "))
match t:
    case 1:
        c = int(input("Enter temperature in Celsius: "))
        print("Converting Celsius to Fahrenheit...")
        f = (c * 9/5) + 32
        print(f"{c}°C is equal to {f}°F")

    case 2:
        f = int(input("Enter temperature in Fahrenheit:"))
        print("Converting Fahrenheit to Celsius...")
        c = (f - 32) * 5/9
        print(f"{f}°F is equal to {c}°C")

    case _:
        print("Invalid input! Please enter a valid temperature.")
