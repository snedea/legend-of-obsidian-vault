#!/usr/bin/env python3
"""
Test the complete AI integration fix with proper initialization
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_complete_ai_integration():
    """Test the complete AI integration including initialization"""

    print("🤖 Testing Complete TinyLlama AI Integration Fix")
    print("=" * 60)

    # Initialize AI like the game does
    print("🚀 Starting AI initialization (like game startup)...")
    try:
        import threading
        from brainbot import initialize_ai, is_ai_available, ai_quiz_system
        ai_thread = threading.Thread(target=initialize_ai, daemon=True)
        ai_thread.start()
        print("✅ AI initialization started in background thread")
    except Exception as e:
        print(f"❌ AI initialization failed: {e}")
        return

    # Test immediate availability (should be False)
    print(f"\n🔍 Immediate AI check: {is_ai_available(wait_timeout=0)}")
    print(f"   Status: {ai_quiz_system.initialization_status}")

    # Test with 1 second wait (like enemy generation)
    print(f"\n⏱️  AI check with 1s wait: {is_ai_available(wait_timeout=1.0)}")
    print(f"   Status: {ai_quiz_system.initialization_status}")

    # Test with 3 second wait (like settings screen)
    print(f"\n⏱️  AI check with 3s wait: {is_ai_available(wait_timeout=3.0)}")
    print(f"   Status: {ai_quiz_system.initialization_status}")

    # Now test enemy generation
    print(f"\n🐉 Testing enemy generation with AI:")
    print("-" * 40)

    from obsidian import vault

    for i in range(2):
        print(f"\n🎯 Enemy #{i+1}:")
        enemy = vault.get_enemy_for_level(5)

        print(f"   Name: {enemy.name}")
        print(f"   Environment: {enemy.environment_description}")
        if hasattr(enemy, 'encounter_narrative') and enemy.encounter_narrative:
            narrative = enemy.encounter_narrative
            if len(narrative) > 80:
                print(f"   Narrative: {narrative[:80]}...")
            else:
                print(f"   Narrative: {narrative}")

        if i == 0:  # After first enemy, show final AI status
            print(f"\n📊 Final AI Status:")
            print(f"   Available: {is_ai_available(wait_timeout=0)}")
            print(f"   Status: {ai_quiz_system.initialization_status}")

    print(f"\n✅ Complete AI integration test finished!")
    print(f"💡 If AI shows 'ready' status but enemies show fallback, there may be an error in AI generation.")

if __name__ == "__main__":
    test_complete_ai_integration()