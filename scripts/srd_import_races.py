import json
import sqlite3
import os
import requests

# Standard path logic
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Races.json')
BASE_URL = "https://www.dnd5eapi.co"


def run_race_importer():
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    with open(SOURCE_JSON, 'r') as f:
        race_list = json.load(f).get('results', [])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"[*] Starting import of {len(race_list)} races...")

    for race in race_list:
        try:
            res = requests.get(BASE_URL + race['url']).json()

            name = res.get('name')
            speed = res.get('speed', 30)
            size = res.get('size', 'Medium')
            alignment = res.get('alignment', '')

            # Ability Bonuses: Convert list of objects to a readable string
            # Example: "DEX +2, CON +1"
            bonuses = []
            for bonus in res.get('ability_bonuses', []):
                score = bonus.get('ability_score', {}).get('name')
                val = bonus.get('bonus')
                bonuses.append(f"{score} +{val}")
            ability_str = ", ".join(bonuses)

            # Traits: Just the names for a quick overview
            trait_names = [t.get('name') for t in res.get('traits', [])]
            traits_str = ", ".join(trait_names)

            cursor.execute('''
                INSERT INTO races (
                    name, speed, ability_bonuses, alignment, size, traits
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, speed, ability_str, alignment, size, traits_str))

            print(f"[>] Imported Race: {name}")

        except Exception as e:
            print(f"[!] Error importing {race.get('name')}: {e}")

    conn.commit()
    conn.close()
    print("\n[SUCCESS] Races table is populated!")


if __name__ == "__main__":
    run_race_importer()
