import os
import sys
import sqlite3

# fmt: off
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_handler import get_connection
from scripts.import_srd import (
    fetch_srd, process_creatures, process_races, process_subraces,
    process_classes, process_subclasses, process_spells, process_features,
    process_items, process_feats, process_backgrounds, process_traits,
    process_languages, process_proficiencies, process_skills
)

#fmt: on


def run_targeted_sync():
    # Map the menu options to the (API Path, Processing Function)
    options = {
        "1": ("creatures", "monsters", process_creatures),
        "2": ("races", "races", process_races),
        "3": ("subraces", "subraces", process_subraces),
        "4": ("classes", "classes", process_classes),
        "5": ("subclasses", "subclasses", process_subclasses),
        "6": ("spells", "spells", process_spells),
        "7": ("features", "features", process_features),
        "8": ("items", "equipment", process_items),
        "9": ("magic_items", "magic-items", process_items),
        "10": ("feats", "feats", process_feats),
        "11": ("backgrounds", "backgrounds", process_backgrounds),
        "12": ("traits", "traits", process_traits),
        "13": ("languages", "languages", process_languages),
        "14": ("proficiencies", "proficiencies", process_proficiencies),
        "15": ("skills", "skills", process_skills)
    }

    while True:
        print("\n--- SRD TARGETED SYNC ---")
        for k, v in options.items():
            print(f"[{k}] {v[0].replace('_', ' ').title()}")
        print("[0] Exit")

        choice = input("\nWhich endpoint do you want to sync? ")

        if choice == '0':
            break

        if choice in options:
            table_label, api_path, func = options[choice]
            print(f"\n>>> Starting sync for {table_label}...")

            conn = get_connection()
            cursor = conn.cursor()

            try:
                data = fetch_srd(api_path)
                if data and 'results' in data:
                    func(cursor, data['results'])
                    conn.commit()
                    print(f"\n[SUCCESS] {table_label} sync complete.")
                else:
                    print(f"[!] No data found for {api_path}")
            except Exception as e:
                print(f"[ERROR] Sync failed: {e}")
            finally:
                conn.close()
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    run_targeted_sync()
