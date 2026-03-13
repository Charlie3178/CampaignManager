import sqlite3
import os

def initialize_db():
    # Ensure the script targets the 'data' folder regardless of where it's run
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'campaign_base.db')
    
    # Create the data directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Initializing database at: {db_path}")

    # 1. Characters Table (PCs and NPCs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race TEXT,
            class_role TEXT,
            level_cr INTEGER DEFAULT 1,
            is_pc BOOLEAN DEFAULT 0,
            affiliation TEXT,
            notes TEXT
        )
    ''')

    # 2. Bestiary Table (Monsters and Creatures)
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
            xp INTEGER
        )
    ''')

    # 3. Items Table (RItems and MItems)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT, -- e.g., Weapon, Armor, Wondrous
            is_magical BOOLEAN DEFAULT 0,
            rarity TEXT DEFAULT 'Common',
            value_gp REAL,
            weight REAL,
            description TEXT,
            requires_attunement BOOLEAN DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
    print("Success: All tables created.")

if __name__ == "__main__":
    initialize_db()