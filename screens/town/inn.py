"""
Inn screen for Legend of the Obsidian Vault - Ye Olde Inn
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class InnScreen(Screen):
    """The Inn - Route to Bar Room and Violet's Room"""

    def compose(self) -> ComposeResult:
        yield Static("Ye Olde Inn", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static("The inn is cozy and warm...")
        yield Static("")
        yield Static("(B)ar Room")
        yield Static("(V)iolet's Room")
        yield Static("(Q) Return to town")

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()
        if key == "Q":
            self.app.pop_screen()
        elif key == "B":
            from .barroom import BarRoomScreen
            self.app.push_screen(BarRoomScreen())
        elif key == "V":
            from .violet import VioletRoomScreen
            self.app.push_screen(VioletRoomScreen())