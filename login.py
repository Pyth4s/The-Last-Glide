import os
import time

PROFILES_FILE = "profiles.txt"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def auth_screen() -> str:
    while True:
        clear_screen()
        print("REGISTER (R)")
        print("LOGIN (L)")
        print("PLAY AS GUEST (G)")
        print("SETTINGS (S)")
        print("QUIT (Q)")
        print("")
        action = input(": ").strip().lower()
        if action.startswith('r'):
            clear_screen()
            print("Info: Registering only saves your progress locally.")
            print("Do you want to continue? (y/n)")
            if input(": ").strip().lower().startswith("y"):
                username = register()
                if username:
                    return username
        elif action.startswith('l'):
            username = login_user()
            if username:
                return username
        elif action.startswith('g'):
            clear_screen()
            print("Info: Playing as Guest will NOT save your progress.")
            print("Registering is only local and saves your progress.")
            print("Do you want to continue? (y/n)")
            if input(": ").strip().lower().startswith("y"):
                return "GUEST"
        elif action.startswith('q'):
            print("Exiting...")
            time.sleep(1)
            exit()
        elif action.startswith('s'):
            clear_screen()
            print("There are no settings.")
            input("Press Enter to continue...")
        else:
            print("Invalid choice.")
            time.sleep(1)

def login_user() -> str | None:
    clear_screen()
    print("LOGIN")
    print("")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) < 3:
                    continue
                stored_user, stored_pass = parts[0], parts[1]
                if username == stored_user and password == stored_pass:
                    print("Login successful!")
                    time.sleep(1)
                    return username
    except FileNotFoundError:
        pass
    print("Wrong username or password.")
    time.sleep(1)
    return None

def register() -> str | None:
    while True:
        clear_screen()
        print("REGISTER NEW ACCOUNT")
        username = input("Choose a username: ").strip()
        if not username:
            print("Username cannot be empty.")
            time.sleep(1)
            continue
        users = {}
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(";")
                    if len(parts) >= 2:
                        users[parts[0]] = parts[1]
        except FileNotFoundError:
            users = {}
        if username in users:
            print(f"The username '{username}' is already taken.")
            time.sleep(1.5)
            return None
        password = input("Choose a password: ").strip()
        if not password:
            print("Password cannot be empty.")
            time.sleep(1)
            continue
        with open(PROFILES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{username};{password};1;\n")
        print("Registration successful! You are now logged in.")
        time.sleep(1)
        return username
