"""
Statistics screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container
from textual import events


class StatsScreen(Screen):
    """Player statistics display"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import WEAPONS, ARMOR, CLASS_TYPES

        with Container(classes="main-border") as container:
            container.border_title = "📊 CHARACTER STATS 📊"
            container.border_subtitle = "⚔️ Your Progress ⚔️"

            if not lov.current_player:
                yield Static("No player loaded")
                return

            p = lov.current_player
            weapon_name = WEAPONS[p.weapon_num][0] if p.weapon_num < len(WEAPONS) else "Stick"
            armor_name = ARMOR[p.armor_num][0] if p.armor_num < len(ARMOR) else "Coat"

            yield Static(f"{p.name}'s Stats", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")
            yield Static(f"Level           : {p.level}")
            yield Static(f"Experience      : {p.experience:,}")
            yield Static(f"Hit Points      : {p.hitpoints} of {p.max_hitpoints}")
            yield Static(f"Forest Fights   : {p.forest_fights}")
            yield Static(f"Player Fights   : {p.player_fights}")
            yield Static("")
            yield Static(f"Gold in hand    : {p.gold:,}", classes="gold")
            yield Static(f"Gold in bank    : {p.bank_gold:,}", classes="gold")
            yield Static("")
            yield Static(f"Weapon          : {weapon_name}")
            yield Static(f"Armor           : {armor_name}")
            yield Static(f"Charm           : {p.charm}", classes="stats")
            yield Static(f"Gems            : {p.gems}")
            yield Static("")
            yield Static(f"Class           : {CLASS_TYPES[p.class_type]['name']}")
            yield Static(f"Gender          : {'Male' if p.gender == 'M' else 'Female'}")
            yield Static("")
            yield Button("(Q) Return to town", id="return_town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for touchscreen/mouse support"""
        if event.button.id == "return_town":
            self.app.pop_screen()

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()