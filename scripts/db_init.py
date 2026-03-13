import sqlite3
import os


def initialize_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'campaign_base.db')

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Initializing database at: {db_path}")

    # 1. Characters Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race TEXT,
            subrace TEXT,
            class_role TEXT,
            subclass TEXT,
            level_cr INTEGER,
            is_pc BOOLEAN,
            affiliation TEXT,
            notes TEXT,
            strength INTEGER DEFAULT 10,
            dexterity INTEGER DEFAULT 10,
            constitution INTEGER DEFAULT 10,
            intelligence INTEGER DEFAULT 10,
            wisdom INTEGER DEFAULT 10,
            charisma INTEGER DEFAULT 10,
            ac INTEGER DEFAULT 10,
            hp INTEGER DEFAULT 10
        );
    ''')

    # 2. Bestiary Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bestiary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT,
            creature_type TEXT,
            alignment TEXT,
            ac INTEGER,
            hp INTEGER,
            cr REAL,
            xp INTEGER,
            notes TEXT
        )
    ''')

    # 3. Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            is_magical BOOLEAN DEFAULT 0,
            rarity TEXT DEFAULT 'Common',
            value_gp REAL,
            weight REAL,
            description TEXT,
            requires_attunement BOOLEAN DEFAULT 0
        )
    ''')

    # 4. Locations Table (Added with Parent support)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location_type TEXT,
            region TEXT,
            description TEXT,
            notes TEXT,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES locations (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Success: All tables (Characters, Bestiary, Items, Locations) created.")


if __name__ == "__main__":
    initialize_db()
