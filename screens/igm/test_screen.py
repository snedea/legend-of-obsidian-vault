"""
Test Screen IGM for Legend of the Obsidian Vault
Testing if barak crashes are name-specific
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class TestScreen(Screen):
    """Test Screen - Debugging barak crashes"""

    def __init__(self):
        super().__init__()
        self.test_mode = True

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Simple test header
        yield Static("        ✦ TEST SCREEN - BARAK DEBUG ✦", classes="barak-title")
        yield Static("    This is a test to see if barak crashes are name-specific", classes="barak-content")
        yield Static("")

        # Test content
        yield Static("If you can see this, the test screen loaded successfully!", classes="barak-content")
        yield Static("This means the issue is specific to the barak.py file or name.", classes="barak-content")
        yield Static("")

        # Simple option
        yield Static("(Q) Return to other places", classes="barak-content")

        # Status line
        yield Static("")
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}"
        yield Static(status_line, classes="barak-status")

        # Command area
        yield Static("")
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"
        yield Static(f"Test Screen Debug - Your command, {lov.current_player.name}? [{time_str}]: █", classes="barak-prompt")

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()
        if key == "Q":
            self.app.pop_screen()