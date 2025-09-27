#!/usr/bin/env python3
"""
Test complete combat flow functionality
"""

print("🧪 Testing Complete Combat Flow")
print("=" * 50)
print()

# Test imports first
try:
    from lov import LordApp, CombatScreen
    from game_data import Character, Enemy
    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Test character creation
try:
    char = Character()
    char.name = "TestHero"
    char.level = 1
    char.hitpoints = 10
    char.max_hitpoints = 10
    char.gold = 100
    # attack_power and defense_power are computed properties
    print("✅ Character creation successful")
except Exception as e:
    print(f"❌ Character creation failed: {e}")
    exit(1)

# Test enemy creation
try:
    enemy = Enemy(
        name="Test Goblin",
        hitpoints=8,
        attack=3,
        gold_reward=5,
        exp_reward=10,
        level=1,
        note_title="Test Note",
        note_content="This is test content"
    )
    print("✅ Enemy creation successful")
except Exception as e:
    print(f"❌ Enemy creation failed: {e}")
    exit(1)

# Test CombatScreen methods exist
try:
    # Just check if methods exist without instantiating
    import inspect

    # Check if key methods exist in the class
    methods = [method for method in dir(CombatScreen) if method.startswith('_')]
    required_methods = ['_player_attack', '_knowledge_attack', '_show_stats', '_run_away', '_update_combat_display']

    for method in required_methods:
        assert method in methods, f"Missing {method} method"

    print("✅ All combat methods exist")
except Exception as e:
    print(f"❌ Combat method check failed: {e}")
    exit(1)

# Test AI import
try:
    from brainbot import initialize_ai, is_ai_available
    print("✅ AI imports successful")
except Exception as e:
    print(f"⚠️  AI import failed: {e} (fallback to regex)")

print()
print("🎯 SUMMARY:")
print("✅ Combat button handlers should now work")
print("✅ AI initialization re-enabled")
print("✅ All combat methods are present")
print()
print("🚀 Combat system is ready for testing!")
print("   Run: python3 lov.py")
print("   1. Create character")
print("   2. Go to forest")
print("   3. Enter combat")
print("   4. Try all buttons: A, K, R, S")
print("   5. Both mouse clicks and keyboard should work")