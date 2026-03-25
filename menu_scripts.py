from utils.db_handler import add_record, get_connection, find_by_hybrid, delete_by_id, update_record
from utils.db_handler import export_table_to_csv, import_from_csv
from scripts import db_init
from scripts.ability_score_roller import roll_stats, assign_stats, apply_racial_bonuses
import sqlite3
import os


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

    elif table_name == 'spells':
        cursor.execute(f"SELECT id, name, level, school FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\n--- SPELLBOOK SUMMARY ---")
        print(f"{'ID':<4} | {'NAME':<30} | {'LVL':<4} | {'SCHOOL'}")
        print("-" * 55)
        for row in rows:
            print(
                f"{row['id']:<4} | {row['name']:<30} | {row['level']:<4} | {row['school']}")

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

    elif category == 'creatures':
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
    print(f" {data['name'].upper()} (ID: {data['id']})")
    print("="*45)

    if table_name == 'characters':
        pc_tag = "[PC]" if data['is_pc'] else "[NPC]"
        # FIXED: Changed 'class_role' to 'class_or_role'
        print(f"{pc_tag} {data['race']} | {data['class_or_role']}")

        # FIXED: Changed 'level_cr' to 'level' and 'hp' to 'hp_max'
        char_level = data.get('level', 1)
        print(f"Level: {char_level} | HP: {data['hp_max']} | AC: {data['ac']}")

        print(f"Stats: S:{data['strength']} D:{data['dexterity']} C:{data['constitution']} "
              f"I:{data['intelligence']} W:{data['wisdom']} Ch:{data['charisma']}")

        # FIXED: Check if affiliation exists before printing (optional safeguard)
        if 'affiliation' in data:
            print(f"Affiliation: {data['affiliation']}")

    elif table_name == 'creatures':
        print(
            f"Type: {data['size']} {data['creature_type']} | Alignment: {data['alignment']}")
        print(
            f"CR: {data['cr']} | HP: {data['hp']} | AC: {data['ac']} | XP: {data['xp']}")
        print(f"Attacks: {data['num_attacks']} | Damage: {data['damage']}")

    elif table_name == 'items':
        magical = "YES" if data['is_magical'] else "NO"
        attune = "YES" if data['requires_attunement'] else "NO"
        print(f"Category: {data['category']} | Rarity: {data['rarity']}")

        coins = []
        for den in ['pp', 'gp', 'ep', 'sp', 'cp']:
            if data.get(den, 0) > 0:
                coins.append(f"{data[den]}{den}")
        val_str = ", ".join(coins) if coins else "0gp"

        print(f"Value: {val_str} | Weight: {data['weight']} lbs")
        print(f"Magical: {magical} | Attunement Required: {attune}")

    elif table_name == 'locations':
        print(f"Type: {data['location_type']} | Region: {data['region']}")
        if data.get('parent_id'):
            print(f"Located Inside (Parent ID): {data['parent_id']}")

    print("-" * 45)

    # Universal Notes/Description check
    if table_name == 'locations':
        print(f"DESCRIPTION: {data['description']}")
        print(f"NOTES: {data['notes']}")
    elif table_name == 'items':
        print(f"DESCRIPTION: {data['description']}")
    else:
        print(f"NOTES: {data['notes']}")

    print("="*45)

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
        print("1. Export All Tables (Golden Backup)")
        print("2. Import Data from CSV")
        print("3. Initialize/Reset Database")
        print("0. Back to Main Menu")

        choice = input("\nSelection: ")

        if choice == '1':
            # Updated to include your full 9-table schema
            tables = [
                'characters', 'creatures', 'items', 'locations',
                'classes', 'races', 'spells', 'subclasses', 'subraces'
            ]
            for table in tables:
                try:
                    export_table_to_csv(table)
                except Exception as e:
                    print(f" [!] Failed to export {table}: {e}")
            print("\n[SUCCESS] All data backed up to the project folder.")

        elif choice == '2':
            print("\nTables: characters, creatures, items, locations, classes, races, spells, subclasses, subraces")
            table = input("Target Table: ").lower()
            file_path = input("Enter CSV filename: ")
            try:
                import_from_csv(table, file_path)
                print(f"\n[SUCCESS] {table} updated from {file_path}")
            except Exception as e:
                print(f"[!] Error during import: {e}")

        elif choice == '3':
            confirm = input("Are you SURE? This wipes all data! (y/n): ")
            if confirm.lower() == 'y':
                # Corrected to use your initialize_db() function
                db_init.initialize_db()
                print("\n[!] Database has been reset to factory defaults.")

        elif choice == '0':
            break


