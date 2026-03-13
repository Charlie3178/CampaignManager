import os
from utils.db_handler import get_all_characters, find_character_by_name
from models import Character


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    while True:
        # clear_screen() # Optional: keeps the terminal tidy
        print("\n===============================")
        print("   CAMPAIGN MANAGER - V1.0")
        print("===============================")
        print("1. View All Characters")
        print("2. Search for a Character")
        print("3. Exit")
        print("-------------------------------")

        choice = input("Selection: ")

        if choice == '1':
            chars = get_all_characters()
            print(f"\n--- Character List ({len(chars)} found) ---")
            for c in chars:
                type_label = "PC" if c.is_pc else "NPC"
                print(f"[{type_label}] {c.name} - {c.race} {c.class_role}")
            input("\nPress Enter to return to menu...")

        elif choice == '2':
            name = input("\nEnter name to search for: ")
            results = find_character_by_name(name)
            if results:
                print(f"\nFound {len(results)} match(es):")
                for r in results:
                    print(f"Name: {r.name}")
                    print(f"Race/Class: {r.race} {r.class_role}")
                    print(f"Notes: {r.notes}")
                    print("-" * 20)
            else:
                print("No characters found with that name.")
            input("\nPress Enter to return to menu...")

        elif choice == '3':
            print("Closing Campaign Manager. Happy Adventuring!")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main_menu()
