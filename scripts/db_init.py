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

    # 6. Spells Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            level INTEGER,          -- 0 for Cantrips, 1-9 for leveled spells
            school TEXT,           -- Evocation, Necromancy, etc.
            casting_time TEXT,
            range TEXT,
            components TEXT,       -- V, S, M
            duration TEXT,
            concentration BOOLEAN,
            ritual BOOLEAN,
            description TEXT,
            higher_level TEXT      -- Scaling details for upcasting
        )
    ''')

    # 7. Races Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS races (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            speed INTEGER,
            ability_bonuses TEXT, -- e.g., 'STR+2, CON+1'
            alignment TEXT,
            size TEXT,
            traits TEXT          -- Darkvision, Stonecunning, etc.
        )
    ''')

    # 8. Subraces Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subraces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_id INTEGER,      -- Links to races.id
            name TEXT NOT NULL,
            ability_bonuses TEXT,
            traits TEXT,
            FOREIGN KEY (race_id) REFERENCES races (id)
        )
    ''')

    # 9. Subclasses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subclasses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,     -- Links to classes.id
            name TEXT NOT NULL,
            flavor_text TEXT,
            features TEXT,        -- Key abilities gained
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')


# 10. Lore & History (World building)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lore_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT, -- e.g., 'Myth', 'History', 'Rumor'
            content TEXT,
            location_id INTEGER,
            FOREIGN KEY (location_id) REFERENCES locations (id)
        )
    ''')

# 11. DM Notes (Campaign management)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dm_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            is_secret INTEGER DEFAULT 1, -- 1 for True, 0 for False
            related_entity_type TEXT, -- e.g., 'npc', 'location', 'item'
            related_entity_id INTEGER
        )
''')

# 12. Class Features (The engine for Step 7 of your Creator)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS class_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            feature_name TEXT NOT NULL,
            level_required INTEGER,
            description TEXT,
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
''')

    conn.commit()
    conn.close()
    print("Success: All tables created in /data folder.")


if __name__ == "__main__":
    initialize_db()
