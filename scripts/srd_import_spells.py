import json
import sqlite3
import os
import requests

# Path logic for running from the scripts folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign_base.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Spells.json')
BASE_URL = "https://www.dnd5eapi.co"


def run_spell_importer():
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    with open(SOURCE_JSON, 'r') as f:
        spell_list = json.load(f).get('results', [])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"[*] Starting import of {len(spell_list)} spells...")

    for spell in spell_list:
        try:
            res = requests.get(BASE_URL + spell['url']).json()

            name = res.get('name')
            level = res.get('level', 0)
            school = res.get('school', {}).get('name', '')
            casting_time = res.get('casting_time', '')
            spell_range = res.get('range', '')

            # Components come in a list [V, S, M]
            components = ", ".join(res.get('components', []))

            duration = res.get('duration', '')
            concentration = 1 if res.get('concentration') else 0
            ritual = 1 if res.get('ritual') else 0

            # Description is usually a list of strings
            desc_list = res.get('desc', [])
            description = "\n".join(desc_list)

            # Higher level scaling
            higher_list = res.get('higher_level', [])
            higher_level = "\n".join(higher_list) if higher_list else ""

            cursor.execute('''
                INSERT INTO spells (
                    name, level, school, casting_time, range, 
                    components, duration, concentration, ritual, 
                    description, higher_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, level, school, casting_time, spell_range,
                  components, duration, concentration, ritual,
                  description, higher_level))

            print(f"[>] Imported: {name} (Level {level})")

        except Exception as e:
            print(f"[!] Error importing {spell.get('name')}: {e}")

    conn.commit()
    conn.close()
    print("\n[SUCCESS] Spells table is populated!")


if __name__ == "__main__":
    run_spell_importer()
