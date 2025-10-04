"""
Player Selection screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Horizontal, Vertical
from textual import events


class PlayerSelectScreen(Screen):
    """Select existing character"""

    can_focus = True

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import CLASS_TYPES

        with Container(classes="main-border") as container:
            container.border_title = "⚔️  CHARACTER SELECTION  ⚔️"
            container.border_subtitle = "🎭 Choose Your Hero 🎭"

            yield Static("Select Character", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")

            players = lov.game_db.get_all_players()
            if not players:
                yield Static("No characters found. Create a new one.")
                yield Static("")
                yield Static("Press any key to return...")
            else:
                yield Static("Existing Characters:")
                yield Static("")

                # 2-column layout with auto-balancing
                players_to_show = players[:10]  # Show up to 10 players
                midpoint = (len(players_to_show) + 1) // 2  # Calculate balanced midpoint

                with Horizontal():
                    with Vertical():
                        # Left column - first half (auto-balanced)
                        for i, player in enumerate(players_to_show[:midpoint]):
                            yield Button(
                                f"{i+1}. {player.name} - Level {player.level} {CLASS_TYPES[player.class_type]['name']}",
                                id=f"player_{player.name}"
                            )

                    with Vertical():
                        # Right column - second half (auto-balanced)
                        for i, player in enumerate(players_to_show[midpoint:], midpoint + 1):
                            yield Button(
                                f"{i}. {player.name} - Level {player.level} {CLASS_TYPES[player.class_type]['name']}",
                                id=f"player_{player.name}"
                            )

            yield Static("")
            yield Static("(Q) Back to main menu")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle player selection"""
        # Delayed import to avoid circular dependency
        import lov
        from screens.town.townsquare import TownSquareScreen

        if event.button.id and event.button.id.startswith("player_"):
            player_name = event.button.id[7:]  # Remove "player_" prefix
            lov.current_player = lov.game_db.load_player(player_name)
            if lov.current_player:
                lov.current_player.daily_reset()
                lov.game_db.save_player(lov.current_player)
                self.app.push_screen(TownSquareScreen())

    def on_mount(self) -> None:
        """Focus the screen when it loads"""
        self.focus()

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov
        from screens.town.townsquare import TownSquareScreen

        key = event.key

        # Handle number keys for character selection
        if key.isdigit():
            index = int(key) - 1
            players = lov.game_db.get_all_players()
            if 0 <= index < len(players) and index < 10:  # Limit to first 10 players
                # Load the selected character
                lov.current_player = lov.game_db.load_player(players[index].name)
                if lov.current_player:
                    lov.current_player.daily_reset()
                    lov.game_db.save_player(lov.current_player)
                    self.app.push_screen(TownSquareScreen())
            else:
                self.notify(f"No character #{key} available")

        # Handle Q for quit
        elif key.upper() == "Q" or not lov.game_db.get_all_players():
            self.app.pop_screen()