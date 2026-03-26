import sqlite3
import json
from utils.api_helper import fetch_srd
from utils.db_handler import get_connection

# --- MAPPER FUNCTIONS ---


def process_creatures(cursor, results):
    for item in results:
        detail = fetch_srd(f"monsters/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Creature: {detail['name']}")

        ac_val = detail['armor_class'][0]['value'] if detail.get(
            'armor_class') else 10
        cursor.execute('''
            INSERT INTO creatures (name, size, creature_type, alignment, ac, hp, str, dex, con, int, wis, cha, cr, xp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (detail['name'], detail['size'], detail['type'], detail['alignment'], ac_val,
              detail['hit_points'], detail['strength'], detail['dexterity'], detail['constitution'],
              detail['intelligence'], detail['wisdom'], detail['charisma'], str(detail['challenge_rating']), detail['xp']))


def process_races(cursor, results):
    for item in results:
        detail = fetch_srd(f"races/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Race: {detail['name']}")

        bonuses = json.dumps(detail.get('ability_bonuses', []))
        traits = json.dumps(detail.get('traits', []))
        cursor.execute('''
            INSERT INTO races (name, speed, ability_bonuses, alignment, size, traits)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (detail['name'], detail['speed'], bonuses, detail['alignment'], detail['size'], traits))


def process_classes(cursor, results):
    for item in results:
        detail = fetch_srd(f"classes/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Class: {detail['name']}")

        profs = json.dumps(detail.get('proficiencies', []))
        cursor.execute('INSERT INTO classes (name, hit_die, profs) VALUES (?, ?, ?)',
                       (detail['name'], detail['hit_die'], profs))


