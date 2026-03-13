# models/actor.py

class Character:
    def __init__(self, name, race, class_role, level_cr=1, is_pc=False, affiliation=None, notes=None, db_id=None):
        self.db_id = db_id
        self.name = name
        self.race = race
        self.class_role = class_role
        self.level_cr = level_cr
        self.is_pc = is_pc
        self.affiliation = affiliation
        self.notes = notes

    def __repr__(self):
        type_label = "PC" if self.is_pc else "NPC"
        return f"<{type_label}: {self.name} ({self.race} {self.class_role})>"