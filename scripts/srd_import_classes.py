import json
import sqlite3
import os
import requests

# This finds the absolute path to the 'scripts' folder where this file lives
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Now it builds the path from the root, regardless of where you run it from
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign_base.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Classes.json')
BASE_URL = "https://www.dnd5eapi.co"


def run_class_importer():
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    with open(SOURCE_JSON, 'r') as f:
        class_list = json.load(f).get('results', [])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for item in class_list:
        # Fetch detailed info for each class
        res = requests.get(BASE_URL + item['url']).json()

        cursor.execute('''
            INSERT INTO classes (class_name, hit_die, primary_ability, features)
            VALUES (?, ?, ?, ?)
        ''', (
            res.get('name'),
            f"d{res.get('hit_die')}",
            "Multiple",  # Can be refined later
            ", ".join([p['name'] for p in res.get('proficiencies', [])])
        ))
        print(f"[>] Imported Class: {res.get('name')}")

    conn.commit()
    conn.close()
    print("\n[SUCCESS] Classes table is populated!")


if __name__ == "__main__":
    run_class_importer()
