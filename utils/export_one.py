import os
import sys
import csv
import sqlite3


# fmt: off
# Adds the main project folder to the path so it can find your db_handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_handler import get_connection
# fmt: on


def export_template():
    # 1. Directly target the /data folder relative to this script
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(utils_dir)
    data_dir = os.path.join(project_root, 'data')

    # 2. Get the tables
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    print("\n--- SRD TEMPLATE EXPORTER ---")
    for i, table in enumerate(tables, 1):
        print(f"[{i}] {table}")
    print("[0] Exit")

    choice = input("\nSelect table to export: ")
    if choice == '0':
        return

    try:
        idx = int(choice) - 1
        table_name = tables[idx]

        # 3. Save directly into project_root/data/
        filename = os.path.join(data_dir, f"{table_name}_template.csv")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")

        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(colnames)
            writer.writerows(rows)

        print(f"\n[SUCCESS] Created: {filename}")
        conn.close()

    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    export_template()
