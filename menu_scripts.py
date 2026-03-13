from utils.db_handler import add_record, get_connection, find_by_hybrid, delete_by_id, update_record


def handle_list_all(table_name):
    """Lists ID and Name for any table."""
    conn = get_connection()
    cursor = conn.cursor()
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
        data['class_role'] = input("Class/Role: ")
        data['level_cr'] = edit_func("Level/CR", 1)
        data['hp'] = edit_func("Hit Points", 10)
        data['ac'] = edit_func("AC", 10)
        data['affiliation'] = input("Affiliation: ")
        data['notes'] = input("Notes: ")

    elif category == 'bestiary':
        data['name'] = input("Creature Name: ")
        data['size'] = input("Size: ")
        data['creature_type'] = input("Type: ")
        data['alignment'] = input("Alignment: ")
        data['hp'] = edit_func("Hit Points", 10)
        data['ac'] = edit_func("AC", 10)
        data['cr'] = edit_func("CR", 0)
        data['xp'] = edit_func("XP Value", 100)
        data['notes'] = input("Actions/Notes: ")

    elif category == 'items':
        data['name'] = input("Item Name: ")
        data['category'] = input("Category: ")
        data['rarity'] = input("Rarity: ")
        data['value_gp'] = edit_func("Value (gp)", 0)
        data['weight'] = edit_func("Weight (lbs)", 0)
        data['is_magical'] = 1 if input(
            "Magical? (y/n): ").lower() == 'y' else 0
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
    """Formatted output for Search/Edit views."""
    print("\n" + "="*45)
    print(f" {data['name'].upper()} (ID: {data['id']})")
    print("="*45)

    if table_name == 'characters':
        print(f"Race: {data['race']} | Class: {data['class_role']}")
        print(
            f"Level: {data['level_cr']} | HP: {data['hp']} | AC: {data['ac']}")
        print(f"Affiliation: {data['affiliation']}")

    elif table_name == 'bestiary':
        print(
            f"Type: {data['size']} {data['creature_type']} | {data['alignment']}")
        print(
            f"CR: {data['cr']} | HP: {data['hp']} | AC: {data['ac']} | XP: {data['xp']}")

    elif table_name == 'items':
        print(f"Type: {data['category']} | Rarity: {data['rarity']}")
        print(f"Value: {data['value_gp']} gp | Weight: {data['weight']} lbs")

    elif table_name == 'locations':
        print(f"Type: {data['location_type']} | Region: {data['region']}")
        if data['parent_id']:
            print(f"Inside Location ID: {data['parent_id']}")

    print("-" * 45)
    # Handle different column names for notes/desc
    notes_val = data['notes'] if 'notes' in data.keys(
    ) else data['description']
    print(f"NOTES: {notes_val}")
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
