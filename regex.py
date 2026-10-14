import re


def is_valid_gmail(email):
    # Regex pattern matching username criteria and ending with @gmail.com
    pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    # return True if the email matches the pattern, otherwise False
    return bool(re.match(pattern, email))


# Test Cases
print(is_valid_gmail("johnny.doe@gmail.com"))
print(is_valid_gmail("bhele+spam@gmail.com"))
print(is_valid_gmail("invalid.email@yahoo.com"))
print(is_valid_gmail("test@gmail.com.br"))
print(is_valid_gmail("jhutho@outlook.com"))
print(is_valid_gmail("ashwinthapa34009@gmail.com"))
print(is_valid_gmail("asian12@gmail.com"))
