from utils.db_handler import add_record, get_connection, find_by_hybrid, delete_by_id, update_record
from utils.db_handler import export_table_to_csv, import_from_csv
from scripts import db_init


def handle_list_all(table_name):
    """Lists ID and Name for any table, with special formatting for Bestiary."""
    conn = get_connection()
    cursor = conn.cursor()

    # Custom query for Bestiary to show CR and Type
    if table_name == 'creatures':
        cursor.execute(f"SELECT id, name, cr, creature_type FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\n--- BESTIARY SUMMARY ---")
        print(f"{'ID':<4} | {'NAME':<25} | {'CR':<5} | {'TYPE'}")
        print("-" * 55)
        for row in rows:
            print(
                f"{row['id']:<4} | {row['name']:<25} | {row['cr']:<5} | {row['creature_type']}")
    elif table_name == 'items':
        cursor.execute(f"SELECT id, name, category, rarity FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\n--- EQUIPMENT & ITEMS ---")
        print(f"{'ID':<4} | {'NAME':<30} | {'CATEGORY':<15} | {'RARITY'}")
        print("-" * 65)
        for row in rows:
            print(
                f"{row['id']:<4} | {row['name']:<30} | {row['category']:<15} | {row['rarity']}")
    else:
        # Keep your original logic for other tables
        cursor.execute(f"SELECT id, name FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\n--- {table_name.upper()} LIST ---")
        print(f"{'ID':<4} | {'NAME'}")
        print("-" * 30)
        for row in rows:
            print(f"{row['id']:<4} | {row['name']}")

    conn.close()


def handle_delete(table_name):
    """Prompts for an ID/Name, confirms, and deletes."""
    search = input(f"\nEnter Name or ID of {table_name[:-1]} to DELETE: ")
    results = find_by_hybrid(table_name, search)

    if not results:
        print("[!] No record found.")
        return

    item = results[0]
    confirm = input(f"Confirm deleting {item['name']}? (y/n): ").lower()
    if confirm == 'y':
        delete_by_id(table_name, item['id'])
        print("[SUCCESS] Record removed.")


def handle_create(category, edit_func):
    """Prompts for input based on the category and saves a new record."""
    print(f"\n--- CREATE NEW {category.upper()[:-1]} ---")
    data = {}

    if category == 'characters':
        data['name'] = input("Name: ")
        data['race'] = input("Race: ")
        data['subrace'] = input("Subrace: ")
        # Matches your db_init schema
        data['class_or_role'] = input("Class/Role: ")
        data['subclass'] = input("Subclass: ")
        data['level'] = edit_func("Level", 1)  # Matches your db_init schema
        data['hp_max'] = edit_func("Max HP", 10)
        data['hp_current'] = data['hp_max']  # Set current to max by default
        data['ac'] = edit_func("AC", 10)

        # Adding the 6 core stats
        data['strength'] = edit_func("Str", 10)
        data['dexterity'] = edit_func("Dex", 10)
        data['constitution'] = edit_func("Con", 10)
        data['intelligence'] = edit_func("Int", 10)
        data['wisdom'] = edit_func("Wis", 10)
        data['charisma'] = edit_func("Cha", 10)

        data['disposition'] = input("Disposition (Friendly/Hostile/etc): ")
        data['is_pc'] = 1 if input(
            "Is this a PC? (y/n): ").lower() == 'y' else 0
        data['affiliation'] = input("Affiliation: ")
        data['backstory'] = input("Backstory: ")
        data['notes'] = input("Notes: ")

    elif category == 'bestiary':
        data['name'] = input("Creature Name: ")
        data['size'] = input("Size: ")
        data['creature_type'] = input("Type: ")
        data['alignment'] = input("Alignment: ")
        data['ac'] = edit_func("AC", 10)
        data['hp'] = edit_func("Hit Points", 10)
        data['cr'] = edit_func("CR", 0.0)
        data['xp'] = edit_func("XP Value", 100)
        data['num_attacks'] = edit_func("Number of Attacks", 1)
        data['damage'] = input("Damage (e.g., 1d8+2): ")
        data['notes'] = input("Actions/Notes: ")

    elif category == 'items':
        data['name'] = input("Item Name: ")
        data['category'] = input("Category: ")
        data['is_magical'] = 1 if input(
            "Magical? (y/n): ").lower() == 'y' else 0
        data['rarity'] = input("Rarity: ")
        data['pp'] = edit_func("Platinum (pp)", 0)
        data['gp'] = edit_func("Gold (gp)", 0)
        data['ep'] = edit_func("Electrum (ep)", 0)
        data['sp'] = edit_func("Silver (sp)", 0)
        data['cp'] = edit_func("Copper (cp)", 0)
        data['weight'] = edit_func("Weight (lbs)", 0.0)
        data['requires_attunement'] = 1 if input(
            "Requires Attunement? (y/n): ").lower() == 'y' else 0
        data['description'] = input("Description: ")

    elif category == 'locations':
        data['name'] = input("Location Name: ")
        data['location_type'] = input("Type: ")
        data['region'] = input("Region: ")
        data['description'] = input("Description: ")
        is_sub = input("Is this inside another location? (y/n): ").lower()
        if is_sub == 'y':
            data['parent_id'] = edit_func("Parent Location ID", 0)
        data['notes'] = input("Notes: ")

    if data.get('name'):
        add_record(category, data)
        print(f"\n[SUCCESS] {data['name']} added to {category}!")


