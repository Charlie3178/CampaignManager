from models import Character, Item, Creature
from utils.db_handler import save_character, save_item, save_creature

def run_integration_test():
    print("--- Starting Database Integration Test ---")

    try:
        # 1. Test NPC Creation
        innkeeper = Character(
            name="Durnan", 
            race="Human", 
            class_role="Innkeeper", 
            notes="Owner of the Yawning Portal."
        )
        npc_id = save_character(innkeeper)
        print(f"[SUCCESS] Saved NPC: {innkeeper.name} (ID: {npc_id})")

        # 2. Test PC Creation
        hero = Character(
            name="Valeros", 
            race="Fighter", 
            class_role="Frontliner", 
            is_pc=True
        )
        pc_id = save_character(hero)
        print(f"[SUCCESS] Saved PC: {hero.name} (ID: {pc_id})")

        # 3. Test Magic Item Creation
        sword = Item(
            name="Sun Blade", 
            category="Weapon", 
            is_magical=True, 
            rarity="Rare", 
            value_gp=5000, 
            weight=3,
            description="A blade of pure primary radiance."
        )
        item_id = save_item(sword)
        print(f"[SUCCESS] Saved Item: {sword.name} (ID: {item_id})")

        # 4. Test Monster Creation
        goblin = Creature(
            name="Goblin", 
            size="Small", 
            creature_type="Humanoid", 
            alignment="Neutral Evil", 
            ac=15, 
            hp=7, 
            cr=0.25, 
            xp=50
        )
        monster_id = save_creature(goblin)
        print(f"[SUCCESS] Saved Monster: {goblin.name} (ID: {monster_id})")

        print("\n--- Test Complete: All entities written to campaign_base.db ---")

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")

if __name__ == "__main__":
    run_integration_test()