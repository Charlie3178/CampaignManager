# Assuming this is your current helper
from utils.db_handler import add_record, get_connection, find_by_hybrid, delete_by_id, update_record
from utils.db_handler import export_table_to_csv, import_from_csv, bulk_import, export_all
from scripts.db_init import initialize_db
from scripts.import_srd import import_all
from utils.roller import roll_stats, assign_stats, apply_racial_bonuses
import sqlite3
import os
import textwrap


def handle_list_all(table_name):
    """Lists ID and Name for any table, with special formatting for Creatures."""
    conn = get_connection()
    cursor = conn.cursor()

    # Custom query for Creatures to show CR and Type
    if table_name == 'creatures':
        cursor.execute(f"SELECT id, name, cr, creature_type FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\n--- Creatures SUMMARY ---")
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

    elif table_name == 'skills':
        cursor.execute(f"SELECT id, name, ability_score FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\n--- SKILLS LIBRARY ---")
        print(f"{'ID':<4} | {'NAME':<20} | {'STAT'}")
        print("-" * 35)
        for row in rows:
            print(f"{row['id']:<4} | {row['name']:<20} | {row['ability_score']}")

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
        data['cclass'] = input("Class/Role: ")
        data['subclass'] = input("Subclass: ")
        data['level'] = edit_func("Level", 1)
        data['mhp'] = edit_func("Max HP", 10)
        data['chp'] = data['mhp']
        data['ac'] = edit_func("AC", 10)
        data['str'] = edit_func("Str", 10)
        data['dex'] = edit_func("Dex", 10)
        data['con'] = edit_func("Con", 10)
        data['int'] = edit_func("Int", 10)
        data['wis'] = edit_func("Wis", 10)
        data['cha'] = edit_func("Cha", 10)
        data['disposition'] = input("Disposition (Friendly/Hostile/etc): ")
        data['pcc'] = 1 if input(
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


def display_details(table, row):
    """
    Handles varying schemas across 18 tables by using 
    fallback keys and safe .get() calls.
    """
    # 1. Convert row to a dict so .get() works reliably
    data = dict(row)

    # 2. THE HEADER (Fixes Bug 11)
    # Checks 'name' first, then 'title' (used in Lore/Notes), then 'Unknown'
    name_val = data.get('name') or data.get('title') or "Unknown Entry"
    entry_id = data.get('id', '??')

    print("\n" + "="*50)
    print(f" {name_val.upper()} (ID: {entry_id}) ".center(50))
    print("="*50)

    # 3. TABLE-SPECIFIC FORMATTING
    if table == 'creatures':
        print(
            f"CR: {data.get('cr', '0')} | Type: {data.get('size', '')} {data.get('creature_type', '')}")
        print(
            f"AC: {data.get('ac', '10')} | HP: {data.get('hp', '0')} | Speed: {data.get('speed', '30ft')}")
        print("-" * 50)
        print(
            f"STR: {data.get('str')} | DEX: {data.get('dex')} | CON: {data.get('con')}")
        print(
            f"INT: {data.get('int')} | WIS: {data.get('wis')} | CHA: {data.get('cha')}")

    elif table == 'items':
        print(
            f"Category: {data.get('category')} | Rarity: {data.get('rarity')}")
        print(
            f"Cost: {data.get('cost', '0gp')} | Weight: {data.get('weight', 0)} lbs")

    elif table == 'spells':
        print(f"Level: {data.get('level')} | School: {data.get('school')}")
        print(
            f"Casting Time: {data.get('casting_time')} | Range: {data.get('range')}")
        print(
            f"Components: {data.get('components')} | Duration: {data.get('duration')}")

    elif table == 'skills':
        print(
            f"Ability: {data.get('ability_score')} | Category: {data.get('category')}")

    # 4. THE UNIVERSAL FALLBACK (Fixes Bugs 1-10)
    # Searches through every possible 'description' column name from your db_init.py
    description_text = (
        data.get('notes') or
        data.get('description') or
        data.get('desc') or
        data.get('traits') or
        data.get('flavor') or
        data.get('profs') or
        data.get('content') or
        "No additional details found in database."
    )

    print("-" * 50)
    print("DETAILS:")
    # Wrap text to 48 chars so it doesn't break the console layout
    print(textwrap.fill(str(description_text), width=48))

    print("="*50)
    input("\nPress Enter to return...")


def handle_search(table):
    search_input = input(f"\nEnter {table.rstrip('s')} Name or ID: ")

    # 1. Fetch the actual record from the database
    # Assuming your db_handler has the find_by_hybrid function
    row = find_by_hybrid(table, search_input)

    # 2. Check if a record was actually found
    if row:
        # 3. Pass the DATABASE ROW (a dict-like object), not the input string
        display_details(table, row)
    else:
        print(f"\n[ERROR] No record found in {table} for '{search_input}'.")


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
    """Matches your GitHub release: No renamed functions, no invented wrappers."""
    while True:
        print("\n--- DATABASE MANAGEMENT ---")
        print("1. Export All Tables (Golden Backup)")
        print("2. Bulk Sync All CSVs (Import All)")
        print("3. Import SRD Data (Monsters & Spells)")
        print("4. Initialize/Reset Database")
        print("0. Back to Main Menu")

        choice = input("\nSelection: ")

        if choice == '1':
            # This is your existing function that produced your screenshot
            export_all()

        elif choice == '2':
            # This is the function we just added/fixed in db_handler
            handle_bulk_sync()

        elif choice == '3':
            # Your existing, separate SRD function
            import_all()

        elif choice == '4':
            confirm = input(
                "[!] WARNING: This will wipe all data. Continue? (y/n): ")
            if confirm.lower() == 'y':
                initialize_db()

        elif choice == '0':
            break


def parse_hit_die(hd_string):
    """Converts '1d12' into 12, or '1d8' into 8."""
    try:
        return int(hd_string.lower().split('d')[1])
    except (ValueError, IndexError):
        return 6


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

    hd_max = parse_hit_die(selected_base_class['hit_die'])

    # --- STEP 6: CALCULATE VITALS ---
    con_mod = (final_stats.get('Constitution', 10) - 10) // 2
    mhp = hd_max + con_mod
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
        "cclass": role_display,
        "alignment": alignment,
        "mhp": mhp,
        "chp": mhp,
        "ac": base_ac,
        "pc": is_player,
        "str": final_stats['Strength'],
        "dex": final_stats['Dexterity'],
        "con": final_stats['Constitution'],
        "int": final_stats['Intelligence'],
        "wis": final_stats['Wisdom'],
        "cha": final_stats['Charisma'],
        "notes": feature_text  # <--- Features automatically added here!
    }

    add_record('characters', new_character)
    conn.close()
    print(f"\n[SUCCESS] {char_name} has been added to Arcanryn!")
    return new_character


