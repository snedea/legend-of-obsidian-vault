"""
Gem Trading screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container
from textual import events


class GemTradingScreen(Screen):
    """Gem trading interface"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        with Container(classes="main-border") as container:
            container.border_title = "💎 GEM TRADING 💎"
            container.border_subtitle = "✨ Power Exchange ✨"

            yield Static("Gem Trading", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")
            yield Static(f"You have {lov.current_player.gems} gems")
            yield Static("Trade 2 gems for 1 stat point:")
            yield Static("")
            yield Button("(D)efense (Vitality)", id="defense")
            yield Button("(S)trength", id="strength")
            yield Button("(H)it Points", id="hitpoints")
            yield Button("(Q) Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for touchscreen/mouse support"""
        import lov

        if event.button.id == "cancel":
            self.app.pop_screen()
        elif event.button.id in ["defense", "strength", "hitpoints"]:
            self._trade_gems(event.button.id)

    def _trade_gems(self, stat_type: str):
        """Handle gem trading for stats"""
        import lov

        if lov.current_player.gems >= 2:
            lov.current_player.gems -= 2

            if stat_type == "defense":
                lov.current_player.defense_power += 1
                stat_name = "Defense"
            elif stat_type == "strength":
                lov.current_player.attack_power += 1
                stat_name = "Strength"
            elif stat_type == "hitpoints":
                lov.current_player.max_hitpoints += 1
                lov.current_player.hitpoints += 1
                stat_name = "Hit Points"

            lov.game_db.save_player(lov.current_player)
            self.notify(f"Your {stat_name} increases by 1!")
            self.app.pop_screen()
        else:
            self.notify("You need 2 gems!")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "Q":
            self.app.pop_screen()
        elif key in ["D", "S", "H"]:
            if key == "D":
                self._trade_gems("defense")
            elif key == "S":
                self._trade_gems("strength")
            elif key == "H":
                self._trade_gems("hitpoints")