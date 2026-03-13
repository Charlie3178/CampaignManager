import sqlite3
import os
from models import Character, Creature, Item


def get_connection():
    """Helper to consistently connect to the database in the /data folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'campaign_base.db')
    return sqlite3.connect(db_path)


def save_character(character):
    """Saves a Character object to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    if character.db_id is None:
        # Create a new record
        query = '''
            INSERT INTO characters (name, race, class_role, level_cr, is_pc, affiliation, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (character.name, character.race, character.class_role,
                  character.level_cr, character.is_pc, character.affiliation, character.notes)
        cursor.execute(query, params)
        character.db_id = cursor.lastrowid  # Update the object with its new ID
    else:
        # Update existing record
        query = '''
            UPDATE characters 
            SET name=?, race=?, class_role=?, level_cr=?, is_pc=?, affiliation=?, notes=?
            WHERE id=?
        '''
        params = (character.name, character.race, character.class_role,
                  character.level_cr, character.is_pc, character.affiliation,
                  character.notes, character.db_id)
        cursor.execute(query, params)

    conn.commit()
    conn.close()
    return character.db_id


def save_creature(creature):
    conn = get_connection()
    cursor = conn.cursor()

    if creature.db_id is None:
        query = '''
            INSERT INTO bestiary (name, size, creature_type, alignment, ac, hp, cr, xp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (creature.name, creature.size, creature.creature_type,
                  creature.alignment, creature.ac, creature.hp, creature.cr, creature.xp)
        cursor.execute(query, params)
        creature.db_id = cursor.lastrowid
    else:
        query = '''
            UPDATE bestiary 
            SET name=?, size=?, creature_type=?, alignment=?, ac=?, hp=?, cr=?, xp=?
            WHERE id=?
        '''
        params = (creature.name, creature.size, creature.creature_type,
                  creature.alignment, creature.ac, creature.hp, creature.cr,
                  creature.xp, creature.db_id)
        cursor.execute(query, params)

    conn.commit()
    conn.close()
    return creature.db_id


def save_item(item):
    conn = get_connection()
    cursor = conn.cursor()

    if item.db_id is None:
        query = '''
            INSERT INTO items (name, category, is_magical, rarity, value_gp, weight, description, requires_attunement)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (item.name, item.category, item.is_magical, item.rarity,
                  item.value_gp, item.weight, item.description, item.requires_attunement)
        cursor.execute(query, params)
        item.db_id = cursor.lastrowid
    else:
        query = '''
            UPDATE items 
            SET name=?, category=?, is_magical=?, rarity=?, value_gp=?, weight=?, description=?, requires_attunement=?
            WHERE id=?
        '''
        params = (item.name, item.category, item.is_magical, item.rarity,
                  item.value_gp, item.weight, item.description,
                  item.requires_attunement, item.db_id)
        cursor.execute(query, params)

    conn.commit()
    conn.close()
    return item.db_id


if __name__ == "__main__":
    # Test creating a new NPC
    test_npc = Character(name="Durnan", race="Human",
                         class_role="Innkeeper", is_pc=False)
    new_id = save_character(test_npc)
    print(f"Saved NPC with ID: {new_id}")

    # Test creating a Magic Item
    test_item = Item(name="Sun Blade", category="Weapon",
                     is_magical=True, rarity="Longsword", value_gp=50000, weight=3)
    item_id = save_item(test_item)
    print(f"Saved Item with ID: {item_id}")


def get_all_characters():
    """Retrieves all characters and returns them as a list of Character objects."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM characters')
    rows = cursor.fetchall()

    characters = []
    for row in rows:
        char = Character(
            name=row['name'],
            race=row['race'],
            class_role=row['class_role'],
            level_cr=row['level_cr'],
            is_pc=bool(row['is_pc']),
            affiliation=row['affiliation'],
            notes=row['notes'],
            db_id=row['id']
        )
        characters.append(char)  # This is inside the loop

    conn.close()  # This is outside the loop
    return characters  # This is outside the loop, lined up with 'conn = ...'


def find_character_by_name(name_query):
    """Finds characters whose names contain the search string."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # We use LIKE with % wildcards so 'Grog' finds 'Grogory' or 'Grog the Tall'
    query = 'SELECT * FROM characters WHERE name LIKE ?'
    cursor.execute(query, (f'%{name_query}%',))

    rows = cursor.fetchall()
    characters = []

    for row in rows:
        characters.append(Character(
            name=row['name'],
            race=row['race'],
            class_role=row['class_role'],
            level_cr=row['level_cr'],
            is_pc=bool(row['is_pc']),
            affiliation=row['affiliation'],
            notes=row['notes'],
            db_id=row['id']
        ))

    conn.close()
    return characters
