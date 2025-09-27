"""
Character Creation screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input
from textual import events


class CharacterCreationScreen(Screen):
    """Character creation with EXACT LORD flow"""

    def __init__(self):
        super().__init__()
        self.step = "name"
        # Delayed import to avoid circular dependency
        from game_data import Character
        self.new_character = Character()

    def compose(self) -> ComposeResult:
        yield Static("Character Creation", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static("What would you like as an alias?", id="content")
        yield Static("")
        yield Static("Name: ", id="prompt")
        yield Input(id="input")

    def on_mount(self) -> None:
        """Focus the input field when screen loads"""
        # Use call_after_refresh to ensure the widget is fully mounted
        self.call_after_refresh(self._focus_input)

    def _focus_input(self) -> None:
        """Focus the input widget after screen is fully rendered"""
        try:
            input_widget = self.query_one("#input", Input)
            input_widget.focus()
        except Exception as e:
            # If focusing fails, that's ok - user can still click to focus
            pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle character creation steps"""
        # Delayed import to avoid circular dependency
        import lov

        value = event.value.strip()

        if self.step == "name":
            if not value or len(value) > 20:
                self.notify("Name must be 1-20 characters")
                return

            # Check if name exists
            if lov.game_db.load_player(value):
                self.notify("Name already exists. Choose another.")
                return

            self.new_character.name = value
            self.step = "gender"
            self._update_gender_prompt()

        elif self.step == "confirm_name":
            confirm = value.upper() if value else "Y"
            if confirm == "Y":
                self.step = "gender"
                self._update_gender_selection()
            elif confirm == "N":
                self.step = "name"
                self.query_one("#content").update("What would you like as an alias?")
                self.query_one("#prompt").update("Name: ")
                self.query_one("#input").value = ""
            else:
                self.notify("Enter Y or N")
                return

        elif self.step == "gender":
            gender = value.upper() if value else "M"
            if gender not in ["M", "F"]:
                self.notify("Enter M or F")
                return

            self.new_character.gender = gender
            if gender == "M":
                self.query_one("#prompt").update("Then don't be wearing any dresses, eh.")
            else:
                self.query_one("#prompt").update("Hmmm, well we'll try to watch our language then.")

            self.step = "class"
            self._update_class_prompt()

        elif self.step == "class":
            class_choice = value.upper() if value else "K"
            if class_choice not in ["K", "P", "D"]:
                self.notify("Enter K, P, or D")
                return

            self.new_character.class_type = class_choice
            self._finish_creation()

    def _update_gender_prompt(self):
        """Update to name confirmation"""
        self.query_one("#prompt").update(f"{self.new_character.name}? [Y] :")
        try:
            input_widget = self.query_one("#input", Input)
            input_widget.value = "Y"
            input_widget.focus()
        except Exception:
            # If there's an issue with the input widget, just continue
            pass

        # Add confirmation step
        self.step = "confirm_name"

    def _update_gender_selection(self):
        """Update to gender selection"""
        self.query_one("#content").update("And your gender?  (M/F) [M]:")
        self.query_one("#prompt").update("")
        try:
            input_widget = self.query_one("#input", Input)
            input_widget.value = "M"
            input_widget.focus()
        except Exception:
            # If there's an issue with the input widget, just continue
            pass

    def _update_class_prompt(self):
        """Update to class selection"""
        self.query_one("#content").update(
            "As you remember your childhood, you remember...\n\n"
            "(K)illing a lot of woodland creatures.\n"
            "(P)abbling in the mystical forces.\n"
            "(D)ying, cheating, and stealing from the blind.\n\n"
            "Pick one. (K,P,D) :"
        )
        try:
            input_widget = self.query_one("#input", Input)
            input_widget.value = ""
            input_widget.focus()
        except Exception:
            # If there's an issue with the input widget, just continue
            pass

    def _finish_creation(self):
        """Complete character creation"""
        # Delayed import to avoid circular dependency
        import lov
        from screens.town.townsquare import TownSquareScreen

        lov.current_player = self.new_character
        lov.current_player.daily_reset()
        lov.game_db.save_player(lov.current_player)

        self.app.push_screen(TownSquareScreen())

    def on_key(self, event: events.Key) -> None:
        if event.key.upper() == "Q":
            self.app.pop_screen()