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
        print("3. Create New Character")
        print("4. Exit")
        print("-------------------------------")

        choice = input("Selection: ")

        if choice == '1':
            from utils.db_handler import get_all_characters
            chars = get_all_characters()
            # ... (Your Option 1 code here)
            input("\nPress Enter to return to menu...")

        elif choice == '2':
            # ... (Your Option 2 Search/Stat Card code here)
            input("\nPress Enter to return to menu...")

        elif choice == '3':
            print("\n" + "="*30)
            print("   CREATE NEW CHARACTER")
            print("="*30)

            def get_int_input(prompt, default=10):
                val = input(f"{prompt} (Default {default}): ")
                return int(val) if val.isdigit() else default

            name = input("Name: ")
            race = input("Race: ")
            subrace = input("Subrace: ")
            role = input("Class/Role: ")
            subclass = input("Subclass: ")
            level = get_int_input("Level/CR", default=1)
            is_pc = input("Is this a Player Character? (y/n): ").lower() == 'y'
            group = input("Affiliation: ")

            print("\n--- Ability Scores ---")
            s_str = get_int_input("Strength")
            s_dex = get_int_input("Dexterity")
            s_con = get_int_input("Constitution")
            s_int = get_int_input("Intelligence")
            s_wis = get_int_input("Wisdom")
            s_cha = get_int_input("Charisma")

            print("\n--- Combat Stats ---")
            s_ac = get_int_input("Armor Class", default=10)
            s_hp = get_int_input("Hit Points", default=10)

            notes = input("\nNotes/Description: ")

            from utils.db_handler import save_character
            new_char = Character(
                name=name, race=race, subrace=subrace,
                class_role=role, subclass=subclass,
                level_cr=level, is_pc=is_pc, affiliation=group, notes=notes,
                strength=s_str, dexterity=s_dex, constitution=s_con,
                intelligence=s_int, wisdom=s_wis, charisma=s_cha,
                ac=s_ac, hp=s_hp
            )
            save_character(new_char)
            print(f"\n[SUCCESS] {name} added to the database.")
            input("\nPress Enter to return to menu...")

        elif choice == '4':
            print("Closing Campaign Manager. Happy Adventuring!")
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main_menu()
