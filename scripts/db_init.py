import sqlite3
import os


def get_db_path():
    # Since this is in /scripts, go UP to root, then DOWN to /data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    return os.path.normpath(os.path.join(project_root, 'data', 'campaign.db'))


def initialize_db():
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"Initializing database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # The "Lean" Table List
    tables = [
        'characters', 'creatures', 'items', 'locations',
        'classes', 'spells', 'races', 'subraces',
        'subclasses', 'lore', 'notes', 'features',
        'backgrounds', 'feats', 'traits', 'proficiencies', 'languages'
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # 1. Characters Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        pc INTEGER DEFAULT 0,
        race INTEGER,
        subr INTEGER,
        cclass INTEGER,  
        subc INTEGER,
        bkgnd INTEGER,
        lvl INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        al TEXT DEFAULT 'N',
        str INTEGER DEFAULT 10,
        dex INTEGER DEFAULT 10,
        con INTEGER DEFAULT 10,
        int INTEGER DEFAULT 10,
        wis INTEGER DEFAULT 10,
        cha INTEGER DEFAULT 10,
        ac INTEGER DEFAULT 10,
        mhp INTEGER DEFAULT 10,
        chp INTEGER DEFAULT 10,
        aff TEXT,
        notes TEXT,
        FOREIGN KEY (race) REFERENCES races (id),
        FOREIGN KEY (subr) REFERENCES subraces (id),
        FOREIGN KEY (cclass) REFERENCES classes (id),
        FOREIGN KEY (subc) REFERENCES subclasses (id),
        FOREIGN KEY (bkgnd) REFERENCES backgrounds (id)
    )''')

    # 2. Bestiary Table (with num_attacks and damage)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS creatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
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
        name TEXT NOT NULL UNIQUE,
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
            name TEXT NOT NULL UNIQUE, location_type TEXT, region TEXT,
            description TEXT, notes TEXT, parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES locations (id)
        )''')


# TABLE 5: CLASSES
    cursor.execute('''
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,  -- Simplified from class_name
    hit_die TEXT,
    profs TEXT           -- Shortened from proficiencies
)''')

    # 6. Spells Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
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
            name TEXT NOT NULL UNIQUE,
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
            name TEXT NOT NULL UNIQUE,
            ability_bonuses TEXT,
            traits TEXT,
            FOREIGN KEY (race_id) REFERENCES races (id)
        )
    ''')

    # 9. Subclasses Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subclasses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,    -- Links to classes.id
        name TEXT NOT NULL UNIQUE,
        flavor TEXT,         -- Simplified from flavor_text
        FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')


# 10. Lore
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lore (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            cat TEXT,
            content TEXT,
            loc_id INTEGER,
            FOREIGN KEY (loc_id) REFERENCES locations (id)
        )
    ''')

    # 11. Notes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            content TEXT,
            secret INTEGER DEFAULT 1,
            ent_type TEXT,
            ent_id INTEGER
        )
    ''')

    # 12. Features
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lvl INTEGER,
            desc TEXT,
            srctype TEXT,
            class_id INTEGER,
            subc_id INTEGER,
            FOREIGN KEY (class_id) REFERENCES classes (id),
            FOREIGN KEY (subc_id) REFERENCES subclasses (id)
        )
    ''')

    # 13. Backgrounds
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backgrounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            feature TEXT,
            profs TEXT
        )
    ''')

    # 14. Feats
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            req TEXT,
            desc TEXT,
            repeat INTEGER DEFAULT 0
        )
    ''')

# 15. Traits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS traits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # 16. Proficiencies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proficiencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT
        )
    ''')

    # 17. Languages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT,
            script TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully with Lean Schema.")


if __name__ == "__main__":
    initialize_db()
