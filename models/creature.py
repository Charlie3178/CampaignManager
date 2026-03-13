# models/creature.py

class Creature:
    def __init__(self, name, size, creature_type, alignment, ac, hp, cr, xp, db_id=None):
        self.db_id = db_id
        self.name = name
        self.size = size
        self.creature_type = creature_type
        self.alignment = alignment
        self.ac = ac
        self.hp = hp
        self.cr = cr
        self.xp = xp

    def __repr__(self):
        return f"<Creature: {self.name} (CR {self.cr} {self.creature_type})>"