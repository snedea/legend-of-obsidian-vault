#!/usr/bin/env python3
"""
Debug AI status and initialization
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_ai_status():
    """Debug the AI status in detail"""

    print("🔍 Debugging AI Status")
    print("=" * 60)

    try:
        from brainbot import ai_quiz_system, is_ai_available, LocalAIClient
        print(f"✅ Successfully imported brainbot modules")

        print(f"\n🧠 AI Quiz System Status:")
        print(f"   ai_available: {ai_quiz_system.ai_available}")
        print(f"   initialization_attempted: {ai_quiz_system.initialization_attempted}")

        print(f"\n🤖 Local AI Client Status:")
        print(f"   model: {ai_quiz_system.local_ai.model is not None}")
        print(f"   available: {ai_quiz_system.local_ai.available}")
        print(f"   loading: {ai_quiz_system.local_ai.loading}")

        print(f"\n🔄 Testing AI initialization:")
        if not ai_quiz_system.initialization_attempted:
            print("   Initializing AI system...")
            ai_quiz_system.initialize()

            # Wait a moment for background initialization
            import time
            print("   Waiting for background initialization...")
            time.sleep(5)

            print(f"   After init - ai_available: {ai_quiz_system.ai_available}")
            print(f"   After init - model loaded: {ai_quiz_system.local_ai.model is not None}")
            print(f"   After init - available: {ai_quiz_system.local_ai.available}")

        # Test the function used by the game
        print(f"\n🎯 is_ai_available() result: {is_ai_available()}")

        # Test AI settings screen status (like the game does)
        try:
            # Check what the settings screen sees
            print(f"\n🖥️ Settings Screen Status Check:")
            print(f"   Same as is_ai_available(): {is_ai_available()}")

        except Exception as e:
            print(f"   Error checking settings: {e}")

    except Exception as e:
        print(f"❌ Error during AI debugging: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ai_status()