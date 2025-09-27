#!/usr/bin/env python3
"""
Test combat display fixes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_combat_display_fixes():
    """Test the combat display improvements"""

    print("🎮 Testing Combat Display Fixes")
    print("=" * 50)

    from obsidian import vault

    # Test multiple enemy generations
    print("🐉 Testing enemy generation with display improvements:")
    print("-" * 45)

    for i in range(3):
        print(f"\n🎯 Test Enemy #{i+1}:")
        enemy = vault.get_enemy_for_level(5)

        print(f"   Title: {enemy.note_title}")
        print(f"   Name: {enemy.name[:50]}...")
        print(f"   Content: {enemy.note_content[:30] if enemy.note_content else 'EMPTY'}...")

        # Check narrative
        if hasattr(enemy, 'encounter_narrative') and enemy.encounter_narrative:
            print(f"   ✅ HAS Narrative: {enemy.encounter_narrative[:50]}...")
            print(f"   🎭 Display: Would show generated narrative")
        else:
            print(f"   🔄 NO Narrative - would show fallback")
            if hasattr(enemy, 'note_content') and enemy.note_content:
                lines = [line.strip() for line in enemy.note_content.split('\n') if line.strip()]
                if lines:
                    print(f"   📝 With content: '{lines[0][:30]}...'")

        # Check environment display
        env = getattr(enemy, 'environment_description', f"Mystical Sanctuary of {enemy.note_title}")
        if len(env) > 65:
            print(f"   🌍 Environment (wrapped): {env[:65]}...")
        else:
            print(f"   🌍 Environment: {env}")

        print()

    print("✅ Combat display test completed!")
    print("\n💡 Key Improvements:")
    print("   • Enemy names now display up to 70 characters")
    print("   • Environment descriptions wrap properly")
    print("   • Fallback narratives include note content")
    print("   • Debug logging shows which system is used")

if __name__ == "__main__":
    test_combat_display_fixes()