#!/usr/bin/env python3
"""
Demo script to showcase Legend of the Obsidian Vault
Creates a test character and shows key game features
"""
import time
import os
from pathlib import Path
from game_data import Character, GameDatabase, WEAPONS, ARMOR
from obsidian import ObsidianVault

def create_demo_character():
    """Create a demo character with some progression"""
    demo_char = Character(
        name="Chester",
        gender="M",
        class_type="K",
        level=3,
        experience=1200,
        hitpoints=60,
        max_hitpoints=60,
        forest_fights=15,
        player_fights=3,
        gold=5000,
        bank_gold=25000,
        weapon_num=2,  # Short Sword
        weapon="Short Sword",
        armor_num=2,   # Leather Vest
        armor="Leather Vest",
        charm=5,
        gems=2,
        days_played=3
    )
    return demo_char

def create_demo_vault():
    """Create some demo notes for testing"""
    demo_path = Path("demo_vault")
    demo_path.mkdir(exist_ok=True)
    (demo_path / ".obsidian").mkdir(exist_ok=True)

    # Create sample notes
    notes = [
        ("Python Basics.md", "# Python Basics\n\nPython is a high-level programming language.\n\n## Key Features\n- Easy syntax\n- Object-oriented\n- Interpreted language"),
        ("Machine Learning.md", "# Machine Learning\n\nML is about making computers learn patterns.\n\n## Algorithms\n- Neural Networks\n- Decision Trees\n- Linear Regression"),
        ("Database Design.md", "# Database Design\n\nProper database design is crucial for performance.\n\n## Normal Forms\n- First Normal Form\n- Second Normal Form\n- Third Normal Form"),
        ("Old Project Ideas.md", "# Old Project Ideas\n\nThese are projects I thought about but never started.\n\n- Web scraper\n- Game engine\n- Chat application"),
    ]

    for filename, content in notes:
        (demo_path / filename).write_text(content)

    return demo_path

def demo_obsidian_integration():
    """Demonstrate Obsidian vault integration"""
    print("🗂️  OBSIDIAN VAULT INTEGRATION DEMO")
    print("=" * 50)

    # Create demo vault
    vault_path = create_demo_vault()
    print(f"Created demo vault at: {vault_path}")

    # Initialize vault
    vault = ObsidianVault(str(vault_path))
    notes = vault.scan_notes(force_rescan=True)

    print(f"\nFound {len(notes)} notes in vault:")
    for note in notes:
        print(f"  📄 {note.title} (Difficulty Level: {note.difficulty_level})")

    # Generate some enemies
    print("\n🐉 GENERATED FOREST ENEMIES:")
    for level in [1, 3, 5]:
        enemy = vault.get_enemy_for_level(level, notes)
        print(f"  Level {level}: {enemy.name}")
        print(f"    HP: {enemy.hitpoints}, Attack: {enemy.attack}, Gold: {enemy.gold_reward}")
        if enemy.note_content:
            question, answer = vault.generate_quiz_question(
                type('Note', (), {'title': enemy.note_title, 'content': enemy.note_content})()
            )
            print(f"    Quiz: {question}")
            print(f"    Answer: {answer}")
        print()

def demo_character_progression():
    """Show character stats and progression"""
    print("⚔️  CHARACTER PROGRESSION DEMO")
    print("=" * 50)

    char = create_demo_character()

    print(f"Character: {char.name}")
    print(f"Class: Death Knight")
    print(f"Level: {char.level}")
    print(f"Experience: {char.experience:,}")
    print(f"Hit Points: {char.hitpoints}/{char.max_hitpoints}")
    print(f"Gold in hand: {char.gold:,}")
    print(f"Gold in bank: {char.bank_gold:,}")
    print(f"Weapon: {char.weapon} (Power: {WEAPONS[char.weapon_num][2]})")
    print(f"Armor: {char.armor} (Defense: {ARMOR[char.armor_num][2]})")
    print(f"Charm: {char.charm}")
    print(f"Daily forest fights: {char.forest_fights}")
    print(f"Daily player fights: {char.player_fights}")

def demo_combat_mechanics():
    """Demonstrate combat calculations"""
    print("\n⚔️  COMBAT MECHANICS DEMO")
    print("=" * 50)

    char = create_demo_character()

    print(f"Attack Power: {char.attack_power}")
    print(f"  = Weapon Power ({WEAPONS[char.weapon_num][2]}) + Level Bonus ({char.level * 2})")

    print(f"\nDefense Power: {char.defense_power}")
    print(f"  = Armor Power ({ARMOR[char.armor_num][2]}) + Level Bonus ({char.level})")

    # Show level up requirements
    from game_data import LEVEL_EXP
    if char.level < 12:
        exp_needed = LEVEL_EXP[char.level] - char.experience
        print(f"\nExperience to next level: {exp_needed:,}")
    else:
        print(f"\nMAX LEVEL REACHED! Ready to fight the Red Dragon!")

def demo_shop_prices():
    """Show weapon and armor shop prices"""
    print("\n🛍️  WEAPON SHOP DEMO")
    print("=" * 50)

    char = create_demo_character()

    print("Available Weapons:")
    for i, (name, price, power) in enumerate(WEAPONS[:8]):  # Show first 8
        if i <= char.weapon_num + 1:  # Can only buy next weapon
            if i == char.weapon_num:
                print(f"  {name} - OWNED (Power: {power})")
            else:
                can_afford = char.gold >= price
                status = "✅ Can afford" if can_afford else "❌ Too expensive"
                print(f"  {name} - {price:,} gold (Power: {power}) - {status}")

def main():
    """Run the complete demo"""
    print("🏰 LEGEND OF THE OBSIDIAN VAULT - DEMO")
    print("🏰 " + "=" * 48)
    print()

    demo_character_progression()
    demo_combat_mechanics()
    demo_shop_prices()
    demo_obsidian_integration()

    print("\n🎮 READY TO PLAY?")
    print("=" * 50)
    print("Run: python3 lov.py")
    print()
    print("Game Features:")
    print("  ✅ Authentic LORD BBS experience")
    print("  ✅ Full terminal interface with colors")
    print("  ✅ Mouse + keyboard controls")
    print("  ✅ Complete combat system")
    print("  ✅ All 18 town square options")
    print("  ✅ Obsidian vault integration")
    print("  ✅ Quiz-based critical hits")
    print("  ✅ Daily limits and banking")
    print("  ✅ Character progression to level 12")
    print("  ✅ Red Dragon final boss")
    print()
    print("Your forgotten notes await in the forest! 🌲🗡️📚")

if __name__ == "__main__":
    main()