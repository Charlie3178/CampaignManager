import json
import sqlite3
import os
import requests
import time

# This finds the absolute path to the 'scripts' folder where this file lives
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Now it builds the path from the root, regardless of where you run it from
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Monsters.json')
BASE_URL = "https://www.dnd5eapi.co"


def flatten_list(data_list):
    """Turns lists of objects (like actions) into a single string."""
    if not data_list:
        return ""
    return "\n\n".join([f"{i.get('name')}: {i.get('desc')}" for i in data_list])


def flatten_dict(data_dict):
    """Turns dictionaries (like speed) into a readable string."""
    if not data_dict:
        return ""
    return ", ".join([f"{k}: {v}" for k, v in data_dict.items()])


def run_importer():
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    with open(SOURCE_JSON, 'r') as f:
        index_data = json.load(f)

    monsters_list = index_data.get('results', [])
    print(f"[*] Found {len(monsters_list)} monsters. Starting download...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for idx, item in enumerate(monsters_list):
        try:
            # Fetch the full data for each monster
            response = requests.get(BASE_URL + item['url'])
            if response.status_code != 200:
                continue
            m = response.json()

            # Process complex fields
            ac = m.get('armor_class', [{}])[0].get('value', 0)
            speed = flatten_dict(m.get('speed'))
            senses = flatten_dict(m.get('senses'))

            # Combine all resistances/immunities for simplicity
            res = f"Resist: {m.get('damage_resistances')} | Immune: {m.get('damage_immunities')} | Cond: {m.get('condition_immunities')}"

            # Prepare the row
            data = (
                m.get('name'), m.get('size'), m.get(
                    'type'), m.get('alignment'),
                ac, m.get('hit_points'), m.get('hit_dice'), speed,
                m.get('strength'), m.get('dexterity'), m.get('constitution'),
                m.get('intelligence'), m.get('wisdom'), m.get('charisma'),
                str(m.get('challenge_rating')), m.get('xp'), senses,
                m.get('languages'), res,
                flatten_list(m.get('special_abilities')),
                flatten_list(m.get('actions')),
                flatten_list(m.get('legendary_actions')),
                ""  # Description placeholder
            )

            query = '''INSERT INTO creatures (
                name, size, creature_type, alignment, ac, hp, hit_dice, speed,
                str, dex, con, int, wis, cha, cr, xp, senses, languages,
                resistances, abilities, actions, legendary_actions, description
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

            cursor.execute(query, data)

            if idx % 10 == 0:
                print(
                    f"[>] Processed {idx}/{len(monsters_list)}: {m.get('name')}")
                conn.commit()  # Save progress every 10

            time.sleep(0.1)  # Be nice to the API

        except Exception as e:
            print(f"[!] Error processing {item['name']}: {e}")

    conn.commit()
    conn.close()
    print("\n[SUCCESS] Bestiary is fully populated!")


if __name__ == "__main__":
    run_importer()