def display_details(table_name, data):
    """Formatted output for Search/Edit views including the Database ID."""
    print("\n" + "="*45)
    # The header now clearly shows NAME and ID
    print(f" {data['name'].upper()} (ID: {data['id']})")
    print("="*45)

    if table_name == 'characters':
        pc_tag = "[PC]" if data['is_pc'] else "[NPC]"
        print(
            f"{pc_tag} {data['race']} {data['subrace']} | {data['class_role']} ({data['subclass']})")
        print(
            f"Level/CR: {data['level_cr']} | HP: {data['hp']} | AC: {data['ac']}")
        print(
            f"Stats: S:{data['strength']} D:{data['dexterity']} C:{data['constitution']} I:{data['intelligence']} W:{data['wisdom']} Ch:{data['charisma']}")
        print(f"Affiliation: {data['affiliation']}")

    elif table_name == 'bestiary':
        print(
            f"Type: {data['size']} {data['creature_type']} | Alignment: {data['alignment']}")
        print(
            f"CR: {data['cr']} | HP: {data['hp']} | AC: {data['ac']} | XP: {data['xp']}")
        # --- New Bestiary Fields ---
        print(f"Attacks: {data['num_attacks']} | Damage: {data['damage']}")

    elif table_name == 'items':
        magical = "YES" if data['is_magical'] else "NO"
        attune = "YES" if data['requires_attunement'] else "NO"
        print(f"Category: {data['category']} | Rarity: {data['rarity']}")

        # --- Clean Currency Display (Hides Zeros) ---
        coins = []
        for den in ['pp', 'gp', 'ep', 'sp', 'cp']:
            if data[den] > 0:
                coins.append(f"{data[den]}{den}")
        val_str = ", ".join(coins) if coins else "0gp"

        print(f"Value: {val_str} | Weight: {data['weight']} lbs")
        print(f"Magical: {magical} | Attunement Required: {attune}")

    elif table_name == 'locations':
        print(f"Type: {data['location_type']} | Region: {data['region']}")
        if data['parent_id']:
            print(f"Located Inside (Parent ID): {data['parent_id']}")

    print("-" * 45)

# Access columns directly by name instead of using .get()
    if table_name == 'locations':
        # Locations has both description AND notes
        print(f"DESCRIPTION: {data['description']}")
        print(f"NOTES: {data['notes']}")
    elif table_name == 'items':
        print(f"DESCRIPTION: {data['description']}")
    else:
        # Characters and Bestiary use 'notes'
        print(f"NOTES: {data['notes']}")

    print("="*45)


def handle_search(table_name):
    """Retrieves and displays full details."""
    search_term = input(f"\nEnter {table_name[:-1]} Name or ID: ")
    results = find_by_hybrid(table_name, search_term)

    if not results:
        print(f"[!] No match found for '{search_term}'.")
    else:
        for row in results:
            display_details(table_name, row)


def handle_edit(table_name, edit_func):
    """Universal editor for all tables."""
    search_term = input(f"\nEnter Name or ID to EDIT: ")
    results = find_by_hybrid(table_name, search_term)

    if not results:
        print("[!] Record not found.")
        return

    item = results[0]
    print(f"\nEditing {item['name']}. (Press Enter to keep current value)")

    updates = {}
    for key in item.keys():
        if key in ['id', 'name']:  # ID is immutable, Name handled separately if needed
            continue

        current_val = item[key]
        label = key.replace('_', ' ').title()

        if isinstance(current_val, (int, float)):
            updates[key] = edit_func(label, current_val)
        else:
            new_val = input(f"{label} [{current_val}]: ")
            updates[key] = new_val if new_val.strip() else current_val

    update_record(table_name, item['id'], updates)
    print(f"\n[SUCCESS] {item['name']} updated!")


def handle_db_management():
    """Submenu for bulk data operations and database maintenance."""
    while True:
        print("\n--- DATABASE MANAGEMENT ---")
        print("1. Export All Templates (CSV)")
        print("2. Import Data from CSV")
        print("3. Initialize/Reset Database")
        print("0. Back to Main Menu")

        choice = input("\nSelection: ")

        if choice == '1':
            tables = ['characters', 'bestiary', 'items', 'locations']
            for table in tables:
                export_table_to_csv(table)
            print("\n[!] Templates/Backups generated in project folder.")

        elif choice == '2':
            table = input(
                "Target Table (characters/bestiary/items/locations): ").lower()
            file_path = input("Enter CSV filename: ")
            try:
                import_from_csv(table, file_path)
            except Exception as e:
                print(f"[!] Error during import: {e}")

        elif choice == '3':
            confirm = input("Are you SURE? This wipes all data! (y/n): ")
            if confirm.lower() == 'y':
                db_init.initialize_db
                print("\n[!] Database reset to factory settings.")

        elif choice == '0':
            break
