"""Program to count the number of digits in a line of text."""

text = input("Enter a line of text: ")

digit_count = 0
for char in text:
    if char.isdigit():
        digit_count += 1

print(f"Number of digits: {digit_count}")