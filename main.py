import os
import time
import login
import game

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(player_name: str):
    while True:
        clear_screen()
        print(f"Welcome, {player_name}!")
        print("Main Menu")
        print("")
        print("S) Speed Mode")
        print("A) Adventure Mode (not coming soon!)")
        print("L) Logout")
        print("Q) Quit")
        print("")
        choice = input("Choose mode (S/A/Q): ").strip().lower()
        if choice.lower().startswith('s') or choice == '1':
            game.start_game(player_name)
        elif choice.lower().startswith('a') or choice == '2':
            clear_screen()
            print("Not coming soon...")
            input("Press Enter to continue...")
            main_menu(player_name)
        elif choice.lower().startswith('l'):
            clear_screen()
            print("Logging out...")
            time.sleep(1)
            login.auth_screen()
        elif choice.lower().startswith('q'):
            print("Goodbye!")
            time.sleep(1)
            exit()
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    clear_screen()
    player = login.auth_screen()
    main_menu(player)
