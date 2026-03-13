import sqlite3
import os


def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'campaign_base.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def find_by_hybrid(table, search_input):
    """Searches by ID if numeric, otherwise by Name."""
    conn = get_connection()
    cursor = conn.cursor()

    if str(search_input).isdigit():
        query = f"SELECT * FROM {table} WHERE id = ?"
        cursor.execute(query, (int(search_input),))
    else:
        query = f"SELECT * FROM {table} WHERE name LIKE ?"
        cursor.execute(query, (f"%{search_input}%",))

    results = cursor.fetchall()
    conn.close()
    return results


def get_all(table):
    """Retrieves all records for 'List All' views."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    results = cursor.fetchall()
    conn.close()
    return results


def delete_by_id(table, item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def add_record(table, data_dict):
    """
    Generic inserter. 
    data_dict keys must match table column names.
    """
    conn = get_connection()
    cursor = conn.cursor()

    columns = ', '.join(data_dict.keys())
    placeholders = ', '.join(['?'] * len(data_dict))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    cursor.execute(query, list(data_dict.values()))
    conn.commit()
    conn.close()


def update_record(table, item_id, update_data):
    """
    A generic updater. 
    update_data should be a dictionary: {"column_name": new_value}
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Dynamically build the SQL SET string (e.g., "name = ?, hp = ?")
    keys = [f"{key} = ?" for key in update_data.keys()]
    query = f"UPDATE {table} SET {', '.join(keys)} WHERE id = ?"

    # Combine values and ID for the final execution
    values = list(update_data.values())
    values.append(item_id)

    cursor.execute(query, values)
    conn.commit()
    conn.close()
