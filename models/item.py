# models/item.py

class Item:
    def __init__(self, name, category, value_gp, weight, is_magical=False, rarity='Common', requires_attunement=False, description=None, db_id=None):
        self.db_id = db_id
        self.name = name
        self.category = category
        self.value_gp = value_gp
        self.weight = weight
        self.is_magical = is_magical
        self.rarity = rarity
        self.requires_attunement = requires_attunement
        self.description = description

    def __repr__(self):
        magic_tag = f" [{self.rarity}]" if self.is_magical else ""
        return f"<Item: {self.name}{magic_tag} ({self.category})>"