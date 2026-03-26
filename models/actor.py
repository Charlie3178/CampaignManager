# models/actor.py

class Character:
    def __init__(self, name, pc=0, race=None, subr=None, cclass=None,
                 subc=None, bkgnd=None, lvl=1, xp=0, al="N", aff="", notes="", **stats):
        self.name = name
        self.pc = pc
        self.race = race
        self.subr = subr
        self.cclass = cclass  # 'class' is reserved in Python
        self.subc = subc
        self.bkgnd = bkgnd
        self.lvl = lvl
        self.xp = xp
        self.al = al
        self.aff = aff
        self.notes = notes

        # Mapping stats: str, dex, con, int, wis, cha, ac, mhp, chp
        self.str = stats.get('str', 10)
        self.dex = stats.get('dex', 10)
        self.con = stats.get('con', 10)
        self.int = stats.get('int', 10)
        self.wis = stats.get('wis', 10)
        self.cha = stats.get('cha', 10)
        self.ac = stats.get('ac', 10)
        self.mhp = stats.get('mhp', 10)
        self.chp = stats.get('chp', 10)

    def __repr__(self):
        type_label = "PC" if self.pc else "NPC"
        return f"<{type_label}: {self.name} ({self.race} {self.cclass})>"
