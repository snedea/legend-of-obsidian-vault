"""
Healer screen for Legend of the Obsidian Vault - Healer's Hut
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input
from textual.containers import Container
from textual import events


class HealerScreen(Screen):
    """Healer's Hut - Healing services"""

    def __init__(self):
        super().__init__()
        self.partial_heal_mode = False

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov
        from game_data import HEALING_COSTS

        with Container(classes="main-border") as container:
            container.border_title = "🏥 HEALER'S HUT 🏥"
            container.border_subtitle = "💊 Health & Restoration 💊"

            yield Static("🏥 Healer's Hut", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")

            # Player status
            hp_missing = lov.current_player.max_hitpoints - lov.current_player.hitpoints
            yield Static(f"Gold: {lov.current_player.gold:,}", classes="gold")
            yield Static(f"Current HP: {lov.current_player.hitpoints}/{lov.current_player.max_hitpoints}")

            if hp_missing == 0:
                yield Static("")
                yield Static("You are already at full health!", classes="content")
                yield Static("")
                yield Button("(Q) Return to town", id="return_town")
            else:
                yield Static(f"HP needed: {hp_missing}")
                yield Static("")

                # Full heal option
                full_heal_cost = HEALING_COSTS.get(lov.current_player.level, 50)
                can_afford_full = lov.current_player.gold >= full_heal_cost
                yield Button(f"(F) Full Heal - {full_heal_cost} gold",
                            id="full_heal", disabled=not can_afford_full)

                # Partial heal option
                yield Button(f"(P) Partial Heal - 1 gold per HP", id="partial_heal")

                if self.partial_heal_mode:
                    yield Static("")
                    yield Static("Enter HP amount to heal (1 gold each):")
                    yield Input(id="heal_amount", placeholder="HP amount")

                yield Static("")
                yield Static("The old healer looks at you with kind eyes.")
                yield Static("'What ails you, brave warrior?'")
                yield Static("")
                yield Button("(Q) Return to town", id="return_town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle healing options"""
        # Delayed import to avoid circular dependency
        import lov
        from game_data import HEALING_COSTS

        if event.button.id == "return_town":
            self.app.pop_screen()
        elif event.button.id == "full_heal":
            hp_missing = lov.current_player.max_hitpoints - lov.current_player.hitpoints
            cost = HEALING_COSTS.get(lov.current_player.level, 50)

            if lov.current_player.gold >= cost and hp_missing > 0:
                lov.current_player.gold -= cost
                lov.current_player.hitpoints = lov.current_player.max_hitpoints
                lov.game_db.save_player(lov.current_player)

                self.notify(f"You are fully healed for {cost} gold!")
                # Refresh the screen
                self.app.pop_screen()
                from .healer import HealerScreen
                self.app.push_screen(HealerScreen())
            else:
                self.notify("You cannot afford full healing!")

        elif event.button.id == "partial_heal":
            self.partial_heal_mode = True
            # Refresh the screen to show input
            self.app.pop_screen()
            from .healer import HealerScreen
            self.app.push_screen(HealerScreen())

    def on_mount(self) -> None:
        """Focus input if in partial heal mode"""
        if self.partial_heal_mode:
            try:
                input_widget = self.query_one("#heal_amount", Input)
                input_widget.focus()
            except:
                pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle partial heal amount"""
        # Delayed import to avoid circular dependency
        import lov

        try:
            heal_amount = int(event.value.strip())
            hp_missing = lov.current_player.max_hitpoints - lov.current_player.hitpoints

            if heal_amount <= 0:
                self.notify("Invalid amount!")
                return

            if heal_amount > hp_missing:
                heal_amount = hp_missing

            cost = heal_amount

            if lov.current_player.gold >= cost:
                lov.current_player.gold -= cost
                lov.current_player.hitpoints += heal_amount
                lov.game_db.save_player(lov.current_player)

                self.notify(f"Healed {heal_amount} HP for {cost} gold!")
                self.app.pop_screen()
            else:
                self.notify(f"You need {cost} gold for that healing!")

        except ValueError:
            self.notify("Please enter a valid number!")

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()

        if key == "Q":
            self.app.pop_screen()
        elif key == "F" and not self.partial_heal_mode:
            # Trigger full heal
            self.on_button_pressed(type('Event', (), {'button': type('Button', (), {'id': 'full_heal'})})())
        elif key == "P" and not self.partial_heal_mode:
            # Trigger partial heal
            self.on_button_pressed(type('Event', (), {'button': type('Button', (), {'id': 'partial_heal'})})())