import base64
import hashlib

from cryptography.fernet import Fernet


def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key


def derive_key(stored_key, master_pwd):
    combined = stored_key + master_pwd.encode()
    hashed = hashlib.sha256(combined).digest()
    return base64.urlsafe_b64encode(hashed)


master_pwd = input("What is the master password?")
stored_key = load_key()
key = derive_key(stored_key, master_pwd)
fer = Fernet(key)


def view():

    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())


def add():
    name = input("Account Name: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a") as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")


while True:
    mode = input(
        "Would you like to add a new password or view existing passwords (view, add)?, or quit (q)?"
    )
    if mode == "q":
        break
    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
