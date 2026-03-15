import sqlite3
import os


def get_db_path():
    # Since this is in /scripts, go UP to root, then DOWN to /data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    return os.path.normpath(os.path.join(project_root, 'data', 'campaign_base.db'))


def initialize_db():
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"Initializing database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop existing tables to apply new schema changes
    tables = ['characters', 'bestiary', 'items', 'locations']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # 1. Characters Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        race TEXT,
        class_or_role TEXT,      -- e.g., 'Level 5 Paladin' or 'Shopkeeper'
        level INTEGER DEFAULT 1,
        alignment TEXT,
        hp_max INTEGER,
        hp_current INTEGER,
        ac INTEGER,
        location_id INTEGER,     -- Link this to your locations table later
        disposition TEXT,        -- Friendly, Hostile, Neutral, Suspicious
        backstory TEXT,
        inventory TEXT,          -- Useful for tracking quest items
        notes TEXT,
        is_pc BOOLEAN DEFAULT 0, -- 1 for Player Character, 0 for NPC
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
''')

    # 2. Bestiary Table (with num_attacks and damage)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS creatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        size TEXT,
        creature_type TEXT,
        alignment TEXT,
        ac INTEGER,
        hp INTEGER,
        hit_dice TEXT,
        speed TEXT,
        str INTEGER, dex INTEGER, con INTEGER, 
        int INTEGER, wis INTEGER, cha INTEGER,
        cr TEXT,
        xp INTEGER,
        senses TEXT,
        languages TEXT,
        resistances TEXT,        -- Combined Damage/Condition immunities/resistances
        abilities TEXT,          -- Special traits (Amphibious, etc.)
        actions TEXT,            -- Standard actions
        legendary_actions TEXT,  -- For boss monsters
        description TEXT,
        notes TEXT
    )
''')

    # 3. Items Table (with full currency wallet)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        cost TEXT,
        weight REAL,
        description TEXT,
        requires_attunement BOOLEAN DEFAULT 0, -- 1 for Yes, 0 for No
        rarity TEXT,                           -- Common, Uncommon, Rare, etc.
        properties TEXT
    )
''')

    # 4. Locations Table
    cursor.execute('''
        CREATE TABLE locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, location_type TEXT, region TEXT,
            description TEXT, notes TEXT, parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES locations (id)
        )''')


# 5 Classes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            hit_die TEXT,          -- e.g., 'd10'
            primary_ability TEXT,  -- e.g., 'Strength'
            description TEXT,
            features TEXT          -- A big text block of class abilities
        )
    ''')

    conn.commit()
    conn.close()
    print("Success: All tables created in /data folder.")


if __name__ == "__main__":
    initialize_db()
