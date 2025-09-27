"""
Gem Trading screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class GemTradingScreen(Screen):
    """Gem trading interface"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        yield Static("Gem Trading", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static(f"You have {lov.current_player.gems} gems")
        yield Static("Trade 2 gems for 1 stat point:")
        yield Static("")
        yield Static("(D)efense (Vitality)")
        yield Static("(S)trength")
        yield Static("(H)it Points")
        yield Static("(Q) Cancel")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "Q":
            self.app.pop_screen()
        elif key in ["D", "S", "H"]:
            if lov.current_player.gems >= 2:
                lov.current_player.gems -= 2

                if key == "D":
                    lov.current_player.defense_power += 1
                    stat_name = "Defense"
                elif key == "S":
                    lov.current_player.attack_power += 1
                    stat_name = "Strength"
                elif key == "H":
                    lov.current_player.max_hitpoints += 1
                    lov.current_player.hitpoints += 1
                    stat_name = "Hit Points"

                lov.game_db.save_player(lov.current_player)
                self.notify(f"Your {stat_name} increases by 1!")
                self.app.pop_screen()
            else:
                self.notify("You need 2 gems!")