def parse_hit_die(hd_string):
    """Converts '1d12' into 12, or '1d8' into 8."""
    try:
        # Split at 'd' and take the second half
        return int(hd_string.lower().split('d')[1])
    except (ValueError, IndexError):
        return 6  # Safe default if the DB entry is messy


def run_character_wizard():
    """Main Orchestrator for Character Creation (Steps 1-7)."""
    db_path = os.path.join('data', 'campaign.db')

    # --- STEP 0: INITIAL IDENTITY & FLAG ---
    is_player = 1
    npc_check = input("Is this an NPC? (y/n): ").lower()
    if npc_check == 'y':
        is_player = 0

    entity_label = "Character" if is_player else "NPC"
    print(f"\n--- {entity_label} Creation Wizard ---")

    # --- DATABASE INIT (FIXED) ---
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # --- STEP 1: CHOOSE RACE ---
    cursor.execute("SELECT id, name FROM races")
    races = cursor.fetchall()

    print(f"\n--- Step 1: Choose {entity_label} Race ---")
    for row in races:
        print(f"{row['id']}. {row['name']}")

    race_choice = int(input("\nSelect a race ID: "))
    selected_base_race = next(
        (r for r in races if r['id'] == race_choice), None)

    # --- STEP 1.5: SUBRACE SELECTION ---
    cursor.execute(
        "SELECT id, name FROM subraces WHERE race_id = ?", (race_choice,))
    subraces = cursor.fetchall()

    if subraces:
        print(
            f"\n--- Step 1.5: Choose {selected_base_race['name']} Subrace ---")
        for sub in subraces:
            print(f"{sub['id']}. {sub['name']}")
        sub_choice = int(input("\nSelect a subrace ID: "))
        selected_sub = next(
            (s for s in subraces if s['id'] == sub_choice), None)
        selected_race_name = f"{selected_sub['name']} {selected_base_race['name']}"
    else:
        selected_race_name = selected_base_race['name']

    # --- STEP 2 & 3: ABILITY SCORES ---
    pool = roll_stats()
    base_stats = assign_stats(pool)

    # --- STEP 4: APPLY RACIAL BONUSES ---
    final_stats = apply_racial_bonuses(base_stats, selected_race_name)

    # --- STEP 5: CHOOSE CLASS ---
    cursor.execute("SELECT id, class_name, hit_die FROM classes")
    classes = cursor.fetchall()

    print(f"\n--- Step 5: Choose {entity_label} Class ---")
    for row in classes:
        print(f"{row['id']}. {row['class_name']} ({row['hit_die']})")

    class_choice = int(input("\nSelect Class ID: "))
    selected_base_class = next(
        (c for c in classes if c['id'] == class_choice), None)

    # --- STEP 5.5: SUBCLASS SELECTION ---
    cursor.execute(
        "SELECT id, name FROM subclasses WHERE class_id = ?", (class_choice,))
    subclasses = cursor.fetchall()

    if subclasses:
        print(
            f"\n--- Step 5.5: Choose {selected_base_class['class_name']} Archetype ---")
        for sc in subclasses:
            print(f"{sc['id']}. {sc['name']}")
        sc_choice = int(input("\nSelect Subclass ID: "))
        selected_subclass = next(
            (s for s in subclasses if s['id'] == sc_choice), None)
        role_display = f"{selected_subclass['name']} {selected_base_class['class_name']}"
    else:
        role_display = selected_base_class['class_name']

    # Corrected variable name: selected_base_class
    hd_max = parse_hit_die(selected_base_class['hit_die'])

    # --- STEP 6: CALCULATE VITALS ---
    con_mod = (final_stats.get('Constitution', 10) - 10) // 2
    max_hp = hd_max + con_mod
    dex_mod = (final_stats.get('Dexterity', 10) - 10) // 2
    base_ac = 10 + dex_mod

