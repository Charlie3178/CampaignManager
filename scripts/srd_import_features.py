import json
import sqlite3
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'campaign.db')
SOURCE_JSON = os.path.join(
    BASE_DIR, 'data', 'API Endpoints', 'SRD-5e-Features.json')
BASE_URL = "https://www.dnd5eapi.co"


def run_feature_importer():
    if not os.path.exists(SOURCE_JSON):
        print(f"[!] {SOURCE_JSON} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SOURCE_JSON, 'r') as f:
        feature_list = json.load(f).get('results', [])

    print(f"[*] Starting import of {len(feature_list)} features...")

    for feat in feature_list:
        try:
            res = requests.get(BASE_URL + feat['url']).json()

            f_name = res.get('name')
            level = res.get('level', 0)

            # Combine description list into one string
            desc_list = res.get('desc', [])
            description = "\n".join(desc_list) if isinstance(
                desc_list, list) else str(desc_list)

            # 1. Handle Class Link
            class_name = res.get('class', {}).get('name')
            cursor.execute(
                "SELECT id FROM classes WHERE class_name = ?", (class_name,))
            class_row = cursor.fetchone()
            class_id = class_row[0] if class_row else None

            # 2. Handle Subclass Link
            subclass_name = res.get('subclass', {}).get('name')
            cursor.execute(
                "SELECT id FROM subclasses WHERE name = ?", (subclass_name,))
            sub_row = cursor.fetchone()
            subclass_id = sub_row[0] if sub_row else None

            # 3. Determine Source Type
            source_type = 'Subclass' if subclass_id else 'Class'

            # 4. Insert into the centralized table
            cursor.execute('''
                INSERT INTO class_features (
                    feature_name, level_required, description, 
                    source_type, class_id, subclass_id
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (f_name, level, description, source_type, class_id, subclass_id))

            print(
                f"[>] Imported: {f_name} ({source_type}: {subclass_name if subclass_id else class_name})")

        except Exception as e:
            print(f"[!] Error importing {feat.get('name')}: {e}")

    conn.commit()
    conn.close()
    print("[SUCCESS] Feature table is fully populated!")


if __name__ == "__main__":
    run_feature_importer()
