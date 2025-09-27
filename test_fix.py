#!/usr/bin/env python3
"""
Test the input fix for Legend of the Obsidian Vault
"""

print("🧪 Testing Character Selection Fix")
print("=" * 50)
print()
print("Expected behavior:")
print("1. Game should start with clear menu options")
print("2. You should see clickable buttons for each option")
print("3. You should be able to either:")
print("   - Click the buttons with mouse")
print("   - Press keyboard keys (N, E, V, B, Q)")
print("4. Should show notifications when options are selected")
print("5. Should successfully transition to character creation")
print()
print("If keyboard doesn't work, buttons should work as backup")
print()
print("🚀 Starting the game now...")
print()

# Import and run the game
from lov import main
main()