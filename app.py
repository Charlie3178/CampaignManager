import os
import sys
from menu_scripts import (
    handle_search, handle_list_all, handle_create_generic,
    handle_delete, handle_edit, run_character_wizard,
    handle_db_management, handle_view_character
)

# Setup directory paths for data persistence
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.join(base_dir, "data")
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


def edit_val(prompt, current):
    """Universal validation helper passed to handle_edit for clean updates."""
    while True:
        new_val = input(f"{prompt} [{current}]: ")
        if not new_val.strip():
            return current
        if isinstance(current, (int, float)):
            try:
                return type(current)(new_val)
            except ValueError:
                print(f"[!] Invalid input. Please enter a number.")
                continue
        return new_val


def general_menu(table_name):
    """
    The universal CRUD interface for all 18 tables.
    Replaces the old 'category_menu' with a streamlined flow.
    """
    while True:
        print(f"\n--- {table_name.upper()} MANAGEMENT ---")
        print("1. Search (Name/ID)")
        print("2. List All")
        print("3. Create New")
        print("4. Edit Existing")
        print("5. Delete Record")
        if table_name == 'characters':
            print("6. View Full Character Sheet")
        print("0. Back")

        choice = input("\nSelection: ")
        if choice == '1':
            handle_search(table_name)
        elif choice == '2':
            handle_list_all(table_name)
        elif choice == '3':
            if table_name == 'characters':
                run_character_wizard()
            else:
                handle_create_generic(table_name)
        elif choice == '4':
            handle_edit(table_name, edit_val)
        elif choice == '5':
            handle_delete(table_name)
        elif choice == '6' and table_name == 'characters':
            handle_view_character()
        elif choice == '0':
            break


def party_menu():
    while True:
        print("\n--- PARTY HUB ---")
        print("1. Characters")
        print("2. Backgrounds")
        print("3. Notes")
        print("0. Back")
        c = input("\nSelection: ")
        if c == '1':
            general_menu('characters')
        elif c == '2':
            general_menu('backgrounds')
        elif c == '3':
            general_menu('notes')
        elif c == '0':
            break


def library_menu():
    while True:
        print("\n--- LIBRARY ---")
        print("1. Classes      5. Traits")
        print("2. Subclasses   6. Features")
        print("3. Races        7. Skills")
        print("4. Subraces     8. Proficiencies")
        print("0. Back")
        c = input("\nSelection: ")
        mapping = {
            '1': 'classes', '2': 'subclasses', '3': 'races', '4': 'subraces',
            '5': 'traits', '6': 'features', '7': 'skills', '8': 'proficiencies'
        }
        if c in mapping:
            general_menu(mapping[c])
        elif c == '0':
            break


def compendium_menu():
    while True:
        print("\n--- COMPENDIUM ---")
        print("1. Items")
        print("2. Spells")
        print("3. Feats")
        print("0. Back")
        c = input("\nSelection: ")
        if c == '1':
            general_menu('items')
        elif c == '2':
            general_menu('spells')
        elif c == '3':
            general_menu('feats')
        elif c == '0':
            break


def world_menu():
    while True:
        print("\n--- WORLD & BESTIARY ---")
        print("1. Creatures")
        print("2. Locations")
        print("3. Lore")
        print("0. Back")
        c = input("\nSelection: ")
        if c == '1':
            general_menu('creatures')
        elif c == '2':
            general_menu('locations')
        elif c == '3':
            general_menu('lore')
        elif c == '0':
            break


def main_menu():
    while True:
        print("\n" + "="*45)
        print("      --- ARCANRYN CAMPAIGN MANAGER ---")
        print("="*45)
        print("  [1]  Party Hub")
        print("  [2]  Library")
        print("  [3]  Compendium")
        print("  [4]  World & Bestiary")
        print("  [5]  Database Management")
        print("  [0]  Exit")
        print("="*45)

        choice = input("Selection: ")
        if choice == '1':
            party_menu()
        elif choice == '2':
            library_menu()
        elif choice == '3':
            compendium_menu()
        elif choice == '4':
            world_menu()
        elif choice == '5':
            handle_db_management()  # Calls your built-in menu
        elif choice == '0':
            print("Closing Arcanryn. Game on.")
            break


if __name__ == "__main__":
    main_menu()
