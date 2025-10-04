"""
Inn screen for Legend of the Obsidian Vault - Ye Olde Inn
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container
from textual import events


class InnScreen(Screen):
    """The Inn - Route to Bar Room and Violet's Room"""

    def compose(self) -> ComposeResult:
        with Container(classes="main-border") as container:
            container.border_title = "🏨 YE OLDE INN 🏨"
            container.border_subtitle = "🍺 Rest & Relaxation 🍺"

            yield Static("Ye Olde Inn", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")
            yield Static("The inn is cozy and warm...")
            yield Static("")
            yield Button("(B)ar Room", id="barroom")
            yield Button("(V)iolet's Room", id="violet")
            yield Button("(Q) Return to town", id="return_town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for touchscreen/mouse support"""
        if event.button.id == "return_town":
            self.app.pop_screen()
        elif event.button.id == "barroom":
            from .barroom import BarRoomScreen
            self.app.push_screen(BarRoomScreen())
        elif event.button.id == "violet":
            from .violet import VioletRoomScreen
            self.app.push_screen(VioletRoomScreen())

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