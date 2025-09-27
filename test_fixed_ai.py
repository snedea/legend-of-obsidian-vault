#!/usr/bin/env python3
"""
Test the fixed TinyLlama AI integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_enemy_generation():
    """Test the enhanced AI enemy generation"""

    print("🤖 Testing Enhanced TinyLlama AI Integration")
    print("=" * 60)

    from obsidian import vault

    print("\n🎯 Testing AI enemy generation with debug output:")
    print("-" * 50)

    # Generate a few enemies to see the AI output
    for i in range(3):
        print(f"\n🐉 Test #{i+1}:")
        print("-" * 30)

        enemy = vault.get_enemy_for_level(5)

        print(f"Final result:")
        print(f"   Name: {enemy.name}")
        print(f"   Environment: {enemy.environment_description}")
        if hasattr(enemy, 'encounter_narrative') and enemy.encounter_narrative:
            narrative = enemy.encounter_narrative
            if len(narrative) > 100:
                print(f"   Narrative: {narrative[:100]}...")
            else:
                print(f"   Narrative: {narrative}")
        else:
            print(f"   ❌ No encounter narrative!")

    print(f"\n✅ AI integration test completed!")
    print(f"Look for debug output above to see if TinyLlama is generating content properly.")

if __name__ == "__main__":
    test_ai_enemy_generation()