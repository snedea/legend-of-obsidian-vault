#!/usr/bin/env python3
"""
Test AI narrative generation specifically
"""
import time
import sys
from obsidian import vault
from brainbot import initialize_ai, is_ai_available, sync_generate_enemy_description

def test_ai_narrative():
    """Test if AI generates rich narratives"""
    print("🧪 Testing AI Narrative Generation")
    print("=" * 50)

    # Initialize AI
    print("🔄 Initializing AI...")
    initialize_ai()

    # Wait for initialization
    max_wait = 10
    for i in range(max_wait):
        if is_ai_available():
            print(f"✅ AI available after {i+1} seconds")
            break
        print(f"⏳ Waiting for AI ({i+1}/{max_wait})...")
        time.sleep(1)
    else:
        print("❌ AI not available after 10 seconds")
        return

    # Test with a sample note
    test_note_title = "Machine Learning Basics"
    test_note_content = """
    Machine learning is a method of data analysis that automates analytical model building.

    Key concepts:
    - 27 different algorithms exist for classification
    - Neural networks have 5 main layers
    - Training datasets typically need 1000+ examples
    - Accuracy scores range from 0.0 to 1.0

    Popular frameworks:
    - TensorFlow
    - PyTorch
    - Scikit-learn

    Next steps: Practice with iris dataset, implement decision trees
    """

    print(f"\n📝 Testing with note: '{test_note_title}'")
    print(f"📄 Content length: {len(test_note_content)} chars")

    # Generate enemy description
    print("\n🤖 Generating AI description...")
    enemy_desc = sync_generate_enemy_description(test_note_title, test_note_content, "Mosquito")

    if enemy_desc:
        print(f"\n✅ AI Generation Successful!")
        print(f"📛 Enemy Name: {enemy_desc.name}")
        print(f"📍 Environment: {enemy_desc.environment_description}")
        print(f"\n🎭 ENCOUNTER NARRATIVE:")
        print(f"   {enemy_desc.encounter_narrative}")
        print(f"\n📊 Narrative length: {len(enemy_desc.encounter_narrative)} chars")

        # Debug all fields
        print(f"\n🔍 DEBUG INFO:")
        print(f"   Description: {enemy_desc.description[:100]}...")
        print(f"   Backstory: {enemy_desc.backstory[:100]}...")
        print(f"   Weapon: {enemy_desc.weapon}")
        print(f"   Armor: {enemy_desc.armor}")

        if len(enemy_desc.encounter_narrative) < 100:
            print("⚠️  WARNING: Narrative is very short - might be fallback")
        elif len(enemy_desc.encounter_narrative) > 300:
            print("✅ Narrative is rich and detailed")
        else:
            print("ℹ️  Narrative is moderate length")

    else:
        print("❌ AI generation failed - no description returned")

    print(f"\n🔚 Test complete")

if __name__ == "__main__":
    test_ai_narrative()