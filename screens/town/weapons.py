"""
Weapons screen for Legend of the Obsidian Vault - King Arthur's Weapons
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual import events


class WeaponsScreen(Screen):
    """King Arthur's Weapons shop"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import WEAPONS

        yield Static("King Arthur's Weapons", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static(f"Gold: {lov.current_player.gold:,}", classes="gold")
        yield Static(f"Current weapon: {WEAPONS[lov.current_player.weapon_num][0]}")
        yield Static("")

        # Show available weapons
        for i, (name, price, power) in enumerate(WEAPONS):
            if i <= lov.current_player.weapon_num + 1:  # Can only buy next weapon
                if i == lov.current_player.weapon_num:
                    yield Static(f"  {name} - OWNED", classes="gold")
                else:
                    can_afford = lov.current_player.gold >= price
                    color = "bright_green" if can_afford else "bright_red"
                    yield Button(f"{i+1}. {name} - {price:,} gold (Power: {power})",
                               id=f"weapon_{i}", disabled=not can_afford)

        yield Static("")
        yield Static("(Q) Return to town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle weapon purchase"""
        # Delayed import to avoid circular dependency
        import lov
        from game_data import WEAPONS

        if event.button.id and event.button.id.startswith("weapon_"):
            weapon_idx = int(event.button.id.split("_")[1])
            weapon_name, price, power = WEAPONS[weapon_idx]

            if lov.current_player.gold >= price:
                lov.current_player.gold -= price
                lov.current_player.weapon_num = weapon_idx
                lov.current_player.weapon = weapon_name
                lov.game_db.save_player(lov.current_player)

                self.notify(f"You bought {weapon_name}!")
                self.app.pop_screen()
            else:
                self.notify("You don't have enough gold!")

    def on_key(self, event: events.Key) -> None:
        if event.key.upper() == "Q":
            self.app.pop_screen()