def process_spells(cursor, results):
    for item in results:
        detail = fetch_srd(f"spells/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Spell: {detail['name']}")

        desc = " ".join(detail.get('desc', []))
        cursor.execute('''
            INSERT INTO spells (name, level, school, casting_time, range, components, duration, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (detail['name'], detail['level'], detail['school']['name'], detail['casting_time'],
              detail['range'], str(detail['components']), detail['duration'], desc))


def process_features(cursor, results):
    for item in results:
        detail = fetch_srd(f"features/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Feature: {detail['name']}")

        desc = " ".join(detail.get('desc', []))
        cursor.execute('INSERT INTO features (name, lvl, desc, srctype) VALUES (?, ?, ?, ?)',
                       (detail['name'], detail['level'], desc, 'Class'))


def process_items(cursor, results):
    for item in results:
        detail = fetch_srd(f"equipment/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Item: {detail['name']}")

        # Flattening cost (e.g., {"quantity": 2, "unit": "gp"})
        cost_str = f"{detail.get('cost', {}).get('quantity', 0)} {detail.get('cost', {}).get('unit', '')}"
        desc = " ".join(detail.get('desc', []))

        cursor.execute('''
            INSERT INTO items (name, category, cost, weight, description, rarity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (detail['name'], detail.get('equipment_category', {}).get('name'),
              cost_str, detail.get('weight'), desc, detail.get('rarity', {}).get('name')))


def process_feats(cursor, results):
    for item in results:
        detail = fetch_srd(f"feats/{item['index']}")
        if not detail:
            continue

        feat_name = detail.get(
            'name', item['index'].replace('-', ' ').capitalize())
        print(f"  - Mapping Feat: {feat_name}")

        # ROBUST PREREQUISITE PARSING
        req_list = []
        for p in detail.get('prerequisites', []):
            # Try name first
            p_text = p.get('name')

            # If no name (like Grappler), check for the ability score requirement
            if not p_text and 'ability_score' in p:
                score_info = p.get('ability_score', {})
                # Get the score abbreviation (STR, DEX, etc.)
                if isinstance(score_info, dict):
                    abbr = score_info.get('index', 'Stat').upper()
                else:
                    abbr = str(score_info).upper()

                # Get the minimum score requirement
                min_val = p.get('minimum_score', '')
                p_text = f"{abbr} {min_val}".strip()

            # Final fallback to index or generic "Requirement"
            p_text = p_text or p.get('index', 'Requirement')
            req_list.append(str(p_text).replace('-', ' ').title())

        req = ", ".join(req_list) if req_list else "None"
        desc = " ".join(detail.get('desc', []))

        cursor.execute('INSERT INTO feats (name, req, desc) VALUES (?, ?, ?)',
                       (feat_name, req, desc))


def process_backgrounds(cursor, results):
    for item in results:
        detail = fetch_srd(f"backgrounds/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Background: {detail['name']}")

        feat_name = detail.get('feature', {}).get('name', 'None')
        cursor.execute('INSERT INTO backgrounds (name, feature) VALUES (?, ?)',
                       (detail['name'], feat_name))


def process_subraces(cursor, results):
    for item in results:
        detail = fetch_srd(f"subraces/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Subrace: {detail['name']}")

        # Look up Parent Race ID
        parent_index = detail.get('race', {}).get('index')
        cursor.execute('SELECT id FROM races WHERE name LIKE ?',
                       (parent_index,))
        row = cursor.fetchone()
        race_id = row[0] if row else None

        bonuses = json.dumps(detail.get('ability_bonuses', []))
        traits = json.dumps([t['name']
                            for t in detail.get('racial_traits', [])])

        cursor.execute('INSERT INTO subraces (name, race_id, ability_bonuses, traits) VALUES (?, ?, ?, ?)',
                       (detail['name'], race_id, bonuses, traits))


def process_subclasses(cursor, results):
    for item in results:
        detail = fetch_srd(f"subclasses/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Subclass: {detail['name']}")

        # Look up Parent Class ID
        parent_index = detail.get('class', {}).get('index')
        cursor.execute(
            'SELECT id FROM classes WHERE name LIKE ?', (parent_index,))
        row = cursor.fetchone()
        class_id = row[0] if row else None

        cursor.execute('INSERT INTO subclasses (name, class_id, flavor) VALUES (?, ?, ?)',
                       (detail['name'], class_id, detail.get('subclass_flavor', '')))


def process_traits(cursor, results):
    for item in results:
        detail = fetch_srd(f"traits/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Trait: {detail['name']}")
        desc = " ".join(detail.get('desc', []))
        cursor.execute('INSERT INTO traits (name, description) VALUES (?, ?)',
                       (detail['name'], desc))


def process_languages(cursor, results):
    for item in results:
        detail = fetch_srd(f"languages/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Language: {detail['name']}")
        cursor.execute('INSERT INTO languages (name, type, script) VALUES (?, ?, ?)',
                       (detail['name'], detail.get('type'), detail.get('script')))


def process_proficiencies(cursor, results):
    for item in results:
        detail = fetch_srd(f"proficiencies/{item['index']}")
        if not detail:
            continue
        print(f"  - Mapping Proficiency: {detail['name']}")
        cursor.execute('INSERT INTO proficiencies (name, type) VALUES (?, ?)',
                       (detail['name'], detail.get('type')))

# --- MASTER EXECUTION ---


def import_all():
    conn = get_connection()
    cursor = conn.cursor()

    # Now that all functions are defined above, we can safely map them here
    endpoints = {
        "creatures": ("monsters", process_creatures),
        "races": ("races", process_races),
        "subraces": ("subraces", process_subraces),
        "classes": ("classes", process_classes),
        "subclasses": ("subclasses", process_subclasses),
        "spells": ("spells", process_spells),
        "features": ("features", process_features),
        "items": ("equipment", process_items),
        "feats": ("feats", process_feats),
        "backgrounds": ("backgrounds", process_backgrounds),
        "traits": ("traits", process_traits),
        "languages": ("languages", process_languages),
        "proficiencies": ("proficiencies", process_proficiencies)
    }

    for table, (path, func) in endpoints.items():
        print(f"\n--- Syncing {table} ---")
        data = fetch_srd(path)
        if data and 'results' in data:
            func(cursor, data['results'])
            conn.commit()

    conn.close()
    print("\n[SUCCESS] Arcanryn database is fully populated.")


if __name__ == "__main__":
    import_all()
