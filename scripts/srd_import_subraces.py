import json
import sqlite3
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Subraces.json')
BASE_URL = "https://www.dnd5eapi.co"


def run_subrace_importer():
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SOURCE_JSON, 'r') as f:
        subrace_list = json.load(f).get('results', [])

    print(f"[*] Starting import of {len(subrace_list)} subraces...")

    for sr in subrace_list:
        try:
            res = requests.get(BASE_URL + sr['url']).json()
            name = res.get('name')
            parent_race_name = res.get('race', {}).get('name')

            # 1. Find the Parent Race ID
            cursor.execute("SELECT id FROM races WHERE name = ?",
                           (parent_race_name,))
            race_row = cursor.fetchone()
            race_id = race_row[0] if race_row else None

            # 2. Ability Bonuses
            bonuses = [
                f"{b['ability_score']['name']} +{b['bonus']}" for b in res.get('ability_bonuses', [])]
            ability_str = ", ".join(bonuses)

            # 3. Traits
            traits = [t['name'] for t in res.get('racial_traits', [])]
            traits_str = ", ".join(traits)

            cursor.execute('''
                INSERT INTO subraces (race_id, name, ability_bonuses, traits)
                VALUES (?, ?, ?, ?)
            ''', (race_id, name, ability_str, traits_str))

            print(f"[>] Imported Subrace: {name} (Parent: {parent_race_name})")

        except Exception as e:
            print(f"[!] Error importing {sr.get('name')}: {e}")

    conn.commit()
    conn.close()
    print("[SUCCESS] Subraces table is populated!")


if __name__ == "__main__":
    run_subrace_importer()
