"""
Marriage Celebration screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class MarriageCelebrationScreen(Screen):
    """Special screen for marriage celebration"""

    def compose(self) -> ComposeResult:
        yield Static("💒 WEDDING CELEBRATION! 💒", classes="header")
        yield Static("=" * 50, classes="separator")
        yield Static("")
        yield Static("🎉 Congratulations! 🎉")
        yield Static("")
        yield Static("You and Violet are now married!")
        yield Static("The entire inn celebrates your union!")
        yield Static("")
        yield Static("Violet whispers: 'I'll always be here for you, my love.'")
        yield Static("")
        yield Static("💍 Marriage Benefits:")
        yield Static("• Free room at the inn")
        yield Static("• Violet's loving support")
        yield Static("• Increased charm and confidence")
        yield Static("")
        yield Static("Press any key to return to the inn...")

    def on_key(self, event: events.Key) -> None:
        # Return to inn after marriage
        self.app.pop_screen()  # Close marriage screen
        self.app.pop_screen()  # Close Violet's room