# --- STEP 6.5: AUTO-FETCH LEVEL 1 FEATURES ---
    # We use the class_choice (the ID) from Step 5
    cursor.execute("""
        SELECT feature_name, description 
        FROM class_features 
        WHERE class_id = ? AND level_required = 1
    """, (class_choice,))

    features = cursor.fetchall()

    if features:
        feature_text = "\n--- LEVEL 1 FEATURES ---\n"
        for f in features:
            feature_text += f"• {f['feature_name']}: {f['description']}\n"
    else:
        feature_text = "No level 1 features found."

    # --- STEP 7: IDENTITY & BACKGROUND ---
    print(f"\n--- Step 7: Final Details ---")
    char_name = input(f"Enter {entity_label} Name: ")
    alignment = input("Enter Alignment: ")

    if not is_player:
        role_note = input("Enter NPC Role/Motivation: ")
        role_display = f"{role_display} ({role_note})"

    # --- SAVE ---
    new_character = {
        "name": char_name,
        "race": selected_race_name,
        "class_or_role": role_display,
        "alignment": alignment,
        "hp_max": max_hp,
        "hp_current": max_hp,
        "ac": base_ac,
        "is_pc": is_player,
        "strength": final_stats['Strength'],
        "dexterity": final_stats['Dexterity'],
        "constitution": final_stats['Constitution'],
        "intelligence": final_stats['Intelligence'],
        "wisdom": final_stats['Wisdom'],
        "charisma": final_stats['Charisma'],
        "notes": feature_text  # <--- Features automatically added here!
    }

    add_record('characters', new_character)
    conn.close()

    print(f"\n[SUCCESS] {char_name} has been added to Arcanryn!")

    return new_character


def handle_view_character():
    """Fetches a character from the DB and displays a formatted sheet."""
    search_term = input("\nEnter Character Name or ID to view: ")

    # Using your existing hybrid finder
    char = find_by_hybrid('characters', search_term)

    if not char:
        print(f"No character found matching '{search_term}'.")
        return

    # Header section
    print("\n" + "="*50)
    print(f" {char['name'].upper().center(48)} ")
    print("="*50)

    # Identity Line
    pc_tag = "[PC]" if char['is_pc'] else "[NPC]"
    print(
        f"{pc_tag} {char['race']} | {char['class_or_role']} | Level {char.get('level', 1)}")
    print(f"Alignment: {char['alignment']}")
    print("-" * 50)

    # Vitals Section
    #
    print(f" HP: {char['hp_current']}/{char['hp_max']} ".center(24) +
          f" AC: {char['ac']} ".center(24))
    print("-" * 50)

    # Ability Scores & Modifiers
    #
    print(f"{'STAT':<12} | {'SCORE':<8} | {'MOD':<5}")
    print("-" * 30)

    stats = ['strength', 'dexterity', 'constitution',
             'intelligence', 'wisdom', 'charisma']
    for stat in stats:
        score = char.get(stat, 10)
        modifier = (score - 10) // 2
        print(f"{stat.capitalize():<12} | {score:<8} | {modifier:+}")

    # Features and Notes
    if char.get('notes'):
        print("\n" + "-" * 50)
        print(" FEATURES & NOTES ")
        print("-" * 50)
        print(char['notes'])

    print("="*50)
    input("\nPress Enter to return to menu...")
