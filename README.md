#This is a work in progress and Below is what I am aiming to accomplish.

# Arcanryn Campaign Manager (v1.2.5)

A comprehensive Python-based tabletop RPG management suite designed for 5e mechanics. This tool manages everything from bestiaries and item shops to complex, "old-school" character creation.

## 🛠 Features (Current & In-Progress)

- **Golden Database Schema:** A robust 12-table SQLite backend with relational integrity for races, classes, sub-mechanics, and lore.
- **Bulk Data Engine:** Automated CSV import/export for rapid world-building and SRD synchronization.
- **Old-School Character Creator:** A 7-step creation engine that prioritizes ability score rolling before class selection.
- **Scalable Design:** Built to transition from a CLI utility to a full-blown text-based "Encounter Module."

## 📊 Database Schema (The Golden 12)

1. **Characters** - Player and NPC base data.
2. **Creatures** - Bestiary with CR and creature types.
3. **Items** - Equipment, rarity, and category tracking.
4. **Locations** - World-building and regional data.
5. **Classes** - Hit dice, primary stats, and proficiency data.
6. **Races** - Ability bonuses and base traits.
7. **Spells** - Comprehensive spellbook with level and school filtering.
8. **Subclasses** - Archetypes linked to parent classes.
9. **Subraces** - Racial variants linked to parent races.
10. **Lore & History** - World myths and historical records.
11. **DM Notes** - Secret campaign tracking and generic entity links.
12. **Class Features** - Level-based ability unlocks.

## 🎲 Character Creation Workflow (v1.2.5)

The creator follows a "Stats-First" philosophy:

1. **Race/Subrace Selection** (Initial identity)
2. **Ability Score Generation** (4d6 drop-lowest, user-assignable pool)
3. **Racial Adjustments** (Bonuses applied to the assignable pool)
4. **Class/Subclass Selection** (Based on the final score results)
5. **Vitals Calculation** (HP, Passive Perception, Initiative, Starting Gold)
6. **Equipment Loadout** (AC calculation and inventory management)
7. **Feature Integration** (Applying class-specific abilities)

## 🚀 Getting Started

1. Run `scripts/git-init.bat` to initialize the environment.
2. Use `main.py` (or your entry point) to access the Management Menu.
3. Use the **Database Management** menu to initialize the tables or import CSV data.
