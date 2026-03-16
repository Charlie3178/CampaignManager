import random


def roll_ability_scores():
    """Rolls 4d6 and drops the lowest value six times."""
    scores = []
    for _ in range(6):
        rolls = [random.randint(1, 6) for _ in range(4)]
        rolls.sort()
        scores.append(sum(rolls[1:]))  # Sum the top 3
    return sorted(scores, reverse=True)


def assign_scores(rolled_scores):
    """Interactive loop to assign rolled scores to attributes."""
    stats = ['Strength', 'Dexterity', 'Constitution',
             'Intelligence', 'Wisdom', 'Charisma']
    final_stats = {}

    print(f"\nYour rolled scores are: {rolled_scores}")

    for stat in stats:
        while True:
            print(f"\nRemaining scores: {rolled_scores}")
            try:
                choice = int(input(f"Assign which score to {stat}? "))
                if choice in rolled_scores:
                    final_stats[stat] = choice
                    rolled_scores.remove(choice)
                    break
                else:
                    print("[!] That score isn't in your pool.")
            except ValueError:
                print("[!] Please enter a valid number.")

    return final_stats


def calculate_modifier(score):
    """Standard 5e modifier calculation: (Score - 10) // 2"""
    return (score - 10) // 2
