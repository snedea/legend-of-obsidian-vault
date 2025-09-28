"""
Violet's Room screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container
from textual import events


class VioletRoomScreen(Screen):
    """Violet's Room - Charm-based flirting interactions"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import VIOLET_FLIRT_OPTIONS

        # Check if Violet is married
        if lov.game_db.is_violet_married():
            husband_name = lov.game_db.get_violet_husband()

            with Container(classes="main-border") as container:
                container.border_title = "💒 VIOLET'S ROOM 💒"
                container.border_subtitle = "💔 Love Lost 💔"

                yield Static("💒 Violet's Room", classes="header")
                yield Static("=-" * 30, classes="separator")
                yield Static("")
                yield Static("You enter Violet's room, but instead of the lovely")
                yield Static("Violet, you find Grizelda, the Inn's cleaning woman!")
                yield Static("")
                yield Static(f"'Violet? She married {husband_name} and moved away.'")
                yield Static("'Now get out of here before I call the guards!'")
                yield Static("")
                yield Button("(Q) Leave quickly", id="leave_quick")
        else:
            with Container(classes="main-border") as container:
                container.border_title = "💜 VIOLET'S ROOM 💜"
                container.border_subtitle = "💕 Romance & Charm 💕"

                yield Static("💜 Violet's Room", classes="header")
                yield Static("=-" * 30, classes="separator")
                yield Static("")
                yield Static("You enter Violet's room. The beautiful barmaid")
                yield Static("looks up at you with sparkling eyes...")
                yield Static("")
                yield Static(f"Your charm: {lov.current_player.charm}", classes="stats")
                yield Static("")

                # Show available flirting options based on charm
                available_options = []
                for charm_req, option_data in VIOLET_FLIRT_OPTIONS.items():
                    if lov.current_player.charm >= charm_req:
                        available_options.append((charm_req, option_data))

                if not available_options:
                    yield Static("Violet looks at you with mild interest, but")
                    yield Static("you lack the charm to do anything...")
                    yield Static("")
                    yield Button("(Q) Leave disappointed", id="leave_disappointed")
                else:
                    yield Static("What would you like to do?")
                    yield Static("")

                    # Show options with hotkeys as buttons
                    hotkey = 1
                    for charm_req, option_data in sorted(available_options):
                        action = option_data["action"]
                        if charm_req == 100:
                            # Special handling for marriage
                            if lov.current_player.married_to:
                                continue  # Skip if already married
                            yield Button(f"({hotkey}) {action} (Charm: {charm_req})",
                                       id=f"flirt_{hotkey}")
                        else:
                            yield Button(f"({hotkey}) {action} (Charm: {charm_req})",
                                       id=f"flirt_{hotkey}")
                        hotkey += 1

                    yield Static("")
                    yield Button("(Q) Leave gracefully", id="leave_graceful")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for touchscreen/mouse support"""
        # Delayed import to avoid circular dependency
        import lov
        from game_data import VIOLET_FLIRT_OPTIONS

        button_id = event.button.id

        if button_id in ["leave_quick", "leave_disappointed", "leave_graceful"]:
            self.app.pop_screen()
            return

        # Handle flirting buttons
        if button_id.startswith("flirt_"):
            try:
                option_num = int(button_id.split("_")[1])

                # Get available options
                available_options = []
                for charm_req, option_data in VIOLET_FLIRT_OPTIONS.items():
                    if lov.current_player.charm >= charm_req:
                        if charm_req == 100 and lov.current_player.married_to:
                            continue  # Skip marriage if already married
                        available_options.append((charm_req, option_data))

                # Check if option number is valid
                if 1 <= option_num <= len(available_options):
                    selected_option = sorted(available_options)[option_num - 1]
                    charm_req, option_data = selected_option

                    # Handle the flirting action
                    self._handle_flirt_action(charm_req, option_data)
            except (ValueError, IndexError):
                pass

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import VIOLET_FLIRT_OPTIONS

        key = event.key.upper()

        if key == "Q":
            self.app.pop_screen()
            return

        # Check if Violet is married (quick exit)
        if lov.game_db.is_violet_married():
            self.app.pop_screen()
            return

        # Handle numbered options
        if key.isdigit():
            option_num = int(key)

            # Get available options
            available_options = []
            for charm_req, option_data in VIOLET_FLIRT_OPTIONS.items():
                if lov.current_player.charm >= charm_req:
                    if charm_req == 100 and lov.current_player.married_to:
                        continue  # Skip marriage if already married
                    available_options.append((charm_req, option_data))

            # Check if option number is valid
            if 1 <= option_num <= len(available_options):
                selected_option = sorted(available_options)[option_num - 1]
                charm_req, option_data = selected_option

                # Handle the flirting action
                self._handle_flirt_action(charm_req, option_data)

    def _handle_flirt_action(self, charm_req: int, option_data: dict):
        """Handle a flirting action with Violet"""
        # Delayed import to avoid circular dependency
        import lov

        action = option_data["action"]
        message = option_data["message"]
        exp_multiplier = option_data["exp_multiplier"]
        special = option_data.get("special")

        # Calculate experience gain (based on player level)
        exp_gain = lov.current_player.level * exp_multiplier

        # Handle special actions
        if special == "marry":
            # Marriage at 100 charm
            lov.current_player.married_to = "Violet"
            lov.current_player.experience += exp_gain
            lov.game_db.marry_violet(lov.current_player.name)

            self.notify(f"{message}")
            self.notify(f"You gain {exp_gain} experience!")

            # Save player changes
            lov.game_db.save_player(lov.current_player)

            # Show marriage celebration
            from .marriage import MarriageCelebrationScreen
            self.app.push_screen(MarriageCelebrationScreen())

        elif special == "laid":
            # Intimate encounter
            lov.current_player.laid_today = True
            lov.current_player.flirted_violet = True
            lov.current_player.experience += exp_gain

            self.notify(f"{message}")
            self.notify(f"You gain {exp_gain} experience!")
            self.notify("You feel refreshed and gain 1 HP!")

            # Heal 1 HP for the encounter
            lov.current_player.hitpoints = min(
                lov.current_player.max_hitpoints,
                lov.current_player.hitpoints + 1
            )

            # Save player changes
            lov.game_db.save_player(lov.current_player)

        else:
            # Regular flirting
            lov.current_player.flirted_violet = True
            lov.current_player.experience += exp_gain

            self.notify(f"{message}")
            self.notify(f"You gain {exp_gain} experience!")

            # Save player changes
            lov.game_db.save_player(lov.current_player)