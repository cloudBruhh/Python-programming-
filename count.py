"""This is a program to count the number of digits, vowels, and consonants in a line of text."""
text = input("Enter a line of text: ")
digit_count = 0
vowel_count = 0
consonant_count = 0
for char in text:
    if char.isdigit():
        digit_count += 1
    elif char.lower() in 'aeiou':
        vowel_count += 1
    elif char.isalpha():
        consonant_count += 1

print(f"Number of digits: {digit_count}")
print(f"Number of vowels: {vowel_count}")
print(f"Number of consonants: {consonant_count}")
