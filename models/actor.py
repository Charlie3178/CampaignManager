# models/actor.py

class Character:
    def __init__(self, name, race, subrace, class_role, subclass,
                 level_cr=1, is_pc=False, affiliation="", notes="", db_id=None,
                 strength=10, dexterity=10, constitution=10,
                 intelligence=10, wisdom=10, charisma=10, ac=10, hp=10):
        self.db_id = db_id
        self.name = name
        self.race = race
        self.subrace = subrace
        self.class_role = class_role
        self.subclass = subclass
        self.level_cr = level_cr
        self.is_pc = is_pc
        self.affiliation = affiliation
        self.notes = notes
        # Stats
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.ac = ac
        self.hp = hp

    def __repr__(self):
        type_label = "PC" if self.is_pc else "NPC"
        return f"<{type_label}: {self.name} ({self.race} {self.class_role})>"
