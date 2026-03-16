import json
import sqlite3
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign.db')
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
            # Use the full URL from the JSON results
            api_url = BASE_URL + sc['url']
            response = requests.get(api_url)

            if response.status_code != 200:
                print(f"[!] API Error {response.status_code} for {sc['name']}")
                continue

            res = response.json()

            # Use .get() to prevent crashes if a key is missing
            sub_name = res.get('name')
            parent_class_name = res.get('class', {}).get('name')

            # 1. Find the Parent Class ID (Using 'class_name' to match your DB)
            cursor.execute(
                "SELECT id FROM classes WHERE class_name = ?", (parent_class_name,))
            class_row = cursor.fetchone()
            class_id = class_row[0] if class_row else None

            # 2. Match your variable names!
            # If the DB column is 'flavor_text', let's name the variable that.
            flavor_text = res.get('subclass_flavor', '')

            # 3. Handle Description
            desc_list = res.get('desc', [])
            description = "\n".join(desc_list) if isinstance(
                desc_list, list) else str(desc_list)

            # 4. Final Insert (Variables match the names above)
            cursor.execute('''
                INSERT INTO subclasses (class_id, name, flavor_text)
                VALUES (?, ?, ?)
            ''', (class_id, sub_name, flavor_text))

            print(
                f"[>] Imported Subclass: {sub_name} (Parent: {parent_class_name})")

        except Exception as e:
            # This will now tell you exactly WHICH variable or key is failing
            print(f"[!] Error importing {sc.get('name', 'Unknown')}: {e}")

    conn.commit()
    conn.close()
    print("[SUCCESS] Subclasses table is populated!")


if __name__ == "__main__":
    run_subclass_importer()
