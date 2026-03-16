import json
import sqlite3
import os
import requests

# Path logic: finds the project root regardless of where script is run
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Items.json')
BASE_URL = "https://www.dnd5eapi.co"


def run_item_importer():
    # 1. Check for the local JSON first (faster)
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    with open(SOURCE_JSON, 'r') as f:
        item_list = json.load(f).get('results', [])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"[*] Starting import of {len(item_list)} items...")

    for item in item_list:
        try:
            # Fetch details from API (or local if you have the full objects)
            res = requests.get(BASE_URL + item['url']).json()

            name = res.get('name')
            category = res.get('equipment_category', {}).get('name', 'General')

            # Formatting Cost (e.g., 10 gp)
            cost_data = res.get('cost', {})
            cost_str = f"{cost_data.get('quantity', 0)} {cost_data.get('unit', '')}"

            weight = res.get('weight', 0)

            # Combine description list into one block
            desc_list = res.get('desc', [])
            description = " ".join(desc_list) if desc_list else ""

            # Identify Rarity (if available in API)
            rarity = res.get('rarity', {}).get('name', 'Common')

            # Logic for Attunement Flag
            # The API usually puts this in the description text
            attunement_needed = 1 if "requires attunement" in description.lower() else 0

            # Collect properties (for weapons/armor)
            props = ", ".join([p['name'] for p in res.get('properties', [])])

            cursor.execute('''
                INSERT INTO items (
                    name, category, cost, weight, description, 
                    requires_attunement, rarity, properties
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, category, cost_str, weight, description, attunement_needed, rarity, props))

            print(f"[>] Imported: {name}")

        except Exception as e:
            print(f"[!] Error importing {item.get('name')}: {e}")

    conn.commit()
    conn.close()
    print("\n[SUCCESS] Items table is populated with attunement and rarity data!")


if __name__ == "__main__":
    run_item_importer()
