import json
import sqlite3
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign_base.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Subclasses.json')
BASE_URL = "https://www.dnd5eapi.co"


def run_subclass_importer():
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SOURCE_JSON, 'r') as f:
        subclass_list = json.load(f).get('results', [])

    print(f"[*] Starting import of {len(subclass_list)} subclasses...")

    for sc in subclass_list:
        try:
            res = requests.get(BASE_URL + sc['url']).json()
            name = res.get('name')
            parent_class_name = res.get('class', {}).get('name')

            # 1. Find the Parent Class ID
            cursor.execute(
                "SELECT id FROM classes WHERE name = ?", (parent_class_name,))
            class_row = cursor.fetchone()
            class_id = class_row[0] if class_row else None

            flavor = res.get('subclass_flavor', '')

            # 2. Features list
            # Some APIs nest features differently
            features = [f['name'] for f in res.get('spells', [])]
            # For SRD, usually the main info is in 'desc'
            desc_list = res.get('desc', [])
            description = "\n".join(desc_list)

            cursor.execute('''
                INSERT INTO subclasses (class_id, name, flavor_text, features)
                VALUES (?, ?, ?, ?)
            ''', (class_id, name, flavor, description))

            print(
                f"[>] Imported Subclass: {name} (Parent: {parent_class_name})")

        except Exception as e:
            print(f"[!] Error importing {sc.get('name')}: {e}")

    conn.commit()
    conn.close()
    print("[SUCCESS] Subclasses table is populated!")


if __name__ == "__main__":
    run_subclass_importer()
