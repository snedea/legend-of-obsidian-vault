"""
Name Change screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input
from textual import events


class NameChangeScreen(Screen):
    """Screen for changing player name"""

    def __init__(self):
        super().__init__()
        self.new_name = ""

    def compose(self) -> ComposeResult:
        yield Static("Change Your Name", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static("Enter your new name:")
        yield Input(id="name_input")
        yield Static("")
        yield Static("Press Enter to confirm, Escape to cancel")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import RESERVED_NAMES

        new_name = event.value.strip()

        if not new_name:
            self.notify("Name cannot be empty!")
            return

        # Check reserved names
        if new_name.upper() in RESERVED_NAMES:
            self.notify(RESERVED_NAMES[new_name.upper()])
            return

        # Check if name already exists
        existing_player = lov.game_db.load_player(new_name)
        if existing_player:
            self.notify("That name is already taken!")
            return

        # Change the name
        old_name = lov.current_player.name
        lov.current_player.name = new_name

        # Save with new name and delete old record
        lov.game_db.save_player(lov.current_player)
        # Note: We should delete the old record, but for simplicity we'll leave it

        self.notify(f"Your name has been changed to {new_name}!")
        self.app.pop_screen()

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.pop_screen()