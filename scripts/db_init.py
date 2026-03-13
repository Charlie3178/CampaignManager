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
        CREATE TABLE characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race TEXT, subrace TEXT, class_role TEXT, subclass TEXT,
            level_cr INTEGER, is_pc BOOLEAN, affiliation TEXT, notes TEXT,
            strength INTEGER DEFAULT 10, dexterity INTEGER DEFAULT 10,
            constitution INTEGER DEFAULT 10, intelligence INTEGER DEFAULT 10,
            wisdom INTEGER DEFAULT 10, charisma INTEGER DEFAULT 10,
            ac INTEGER DEFAULT 10, hp INTEGER DEFAULT 10
        )''')

    # 2. Bestiary Table (with num_attacks and damage)
    cursor.execute('''
        CREATE TABLE bestiary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT, creature_type TEXT, alignment TEXT,
            ac INTEGER, hp INTEGER, num_attacks INTEGER DEFAULT 1,
            damage TEXT, cr REAL, xp INTEGER, notes TEXT
        )''')

    # 3. Items Table (with full currency wallet)
    cursor.execute('''
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, category TEXT, rarity TEXT,
            cp INTEGER DEFAULT 0, sp INTEGER DEFAULT 0, ep INTEGER DEFAULT 0,
            gp INTEGER DEFAULT 0, pp INTEGER DEFAULT 0,
            weight REAL DEFAULT 0.0, is_magical BOOLEAN DEFAULT 0,
            requires_attunement BOOLEAN DEFAULT 0, description TEXT
        )''')

    # 4. Locations Table
    cursor.execute('''
        CREATE TABLE locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, location_type TEXT, region TEXT,
            description TEXT, notes TEXT, parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES locations (id)
        )''')

    conn.commit()
    conn.close()
    print("Success: All tables created in /data folder.")


if __name__ == "__main__":
    initialize_db()
