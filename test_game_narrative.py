#!/usr/bin/env python3
"""
Test the actual game narrative generation
"""
import sys
import time
from obsidian import vault
from brainbot import initialize_ai, is_ai_available

def test_game_narrative():
    """Test narrative generation as it works in the game"""
    print("🎮 Testing Game Narrative Generation")
    print("=" * 50)

    # Initialize AI (like the game does)
    print("🔄 Initializing AI...")
    initialize_ai()

    # Wait for AI
    for i in range(5):
        if is_ai_available():
            print(f"✅ AI available after {i+1} seconds")
            break
        print(f"⏳ Waiting for AI ({i+1}/5)...")
        time.sleep(1)

    # Get a real note from the vault
    print("\n🗂️ Getting notes from vault...")
    notes = vault.scan_notes()
    if not notes:
        print("❌ No notes found in vault")
        return

    # Use the first note
    test_note = notes[0]
    print(f"📝 Using note: '{test_note.title}'")
    print(f"📄 Path: {test_note.path}")
    print(f"📊 Content length: {len(test_note.content)} chars")

    # Generate enemy like the game does
    print(f"\n🐉 Generating enemy for level 5...")
    enemy = vault.get_enemy_for_level(5, [test_note])

    if enemy:
        print(f"\n✅ Enemy Generated!")
        print(f"📛 Name: {enemy.name}")
        print(f"💪 HP: {enemy.hitpoints}")

        print(f"\n🎭 ENCOUNTER NARRATIVE:")
        if hasattr(enemy, 'encounter_narrative') and enemy.encounter_narrative:
            print(f"   {enemy.encounter_narrative}")
            print(f"\n📊 Narrative length: {len(enemy.encounter_narrative)} chars")

            if len(enemy.encounter_narrative) > 300:
                print("✅ Rich and detailed narrative!")
            elif len(enemy.encounter_narrative) > 150:
                print("ℹ️  Moderate length narrative")
            else:
                print("⚠️  Short narrative")
        else:
            print("❌ No encounter narrative found")

        # Check if note content is being used
        if hasattr(enemy, 'note_content') and enemy.note_content:
            print(f"\n📄 Note content available: {len(enemy.note_content)} chars")
            if test_note.title.lower() in enemy.encounter_narrative.lower():
                print("✅ Note title found in narrative")
            else:
                print("⚠️  Note title not found in narrative")
        else:
            print("\n❌ No note content attached to enemy")

    else:
        print("❌ Failed to generate enemy")

    print(f"\n🔚 Test complete")

if __name__ == "__main__":
    test_game_narrative()