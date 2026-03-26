import random
import sqlite3
import os


def roll_stats():
    """Step 2: Generates 6 stats using the 10 + 1d8 method."""
    return sorted([10 + random.randint(1, 8) for _ in range(6)], reverse=True)


def parse_bonuses(bonus_string):
    """Utility: Converts 'STR +2, CHA +1' to a dictionary."""
    if not bonus_string:
        return {}
    mapping = {"STR": "Strength", "DEX": "Dexterity", "CON": "Constitution",
               "INT": "Intelligence", "WIS": "Wisdom", "CHA": "Charisma"}
    bonuses = {}
    parts = bonus_string.split(',')
    for part in parts:
        part = part.strip()
        if ' ' in part:
            abbr, val = part.split(' ')
            full_name = mapping.get(abbr.upper())
            if full_name:
                bonuses[full_name] = int(val.replace('+', ''))
    return bonuses


def assign_stats(pool):
    """Step 3: Interactive loop to assign the rolled pool to attributes."""
    stats = {
        "Strength": 0, "Dexterity": 0, "Constitution": 0,
        "Intelligence": 0, "Wisdom": 0, "Charisma": 0
    }
    available_scores = pool.copy()

    for stat_name in stats.keys():
        while True:
            print(f"\nRemaining Pool: {available_scores}")
            try:
                val = int(input(f"Assign a value to {stat_name}: "))
                if val in available_scores:
                    stats[stat_name] = val
                    available_scores.remove(val)
                    break
                else:
                    print(f"[!] {val} is not in your pool.")
            except ValueError:
                print("[!] Please enter a valid number.")
    return stats


def apply_racial_bonuses(base_stats, race_name):
    """Step 4: Pulls bonuses from data/campaign.db and adds them."""
    db_path = os.path.join('data', 'campaign.db')
    if not os.path.exists(db_path):
        return base_stats  # Return stats as-is if DB isn't there yet

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ability_bonuses FROM races WHERE name = ?", (race_name,))
    row = cursor.fetchone()
    conn.close()

    if row and row['ability_bonuses']:
        bonuses = parse_bonuses(row['ability_bonuses'])
        for stat, val in bonuses.items():
            if stat in base_stats:
                base_stats[stat] += val
    return base_stats


if __name__ == "__main__":
    # This block allows you to run the script standalone for testing
    print("--- Arcanryn Character Stat Roller ---")
    my_pool = roll_stats()
    print(f"Your 10+1d8 Pool: {my_pool}")

    assigned = assign_stats(my_pool)

    # Example: If you manually want to test a race bonus
    # final = apply_racial_bonuses(assigned, "Dragonborn")

    print("\nFinal Base Stats:")
    for s, v in assigned.items():
        print(f"{s}: {v}")