def handle_view_character():
    """Fetches a character from the DB and displays a formatted sheet."""
    search_term = input("\nEnter Character Name or ID to view: ")

    char = find_by_hybrid('characters', search_term)
    if not char:
        print(f"No character found matching '{search_term}'.")
        return

    # Header section
    print("\n" + "="*50)
    print(f" {char['name'].upper().center(48)} ")
    print("="*50)
    # Identity Line
    pc_tag = "[PC]" if char['pc'] else "[NPC]"
    print(
        f"{pc_tag} Race ID: {char['race']} | Class ID: {char['cclass']} | Level {char['lvl']}")
    print(f" HP: {char['chp']}/{char['mhp']} ".center(24) +
          f" AC: {char['ac']} ".center(24))
    # Vitals Section
    #
    print(f" HP: {char['chp']}/{char['mhp']} ".center(24) +
          f" AC: {char['ac']} ".center(24))
    print("-" * 50)
    # Ability Scores & Modifiers
    #
    print(f"{'STAT':<12} | {'SCORE':<8} | {'MOD':<5}")
    print("-" * 30)
    stats = ['str', 'dex', 'con',
             'int', 'wis', 'cha']
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

    # Generic creater for non-character tables


def handle_create_generic(table_name):
    # Dynamically asks for input based on table columns.
    conn = get_connection()
    cursor = conn.cursor()
    # Get column names (excluding 'id')
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row['name'] for row in cursor.fetchall() if row['name'] != 'id']
    new_data = {}
    print(f"\n--- Create New {table_name[:-1].capitalize()} ---")
    for col in columns:
        val = input(f"{col.replace('_', ' ').capitalize()}: ")
        # Basic type conversion: if it looks like a number, make it one
        if val.isdigit():
            new_data[col] = int(val)
        else:
            new_data[col] = val
    # Use your existing add_record utility
    add_record(table_name, new_data)
    print(f"Successfully added to {table_name}!")
    conn.close()


def handle_view_creature():
    """Detailed Stat Block view for SRD and Homebrew creatures."""
    search_term = input("\nEnter Creature Name or ID: ")
    monster = find_by_hybrid('creatures', search_term)

    if not monster:
        print(f"Creature '{search_term}' not found.")
        return

    print("\n" + "="*50)
    print(f" {monster['name'].upper()} (CR: {monster['cr']}) ".center(50))
    print("-" * 50)
    print(
        f"Type: {monster['size']} {monster['creature_type']} | AC: {monster['ac']} | HP: {monster['hp']}")
    print(f"Speed: {monster['speed']}")
    print("-" * 50)
    # Since monsters have flat stats in the SRD table:
    print(
        f"STR: {monster['str']} | DEX: {monster['dex']} | CON: {monster['con']}")
    print(
        f"INT: {monster['int']} | WIS: {monster['wis']} | CHA: {monster['cha']}")

    if monster.get('description'):
        print("-" * 50)
        print(monster['description'])
    print("="*50)
    input("\nPress Enter to return...")


def handle_bulk_sync():
    tables = [
        'characters', 'creatures', 'items', 'locations', 'classes', 'spells',
        'races', 'subraces', 'subclasses', 'lore', 'notes', 'features',
        'backgrounds', 'feats', 'traits', 'proficiencies', 'languages', 'skills'
    ]
    print("\n--- STARTING BULK SYNC ---")
    bulk_import(tables)
    print("\n[SUCCESS] Sync Complete.")
