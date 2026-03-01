"""
Weapons screen for Legend of the Obsidian Vault - King Arthur's Weapons
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container
from textual import events


class WeaponsScreen(Screen):
    """King Arthur's Weapons shop"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import WEAPONS

        with Container(classes="main-border") as container:
            container.border_title = "⚔️  KING ARTHUR'S WEAPONS  ⚔️"
            container.border_subtitle = "🗡️ Legendary Blades Await 🗡️"

            # Weapons Shop ASCII Art Header
            yield Static("        ░░░  ✦ KING ARTHUR'S LEGENDARY FORGE ✦  ░░░", classes="weapons-title")
            yield Static("", classes="separator")
            yield Static("                     ╱╲", classes="weapons-sword")
            yield Static("                    ╱  ╲", classes="weapons-sword")
            yield Static("                   ╱ ⚔️ ╲", classes="weapons-blade")
            yield Static("                  ╱      ╲", classes="weapons-sword")
            yield Static("                 ╱════════╲", classes="weapons-sword")
            yield Static("                    ║██║", classes="weapons-hilt")
            yield Static("                    ║██║", classes="weapons-hilt")
            yield Static("                  ══╩══╩══", classes="weapons-guard")
            yield Static("        🗡️═══════════════════════════════════════🗡️", classes="weapons-border")
            yield Static("══════════════════════════════════════════════════════════", classes="weapons-border")
            yield Static("")

            yield Static(f"    💰 Gold: {lov.current_player.gold:,}", classes="gold")
            current_weapon = WEAPONS[lov.current_player.weapon_num]
            yield Static(f"    ⚔️  Current weapon: {current_weapon[0]} (Power: {current_weapon[2]})", classes="weapons-current")
            yield Static("")

            # Show available weapons (can only buy next tier)
            for i, (name, price, power) in enumerate(WEAPONS):
                if i <= lov.current_player.weapon_num + 1:  # Can only buy next weapon
                    if i == lov.current_player.weapon_num:
                        yield Static(f"    ✓ {name} - OWNED (Power: {power})", classes="gold")
                    else:
                        can_afford = lov.current_player.gold >= price
                        current_power = WEAPONS[lov.current_player.weapon_num][2]
                        power_improvement = power - current_power

                        button_text = f"{i+1}. {name} - {price:,} gold"
                        button_text += f" (Power: {power}, +{power_improvement})"

                        yield Button(button_text, id=f"weapon_{i}", disabled=not can_afford)

            yield Static("")
            yield Static("    The blacksmith examines your current blade.", classes="weapons-dialogue")
            yield Static("    'Only the finest weapons for a true warrior!'", classes="weapons-dialogue")
            yield Static("")
            yield Button("(Q) Return to town", id="return_town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle weapon purchase"""
        # Delayed import to avoid circular dependency
        import lov
        from game_data import WEAPONS

        if event.button.id == "return_town":
            self.app.pop_screen()
        elif event.button.id and event.button.id.startswith("weapon_"):
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