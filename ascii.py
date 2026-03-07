def display_ascii_values(text):
    for char in text:

        ascii_value = ord(char)

        # Display the character and its ASCII value
        print(f"Character: {char}, ASCII Value: {ascii_value}")

# Get the text from the user
text = input("Please enter a line of text: ")

# Call the function to display the ASCII values
display_ascii_values(text)

