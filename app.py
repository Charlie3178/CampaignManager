import menu_scripts


def edit_val(prompt, current):
    """Universal validation helper passed to scripts."""
    while True:
        new_val = input(f"{prompt} [{current}]: ")
        if not new_val.strip():
            return current
        if isinstance(current, (int, float)):
            try:
                # Handle floats for CR/Weight, ints for HP/AC
                return type(current)(new_val)
            except ValueError:
                print(f"[!] Invalid input. Please enter a number.")
                continue
        return new_val


def category_menu(title, table_name):
    """A single function that handles ALL sub-menus."""
    while True:
        print(f"\n--- {title.upper()} ---")
        print("1. Create")
        print("2. Delete")
        print("3. Edit")
        print("4. List All")
        print("5. Search (Name/ID)")
        print("6. Back to Main Menu")

        choice = input("\nSelection: ")

        if choice == '1':
            menu_scripts.handle_create(table_name, edit_val)
        elif choice == '2':
            menu_scripts.handle_delete(table_name)
        elif choice == '3':
            menu_scripts.handle_edit(table_name, edit_val)
        elif choice == '4':
            menu_scripts.handle_list_all(table_name)
        elif choice == '5':
            menu_scripts.handle_search(table_name)
        elif choice == '6':
            break


def main_menu():
    while True:
        print("\n===============================")
        print("    CAMPAIGN MANAGER - V1.0")
        print("===============================")
        print("1. Characters")
        print("2. Creatures")
        print("3. Items")
        print("4. Locations")
        print("5. Exit")
        print("-------------------------------")

        choice = input("Selection: ")

        if choice == '1':
            category_menu("Character Management", "characters")
        elif choice == '2':
            category_menu("Monster Bestiary", "bestiary")
        elif choice == '3':
            category_menu("Item Compendium", "items")
        elif choice == '4':
            category_menu("Location Atlas", "locations")
        elif choice == '5':
            print("Exiting...")
            break


if __name__ == "__main__":
    main_menu()
