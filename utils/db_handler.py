import sqlite3
import os
import csv


def get_connection():
    """Calculates path and returns a live connection to the /data folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    db_path = os.path.normpath(os.path.join(
        project_root, 'data', 'campaign.db'))

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- DATABASE MANAGEMENT FUNCTIONS ---


def export_table_to_csv(table_name):
    """Generates a CSV template and saves it in the /data folder."""
    conn = get_connection()
    cursor = conn.cursor()

    # Calculate the path to the data folder for the CSV output
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    # This places the CSV inside F:\__CampaignManager\data\
    output_path = os.path.normpath(os.path.join(
        project_root, 'data', f"{table_name}_template.csv"))

    try:
        # Get headers even if table is empty
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
        headers = [desc[0] for desc in cursor.description]

        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            # Write data if any exists
            cursor.execute(f"SELECT * FROM {table_name}")
            for row in cursor.fetchall():
                writer.writerow(dict(row))

        print(f"[SUCCESS] Created export at: {output_path}")
    except sqlite3.OperationalError as e:
        print(f"[!] Export Error: {e}")
    finally:
        conn.close()


def import_from_csv(table_name, file_name):
    # 1. Calculate path (Get the project root from this file's location)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)

    # 2. Force the search into the 'data' folder
    file_path = os.path.normpath(os.path.join(project_root, 'data', file_name))

    if not os.path.exists(file_path):
        print(f"[!] File not found in data folder: {file_name}")
        return

    # 3. Open and Process File
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean numeric data: Convert strings to int/float
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif value.replace('.', '', 1).isdigit():
                    try:
                        row[key] = float(value)
                    except ValueError:
                        pass  # Keep as string if it's not actually a float

            # 4. Use your existing add_record function to save to DB
            add_record(table_name, row)

    # IMPORTANT: This print must be indented inside the function
    print(f"[SUCCESS] Imported data into {table_name}!")


def bulk_import(tables):
    for table in tables:
        file_name = f"{table}_template.csv"
        import_from_csv(table, file_name)


def export_all():
    """The 'Golden Backup' - Exports all 17 tables to CSV templates."""
    tables = [
        'characters', 'creatures', 'items', 'locations', 'classes', 'spells',
        'races', 'subraces', 'subclasses', 'lore', 'notes', 'features',
        'backgrounds', 'feats', 'traits', 'proficiencies', 'languages'
    ]
    print("\n--- STARTING GOLDEN BACKUP (EXPORT) ---")
    for table in tables:
        file_name = f"{table}_template.csv"
        try:
            # Reusing your existing export logic
            export_table_to_csv(table)
            print(f" [OK] Exported {table} to {file_name}")
        except Exception as e:
            print(f" [!] Failed to export {table}: {e}")
    print("\n[SUCCESS] All tables exported to /data folder.")


# --- CRUD FUNCTIONS FOR MENU_SCRIPTS ---


def add_record(table, data_dict):
    """Generic inserter used by 'Create' menus."""
    conn = get_connection()
    cursor = conn.cursor()
    columns = ', '.join(data_dict.keys())
    placeholders = ', '.join(['?'] * len(data_dict))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(query, list(data_dict.values()))
        conn.commit()
    finally:
        conn.close()


def delete_by_id(table, item_id):
    """Generic deleter used by 'Delete' menus."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def find_by_hybrid(table, search_input):
    """Searches by ID or the first text-based column available in the table."""
    conn = get_connection()
    # Ensure you are using Row factory to get the dictionary-like results
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if str(search_input).isdigit():
        query = f"SELECT * FROM {table} WHERE id = ?"
        cursor.execute(query, (int(search_input),))
    else:
        # 1. Get the column names for this specific table
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]

        # 2. Pick the best 'name' column (fallback to first text column if 'name' is missing)
        search_col = 'name' if 'name' in columns else columns[1]

        query = f"SELECT * FROM {table} WHERE {search_col} LIKE ?"
        cursor.execute(query, (f"%{search_input}%",))

    results = cursor.fetchall()
    conn.close()

    if results:
        # Now this will return the full Row object which you can print keys from
        return results[0]
    return None


def get_all(table):
    """Retrieves all records for 'List All' views."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    results = cursor.fetchall()
    conn.close()
    return results


def update_record(table, item_id, update_data):
    """Generic updater used by 'Edit' menus."""
    conn = get_connection()
    cursor = conn.cursor()
    keys = [f"{key} = ?" for key in update_data.keys()]
    query = f"UPDATE {table} SET {', '.join(keys)} WHERE id = ?"
    values = list(update_data.values())
    values.append(item_id)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
