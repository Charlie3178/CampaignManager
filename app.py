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
        print("6.Database Management")
        print("0. Back to Main Menu")

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
            menu_scripts.handle_db_management()
        elif choice == '0':
            break


def main_menu():
    while True:
        print("\n=== CAMPAIGN MANAGER HUB ===")
        print("1. Character Records")
        print("2. Bestiary (Monsters)")
        print("3. Item Compendium")
        print("4. Location Atlas")
        print("5. Database Management")  # New Option
        print("0. Exit")

        choice = input("\nSelection: ")

        if choice == '1':
            category_menu("Characters", "characters")
        elif choice == '2':
            category_menu("Bestiary", "bestiary")
        elif choice == '3':
            category_menu("Items", "items")
        elif choice == '4':
            category_menu("Locations", "locations")
        elif choice == '5':
            menu_scripts.handle_db_management()
        elif choice == '0':
            break


if __name__ == "__main__":
    main_menu()
