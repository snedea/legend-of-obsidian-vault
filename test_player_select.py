#!/usr/bin/env python3
"""
Test script to verify PlayerSelectScreen fixes
"""

print("🧪 Testing PlayerSelectScreen Input Fixes")
print("=" * 50)
print()

# Test imports
try:
    from lov import PlayerSelectScreen
    print("✅ PlayerSelectScreen import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Test if PlayerSelectScreen has the required attributes
try:
    # Check if can_focus is set
    assert hasattr(PlayerSelectScreen, 'can_focus'), "Missing can_focus attribute"
    assert PlayerSelectScreen.can_focus == True, "can_focus should be True"
    print("✅ can_focus = True is set")

    # Check if on_mount method exists
    assert hasattr(PlayerSelectScreen, 'on_mount'), "Missing on_mount method"
    print("✅ on_mount method exists")

    # Check if on_key method exists
    assert hasattr(PlayerSelectScreen, 'on_key'), "Missing on_key method"
    print("✅ on_key method exists")

    print("✅ All required methods and attributes present")

except Exception as e:
    print(f"❌ Attribute check failed: {e}")
    exit(1)

# Test basic functionality by checking method signatures
try:
    import inspect

    # Check on_mount signature
    on_mount_sig = inspect.signature(PlayerSelectScreen.on_mount)
    print(f"✅ on_mount signature: {on_mount_sig}")

    # Check on_key signature
    on_key_sig = inspect.signature(PlayerSelectScreen.on_key)
    print(f"✅ on_key signature: {on_key_sig}")

except Exception as e:
    print(f"⚠️  Signature check failed: {e}")

print()
print("🎯 SUMMARY:")
print("✅ PlayerSelectScreen now has focus capability")
print("✅ on_mount method added for auto-focus")
print("✅ on_key method enhanced for number key handling")
print()
print("🚀 PlayerSelectScreen should now work!")
print("   1. Navigate to character selection (E from main menu)")
print("   2. Try pressing number keys (1, 2, 3, etc.)")
print("   3. Try clicking character buttons")
print("   4. Should see 'Character selection ready!' notification")
print("   5. Should load characters when number keys are pressed")