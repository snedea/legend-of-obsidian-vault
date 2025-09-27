"""
Armor screen for Legend of the Obsidian Vault - Abdul's Armor
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual import events


class ArmorScreen(Screen):
    """Abdul's Armor shop - Progressive armor upgrades"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import ARMOR

        # Abdul's Armor Shop ASCII Art Header
        yield Static("         ⚔️⚜️ ABDUL'S LEGENDARY ARMORY ⚜️⚔️", classes="armor-banner")
        yield Static("", classes="separator")
        yield Static("              ╔═══════════════════════╗", classes="armor-shield")
        yield Static("             ╔╝                       ╚╗", classes="armor-shield")
        yield Static("            ╔╝   ⚜️  MASTER ARMOR  ⚜️   ╚╗", classes="armor-decoration")
        yield Static("           ╔╝        ╔═══════╗         ╚╗", classes="armor-shield")
        yield Static("          ╔╝         ║███████║          ╚╗", classes="armor-shield")
        yield Static("         ╔╝          ║███████║           ╚╗", classes="armor-shield")
        yield Static("        ╔╝           ╚═══════╝            ╚╗", classes="armor-shield")
        yield Static("       ╔╝     ⚔️═══════════════════⚔️      ╚╗", classes="armor-swords")
        yield Static("      ╔╝═══════════════════════════════════╚╗", classes="armor-border")
        yield Static("══════════════════════════════════════════════════", classes="armor-border")
        yield Static("")
        yield Static(f"Gold: {lov.current_player.gold:,}", classes="gold")
        current_armor = ARMOR[lov.current_player.armor_num]
        yield Static(f"Current armor: {current_armor[0]} (Defense: {current_armor[2]})")
        yield Static("")

        # Show available armor (can only buy next tier)
        for i, (name, price, defense) in enumerate(ARMOR):
            if i <= lov.current_player.armor_num + 1:  # Can only buy next armor
                if i == lov.current_player.armor_num:
                    yield Static(f"  {name} - OWNED (Defense: {defense})", classes="gold")
                else:
                    can_afford = lov.current_player.gold >= price
                    current_def = ARMOR[lov.current_player.armor_num][2]
                    def_improvement = defense - current_def

                    button_text = f"{i+1}. {name} - {price:,} gold"
                    button_text += f" (Defense: {defense}, +{def_improvement})"

                    yield Button(button_text, id=f"armor_{i}", disabled=not can_afford)

        yield Static("")
        yield Static("Abdul examines your current protection.")
        yield Static("'A warrior needs the finest armor to survive!'")
        yield Static("")
        yield Static("(Q) Return to town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle armor purchase"""
        # Delayed import to avoid circular dependency
        import lov
        from game_data import ARMOR

        if event.button.id and event.button.id.startswith("armor_"):
            armor_idx = int(event.button.id.split("_")[1])
            armor_name, price, defense = ARMOR[armor_idx]

            if lov.current_player.gold >= price:
                old_defense = ARMOR[lov.current_player.armor_num][2]
                defense_gain = defense - old_defense

                lov.current_player.gold -= price
                lov.current_player.armor_num = armor_idx
                lov.current_player.armor = armor_name
                lov.game_db.save_player(lov.current_player)

                self.notify(f"You bought {armor_name}!")
                self.notify(f"Defense increased by {defense_gain}!")
                self.app.pop_screen()
            else:
                self.notify("You don't have enough gold!")

    def on_key(self, event: events.Key) -> None:
        if event.key.upper() == "Q":
            self.app.pop_screen()